"""Entrada da aplicação Streamlit (A3).

Responsável por:
- configurar o layout;
- aplicar tema dark consistente;
- carregar o CSV;
- montar a navegação de páginas.
"""

from pathlib import Path
from colorama import init
import streamlit as st


from pages.courses_analytics_page import coursesAnalyticsPage
from pages.finance_programs_page import financialProgramsPage
from pages.members_page import membersPage
from pages.national_vision_page import nationalVisionPage
from pages.students_profile_page import studentsProfilePage
from services.extract_csv_service import extractCsv
from components.ui_helpers import apply_dark_theme


init(autoreset=True)  # Função para inicializar a lib colorama
st.set_page_config(
    page_title="Dashboard INEP — Ensino Superior (A3)",
    layout="wide",  # Para ocupar todo o espaço horizontal da página
    page_icon=":bar_chart:",
)

# Tema visual deve ser aplicado cedo, antes das páginas renderizarem conteúdo.
apply_dark_theme()

_root_url = Path(__file__).resolve().parent.parent
CSV_PATH = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"

CSV_PATH = "https://drive.google.com/file/d/1P9Hehhe8mh2cE44AYw081M_Fhp0DPWYX/view?usp=sharing"

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
        st.Page(
            lambda: financialProgramsPage(df),
            title="Programas de Financiamento",
            url_path="finance-programs",
        ),
        st.Page(
            lambda: coursesAnalyticsPage(df),
            title="Análise de Cursos",
            url_path="courses-analytics",
        ),
        st.Page(
            lambda: membersPage(),
            title="Integrantes",
            url_path="members",
        ),
        st.Page(
            "https://github.com/Gabrielsilvamagalhaes/dashboards-inep-big-data-a3",
            title="GitHub",
            icon=":material/open_in_new:",
        ),
        st.Page(
            "https://colab.research.google.com/drive/1YjvgMnjOtm3wrT-GBRvv48UiZZD4rxyw?usp=sharing#scrollTo=RJi9wxUYwLzu",
            title="Google Colab",
            icon=":material/open_in_new:",
        ),
    ],
    position="top",
)
pg.run()
