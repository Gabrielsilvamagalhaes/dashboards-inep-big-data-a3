from pandas import DataFrame
import streamlit as st
from typing import cast

from dashboards.total_courses_dashboard import getTotalCoursesCharts
from dashboards.total_students_institutions_dashboard import getTotalStudentsInstitutionsChart
from dashboards.total_students_per_region_dashboard import (
    getTotalStudentsPerRegionChart,
)
from dashboards.total_students_per_state_dashboard import getTotalStudentsPerStateChart
from dashboards.total_students_donut_dashboard import getTotalStudentsDonutChart


def nationalVisionPage(df: DataFrame):
    df = df.dropna(subset=["NO_REGIAO"])

    st.dataframe(df)

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
    df_filtered_by_region = df[df["NO_REGIAO"].isin(select_regions)]

    col1, col2 = st.columns(2)

    with col1:
        total_students_per_region_graphic = getTotalStudentsPerRegionChart(
            cast(DataFrame, df), select_regions
        )
        st.plotly_chart(total_students_per_region_graphic)

    with col2:
        total_students_per_state_graphic = getTotalStudentsPerStateChart(
            cast(DataFrame, df), select_regions
        )
        st.plotly_chart(total_students_per_state_graphic)

    col3, col4 = st.columns(2)

    with col3:
        total_students_institutions_graphic = getTotalStudentsInstitutionsChart(df)
        st.plotly_chart(total_students_institutions_graphic)

    with col4:
        total_students_workflow_donut = getTotalStudentsDonutChart(df)
        st.plotly_chart(total_students_workflow_donut)

    result = getTotalCoursesCharts(cast(DataFrame, df_filtered_by_region))
    total_courses_indicator, total_courses_graphic = result.get(
        "total_courses_indicator"
    ), result.get("total_courses_graphic")

    col5, col6 = st.columns([1, 3])

    with col5:
        st.plotly_chart(total_courses_indicator)

    with col6:
        st.plotly_chart(total_courses_graphic)
