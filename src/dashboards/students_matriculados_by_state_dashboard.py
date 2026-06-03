from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure


def getStudentsMatriculadosByStateChart(df: DataFrame) -> Figure:
    """Matriculados por estado (todos os UFs do recorte), barras verticais."""
    by_state = (
        df.groupby("NO_UF", as_index=False)
        .agg(Matriculados=("QT_MAT", "sum"), Região=("NO_REGIAO", "first"))
        .rename(columns={"NO_UF": "Estado"})
        .sort_values("Matriculados", ascending=False)
    )

    fig = px.bar(
        by_state,
        x="Estado",
        y="Matriculados",
        color="Região",
        title="Matriculados por Estado (Censo ES 2024)",
    )
    fig.update_layout(
        height=450,
        bargap=0.15,
        xaxis_title="Estado",
        yaxis_title="Matriculados",
        legend_title="Região",
    )
    fig.update_xaxes(tickangle=-45)
    fig.update_traces(width=0.75)
    return fig
