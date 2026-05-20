from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure


def getTotalStudentsInstitutionsChart(df: DataFrame, years: int) -> Figure:
    """Função que retorna total de instituições por ano"""
    df_education = df["CO_IES"]

    total_institutions = df_education.nunique()
    total_institutions = {"Ano": years, "Total": [total_institutions]}

    fig = px.bar(
        total_institutions,
        x="Ano",
        y="Total",
        title="Total de Instituições por Ano",
        labels={"y": "Total de Instituiçoes", "x": "Ano"},
        text_auto=",.0f",
    )

    fig.update_traces(marker_color="CornflowerBlue", width=0.1)
    fig.update_layout(yaxis_tickformat=",.0f")

    return fig
