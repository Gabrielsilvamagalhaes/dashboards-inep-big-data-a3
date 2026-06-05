import gc
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
    gdown.download(source_url, str(target_file_path), quiet=False)
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


def _build_read_dtypes(usecols: list[str]) -> dict[str, str]:
    """Tipos explícitos evitam inferência de float64 durante o parse do CSV."""
    category_cols = get_category_columns()
    id_cols = get_integer_id_columns()
    dtypes: dict[str, str] = {}

    for col in usecols:
        if col in category_cols:
            dtypes[col] = "string"
        elif col in id_cols:
            dtypes[col] = "Int32"
        else:
            dtypes[col] = "float32"

    return dtypes


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


def _load_csv_chunked(source: str, usecols: list[str]) -> pd.DataFrame:
    """Lê o CSV em blocos para limitar o pico de memória no deploy gratuito."""
    dtypes = _build_read_dtypes(usecols)
    chunks: list[pd.DataFrame] = []
    total_rows = 0

    for chunk_index, chunk in enumerate(
        pd.read_csv(
            source,
            sep=CSV_SEP,
            encoding=CSV_ENCODING,
            usecols=usecols,
            dtype=dtypes,
            chunksize=CHUNK_SIZE,
            low_memory=True,
        ),
        start=1,
    ):
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
        dtypes = _build_read_dtypes(usecols)
        for chunk_index, chunk in enumerate(
            pd.read_csv(
                source,
                sep=CSV_SEP,
                encoding=CSV_ENCODING,
                usecols=usecols,
                dtype=dtypes,
                chunksize=CHUNK_SIZE,
                low_memory=True,
            ),
            start=1,
        ):
            chunk = _optimize_dataframe(chunk)
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
    return result


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

    read_source = normalized_source
    if _is_google_drive_url(normalized_source):
        suffix = ".parquet" if _is_parquet_source(normalized_source) else ".csv"
        read_source = _download_drive_file_to_cache(normalized_source, suffix=suffix)

    if _is_parquet_source(read_source):
        df = _load_parquet(read_source)
    else:
        df = _load_csv_all_rows(read_source)

    save_csv_cache(normalized_source, df)
    return df
