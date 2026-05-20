from typing import Literal
from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import (
    MIN_ENROLLMENT_FOR_RATE,
    prepare_courses_summary,
)

CompletionRanking = Literal["highest", "lowest"]


def _eligible_summary(df: DataFrame, min_enrollment: int) -> DataFrame:
    summary = prepare_courses_summary(df)
    return summary[summary["Matriculados"] >= min_enrollment]


def getCoursesCompletionRateChart(
    df: DataFrame,
    top_n: int = 20,
    min_enrollment: int = MIN_ENROLLMENT_FOR_RATE,
    ranking: CompletionRanking = "highest",
) -> Figure:
    """Top ou bottom cursos por taxa de conclusão (concluintes / matriculados)."""
    eligible = _eligible_summary(df, min_enrollment)
    ascending = ranking == "lowest"
    top = eligible.nlargest(top_n, "Taxa de Conclusão (%)") if not ascending else eligible.nsmallest(
        top_n, "Taxa de Conclusão (%)"
    )

    title_suffix = "Maior" if not ascending else "Menor"
    fig = px.bar(
        top,
        y="NO_CINE_ROTULO",
        x="Taxa de Conclusão (%)",
        orientation="h",
        title=(
            f"Top {top_n} Cursos com {title_suffix} Taxa de Conclusão "
            f"(mín. {min_enrollment:,} matriculados, 2024)"
        ),
        color="Taxa de Conclusão (%)",
        color_continuous_scale="Greens" if not ascending else "Reds",
        text_auto=".1f",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending" if ascending else "total descending", "title": ""},
        xaxis_title="Taxa de Conclusão (%)",
        showlegend=False,
        height=max(500, top_n * 28),
    )
    return fig


def getCoursesCompletionScatterChart(
    df: DataFrame, min_enrollment: int = MIN_ENROLLMENT_FOR_RATE
) -> Figure:
    """Relação entre volume de matrículas e taxa de conclusão por curso."""
    eligible = _eligible_summary(df, min_enrollment)

    fig = px.scatter(
        eligible,
        x="Matriculados",
        y="Taxa de Conclusão (%)",
        hover_name="NO_CINE_ROTULO",
        size="Ingressantes",
        title="Matrículas x Taxa de Conclusão por Curso (2024)",
        color="Taxa de Conclusão (%)",
        color_continuous_scale="Viridis",
        labels={
            "Matriculados": "Matriculados",
            "Taxa de Conclusão (%)": "Taxa de Conclusão (%)",
        },
    )
    fig.update_layout(
        xaxis_title="Matriculados",
        yaxis_title="Taxa de Conclusão (%)",
        height=520,
    )
    return fig
