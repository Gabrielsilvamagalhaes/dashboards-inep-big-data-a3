import pandas as pd
import streamlit as st
from urllib.parse import parse_qs, urlparse

from cache.csv import get_cache_dir, get_cached_csv, save_csv_cache
from utils.logger import displayLog

try:
    import gdown  # type: ignore[reportMissingImports]
except ImportError:  # pragma: no cover
    gdown = None


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
    if gdown is None:
        raise ImportError(
            "Pacote 'gdown' não encontrado. Instale com: pip install gdown"
        )

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

@st.cache_data
def extractCsv(path: str) -> pd.DataFrame:
    """
    Função que extratai dataframe  de csv(s).\n
    Apenas informe o caminho do arquivo em string
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

    # Variavel para limitar a busca de linhas do csv, porque o tamanho é muito grande
    limitRows = 570000
    size = 80000
    chunks = []
    total = 0

    displayLog('Iniciando extração do csv')

    for chunk in pd.read_csv(read_source, sep=';', encoding='iso-8859-1', chunksize=size, low_memory=False):
        # if total >= limitRows:
        #     break

        chunk = chunk[chunk['NO_REGIAO'].notna()]
        chunks.append(chunk)
        total +=len(chunk)

        

    displayLog(f'Total de linhas extráidas: {total}')
    df = pd.concat(chunks).reset_index()
    save_csv_cache(normalized_source, df)
    return df





