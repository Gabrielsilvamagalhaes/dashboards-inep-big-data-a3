from typing import TypedDict
from pandas import DataFrame
import plotly.graph_objects as go
import plotly.express as px
from plotly.graph_objs import Figure


class CoursesCharts(TypedDict):
    total_courses_indicator: Figure
    total_courses_graphic: Figure


def getTotalCoursesCharts(df: DataFrame) -> CoursesCharts:
    """Função que retorna um dicionario contendo um indicador da quantidade
    total de cursos cadastrados e um grafico dos top 10 cursos por quantidade"""
    df_education = df["NO_CURSO"]
    total_courses = len(df_education.unique())

    fig_total = go.Figure(
        go.Indicator(
            mode="number",
            value=total_courses,
            number={"valueformat": ",.0f"},
            title={"text": "Total de Cursos Cadastrados (Brasil)"},
        )
    )
    fig_total.update_layout(separators=",.")

    df_count = df_education.value_counts().reset_index().head(10)
    df_count.columns = ["Curso", "Quantidade"]

    fig = px.bar(
        df_count,
        y="Curso",
        x="Quantidade",
        orientation="h",
        title="Top 10 Cursos por Quantidade",
        text_auto=".2s",
        color="Quantidade",
        color_continuous_scale="Blues",
    )

    fig.update_layout(yaxis={"categoryorder": "total ascending"}, height=900)

    return {"total_courses_indicator": fig_total, "total_courses_graphic": fig}
