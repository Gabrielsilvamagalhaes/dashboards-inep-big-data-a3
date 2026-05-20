from pandas import DataFrame
import pandas as pd
import plotly.express as px
import streamlit as st

from dashboards.total_students_per_age_dashboard import getTotalStudentsPerAgeCharts
from dashboards.total_students_per_gender_dashboard import getTotalStudentsPerGenderCharts


def studentsProfilePage(df: DataFrame):
    # st.dataframe(df)

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
    fig_distribuicao, fig_comparativo = result.get("total_students_per_age"), result.get(
        "evolution_students_per_age"
    )

    with st.container(width="stretch"):
        st.plotly_chart(fig_distribuicao)

    with st.container(width="stretch"):
        st.plotly_chart(fig_comparativo)
