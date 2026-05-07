from pathlib import Path
import hashlib
from urllib.parse import urlparse

import pandas as pd

from utils.logger import displayLog


def _resolve_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def get_cache_dir() -> Path:
    cache_dir = _resolve_project_root() / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir


def _build_cache_key(source: str | Path) -> str:
    source_text = str(source).strip()
    parsed_source = urlparse(source_text)

    if parsed_source.scheme in ("http", "https"):
        source_hash = hashlib.sha256(source_text.encode("utf-8")).hexdigest()[:12]
        return f"url_{source_hash}"

    return Path(source_text).stem


def _build_cache_file_path(source: str | Path) -> Path:
    """Função para criação do caminho do cache """
    cache_dir = get_cache_dir()
    cache_key = _build_cache_key(source)
    return cache_dir / f"{cache_key}.pkl"


def get_cached_csv(source: str | Path) -> pd.DataFrame | None:
    """
        Função para buscar o cache do arquivo csv. 
        Caso, não tenha cache, retorna None
    """
    cache_file_path = _build_cache_file_path(source)
    if cache_file_path.exists():
        displayLog(f"Carregando cache: {cache_file_path}")
        return pd.read_pickle(cache_file_path)

    return None


def save_csv_cache(source: str | Path, dataframe: pd.DataFrame) -> None:
    """Função  para salvar o cache do arquivo csv"""
    cache_file_path = _build_cache_file_path(source)
    dataframe.to_pickle(cache_file_path)
    displayLog(f"Cache criado: {cache_file_path}")
