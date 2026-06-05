from typing import cast

from pandas import DataFrame
import streamlit as st

from components.ui_helpers import apply_plotly_dark, render_page_header
from dashboards.financing_programs_constants import STAGE_LABEL, STAGE_PREFIX, FinancingStage
from dashboards.financing_programs_by_region_dashboard import (
    getFinancingProgramsByRegionChart,
)
from dashboards.financing_programs_by_stage_dashboard import getFinancingProgramsByStageCharts
from dashboards.financing_programs_share_dashboard import getFinancingProgramsShareChart
from dashboards.financing_programs_totals import get_reembolsavel_discrepancy
from dashboards.financing_reembolsavel_dashboard import (
    getFinancingReembolsavelChart,
)


def financialProgramsPage(df: DataFrame):
    """Página 'Programas de Financiamento' com filtros e visualizações coerentes."""

    # df = df.dropna(subset=["NO_REGIAO"])
    regions = sorted(df["NO_REGIAO"].dropna().unique())

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

    total_mat_financ = float(df["QT_MAT_FINANC"].fillna(0).sum())
    total_fies = float(df["QT_MAT_FIES"].fillna(0).sum())
    total_prouni = float(df["QT_MAT_PROUNII"].fillna(0).sum()) + float(
        df["QT_MAT_PROUNIP"].fillna(0).sum()
    )

    kpi1, kpi2, kpi3 = st.columns(3)

    kpi1.metric(
        "Matriculados em Programas de Financiamento",
        f"{total_mat_financ:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )

    kpi2.metric(
        "Matriculados via FIES",
        f"{total_fies:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )

    kpi3.metric(
        "Matriculados via PROUNI",
        f"{total_prouni:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )

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
    reembolsavel_pie = getFinancingReembolsavelChart(df_filtered, stage)

    c_share, c_reemb = st.columns(2, gap="large")
    with c_share:
        st.plotly_chart(apply_plotly_dark(share_pie), use_container_width=True)
    with c_reemb:
        st.plotly_chart(apply_plotly_dark(reembolsavel_pie), use_container_width=True)

    discrepancy = get_reembolsavel_discrepancy(df_filtered, stage)
    delta_reemb = abs(discrepancy["delta_reembolsavel"])
    delta_nreemb = abs(discrepancy["delta_nao_reembolsavel"])
    if delta_reemb >= 1 or delta_nreemb >= 1:
        st.caption(
            "O gráfico da direita agrupa os programas da esquerda "
            "(FIES + Outros Reembolsáveis vs PROUNI + Outros Não Reembolsáveis), "
            "por isso as porcentagens entre os dois gráficos são coerentes. "
            f"Os totais oficiais do INEP (FINANC_REEMB / FINANC_NREEMB) "
            f"diferem em {delta_reemb:,.0f} reembolsáveis e {delta_nreemb:,.0f} "
            f"não reembolsáveis em relação a essa soma por programa.".replace(",", ".")
        )

    stage_charts = getFinancingProgramsByStageCharts(df_filtered)

    st.plotly_chart(
        apply_plotly_dark(stage_charts["financing_programs_by_stage"]),
        use_container_width=True,
    )

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
