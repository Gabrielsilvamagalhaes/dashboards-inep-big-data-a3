"""Module providing a function to resolve csv path."""

from pathlib import Path
from typing import cast

from colorama import init
from pandas import DataFrame
import plotly.express as px
import streamlit as st

from dashboards.total_courses_dashboard import getTotalCoursesCharts
from dashboards.total_students_finished_dashboard import getTotalStudentsFinishedChart
from dashboards.total_students_institutions_dashboard import getTotalStudentsInstitutionsChart
from dashboards.total_students_new_entrants_dashboard import getTotalStudentsNewEntrantsChart
from dashboards.total_students_per_region_dashboard import (
    getTotalStudentsPerRegionChart,
)
from dashboards.total_students_per_state_dashboard import getTotalStudentsPerStateChart

from dashboards.total_students_registred_dashboard import getTotalStudentsRegistredChart
from services.extract_csv_service import extractCsv


init(autoreset=True)  # Função para inicializar a lib colorama
st.set_page_config(layout="wide")  # Para ocupar todo o espaço horizontal da pagina

_root_url = Path(__file__).resolve().parent.parent
CSV_PATH = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"

CSV_PATH = "https://drive.google.com/file/d/1DDt40eAzPweMlXh-Z4pg5Lp9Up85U0HL/view?usp=sharing"

df = extractCsv(CSV_PATH)

df = df.dropna(subset=["NO_REGIAO"])
region = st.sidebar.selectbox("Região", df["NO_REGIAO"].unique())


df_filtered_per_region = df[df["NO_REGIAO"] == region]
st.dataframe(df_filtered_per_region)

df_education = df["NO_REGIAO"]
regions = sorted(df_education.unique())

# Estilizando label do multiselect
st.markdown(
    "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Regiões'>Filtrar por Regiões</h4>",
    unsafe_allow_html=True,
)

select_regions = st.multiselect(
    "Filtrar por regiões", regions, default=regions, label_visibility="hidden"
)
col1, col2 = st.columns(2)

total_students_per_region_graphic = getTotalStudentsPerRegionChart(
    cast(DataFrame, df_education), select_regions
)
col1.plotly_chart(total_students_per_region_graphic, width="stretch", on_select="rerun")


df_education = df[["NO_REGIAO", "NO_UF"]]
total_students_per_state_graphic = getTotalStudentsPerStateChart(
    cast(DataFrame, df_education), select_regions
)
col2.plotly_chart(total_students_per_state_graphic)


col3, col4, col5, col6 = st.columns(4)


years = sorted(df["NU_ANO_CENSO"].dropna().astype(int).unique().tolist())

# Total de inscritos
total_students_registred_graphic = getTotalStudentsRegistredChart(df, years)
col3.plotly_chart(total_students_registred_graphic)

# Total Concluintes
total_students_finished_graphic = getTotalStudentsFinishedChart(df, years)
col4.plotly_chart(total_students_finished_graphic)

# Total ingressantes
total_students_new_entrants_graphic = getTotalStudentsNewEntrantsChart(df, years)
col5.plotly_chart(total_students_new_entrants_graphic)

# Total de instituições
total_students_institutions_graphic = getTotalStudentsInstitutionsChart(df, years)
col6.plotly_chart(total_students_institutions_graphic)

col7, col8 = st.columns([1, 3])

# Total de cursos
result = getTotalCoursesCharts(df)
total_courses_indicator, total_courses_graphic = result.get("total_courses_indicator"), result.get(
    "total_courses_graphic"
)
col7.plotly_chart(total_courses_indicator)
col8.plotly_chart(total_courses_graphic)
