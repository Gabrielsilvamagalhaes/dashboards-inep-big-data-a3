from typing import cast

from pandas import DataFrame
import streamlit as st

from dashboards.courses_analytics_constants import (
    AREA_COLUMN,
    MODALITY_LABELS,
    TOP_N_DEFAULT,
    MIN_ENROLLMENT_FOR_RATE,
)
from dashboards.courses_analytics_kpi_dashboard import getCoursesAnalyticsKpiCharts
from dashboards.courses_completion_rate_dashboard import (
    getCoursesCompletionRateChart,
    getCoursesCompletionScatterChart,
)
from dashboards.courses_demand_by_area_dashboard import (
    getCoursesCompletionByAreaChart,
    getCoursesDemandByAreaChart,
)
from dashboards.courses_top_entrants_dashboard import getCoursesTopEntrantsChart
from dashboards.courses_top_matriculations_dashboard import getCoursesTopMatriculationsChart


def _apply_modality_filter(df: DataFrame, modality_key: str) -> DataFrame:
    if modality_key == "all" or "TP_MODALIDADE_ENSINO" not in df.columns:
        return df
    code = int(modality_key)
    return cast(DataFrame, df[df["TP_MODALIDADE_ENSINO"] == code])


def coursesAnalyticsPage(df: DataFrame):
    df = df.dropna(subset=["NO_CINE_ROTULO"])

    areas = sorted(df[AREA_COLUMN].dropna().unique()) if AREA_COLUMN in df.columns else []
    st.markdown(
        "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Área'>Filtrar por Área do Conhecimento (CINE)</h4>",
        unsafe_allow_html=True,
    )
    select_areas = st.multiselect(
        "Filtrar por área CINE",
        areas,
        default=areas,
        label_visibility="hidden",
    )

    modality_options = {
        "all": "Todas as modalidades",
        **{str(k): v for k, v in MODALITY_LABELS.items()},
    }
    st.markdown(
        "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Modalidade'>Filtrar por Modalidade de Ensino</h4>",
        unsafe_allow_html=True,
    )
    modality_label = st.selectbox(
        "Modalidade de ensino",
        list(modality_options.values()),
        label_visibility="hidden",
    )
    modality_key = next(k for k, v in modality_options.items() if v == modality_label)

    top_n = TOP_N_DEFAULT
    min_enrollment = MIN_ENROLLMENT_FOR_RATE

    df_filtered = df
    if select_areas and AREA_COLUMN in df_filtered.columns:
        df_filtered = cast(DataFrame, df_filtered[df_filtered[AREA_COLUMN].isin(select_areas)])
    df_filtered = _apply_modality_filter(df_filtered, modality_key)

    kpi = getCoursesAnalyticsKpiCharts(df_filtered)
    col_k2, col_k3, col_k4 = st.columns(3)
    with col_k2:
        st.plotly_chart(kpi["courses_mat_indicator"])
    with col_k3:
        st.plotly_chart(kpi["courses_ing_indicator"])
    with col_k4:
        st.plotly_chart(kpi["courses_completion_indicator"])

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(getCoursesTopMatriculationsChart(df_filtered, top_n))
    with col2:
        st.plotly_chart(getCoursesTopEntrantsChart(df_filtered, top_n))

    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            getCoursesCompletionRateChart(df_filtered, top_n, min_enrollment, ranking="highest")
        )
    with col4:
        st.plotly_chart(
            getCoursesCompletionRateChart(df_filtered, top_n, min_enrollment, ranking="lowest")
        )

    col5, col6 = st.columns(2)
    with col5:
        st.plotly_chart(getCoursesDemandByAreaChart(df_filtered))
    with col6:
        st.plotly_chart(getCoursesCompletionByAreaChart(df_filtered))

    st.plotly_chart(getCoursesCompletionScatterChart(df_filtered, min_enrollment))
