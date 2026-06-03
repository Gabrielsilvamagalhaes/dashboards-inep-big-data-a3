from typing import cast

from pandas import DataFrame
import streamlit as st

from components.ui_helpers import apply_plotly_dark, render_insight, render_page_header
from dashboards.financing_programs_constants import (
    FINANCING_PROGRAMS,
    FINANCING_PROGRAM_EXTRA,
    STAGE_PREFIX,
)

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
    """Página 'Programas de Financiamento' com filtros e visualizações coerentes."""

    df = df.dropna(subset=["NO_REGIAO"])
    regions = sorted(df["NO_REGIAO"].unique())

    render_page_header(
        "Programas de Financiamento",
        "Análise do impacto dos programas (FIES, PROUNI e outros) com recorte por região e etapa.",
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
        st.plotly_chart(apply_plotly_dark(kpi["financing_total_indicator"]), use_container_width=True)
    with col_k2:
        st.plotly_chart(apply_plotly_dark(kpi["financing_fies_indicator"]), use_container_width=True)
    with col_k3:
        st.plotly_chart(apply_plotly_dark(kpi["financing_prouni_indicator"]), use_container_width=True)

    st.markdown("<hr/>", unsafe_allow_html=True)

    stage_options: list[FinancingStage] = ["ingressantes", "matriculados", "concluintes"]
    stage_labels = [STAGE_LABEL[s] for s in stage_options]
    selected_label = st.selectbox(
        "Etapa do estudante",
        stage_labels,
        index=1,
        label_visibility="hidden",
    )
    stage = stage_options[stage_labels.index(selected_label)]

    # ---------------------------
    # Insight e visualizações por etapa
    # ---------------------------
    share_pie = getFinancingProgramsShareChart(df_filtered, stage)

    # Cálculo do "maior programa" para exibir um insight textual antes dos gráficos.
    prefix = STAGE_PREFIX[stage]
    program_totals: list[tuple[str, float]] = []
    total_all_programs = 0.0
    for program_label, program_suffix in FINANCING_PROGRAMS:
        qty = float(df_filtered[f"{prefix}_{program_suffix}"].fillna(0).sum()) if f"{prefix}_{program_suffix}" in df_filtered.columns else 0.0
        for extra_suffix in FINANCING_PROGRAM_EXTRA.get(program_label, []):
            extra_col = f"{prefix}_{extra_suffix}"
            if extra_col in df_filtered.columns:
                qty += float(df_filtered[extra_col].fillna(0).sum())
        if qty > 0:
            program_totals.append((program_label, qty))
            total_all_programs += qty

    lead_program, lead_qty = max(program_totals, key=lambda x: x[1]) if program_totals else ("—", 0.0)
    lead_share = (lead_qty / total_all_programs * 100) if total_all_programs > 0 else 0.0
    render_insight(
        f"Maior participação na etapa selecionada: {lead_program} "
        f"({lead_share:.1f}% do total de programas no recorte)."
    )

    reembolsavel_pie = getFinancingReembolsavelChart(df_filtered, stage)

    c_share, c_reemb = st.columns(2, gap="large")
    with c_share:
        st.plotly_chart(apply_plotly_dark(share_pie), use_container_width=True)
    with c_reemb:
        st.plotly_chart(apply_plotly_dark(reembolsavel_pie), use_container_width=True)

    stage_charts = getFinancingProgramsByStageCharts(df_filtered)

    col3, col4 = st.columns(2)

    with col3:
        st.plotly_chart(
            apply_plotly_dark(stage_charts["financing_programs_by_stage"]),
            use_container_width=True,
        )

    with col4:
        # Importante: a visualização por região deve usar a mesma etapa selecionada.
        st.plotly_chart(
            apply_plotly_dark(
                getFinancingProgramsByRegionChart(
                    df_filtered,
                    select_regions,
                    stage_prefix=STAGE_PREFIX[stage],
                )
            ),
            use_container_width=True,
        )
