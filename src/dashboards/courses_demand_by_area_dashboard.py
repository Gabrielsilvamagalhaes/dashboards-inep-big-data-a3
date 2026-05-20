from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.courses_analytics_constants import AREA_COLUMN, CHART_COLORS


def getCoursesDemandByAreaChart(df: DataFrame) -> Figure:
    """Matrículas agregadas por área geral do CINE."""
    if AREA_COLUMN not in df.columns:
        raise KeyError(f"Coluna {AREA_COLUMN} não encontrada no dataset.")

    by_area = (
        df.groupby(AREA_COLUMN, as_index=False)[["QT_MAT", "QT_ING", "QT_CONC"]]
        .sum()
        .rename(
            columns={
                AREA_COLUMN: "Área CINE",
                "QT_MAT": "Matriculados",
                "QT_ING": "Ingressantes",
                "QT_CONC": "Concluintes",
            }
        )
        .sort_values("Matriculados", ascending=True)
    )

    fig = px.bar(
        by_area,
        y="Área CINE",
        x="Matriculados",
        orientation="h",
        title="Matrículas por Área do Conhecimento (CINE) — 2024",
        color="Matriculados",
        color_continuous_scale="Blues",
        text_auto=".2s",
    )
    fig.update_layout(
        yaxis_title="",
        xaxis_title="Matriculados",
        showlegend=False,
        height=max(480, len(by_area) * 36),
    )
    fig.update_traces(marker_color=CHART_COLORS["matriculados"])
    return fig


def getCoursesCompletionByAreaChart(df: DataFrame) -> Figure:
    """Taxa média de conclusão ponderada por área CINE."""
    if AREA_COLUMN not in df.columns:
        raise KeyError(f"Coluna {AREA_COLUMN} não encontrada no dataset.")

    by_area = df.groupby(AREA_COLUMN, as_index=False)[["QT_MAT", "QT_CONC"]].sum()
    mat = by_area["QT_MAT"].replace(0, float("nan"))
    by_area["Taxa de Conclusão (%)"] = (by_area["QT_CONC"] / mat * 100).fillna(0)
    by_area = by_area.rename(columns={AREA_COLUMN: "Área CINE"}).sort_values(
        "Taxa de Conclusão (%)", ascending=True
    )

    fig = px.bar(
        by_area,
        y="Área CINE",
        x="Taxa de Conclusão (%)",
        orientation="h",
        title="Taxa de Conclusão por Área do Conhecimento (CINE) — 2024",
        color="Taxa de Conclusão (%)",
        color_continuous_scale="Greens",
        text_auto=".1f",
    )
    fig.update_layout(
        yaxis_title="",
        xaxis_title="Taxa de Conclusão (%)",
        showlegend=False,
        height=max(480, len(by_area) * 36),
    )
    return fig
