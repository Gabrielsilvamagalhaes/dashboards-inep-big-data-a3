from typing import TypedDict

from pandas import DataFrame, Series
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Figure

from dashboards.courses_analytics_constants import CHART_COLORS, COURSE_COLUMN, format_br_number

_COURSE_NAME_COLUMNS = (COURSE_COLUMN, "NO_CURSO")


class CoursesCharts(TypedDict):
    total_courses_indicator: Figure
    total_courses_graphic: Figure


def _resolve_course_column(df: DataFrame) -> str | None:
    """Escolhe a coluna de nome do curso que realmente tem dados no microdado."""
    for column in _COURSE_NAME_COLUMNS:
        if column not in df.columns:
            continue
        valid = df[column].dropna().astype(str).str.strip()
        if valid.ne("").any():
            return column
    return None


def _course_name_series(df: DataFrame) -> Series:
    column = _resolve_course_column(df)
    if column is None:
        return Series(dtype="object")

    names = df[column].dropna().astype(str).str.strip()
    return names[names != ""]


def getTotalCoursesCharts(df: DataFrame) -> CoursesCharts:
    """Indicador e top 10 de cursos cadastrados no recorte."""
    course_names = _course_name_series(df)
    total_courses = int(course_names.nunique())

    fig_total = go.Figure(
        go.Indicator(
            mode="number",
            value=total_courses,
            number={"valueformat": ",.0f"},
            title={"text": "Total de Cursos Cadastrados (Brasil)"},
        )
    )
    fig_total.update_layout(separators=",.", height=300)

    df_count = (
        course_names.value_counts().head(10).rename_axis("Curso").reset_index(name="Quantidade")
    )
    df_count["Curso"] = df_count["Curso"].astype(str)

    if df_count.empty:
        fig = go.Figure()
        fig.update_layout(
            title="Top 10 Cursos por Quantidade",
            annotations=[
                {
                    "text": "Sem nomes de curso disponíveis no recorte filtrado.",
                    "xref": "paper",
                    "yref": "paper",
                    "x": 0.5,
                    "y": 0.5,
                    "showarrow": False,
                    "font": {"size": 14, "color": "#e8eaf0"},
                }
            ],
            height=400,
        )
        return {"total_courses_indicator": fig_total, "total_courses_graphic": fig}

    fig = px.bar(
        df_count,
        y="Curso",
        x="Quantidade",
        orientation="h",
        title="Top 10 Cursos por Quantidade de Registros",
        color="Quantidade",
        color_continuous_scale="Blues",
    )
    fig.update_layout(
        yaxis={
            "categoryorder": "total ascending",
            "title": "Curso",
            "type": "category",
            "tickfont": {"size": 11, "color": "#e8eaf0"},
        },
        xaxis_title="Quantidade de registros",
        showlegend=False,
        height=max(500, len(df_count) * 48),
        margin={"l": 12, "r": 48, "t": 56, "b": 40},
        separators=",.",
        hoverlabel={"bgcolor": "black", "font_size": 13},
    )
    fig.update_xaxes(range=[0, df_count["Quantidade"].max() * 1.18])
    fig.update_traces(
        marker_color=CHART_COLORS["matriculados"],
        text=[format_br_number(v) for v in df_count["Quantidade"]],
        textposition="outside",
        textfont={"size": 12, "color": "#FFFFFF"},
        cliponaxis=False,
        hovertemplate="<b>%{y}</b><br>Registros: %{x:,.0f}<extra></extra>",
    )

    return {"total_courses_indicator": fig_total, "total_courses_graphic": fig}
