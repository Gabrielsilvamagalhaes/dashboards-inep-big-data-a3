"""Module providing a function to resolve csv path."""

from pathlib import Path
from typing import cast

from colorama import init
from pandas import DataFrame
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

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

df_education = df["QT_CONC"]

total_students_finished = df_education.sum()
total_students_finished = {"Ano": years, "Total": [total_students_finished]}

fig = px.bar(
    total_students_finished,
    x="Ano",
    y="Total",
    title="Concluintes totais por ano",
    labels={"y": "Quantidade de Pessoas", "x": "Censo"},
    text_auto=",.0f",
)

fig.update_traces(marker_color="CornflowerBlue", width=0.1)
fig.update_layout(yaxis_tickformat=",.0f")

col4.plotly_chart(fig)

# Total ingressantes

df_education = df["QT_ING"]

total_students_new_entrants = df_education.sum()
total_students_new_entrants = {"Ano": years, "Total": [total_students_new_entrants]}


fig = px.bar(
    total_students_new_entrants,
    x="Ano",
    y="Total",
    title="Ingressantes totais por ano",
    labels={"y": "Quantidade de Pessoas", "x": "Censo"},
    text_auto=",.0f",
)

fig.update_traces(marker_color="CornflowerBlue", width=0.1)
fig.update_layout(yaxis_tickformat=",.0f")

col5.plotly_chart(fig)

# Total de instituições

df_education = df["CO_IES"]

total_institutions = df_education.nunique()
total_institutions = {"Ano": years, "Total": [total_institutions]}

fig = px.bar(
    total_institutions,
    x="Ano",
    y="Total",
    title="Total de Instituições por Ano",
    labels={"y": "Total de Instituiçoes", "x": "Ano"},
    text_auto=",.0f",
)

fig.update_traces(marker_color="CornflowerBlue", width=0.1)
fig.update_layout(yaxis_tickformat=",.0f")

col6.plotly_chart(fig)

col7, col8 = st.columns([1, 3])

# Total de cursos

df_education = df["NO_CINE_ROTULO"]
total_courses = df_education.count()

fig_total = go.Figure(
    go.Indicator(
        mode="number",
        value=total_courses,
        number={"valueformat": ",.0f"},
        title={"text": "Total de Cursos Cadastrados (Brasil)"},
    )
)

col7.plotly_chart(fig_total)


df_count = df_education.value_counts().reset_index().head(20)
df_count.columns = ["Curso", "Quantidade"]

fig = px.bar(
    df_count,
    y="Curso",
    x="Quantidade",
    orientation="h",
    title="Top 20 Cursos por Quantidade",
    text_auto=",.0f",
    color="Quantidade",
    color_continuous_scale="Blues",
)

fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=900)

col8.plotly_chart(fig)
