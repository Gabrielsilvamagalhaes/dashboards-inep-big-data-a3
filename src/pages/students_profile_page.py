from pandas import DataFrame
import streamlit as st

# Importações existentes
from dashboards.total_students_per_age_dashboard import getTotalStudentsPerAgeCharts
from dashboards.total_students_per_gender_dashboard import getTotalStudentsPerGenderCharts
from dashboards.total_students_per_race_dashboard import (
    getStudentsComparisonByRaceChart,
)

# NOVA IMPORTAÇÃO
from dashboards.total_students_per_disability_dashboard import (
    getStudentsDistributionByDisabilityChart,
    getStudentsComparisonByDisabilityChart,
)


def studentsProfilePage(df: DataFrame):

    result = getTotalStudentsPerGenderCharts(df)
    fig_genero = result.get("total_students_per_gender")
    with st.container(width="stretch"):
        st.plotly_chart(fig_genero)

    result = getTotalStudentsPerAgeCharts(df)
    fig_dist_age = result.get("total_students_per_age")
    with st.container(width="stretch"):
        st.plotly_chart(fig_dist_age)

    fig_raca_comp = getStudentsComparisonByRaceChart(df)

    with st.container(width="stretch"):
        st.plotly_chart(fig_raca_comp)

    fig_def_dist = getStudentsDistributionByDisabilityChart(df)
    fig_def_comp = getStudentsComparisonByDisabilityChart(df)
    with st.container(width="stretch"):
        st.plotly_chart(fig_def_dist)
    with st.container(width="stretch"):
        st.plotly_chart(fig_def_comp)
