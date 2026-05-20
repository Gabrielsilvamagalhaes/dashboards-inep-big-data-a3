from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import CHART_COLORS, prepare_courses_summary


def getCoursesTopEntrantsChart(df: DataFrame, top_n: int = 20) -> Figure:
    """Top cursos por número de ingressantes."""
    summary = prepare_courses_summary(df)
    top = summary.nlargest(top_n, "Ingressantes")

    fig = px.bar(
        top,
        y="NO_CINE_ROTULO",
        x="Ingressantes",
        orientation="h",
        title=f"Top {top_n} Cursos com Mais Ingressantes (2024)",
        color="Ingressantes",
        color_continuous_scale="Purples",
        text_auto=".2s",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending", "title": ""},
        xaxis_title="Ingressantes",
        showlegend=False,
        height=max(500, top_n * 28),
    )
    fig.update_traces(marker_color=CHART_COLORS["ingressantes"])
    return fig
