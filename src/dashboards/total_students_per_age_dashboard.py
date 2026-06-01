from typing import TypedDict
from pandas import DataFrame
import plotly.express as px
import pandas as pd
from plotly.graph_objs import Figure


class AgeCharts(TypedDict):
    total_students_per_age: Figure
    evolution_students_per_age: Figure


def getTotalStudentsPerAgeCharts(df: DataFrame) -> AgeCharts:
    """Função que retorna um dicionario de graficos da distribuição de alunos matriculados
    por idade e evolução de alunos por faixa etária"""

    df_education = df

    # Faixa etária
    nomes_faixas = ["0 a 17", "18 a 24", "25 a 29", "35 a 39", "40 a 49", "50 a 59", "60+"]

    cols_ing = [
        "QT_ING_0_17",
        "QT_ING_18_24",
        "QT_ING_25_29",
        "QT_ING_35_39",
        "QT_ING_40_49",
        "QT_ING_50_59",
        "QT_ING_60_MAIS",
    ]
    cols_mat = [
        "QT_MAT_0_17",
        "QT_MAT_18_24",
        "QT_MAT_25_29",
        "QT_MAT_35_39",
        "QT_MAT_40_49",
        "QT_MAT_50_59",
        "QT_MAT_60_MAIS",
    ]
    cols_conc = [
        "QT_CONC_0_17",
        "QT_CONC_18_24",
        "QT_CONC_25_29",
        "QT_CONC_35_39",
        "QT_CONC_40_49",
        "QT_CONC_50_59",
        "QT_CONC_60_MAIS",
    ]

    linhas_da_tabela = []

    # acoplando coluna em var
    for faixa, col_ing, col_mat, col_conc in zip(nomes_faixas, cols_ing, cols_mat, cols_conc):

        # Soma o total daquela coluna específica
        total_ing = df_education[col_ing].sum()
        total_mat = df_education[col_mat].sum()
        total_conc = df_education[col_conc].sum()

        linhas_da_tabela.append([faixa, "1. Ingressantes", total_ing])
        linhas_da_tabela.append([faixa, "2. Matriculados", total_mat])
        linhas_da_tabela.append([faixa, "3. Concluintes", total_conc])

    tabela_idades = pd.DataFrame(linhas_da_tabela, columns=["Faixa Etária", "Etapa", "Quantidade"])

    tabela_apenas_mat = tabela_idades[tabela_idades["Etapa"] == "2. Matriculados"]

    fig_distribuicao = px.bar(
        tabela_apenas_mat,
        x="Quantidade",
        y="Faixa Etária",
        orientation="h",
        title="Distribuição de Alunos Matriculados por Idade",
        color="Faixa Etária",
    )

    fig_distribuicao.update_layout(
        yaxis={"categoryorder": "array", "categoryarray": nomes_faixas[::-1]}
    )

    return {
        "total_students_per_age": fig_distribuicao,
    }
