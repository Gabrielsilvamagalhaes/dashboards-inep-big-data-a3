from pandas import DataFrame
import streamlit as st

from components.ui_helpers import apply_plotly_dark, render_insight, render_page_header

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
    """Página 'Perfil dos Estudantes' com filtro por região e insights textuais."""

    df = df.dropna(subset=["NO_REGIAO"])

    render_page_header(
        "Perfil dos Estudantes",
        "Análises por gênero, idade, raça/cor e deficiência (com recorte por região).",
    )

    # Filtro por região.
    regions = sorted(df["NO_REGIAO"].dropna().unique())
    select_regions = st.multiselect(
        "Filtrar por regiões",
        regions,
        default=regions,
        label_visibility="hidden",
    )

    df_filtered = df[df["NO_REGIAO"].isin(select_regions)]

    # Insight 1: participação relativa de gênero (base QT_MAT_FEM/MASC).
    female = float(df_filtered["QT_MAT_FEM"].fillna(0).sum())
    male = float(df_filtered["QT_MAT_MASC"].fillna(0).sum())
    total_gender = female + male
    female_share = (female / total_gender * 100) if total_gender > 0 else 0.0

    lead_gender = (
        "Feminino" if female_share >= 50 else "Masculino"
    )
    render_insight(
        f"No recorte, {lead_gender} lidera a distribuição de matrículas. "
        f"Feminino: {female_share:.1f}% (QT_MAT_FEM vs. QT_MAT_MASC)."
    )

    # KPIs resumidos para orientar o gestor antes dos gráficos.
    col1, col2, col3 = st.columns(3)
    col1.metric("Matrículas Femininas", f"{female:,.0f}")
    col2.metric("Matrículas Masculinas", f"{male:,.0f}")
    col3.metric("Total (FEM+MASC)", f"{total_gender:,.0f}")

    st.markdown("<hr/>", unsafe_allow_html=True)

    # Layout 2x2 para reduzir rolagem.
    row1_a, row1_b = st.columns(2, gap="large")
    with row1_a:
        result = getTotalStudentsPerGenderCharts(df_filtered)
        fig_gender = result.get("total_students_per_gender")
        st.plotly_chart(apply_plotly_dark(fig_gender), use_container_width=True)

    with row1_b:
        result = getTotalStudentsPerAgeCharts(df_filtered)
        fig_age = result.get("total_students_per_age")
        st.plotly_chart(apply_plotly_dark(fig_age), use_container_width=True)

    row2_a, row2_b = st.columns(2, gap="large")
    with row2_a:
        fig_race = getStudentsComparisonByRaceChart(df_filtered)
        st.plotly_chart(apply_plotly_dark(fig_race), use_container_width=True)

    with row2_b:
        fig_def_dist = getStudentsDistributionByDisabilityChart(df_filtered)
        st.plotly_chart(apply_plotly_dark(fig_def_dist), use_container_width=True)

    # Comparativo de deficiência (full width) para manter leitura.
    fig_def_comp = getStudentsComparisonByDisabilityChart(df_filtered)
    with st.container(width="stretch"):
        st.plotly_chart(apply_plotly_dark(fig_def_comp), use_container_width=True)
