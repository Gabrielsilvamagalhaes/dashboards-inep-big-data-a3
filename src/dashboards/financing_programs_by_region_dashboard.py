from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd

from dashboards.financing_programs_constants import (
    FINANCING_PROGRAM_EXTRA,
    FINANCING_PROGRAMS,
    PROGRAM_COLORS,
    STAGE_LABEL,
    STAGE_PREFIX,
)


def getFinancingProgramsByRegionChart(
    df: DataFrame, select_regions: list[str], stage_prefix: str = "QT_MAT"
) -> Figure:
    """
    Distribuição regional dos programas de financiamento (por etapa).

    A lógica de agregação de "Outros ..." deve ser consistente com o gráfico de share
    (pie) da página de Programas de Financiamento.
    """

    # Deduz o nome da etapa a partir do prefixo (QT_ING, QT_MAT, QT_CONC).
    stage = next((s for s, p in STAGE_PREFIX.items() if p == stage_prefix), None)
    stage_label = STAGE_LABEL.get(stage, "Matriculados")
    df_filtered = df[df["NO_REGIAO"].isin(select_regions)]

    rows = []
    for region in select_regions:
        region_df = df_filtered[df_filtered["NO_REGIAO"] == region]

        for program_label, program_suffix in FINANCING_PROGRAMS:
            base_col = f"{stage_prefix}_{program_suffix}"
            qty = float(region_df[base_col].fillna(0).sum()) if base_col in region_df.columns else 0.0

            # Agrega colunas extras para os "Outros ...", mantendo a mesma coerência do share.
            for extra_suffix in FINANCING_PROGRAM_EXTRA.get(program_label, []):
                extra_col = f"{stage_prefix}_{extra_suffix}"
                if extra_col in region_df.columns:
                    qty += float(region_df[extra_col].fillna(0).sum())

            if qty > 0:
                rows.append([region, program_label, qty])

    table = pd.DataFrame(rows, columns=["Região", "Programa", "Quantidade"])
    if table.empty:
        # Retorna um gráfico vazio para evitar quebra de UI no caso de recorte sem dados.
        fig = Figure()
        fig.update_layout(title=f"Programas de Financiamento por Região — {stage_label} (2024)")
        return fig

    fig = px.bar(
        table,
        x="Região",
        y="Quantidade",
        color="Programa",
        barmode="group",
        title=f"Programas de Financiamento por Região — {stage_label} (2024)",
        color_discrete_map=PROGRAM_COLORS,
        text_auto=".2s",
    )
    fig.update_layout(
        xaxis_title="Região",
        yaxis_title="Quantidade de estudantes",
        legend_title="Programa",
    )
    return fig


# def getFinancingTotalByRegionChart(
#     df: DataFrame, select_regions: list[str], stage_prefix: str = "QT_MAT"
# ) -> Figure:
#     """Total de estudantes em programas de financiamento por região."""
#     col_total = f"{stage_prefix}_FINANC"
#     df_filtered = df[df["NO_REGIAO"].isin(select_regions)]

#     by_region = (
#         df_filtered.groupby("NO_REGIAO", as_index=False)[col_total]
#         .sum()
#         .rename(columns={"NO_REGIAO": "Região", col_total: "Quantidade"})
#     )

#     fig = px.bar(
#         by_region,
#         x="Região",
#         y="Quantidade",
#         title="Total em Programas de Financiamento por Região — Matriculados (2024)",
#         color="Quantidade",
#         color_continuous_scale="Blues",
#         text_auto=".2s",
#     )
#     fig.update_layout(
#         xaxis_title="Região",
#         yaxis_title="Quantidade de estudantes",
#         showlegend=False,
#     )
#     return fig
