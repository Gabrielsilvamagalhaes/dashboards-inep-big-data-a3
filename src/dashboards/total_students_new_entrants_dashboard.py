from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure


def getTotalStudentsNewEntrantsChart(df: DataFrame, years: int) -> Figure:
    """Função que retorna total de ingressantes por ano"""
    df_education = df["QT_ING"]

    total_students_new_entrants = df_education.sum()
    total_students_new_entrants = {"Ano": years, "Total": [total_students_new_entrants]}

    fig = px.bar(
        total_students_new_entrants,
        x="Ano",
        y="Total",
        title="Ingressantes totais por ano",
        labels={"y": "Quantidade de Pessoas", "x": "Censo"},
        text_auto=",.0f",
    )

    fig.update_traces(marker_color="CornflowerBlue", width=0.1)
    fig.update_layout(yaxis_tickformat=",.0f")

    return fig
