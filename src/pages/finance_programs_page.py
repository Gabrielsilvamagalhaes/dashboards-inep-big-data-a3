from typing import cast

from pandas import DataFrame
import streamlit as st

from dashboards.financing_programs_by_region_dashboard import (
    getFinancingProgramsByRegionChart,
)
from dashboards.financing_programs_by_stage_dashboard import getFinancingProgramsByStageCharts
from dashboards.financing_programs_constants import STAGE_LABEL, FinancingStage
from dashboards.financing_programs_kpi_dashboard import getFinancingKpiCharts
from dashboards.financing_programs_share_dashboard import getFinancingProgramsShareChart
from dashboards.financing_reembolsavel_dashboard import (
    getFinancingReembolsavelChart,
)


def financialProgramsPage(df: DataFrame):
    df = df.dropna(subset=["NO_REGIAO"])
    regions = sorted(df["NO_REGIAO"].unique())

    st.markdown(
        "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Regiões'>Filtrar por Regiões</h4>",
        unsafe_allow_html=True,
    )
    select_regions = st.multiselect(
        "Filtrar por regiões",
        regions,
        default=regions,
        label_visibility="hidden",
    )
    df_filtered = cast(DataFrame, df[df["NO_REGIAO"].isin(select_regions)])

    kpi = getFinancingKpiCharts(df_filtered)
    col_k1, col_k2, col_k3 = st.columns(3)
    with col_k1:
        st.plotly_chart(kpi["financing_total_indicator"])
    with col_k2:
        st.plotly_chart(kpi["financing_fies_indicator"])
    with col_k3:
        st.plotly_chart(kpi["financing_prouni_indicator"])

    st.markdown(
        "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Etapa'>Filtrar por Etapa do Estudante</h4>",
        unsafe_allow_html=True,
    )
    stage_options: list[FinancingStage] = ["ingressantes", "matriculados", "concluintes"]
    stage_labels = [STAGE_LABEL[s] for s in stage_options]
    selected_label = st.selectbox(
        "Etapa do estudante",
        stage_labels,
        index=1,
        label_visibility="hidden",
    )
    stage = stage_options[stage_labels.index(selected_label)]

    # col1, col2 = st.columns(2)
    st.plotly_chart(getFinancingProgramsShareChart(df_filtered, stage))

    stage_charts = getFinancingProgramsByStageCharts(df_filtered)

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(stage_charts["financing_programs_by_stage"])

    with col4:
        st.plotly_chart(getFinancingProgramsByRegionChart(df_filtered, select_regions))
