from pandas import DataFrame
import plotly.express as px
import streamlit as st
from typing import cast

from dashboards.total_courses_dashboard import getTotalCoursesCharts
from dashboards.total_students_finished_dashboard import getTotalStudentsFinishedChart
from dashboards.total_students_institutions_dashboard import getTotalStudentsInstitutionsChart
from dashboards.total_students_new_entrants_dashboard import getTotalStudentsNewEntrantsChart
from dashboards.total_students_per_region_dashboard import (
    getTotalStudentsPerRegionChart,
)
from dashboards.total_students_per_state_dashboard import getTotalStudentsPerStateChart
from dashboards.total_students_registred_dashboard import getTotalStudentsRegistredChart


def nationalVisionPage(df: DataFrame):
    df = df.dropna(subset=["NO_REGIAO"])

    df_regions = df["NO_REGIAO"]
    regions = sorted(df_regions.unique())

    # Estilizando label do multiselect
    st.markdown(
        "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Regiões'>Filtrar por Regiões</h4>",
        unsafe_allow_html=True,
    )

    select_regions = st.multiselect(
        "Filtrar por regiões", regions, default=regions, label_visibility="hidden"
    )
    col1, col2 = st.columns(2)

    with col1:
        total_students_per_region_graphic = getTotalStudentsPerRegionChart(
            cast(DataFrame, df), select_regions
        )
        st.plotly_chart(
            total_students_per_region_graphic,
        )

    with col2:
        total_students_per_state_graphic = getTotalStudentsPerStateChart(
            cast(DataFrame, df), select_regions
        )
        st.plotly_chart(total_students_per_state_graphic)

    col3, col4, col5, col6 = st.columns(4)

    years = sorted(df["NU_ANO_CENSO"].dropna().astype(int).unique().tolist())

    with col3:
        # Total de inscritos
        total_students_registred_graphic = getTotalStudentsRegistredChart(df, years)
        st.plotly_chart(total_students_registred_graphic)

    with col4:
        # Total Concluintes
        total_students_finished_graphic = getTotalStudentsFinishedChart(df, years)
        st.plotly_chart(total_students_finished_graphic)

    with col5:
        # Total ingressantes
        total_students_new_entrants_graphic = getTotalStudentsNewEntrantsChart(df, years)
        st.plotly_chart(total_students_new_entrants_graphic)

    with col6:
        # Total de instituições
        total_students_institutions_graphic = getTotalStudentsInstitutionsChart(df, years)
        st.plotly_chart(total_students_institutions_graphic)

    col7, col8 = st.columns([1, 3])

    result = getTotalCoursesCharts(df)
    total_courses_indicator, total_courses_graphic = result.get(
        "total_courses_indicator"
    ), result.get("total_courses_graphic")

    with col7:
        # Indicador de total de cursos
        st.plotly_chart(total_courses_indicator)

    with col8:
        # Top 20 cursos
        st.plotly_chart(total_courses_graphic)
