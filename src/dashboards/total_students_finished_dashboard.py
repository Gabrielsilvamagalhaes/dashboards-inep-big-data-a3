from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure


def getTotalStudentsFinishedChart(df: DataFrame, years: int) -> Figure:
    """Função que retorna grafico de concluintes totais"""
    df_education = df["QT_CONC"]

    total_students_finished = df_education.sum()
    total_students_finished = {"Ano": years, "Total": [total_students_finished]}

    fig = px.bar(
        total_students_finished,
        x="Ano",
        y="Total",
        title="Concluintes totais por ano",
        labels={"y": "Quantidade de Pessoas", "x": "Censo"},
        text_auto=",.0f",
    )
    fig.update_traces(marker_color="CornflowerBlue", width=0.1)
    fig.update_layout(yaxis_tickformat=",.0f")

    return fig
