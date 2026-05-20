"""Module providing a function to resolve csv path."""

from pathlib import Path


from colorama import init
from pandas import DataFrame
import plotly.express as px
import streamlit as st


from pages.national_vision_page import nationalVisionPage
from services.extract_csv_service import extractCsv


init(autoreset=True)  # Função para inicializar a lib colorama
st.set_page_config(layout="wide")  # Para ocupar todo o espaço horizontal da pagina

_root_url = Path(__file__).resolve().parent.parent
CSV_PATH = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"

CSV_PATH = "https://drive.google.com/file/d/1DDt40eAzPweMlXh-Z4pg5Lp9Up85U0HL/view?usp=sharing"

df = extractCsv(CSV_PATH)

pg = st.navigation(
    [
        st.Page(
            nationalVisionPage(df),
            title="Visão Nacional",
        ),
        # st.Page(page2, title="Second page", icon=":material/favorite:"),
        st.Page("https://docs.streamlit.io", title="Streamlit Docs", icon=":material/open_in_new:"),
    ]
)
pg.run()
