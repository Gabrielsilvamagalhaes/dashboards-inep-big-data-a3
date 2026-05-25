import pandas as pd
from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import plotly.graph_objects as go


def getStudentsDistributionByDisabilityChart(df: DataFrame) -> Figure:
    """Função que retorna o indicador de alunos matriculados com deficiência."""

    total_mat = df["QT_MAT_DEFICIENTE"].sum()

    fig = go.Figure(
        go.Indicator(
            mode="number",
            value=total_mat,
            number={"valueformat": ",.0f"},
            title={"text": "Total de Estudantes com Deficiência (Matriculados)"},
        )
    )

    fig.update_layout(template="plotly_dark", height=400, separators=",.")

    return fig


def getStudentsComparisonByDisabilityChart(df: DataFrame) -> Figure:
    """Função que retorna o comparativo (Ingresso x Matrícula x Conclusão) para estudantes com deficiência."""

    total_ing = df["QT_ING_DEFICIENTE"].sum()
    total_mat = df["QT_MAT_DEFICIENTE"].sum()
    total_conc = df["QT_CONC_DEFICIENTE"].sum()

    linhas = [
        ["1. Ingressantes", total_ing],
        ["2. Matriculados", total_mat],
        ["3. Concluintes", total_conc],
    ]

    tabela_def = pd.DataFrame(linhas, columns=["Etapa", "Quantidade"])

    fig = px.bar(
        tabela_def,
        x="Etapa",
        y="Quantidade",
        color="Etapa",
        title="Perfil dos Estudantes com Deficiência (Ingresso × Matrícula × Conclusão)",
        text_auto=",.0f",
    )

    fig.update_layout(
        template="plotly_dark",
        title_x=0.5,
        height=600,
        separators=",.",
        showlegend=False,
    )

    return fig
