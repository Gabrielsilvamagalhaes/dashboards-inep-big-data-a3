from pandas import DataFrame
import streamlit as st
from typing import cast

import plotly.express as px
from plotly.graph_objs import Figure

from components.ui_helpers import (
    apply_plotly_dark,
    render_page_header,
)
from services.calculate_veterans import calculateVeterans

from dashboards.students_matriculados_by_state_dashboard import (
    getStudentsMatriculadosByStateChart,
)
from dashboards.total_courses_dashboard import getTotalCoursesCharts
from dashboards.total_students_institutions_dashboard import getTotalStudentsInstitutionsChart
from dashboards.total_students_donut_dashboard import getTotalStudentsDonutChart


def _total_students_by_region_pie(df: DataFrame) -> Figure:
    """Distribuição de *matriculados* por região (QT_MAT como base)."""

    region_totals = (
        df.groupby("NO_REGIAO", as_index=False)["QT_MAT"]
        .sum()
        .rename(columns={"NO_REGIAO": "Região", "QT_MAT": "Matriculados"})
    )

    fig = px.pie(
        region_totals,
        names="Região",
        values="Matriculados",
        title="Distribuição de Matriculados por Região (Censo ES 2024)",
        hole=0.35,
    )
    fig.update_traces(
        textinfo="percent+label",
    )
    return fig


def nationalVisionPage(df: DataFrame):
    """Página 'Visão Nacional' com KPIs e insight por região."""

    # df = df.dropna(subset=["NO_REGIAO"])

    regions = sorted(df["NO_REGIAO"].dropna().unique())

    render_page_header(
        "Visão Nacional",
        "Panorama estratégico do ensino superior brasileiro com recorte por região (Censo ES 2024).",
    )

    # Filtro principal da página.
    select_regions = st.multiselect(
        "Filtrar por regiões",
        regions,
        default=regions,
        label_visibility="hidden",
    )

    # Recorte aplicado a todos os KPIs e gráficos.
    df_filtered_by_region = cast(DataFrame, df[df["NO_REGIAO"].isin(select_regions)])

    # with st.expander("Ver amostra dos dados (head)"):
    #     st.dataframe(df_filtered_by_region.head(30))

    # ---------------------------
    # KPIs (fluxo do ensino superior)
    # ---------------------------
    total_ingressantes = float(df["QT_ING"].fillna(0).sum())
    total_matriculados = float(df["QT_MAT"].fillna(0).sum())
    total_concluintes = float(df["QT_CONC"].fillna(0).sum())
    total_veteranos = calculateVeterans(
        total_matriculados=int(total_matriculados),
        total_ingressantes=int(total_ingressantes),
    )

    kpi1, kpi2, kpi3, kpi4 = st.columns(4)
    kpi1.metric(
        "Calouros",
        f"{total_ingressantes:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
    kpi2.metric(
        "Matriculados",
        f"{total_matriculados:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )
    kpi3.metric(
        "Veteranos", f"{total_veteranos:,.0f}".replace(",", "X").replace(".", ",").replace("X", ".")
    )
    kpi4.metric(
        "Formandos",
        f"{total_concluintes:,.0f}".replace(",", "X").replace(".", ",").replace("X", "."),
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    # ---------------------------
    # Visuais principais
    # ---------------------------
    c1, c2 = st.columns(2, gap="large")
    with c1:
        region_pie = _total_students_by_region_pie(df_filtered_by_region)
        st.plotly_chart(apply_plotly_dark(region_pie), use_container_width=True)

    with c2:
        workflow_donut = getTotalStudentsDonutChart(df_filtered_by_region)
        st.plotly_chart(apply_plotly_dark(workflow_donut), use_container_width=True)

    states_chart = getStudentsMatriculadosByStateChart(df_filtered_by_region)
    st.plotly_chart(apply_plotly_dark(states_chart), use_container_width=True)

    # Cursos: indicador e top 10 por recorte (região).
    result = getTotalCoursesCharts(df_filtered_by_region)

    total_courses_graphic = result.get("total_courses_graphic")

    c3, c4 = st.columns(2, gap="large")
    with c3:
        institutions_indicator = getTotalStudentsInstitutionsChart(df_filtered_by_region)
        st.plotly_chart(apply_plotly_dark(institutions_indicator), use_container_width=True)

    with c4:
        total_courses_indicator = result.get("total_courses_indicator")
        st.plotly_chart(apply_plotly_dark(total_courses_indicator), use_container_width=True)

    st.plotly_chart(apply_plotly_dark(total_courses_graphic), use_container_width=True)
