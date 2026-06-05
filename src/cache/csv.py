from pathlib import Path
import hashlib
from urllib.parse import urlparse

import pandas as pd

from utils.logger import displayLog

# Incrementar quando mudar tipos/colunas do dataframe em cache.
_CACHE_VERSION = "v2"


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
    cache_dir = get_cache_dir()
    cache_key = _build_cache_key(source)
    return cache_dir / f"{cache_key}_{_CACHE_VERSION}.parquet"


def _legacy_pickle_path(source: str | Path) -> Path:
    cache_dir = get_cache_dir()
    cache_key = _build_cache_key(source)
    return cache_dir / f"{cache_key}.pkl"


def get_cached_csv(source: str | Path) -> pd.DataFrame | None:
    """Busca cache em Parquet; aceita pickle legado e migra automaticamente."""
    parquet_path = _build_cache_file_path(source)
    if parquet_path.exists():
        displayLog(f"Carregando cache: {parquet_path}")
        return pd.read_parquet(parquet_path)

    legacy_path = _legacy_pickle_path(source)
    if legacy_path.exists():
        displayLog(f"Carregando cache legado: {legacy_path}")
        dataframe = pd.read_pickle(legacy_path)
        save_csv_cache(source, dataframe)
        return dataframe

    return None


def save_csv_cache(source: str | Path, dataframe: pd.DataFrame) -> None:
    """Salva cache compacto em Parquet."""
    cache_file_path = _build_cache_file_path(source)
    dataframe.to_parquet(cache_file_path, index=False, compression="snappy")
    displayLog(f"Cache criado: {cache_file_path}")

    legacy_path = _legacy_pickle_path(source)
    if legacy_path.exists():
        legacy_path.unlink(missing_ok=True)
