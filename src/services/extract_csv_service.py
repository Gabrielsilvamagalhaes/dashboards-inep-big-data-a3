import gc

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

CSV_SEP = ";"
CSV_ENCODING = "iso-8859-1"
CHUNK_SIZE = 80_000


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


def _download_drive_csv_to_cache(source_url: str) -> str:
    from cache.csv import get_cache_dir

    if gdown is None:
        raise ImportError("Pacote 'gdown' não encontrado. Instale com: pip install gdown")

    parsed_source = urlparse(source_url)
    query_params = parse_qs(parsed_source.query)
    file_id = query_params.get("id", ["drive_file"])[0]

    cache_dir = get_cache_dir()
    target_file_path = cache_dir / f"{file_id}.csv"

    if target_file_path.exists():
        displayLog(f"Usando CSV baixado em cache: {target_file_path}")
        return str(target_file_path)

    displayLog("Baixando CSV do Google Drive com gdown")
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


def _optimize_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    category_cols = get_category_columns()
    id_cols = get_integer_id_columns()

    for col in df.columns:
        if col in category_cols:
            df[col] = df[col].astype("category")
        elif col in id_cols:
            df[col] = pd.to_numeric(df[col], errors="coerce").astype("Int32")
        else:
            df[col] = pd.to_numeric(df[col], errors="coerce", downcast="integer")

    return df


def _load_csv_all_rows(source: str) -> pd.DataFrame:
    displayLog("Iniciando extração do csv (todas as linhas)")

    usecols = _resolve_usecols(source)

    df = pd.read_csv(
        source,
        sep=CSV_SEP,
        encoding=CSV_ENCODING,
        usecols=usecols,
        low_memory=False,
    )
    gc.collect()

    df = _optimize_dataframe(df)

    displayLog(f"Total de linhas extraídas: {len(df)}")
    return df


@st.cache_data(show_spinner="Carregando e preparando dados...")
def extractCsv(path: str) -> pd.DataFrame:
    """
    Extrai o dataframe do CSV mantendo todas as linhas.
    Carrega apenas as colunas usadas pelos dashboards para caber na RAM do Streamlit Cloud.
    """
    normalized_source = _normalize_csv_source(path)

    cached_dataframe = get_cached_csv(path)
    if cached_dataframe is None and normalized_source != path:
        cached_dataframe = get_cached_csv(normalized_source)

    if cached_dataframe is not None:
        return cached_dataframe

    read_source = normalized_source
    if _is_google_drive_url(normalized_source):
        read_source = _download_drive_csv_to_cache(normalized_source)

    df = _load_csv_all_rows(read_source)
    save_csv_cache(normalized_source, df)
    return df
