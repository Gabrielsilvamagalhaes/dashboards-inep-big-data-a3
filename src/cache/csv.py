from pathlib import Path

import pandas as pd

from utils.logger import displayLog


def _resolve_project_root() -> Path:
    return Path(__file__).resolve().parent.parent.parent


def _build_cache_file_path(csv_path: Path) -> Path:
    """Função para criação do caminho do cache """
    cache_dir = _resolve_project_root() / "cache"
    cache_dir.mkdir(parents=True, exist_ok=True)
    return cache_dir / f"{csv_path.stem}.pkl"


def get_cached_csv(csv_path: Path) -> pd.DataFrame | None:
    """
        Função para buscar o cache do arquivo csv. 
        Caso, não tenha cache, retorna None
    """
    cache_file_path = _build_cache_file_path(csv_path)
    if cache_file_path.exists():
        displayLog(f"Carregando cache: {cache_file_path}")
        return pd.read_pickle(cache_file_path)

    return None


def save_csv_cache(csv_path: Path, dataframe: pd.DataFrame) -> None:
    """Função  para salvar o cache do arquivo csv"""
    cache_file_path = _build_cache_file_path(csv_path)
    dataframe.to_pickle(cache_file_path)
    displayLog(f"Cache criado: {cache_file_path}")
