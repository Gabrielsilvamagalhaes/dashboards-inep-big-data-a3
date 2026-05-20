from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import CHART_COLORS, prepare_courses_summary


def getCoursesTopMatriculationsChart(df: DataFrame, top_n: int = 20) -> Figure:
    """Top cursos por número de matriculados."""
    summary = prepare_courses_summary(df)
    top = summary.nlargest(top_n, "Matriculados")

    fig = px.bar(
        top,
        y="NO_CINE_ROTULO",
        x="Matriculados",
        orientation="h",
        title=f"Top {top_n} Cursos com Mais Matrículas (2024)",
        color="Matriculados",
        color_continuous_scale="Blues",
        text_auto=".2s",
    )
    fig.update_layout(
        yaxis={"categoryorder": "total ascending", "title": ""},
        xaxis_title="Matriculados",
        showlegend=False,
        height=max(500, top_n * 28),
    )
    fig.update_traces(marker_color=CHART_COLORS["matriculados"])
    return fig
