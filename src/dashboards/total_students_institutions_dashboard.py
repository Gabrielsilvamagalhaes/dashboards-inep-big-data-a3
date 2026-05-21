from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.graph_objects as go


def getTotalStudentsInstitutionsChart(df: DataFrame) -> Figure:
    """Função que retorna total de instituições por ano"""
    total_institutions = df["CO_IES"].nunique()

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=total_institutions,
            number={"valueformat": ",.0f"},
            title={"text": "Total de Instituições (Brasil)"},
        )
    )
    fig.update_layout(separators=",.")
    fig.update_layout(height=300)

    return fig
