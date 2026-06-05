from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import (
    CHART_COLORS,
    format_br_number,
    prepare_courses_summary,
)
from components.theme_constants import plotly_hoverlabel


def getCoursesTopEntrantsChart(df: DataFrame, top_n: int = 20) -> Figure:
    """Top cursos por número de calouros."""
    summary = prepare_courses_summary(df)
    top = summary.nlargest(top_n, "Ingressantes").rename(
        columns={"NO_CINE_ROTULO": "Cursos", "Ingressantes": "Calouros"}
    )

    fig = px.bar(
        top,
        y="Cursos",
        x="Calouros",
        orientation="h",
        title=f"Top {top_n} Cursos com Mais Calouros (2024)",
        color="Calouros",
        color_continuous_scale="Purples",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending", "title": "Cursos"},
        xaxis_title="Calouros",
        showlegend=False,
        height=max(500, top_n * 28),
        margin={"r": 72},
        separators=",.",
        hoverlabel=plotly_hoverlabel(font_size=13),
    )
    fig.update_xaxes(range=[0, top["Calouros"].max() * 1.18])
    fig.update_traces(
        marker_color=CHART_COLORS["ingressantes"],
        text=[format_br_number(v) for v in top["Calouros"]],
        textposition="outside",
        textfont={"size": 18},
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Calouros: %{x:,.0f}<extra></extra>",
    )
    return fig
