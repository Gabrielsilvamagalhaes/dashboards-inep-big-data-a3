from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure


def getTotalStudentsInstitutionsChart(df: DataFrame) -> Figure:
    """Função que retorna total de instituições por ano"""
    df_education = df[
        [
            "NU_ANO_CENSO",
            "CO_IES",
        ]
    ]

    total_institutions = (
        df_education.groupby("NU_ANO_CENSO", as_index=False)["CO_IES"]
        .nunique()
        .rename(
            columns={
                "NU_ANO_CENSO": "Ano",
                "CO_IES": "Total",
            }
        )
    )

    total_institutions["Ano"] = total_institutions["Ano"].astype(str)

    fig = px.bar(
        total_institutions,
        x="Ano",
        y="Total",
        title="Total de Instituições",
        labels={"Total": "Total de Instituições", "Ano": "Censo"},
        text_auto="",
    )

    fig.update_traces(marker_color="CornflowerBlue", width=0.1)
    fig.update_xaxes(type="category")
    fig.update_layout(yaxis_tickformat="")

    return fig
