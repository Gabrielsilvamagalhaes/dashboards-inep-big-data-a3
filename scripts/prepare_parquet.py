"""
Converte o CSV do Censo ES 2024 em Parquet compacto para deploy no Streamlit Cloud.

Execute uma vez no Google Colab ou na sua máquina (com RAM suficiente), faça upload
do .parquet gerado no Google Drive e aponte DATA_URL em src/app.py para o novo link.

Uso local:
    python scripts/prepare_parquet.py --csv caminho/para/MICRODADOS.csv --out cache/dados.parquet

Uso com URL do Drive (CSV):
    python scripts/prepare_parquet.py --url "https://drive.google.com/..." --out cache/dados.parquet
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "src"))

from services.extract_csv_service import (  # noqa: E402
    _download_drive_file_to_cache,
    _is_google_drive_url,
    _is_parquet_source,
    _load_csv_all_rows,
    _normalize_csv_source,
    _optimize_dataframe,
)
import pandas as pd  # noqa: E402


def main() -> None:
    parser = argparse.ArgumentParser(description="Gera Parquet otimizado para o dashboard INEP.")
    parser.add_argument("--csv", type=Path, help="Caminho local do CSV")
    parser.add_argument("--url", type=str, help="URL do Google Drive (CSV ou Parquet)")
    parser.add_argument(
        "--out",
        type=Path,
        default=ROOT / "cache" / "microdados_inep_2024.parquet",
        help="Arquivo Parquet de saída",
    )
    args = parser.parse_args()

    if not args.csv and not args.url:
        parser.error("Informe --csv ou --url")

    source = str(args.csv) if args.csv else _normalize_csv_source(args.url)
    if args.url and _is_google_drive_url(source) and not _is_parquet_source(source):
        source = _download_drive_file_to_cache(source, suffix=".csv")

    if _is_parquet_source(source):
        df = pd.read_parquet(source)
        df = _optimize_dataframe(df)
    else:
        df = _load_csv_all_rows(source)

    args.out.parent.mkdir(parents=True, exist_ok=True)
    df.to_parquet(args.out, index=False, compression="snappy")

    csv_size = Path(source).stat().st_size if Path(source).exists() else 0
    parquet_size = args.out.stat().st_size
    print(f"Linhas: {len(df):,}".replace(",", "."))
    print(f"Colunas: {len(df.columns)}")
    print(f"Parquet salvo em: {args.out}")
    if csv_size:
        ratio = (1 - parquet_size / csv_size) * 100
        print(f"Tamanho CSV: {csv_size / 1_000_000:.1f} MB")
        print(f"Tamanho Parquet: {parquet_size / 1_000_000:.1f} MB (~{ratio:.0f}% menor)")


if __name__ == "__main__":
    main()
