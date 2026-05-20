from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd

from dashboards.financing_programs_constants import PROGRAM_COLORS


def getFinancingProgramsByRegionChart(
    df: DataFrame, select_regions: list[str], stage_prefix: str = "QT_MAT"
) -> Figure:
    """Distribuição regional dos principais programas (matriculados por padrão)."""
    df_filtered = df[df["NO_REGIAO"].isin(select_regions)]

    programs = [
        ("FIES", f"{stage_prefix}_FIES"),
        ("PROUNI Integral", f"{stage_prefix}_PROUNII"),
        ("PROUNI Parcial", f"{stage_prefix}_PROUNIP"),
    ]

    rows = []
    for region in select_regions:
        region_df = df_filtered[df_filtered["NO_REGIAO"] == region]
        for label, col in programs:
            if col not in region_df.columns:
                continue
            rows.append([region, label, float(region_df[col].fillna(0).sum())])

    table = pd.DataFrame(rows, columns=["Região", "Programa", "Quantidade"])

    fig = px.bar(
        table,
        x="Região",
        y="Quantidade",
        color="Programa",
        barmode="group",
        title="FIES e PROUNI por Região — Matriculados (2024)",
        color_discrete_map=PROGRAM_COLORS,
        text_auto=".2s",
    )
    fig.update_layout(
        xaxis_title="Região",
        yaxis_title="Quantidade de estudantes",
        legend_title="Programa",
    )
    return fig


def getFinancingTotalByRegionChart(
    df: DataFrame, select_regions: list[str], stage_prefix: str = "QT_MAT"
) -> Figure:
    """Total de estudantes em programas de financiamento por região."""
    col_total = f"{stage_prefix}_FINANC"
    df_filtered = df[df["NO_REGIAO"].isin(select_regions)]

    by_region = (
        df_filtered.groupby("NO_REGIAO", as_index=False)[col_total]
        .sum()
        .rename(columns={"NO_REGIAO": "Região", col_total: "Quantidade"})
    )

    fig = px.bar(
        by_region,
        x="Região",
        y="Quantidade",
        title="Total em Programas de Financiamento por Região — Matriculados (2024)",
        color="Quantidade",
        color_continuous_scale="Blues",
        text_auto=".2s",
    )
    fig.update_layout(
        xaxis_title="Região",
        yaxis_title="Quantidade de estudantes",
        showlegend=False,
    )
    return fig
