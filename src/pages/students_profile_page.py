from pandas import DataFrame
import streamlit as st

# Importações existentes
from dashboards.total_students_per_age_dashboard import getTotalStudentsPerAgeCharts
from dashboards.total_students_per_gender_dashboard import getTotalStudentsPerGenderCharts
from dashboards.total_students_per_race_dashboard import (
    getStudentsDistributionByRaceChart,
    getStudentsComparisonByRaceChart,
)

# NOVA IMPORTAÇÃO
from dashboards.total_students_per_disability_dashboard import (
    getStudentsDistributionByDisabilityChart,
    getStudentsComparisonByDisabilityChart,
)


def studentsProfilePage(df: DataFrame):

    result = getTotalStudentsPerGenderCharts(df)
    fig_genero, fig_barras = result.get("total_students_per_gender"), result.get(
        "total_students_gender_per_stage"
    )
    col1, col2 = st.columns([1, 2])
    with col1:
        st.plotly_chart(fig_genero)
    with col2:
        st.plotly_chart(fig_barras)

    result = getTotalStudentsPerAgeCharts(df)
    fig_dist_age, fig_comp_age = result.get("total_students_per_age"), result.get(
        "evolution_students_per_age"
    )
    with st.container(width="stretch"):
        st.plotly_chart(fig_dist_age)
    with st.container(width="stretch"):
        st.plotly_chart(fig_comp_age)

    fig_raca_dist = getStudentsDistributionByRaceChart(df)
    fig_raca_comp = getStudentsComparisonByRaceChart(df)
    with st.container(width="stretch"):
        st.plotly_chart(fig_raca_dist)
    with st.container(width="stretch"):
        st.plotly_chart(fig_raca_comp)

    fig_def_dist = getStudentsDistributionByDisabilityChart(df)
    fig_def_comp = getStudentsComparisonByDisabilityChart(df)
    with st.container(width="stretch"):
        st.plotly_chart(fig_def_dist)
    with st.container(width="stretch"):
        st.plotly_chart(fig_def_comp)
