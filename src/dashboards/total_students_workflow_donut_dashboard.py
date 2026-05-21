from pandas import DataFrame
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure


def getTotalStudentsDonutChart(df: DataFrame) -> Figure:
    """Função que retorna um donut do fluxo total de estudantes no ensino superior"""

    df_education = df

    total_inscritos = df_education["QT_INSCRITO_TOTAL"].sum()
    total_ingressantes = df_education["QT_ING"].sum()
    total_matriculados = df_education["QT_MAT"].sum()
    total_concluintes = df_education["QT_CONC"].sum()

    linhas_da_tabela = [
        ["Inscritos", total_inscritos],
        ["Novatos", total_ingressantes],
        ["Veteranos", total_matriculados],
        ["Formandos", total_concluintes],
    ]

    tabela_workflow = pd.DataFrame(linhas_da_tabela, columns=["Etapa", "Quantidade"])

    fig = px.pie(
        tabela_workflow,
        names="Etapa",
        values="Quantidade",
        title="Distribuição total de estudantes no ensino superior",
        hole=0.4,
        color="Etapa",
        color_discrete_map={
            "Inscritos": "#2C5E8A",
            "Novatos": "#3A8D7C",
            "Veteranos": "#88398A",
            "Formandos": "#C7822D",
        },
    )

    fig.update_traces(
        textinfo="percent+label", hovertemplate="%{label}: %{value:,.0f}<extra></extra>"
    )

    return fig
