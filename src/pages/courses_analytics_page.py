from typing import cast

from pandas import DataFrame
import streamlit as st

from components.ui_helpers import apply_plotly_dark, render_page_header

from dashboards.courses_analytics_constants import (
    AREA_COLUMN,
    MODALITY_LABELS,
    TOP_N_DEFAULT,
    MIN_ENROLLMENT_FOR_RATE,
)
from dashboards.courses_completion_rate_dashboard import (
    getCoursesCompletionRateChart,
)
from dashboards.courses_top_entrants_dashboard import getCoursesTopEntrantsChart
from dashboards.courses_top_matriculations_dashboard import getCoursesTopMatriculationsChart


def coursesAnalyticsPage(df: DataFrame):
    df = df.dropna(subset=["NO_CINE_ROTULO"])

    render_page_header(
        "Análise de Cursos",
        "Demanda, ingressantes e taxa de conclusão com filtros por área/modalidade e região.",
    )

    # Filtro por região (mantido no mesmo estilo das demais páginas).
    regions = sorted(df["NO_REGIAO"].dropna().unique()) if "NO_REGIAO" in df.columns else []
    select_regions = st.multiselect(
        "Filtrar por regiões",
        regions,
        default=regions,
        label_visibility="hidden",
    )

    df = cast(DataFrame, df[df["NO_REGIAO"].isin(select_regions)]) if select_regions else df

    top_n = st.slider(
        "Top N cursos (para gráficos de ranking)",
        min_value=5,
        max_value=50,
        value=int(TOP_N_DEFAULT),
        step=5,
    )
    min_enrollment = MIN_ENROLLMENT_FOR_RATE

    df_filtered = df

    total_mat = float(df["QT_MAT"].fillna(0).sum())
    total_conc = float(df["QT_CONC"].fillna(0).sum())
    completion_rate = (total_conc / total_mat * 100) if total_mat > 0 else 0.0

    st.metric(
        "Taxa de Conclusão Geral", f"{completion_rate:,.1f}%", help="Porcentagem de conclusão geral"
    )

    st.markdown("<hr/>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.plotly_chart(
            apply_plotly_dark(getCoursesTopMatriculationsChart(df_filtered, top_n)),
            use_container_width=True,
        )
    with col2:
        st.plotly_chart(
            apply_plotly_dark(getCoursesTopEntrantsChart(df_filtered, top_n)),
            use_container_width=True,
        )

    completion_top_n = min(top_n, 10)
    col3, col4 = st.columns(2)
    with col3:
        st.plotly_chart(
            apply_plotly_dark(
                getCoursesCompletionRateChart(
                    df_filtered, completion_top_n, min_enrollment, ranking="highest"
                )
            ),
            use_container_width=True,
        )
    with col4:
        st.plotly_chart(
            apply_plotly_dark(
                getCoursesCompletionRateChart(
                    df_filtered, completion_top_n, min_enrollment, ranking="lowest"
                )
            ),
            use_container_width=True,
        )
