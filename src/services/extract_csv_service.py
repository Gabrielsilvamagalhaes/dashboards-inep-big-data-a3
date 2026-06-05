import gc
import os
from pathlib import Path

import pandas as pd
import streamlit as st
from urllib.parse import parse_qs, urlparse

from cache.csv import get_cached_csv, save_csv_cache
from services.csv_columns import (
    get_category_columns,
    get_integer_id_columns,
    get_required_csv_columns,
)
from utils.logger import displayLog

try:
    import gdown  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    gdown = None

try:
    import pyarrow as pa  # type: ignore[reportMissingImports]
    import pyarrow.parquet as pq  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    pa = None
    pq = None

CSV_SEP = ";"
CSV_ENCODING = "iso-8859-1"
# Chunks menores reduzem o pico de RAM no Streamlit Cloud (tier gratuito ~1 GB).
CHUNK_SIZE = 25_000

_LOCAL_CSV_NAME = "MICRODADOS_CADASTRO_CURSOS_2024.csv"
_LOCAL_PARQUET_NAME = "microdados_inep_2024.parquet"


def _project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _extract_drive_file_id(path: str) -> str | None:
    parsed_source = urlparse(path)
    if "drive.google.com" not in parsed_source.netloc:
        return None

    query_params = parse_qs(parsed_source.query)
    if "/file/d/" in parsed_source.path:
        try:
            return parsed_source.path.split("/file/d/")[1].split("/")[0]
        except IndexError:
            return None
    if "id" in query_params and query_params["id"]:
        return query_params["id"][0]
    return None


def _local_data_candidates(preferred: str) -> list[Path]:
    root = _project_root()
    cache_dir = root / "cache"
    candidates: list[Path] = []

    env_path = os.environ.get("INEP_DATA_PATH", "").strip()
    if env_path:
        candidates.append(Path(env_path))

    candidates.extend(
        [
            root / "samples" / _LOCAL_CSV_NAME,
            cache_dir / _LOCAL_PARQUET_NAME,
        ]
    )

    file_id = _extract_drive_file_id(preferred)
    if file_id:
        candidates.extend(
            [
                cache_dir / f"{file_id}.csv",
                cache_dir / f"{file_id}.parquet",
            ]
        )

    seen: set[Path] = set()
    existing: list[Path] = []
    for candidate in candidates:
        resolved = candidate.resolve()
        if resolved in seen or not resolved.exists():
            continue
        seen.add(resolved)
        existing.append(resolved)
    return existing


def resolve_data_source(preferred: str) -> str:
    """
    Prioriza arquivo local/cache quando existir (dev offline).
    No Streamlit Cloud, normalmente só há URL remota e o download segue.
    """
    local_sources = _local_data_candidates(preferred)
    if local_sources:
        chosen = local_sources[0]
        displayLog(f"Usando fonte local (sem download): {chosen}")
        return str(chosen)
    return preferred


def _download_help_message(preferred: str, error: Exception) -> str:
    root = _project_root()
    local_sources = _local_data_candidates(preferred)
    lines = [
        "Não foi possível baixar o arquivo do Google Drive.",
        f"Detalhe: {error}",
        "",
        "Alternativas para rodar localmente:",
        f"1. Baixe o CSV do INEP e salve em: {root / 'samples' / _LOCAL_CSV_NAME}",
        f"2. Ou gere um Parquet e salve em: {root / 'cache' / _LOCAL_PARQUET_NAME}",
        "3. Ou defina a variável de ambiente INEP_DATA_PATH com o caminho do arquivo",
        "",
        "Verifique também firewall, proxy, VPN ou conexão com a internet.",
    ]
    if local_sources:
        lines.insert(
            4,
            f"Arquivos locais detectados (use um deles): {', '.join(str(p) for p in local_sources)}",
        )
    return "\n".join(lines)


def _normalize_csv_source(path: str) -> str:
    parsed_source = urlparse(path)
    if parsed_source.scheme not in ("http", "https"):
        return path

    if "drive.google.com" not in parsed_source.netloc:
        return path

    query_params = parse_qs(parsed_source.query)
    file_id = None

    if "/file/d/" in parsed_source.path:
        try:
            file_id = parsed_source.path.split("/file/d/")[1].split("/")[0]
        except IndexError:
            file_id = None
    elif "id" in query_params and query_params["id"]:
        file_id = query_params["id"][0]

    if not file_id:
        return path

    return f"https://drive.google.com/uc?export=download&id={file_id}"


def _is_google_drive_url(path: str) -> bool:
    parsed_source = urlparse(path)
    return parsed_source.scheme in ("http", "https") and "drive.google.com" in parsed_source.netloc


def _is_parquet_source(path: str) -> bool:
    parsed = urlparse(path)
    if parsed.scheme in ("http", "https"):
        return parsed.path.lower().endswith(".parquet")
    return Path(path).suffix.lower() == ".parquet"


def _download_drive_file_to_cache(source_url: str, *, suffix: str) -> str:
    from cache.csv import get_cache_dir

    if gdown is None:
        raise ImportError("Pacote 'gdown' não encontrado. Instale com: pip install gdown")

    parsed_source = urlparse(source_url)
    query_params = parse_qs(parsed_source.query)
    file_id = query_params.get("id", ["drive_file"])[0]

    cache_dir = get_cache_dir()
    target_file_path = cache_dir / f"{file_id}{suffix}"

    if target_file_path.exists():
        displayLog(f"Usando arquivo baixado em cache: {target_file_path}")
        return str(target_file_path)

    displayLog(f"Baixando {suffix} do Google Drive com gdown")
    try:
        gdown.download(source_url, str(target_file_path), quiet=False)
    except Exception as exc:
        local_sources = _local_data_candidates(source_url)
        if local_sources:
            displayLog(
                f"Download falhou; usando arquivo local: {local_sources[0]}"
            )
            return str(local_sources[0])
        raise ConnectionError(_download_help_message(source_url, exc)) from exc
    return str(target_file_path)


def _resolve_usecols(source: str) -> list[str]:
    required = set(get_required_csv_columns())
    header = pd.read_csv(source, sep=CSV_SEP, encoding=CSV_ENCODING, nrows=0)
    available = set(header.columns)
    usecols = sorted(required & available)
    missing = required - available

    if missing:
        sample = ", ".join(sorted(missing)[:8])
        displayLog(f"Aviso: {len(missing)} colunas esperadas ausentes no CSV (ex.: {sample})")

    displayLog(f"Lendo {len(usecols)} de {len(available)} colunas do CSV")
    return usecols


def _read_csv_chunks(source: str, usecols: list[str]):
    """
    Lê o CSV em blocos sem dtype fixo no parse.

    O microdado INEP mistura vazios e tokens inválidos em colunas numéricas;
    forçar float32/Int32 no read_csv quebra o parser C do pandas.
    """
    return pd.read_csv(
        source,
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        usecols=usecols,
        chunksize=CHUNK_SIZE,
        low_memory=True,
        na_values=["", " ", "NA", "N/A", "NULL", "-"],
        keep_default_na=True,
    )


def _optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    category_cols = get_category_columns()
    id_cols = get_integer_id_columns()

    for col in df.columns:
        if col in category_cols:
            df[col] = df[col].astype("category")
        elif col in id_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int32")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce", downcast="float")

    return df


def _optimize_chunk_for_staging(df: pd.DataFrame) -> pd.DataFrame:
    """Otimiza numéricos no staging sem category (evita schema divergente no Parquet)."""
    category_cols = get_category_columns()
    id_cols = get_integer_id_columns()

    for col in df.columns:
        if col in category_cols:
            df[col] = df[col].astype("string")
        elif col in id_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int32")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce", downcast="float")

    return df


def _load_csv_chunked(source: str, usecols: list[str]) -> pd.DataFrame:
    """Lê o CSV em blocos para limitar o pico de memória no deploy gratuito."""
    chunks: list[pd.DataFrame] = []
    total_rows = 0

    for chunk_index, chunk in enumerate(_read_csv_chunks(source, usecols), start=1):
        chunk = _optimize_dataframe(chunk)
        chunks.append(chunk)
        total_rows += len(chunk)

        if chunk_index % 4 == 0:
            displayLog(f"Lidos {total_rows:,} registros...".replace(",", "."))
            gc.collect()

    if not chunks:
        return pd.DataFrame(columns=usecols)

    if len(chunks) == 1:
        return chunks[0]

    displayLog("Concatenando blocos do CSV...")
    result = pd.concat(chunks, ignore_index=True, copy=False)
    del chunks
    gc.collect()
    return result


def _load_csv_via_staging_parquet(source: str, usecols: list[str]) -> pd.DataFrame:
    """
    Converte CSV -> Parquet em blocos (pico de RAM ~1 chunk) e recarrega tipado.
    Útil quando o parse direto do CSV estoura a RAM do Streamlit Cloud.
    """
    if pa is None or pq is None:
        displayLog("pyarrow indisponível; usando leitura em blocos sem staging")
        return _load_csv_chunked(source, usecols)

    from cache.csv import get_cache_dir

    staging_path = get_cache_dir() / f"staging_{Path(source).stem}.parquet"
    writer: pq.ParquetWriter | None = None
    total_rows = 0

    try:
        for chunk_index, chunk in enumerate(_read_csv_chunks(source, usecols), start=1):
            chunk = _optimize_chunk_for_staging(chunk)
            table = pa.Table.from_pandas(chunk, preserve_index=False)
            if writer is None:
                writer = pq.ParquetWriter(staging_path, table.schema, compression="snappy")
            writer.write_table(table)
            total_rows += len(chunk)

            del chunk, table
            if chunk_index % 4 == 0:
                displayLog(f"Staging parquet: {total_rows:,} registros...".replace(",", "."))
            gc.collect()
    finally:
        if writer is not None:
            writer.close()

    displayLog(f"Recarregando staging parquet ({total_rows:,} registros)".replace(",", "."))
    result = pd.read_parquet(staging_path)
    staging_path.unlink(missing_ok=True)
    gc.collect()
    return _optimize_dataframe(result)


def _load_csv_all_rows(source: str) -> pd.DataFrame:
    displayLog("Iniciando extração do csv (todas as linhas, leitura em blocos)")

    usecols = _resolve_usecols(source)
    df = _load_csv_via_staging_parquet(source, usecols)

    displayLog(f"Total de linhas extraídas: {len(df)}")
    return df


def _load_parquet(source: str) -> pd.DataFrame:
    displayLog("Carregando Parquet pré-processado")
    df = pd.read_parquet(source)
    displayLog(f"Total de linhas no Parquet: {len(df)}")
    return _optimize_dataframe(df)


@st.cache_resource(show_spinner="Carregando e preparando dados...")
def extractCsv(path: str) -> pd.DataFrame:
    """
    Extrai o dataframe mantendo todas as linhas.
    Carrega apenas as colunas usadas pelos dashboards para caber na RAM do Streamlit Cloud.

    Preferir um arquivo .parquet no Google Drive (gerado localmente/Colab) para deploy gratuito.
    """
    normalized_source = _normalize_csv_source(path)

    cached_dataframe = get_cached_csv(path)
    if cached_dataframe is None and normalized_source != path:
        cached_dataframe = get_cached_csv(normalized_source)

    if cached_dataframe is not None:
        return cached_dataframe

    resolved_source = resolve_data_source(path)
    read_source = resolved_source
    if _is_google_drive_url(normalized_source) and not Path(resolved_source).exists():
        suffix = ".parquet" if _is_parquet_source(normalized_source) else ".csv"
        read_source = _download_drive_file_to_cache(normalized_source, suffix=suffix)

    if _is_parquet_source(read_source):
        df = _load_parquet(read_source)
    else:
        df = _load_csv_all_rows(read_source)

    save_csv_cache(normalized_source, df)
    return df
