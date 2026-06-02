import pandas as pd
from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px


def getStudentsComparisonByRaceChart(df: DataFrame) -> Figure:
    """Função que retorna o gráfico comparativo de estudantes por raça/cor (Ingresso × Matrícula × Conclusão)"""

    nomes_raca = ["Branca", "Preta", "Parda", "Amarela", "Indígena", "Não Declarada"]

    cols_ing = [
        "QT_ING_BRANCA",
        "QT_ING_PRETA",
        "QT_ING_PARDA",
        "QT_ING_AMARELA",
        "QT_ING_INDIGENA",
        "QT_ING_CORND",
    ]
    cols_mat = [
        "QT_MAT_BRANCA",
        "QT_MAT_PRETA",
        "QT_MAT_PARDA",
        "QT_MAT_AMARELA",
        "QT_MAT_INDIGENA",
        "QT_MAT_CORND",
    ]
    cols_conc = [
        "QT_CONC_BRANCA",
        "QT_CONC_PRETA",
        "QT_CONC_PARDA",
        "QT_CONC_AMARELA",
        "QT_CONC_INDIGENA",
        "QT_CONC_CORND",
    ]

    linhas = []
    for raca, col_ing, col_mat, col_conc in zip(nomes_raca, cols_ing, cols_mat, cols_conc):
        total_ing = df[col_ing].sum()
        total_mat = df[col_mat].sum()
        total_conc = df[col_conc].sum()

        total_veteranos = max(total_mat - total_ing, 0)

        linhas.append([raca, "1. Calouros", total_ing])
        linhas.append([raca, "2. Veteranos", total_veteranos])
        linhas.append([raca, "3. Formandos", total_conc])

    tabela_raca = pd.DataFrame(linhas, columns=["Raça/Cor", "Etapa", "Quantidade"])

    fig = px.bar(
        tabela_raca,
        x="Raça/Cor",
        y="Quantidade",
        color="Etapa",
        barmode="group",
        title="Perfil dos Estudantes por Raça/Cor (Calouros × Veteranos × Formandos)",
        text_auto=",.0f",
    )

    fig.update_layout(template="plotly_dark", title_x=0.5, height=650, separators=",.")

    return fig
