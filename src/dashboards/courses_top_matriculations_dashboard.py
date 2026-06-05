from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import (
    CHART_COLORS,
    format_br_number,
    prepare_courses_summary,
)
from components.theme_constants import plotly_hoverlabel


def getCoursesTopMatriculationsChart(df: DataFrame, top_n: int = 20) -> Figure:
    """Top cursos por número de matriculados."""
    summary = prepare_courses_summary(df)
    top = summary.nlargest(top_n, "Matriculados").rename(columns={"NO_CINE_ROTULO": "Cursos"})

    fig = px.bar(
        top,
        y="Cursos",
        x="Matriculados",
        orientation="h",
        title=f"Top {top_n} Cursos com Mais Matrículas (2024)",
        color="Matriculados",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending", "title": "Cursos"},
        xaxis_title="Matriculados",
        showlegend=False,
        height=max(500, top_n * 28),
        margin={"r": 72},
        separators=",.",
        hoverlabel=plotly_hoverlabel(font_size=13),
    )
    fig.update_xaxes(range=[0, top["Matriculados"].max() * 1.18])
    fig.update_traces(
        marker_color=CHART_COLORS["matriculados"],
        text=[format_br_number(v) for v in top["Matriculados"]],
        textposition="outside",
        textfont={"size": 18},
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Matriculados: %{x:,.0f}<extra></extra>",
    )
    return fig
