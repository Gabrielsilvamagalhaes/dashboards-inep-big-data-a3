"""Module providing a function to resolve csv path."""

from pathlib import Path
from colorama import init
import plotly.express as px
import streamlit as st


from pages.national_vision_page import nationalVisionPage
from pages.students_profile_page import studentsProfilePage
from services.extract_csv_service import extractCsv


init(autoreset=True)  # Função para inicializar a lib colorama
st.set_page_config(layout="wide")  # Para ocupar todo o espaço horizontal da pagina

_root_url = Path(__file__).resolve().parent.parent
CSV_PATH = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"

CSV_PATH = "https://drive.google.com/file/d/1DDt40eAzPweMlXh-Z4pg5Lp9Up85U0HL/view?usp=sharing"

df = extractCsv(CSV_PATH)

# Utilizando labmda para as funções serem chamadas apenas quando o streamlit iniciar
pg = st.navigation(
    [
        st.Page(
            lambda: nationalVisionPage(df),
            title="Visão Nacional",
            url_path="home",
        ),
        st.Page(
            lambda: studentsProfilePage(df),
            title="Perfil dos Estudantes",
            url_path="students-profile",
        ),
        st.Page("https://docs.streamlit.io", title="Streamlit Docs", icon=":material/open_in_new:"),
    ]
)
pg.run()
