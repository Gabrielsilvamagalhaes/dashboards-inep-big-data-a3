from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd

from dashboards.financing_programs_constants import (
    FINANCING_PROGRAMS,
    FINANCING_PROGRAM_EXTRA,
    PROGRAM_COLORS,
    STAGE_LABEL,
    STAGE_PREFIX,
    FinancingStage,
)


def _program_totals(df: DataFrame, stage: FinancingStage) -> pd.DataFrame:
    prefix = STAGE_PREFIX[stage]
    rows = []
    for label, suffix in FINANCING_PROGRAMS:
        col = f"{prefix}_{suffix}"
        qty = float(df[col].fillna(0).sum()) if col in df.columns else 0.0
        for extra in FINANCING_PROGRAM_EXTRA.get(label, []):
            extra_col = f"{prefix}_{extra}"
            if extra_col in df.columns:
                qty += float(df[extra_col].fillna(0).sum())
        rows.append([label, qty])
    table = pd.DataFrame(rows, columns=["Programa", "Quantidade"])
    return table[table["Quantidade"] > 0]


def getFinancingProgramsShareChart(df: DataFrame, stage: FinancingStage) -> Figure:
    """Participação nos programas de financiamento para uma etapa (ingresso, matrícula ou conclusão)."""
    table = _program_totals(df, stage)
    stage_label = STAGE_LABEL[stage]

    fig = px.pie(
        table,
        names="Programa",
        values="Quantidade",
        color="Programa",
        title=f"Participação em Programas de Financiamento — {stage_label} (2024)",
        hole=0.4,
        color_discrete_map=PROGRAM_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig
