from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px


def getTotalStudentsPerStateChart(df: DataFrame, select_regions: list) -> Figure:
    """Função que retorna o grafico da distribuição do total de alunos por estado"""
    df_education = df[["NO_REGIAO", "NO_UF"]]

    df_education_filtered = df_education[df_education["NO_REGIAO"].isin(select_regions)]

    total_state = (
        df_education_filtered.groupby(["NO_REGIAO", "NO_UF"], observed=True)
        .size()
        .reset_index(name="Total")
        .rename(columns={"NO_REGIAO": "Região", "NO_UF": "Estado"})
    )

    total_state_filtered = (
        total_state.sort_values(["Região", "Total"], ascending=[True, False])
        .groupby("Região", group_keys=False)
        .head(5)
    )

    total_students_per_state_graphic = px.bar(
        total_state_filtered,
        x="Estado",
        y="Total",
        title="Top Distribuição de Alunos por Estados e Região (Censo 2024)",
        labels={"Total": "Quantidade de Pessoas", "Estado": "Estado", "Região": "Região"},
        color="Região",
        text_auto=".2s",
    )

    total_students_per_state_graphic.update_layout(xaxis={"categoryorder": "total descending"})

    return total_students_per_state_graphic
