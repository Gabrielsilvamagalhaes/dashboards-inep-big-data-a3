from typing import TypedDict
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
)
from services.calculate_veterans import calculateVeterans


class FinancingByStageCharts(TypedDict):
    financing_programs_by_stage: Figure


def _sum_program_columns(df: DataFrame, prefix: str, suffixes: list[str]) -> float:
    total = 0.0
    for suffix in suffixes:
        col = f"{prefix}_{suffix}"
        if col in df.columns:
            total += float(df[col].fillna(0).sum())
    return total


def _program_quantity(df: DataFrame, stage: str, program_label: str, suffix: str) -> float:
    suffixes = [suffix, *FINANCING_PROGRAM_EXTRA.get(program_label, [])]

    if stage == "matriculados":
        qty_mat = _sum_program_columns(df, STAGE_PREFIX["matriculados"], suffixes)
        qty_ing = _sum_program_columns(df, STAGE_PREFIX["ingressantes"], suffixes)
        return float(calculateVeterans(qty_mat, qty_ing))

    prefix = STAGE_PREFIX[stage]
    return _sum_program_columns(df, prefix, suffixes)


def _build_stage_table(df: DataFrame) -> pd.DataFrame:
    rows = []
    for stage in ("ingressantes", "matriculados", "concluintes"):
        stage_label = STAGE_LABEL[stage]

        for program_label, suffix in FINANCING_PROGRAMS:
            qty = _program_quantity(df, stage, program_label, suffix)
            rows.append([stage_label, program_label, qty])
    return pd.DataFrame(rows, columns=["Etapa", "Programa", "Quantidade"])


def getFinancingProgramsByStageCharts(df: DataFrame) -> FinancingByStageCharts:
    """Comparativo de programas por etapa e foco FIES x PROUNI."""
    table = _build_stage_table(df)

    # table["Etapa"] = table["Etapa"].replace("Matriculados", "Veteranos")

    fig_programs = px.bar(
        table,
        x="Etapa",
        y="Quantidade",
        color="Programa",
        barmode="group",
        title="Programas de Financiamento por Etapa no Ensino Superior (2024)",
        color_discrete_map=PROGRAM_COLORS,
        text_auto=".2s",
    )
    fig_programs.update_layout(
        xaxis_title="Etapa",
        yaxis_title="Quantidade de estudantes",
        legend_title="Programa",
    )

    return {
        "financing_programs_by_stage": fig_programs,
    }
