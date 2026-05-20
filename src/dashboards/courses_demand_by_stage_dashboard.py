from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import CHART_COLORS, prepare_courses_summary


def getCoursesDemandByStageChart(df: DataFrame, top_n: int = 15) -> Figure:
    """Comparativo ingressantes, matriculados e concluintes nos cursos com mais matrículas."""
    summary = prepare_courses_summary(df)
    top_courses = summary.nlargest(top_n, "Matriculados")["NO_CINE_ROTULO"].tolist()
    filtered = summary[summary["NO_CINE_ROTULO"].isin(top_courses)]

    long_df = filtered.melt(
        id_vars=["NO_CINE_ROTULO"],
        value_vars=["Ingressantes", "Matriculados", "Concluintes"],
        var_name="Etapa",
        value_name="Quantidade",
    )

    fig = px.bar(
        long_df,
        x="NO_CINE_ROTULO",
        y="Quantidade",
        color="Etapa",
        barmode="group",
        title=f"Demanda por Etapa — Top {top_n} Cursos por Matrículas (2024)",
        color_discrete_map={
            "Ingressantes": CHART_COLORS["ingressantes"],
            "Matriculados": CHART_COLORS["matriculados"],
            "Concluintes": CHART_COLORS["concluintes"],
        },
        text_auto=".2s",
    )
    fig.update_layout(
        xaxis_title="Curso",
        yaxis_title="Quantidade de estudantes",
        legend_title="Etapa",
        xaxis_tickangle=-45,
        height=560,
    )
    return fig
