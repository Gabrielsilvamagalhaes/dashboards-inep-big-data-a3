from typing import TypedDict
from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd


class GenderCharts(TypedDict):
    total_students_per_gender: Figure
    total_students_gender_per_stage: Figure


def getTotalStudentsPerGenderCharts(df: DataFrame) -> GenderCharts:
    """Função que retorna um dicionario a distribuição de genero de estudantes matriculados ativos
    e comparativo de genero por etapa no ensino superior"""
    df_education = df

    # Mulheres
    total_mat_fem = df_education["QT_MAT_FEM"].sum()

    # Homens
    total_mat_masc = df_education["QT_MAT_MASC"].sum()

    linhas_pizza = [["Feminino", total_mat_fem], ["Masculino", total_mat_masc]]

    tabela_genero = pd.DataFrame(linhas_pizza, columns=["Gênero", "Quantidade"])

    fig_genero = px.pie(
        tabela_genero,
        names="Gênero",
        values="Quantidade",
        color="Gênero",
        title="Distribuição de Gênero (Total de Matrículas Ativas)",
        hole=0.4,
        color_discrete_map={"Feminino": "#88398A", "Masculino": "#2C5E8A"},
    )

    return {"total_students_per_gender": fig_genero}
