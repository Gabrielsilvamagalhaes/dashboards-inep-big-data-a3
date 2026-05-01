import streamlit as st

# from utils.project_root_url import _root_url
from services.extract_csv_service import extractCsv

from pathlib import Path

_root_url = Path(__file__).resolve().parent.parent

_csv_path = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"


df = extractCsv(_csv_path)
df
