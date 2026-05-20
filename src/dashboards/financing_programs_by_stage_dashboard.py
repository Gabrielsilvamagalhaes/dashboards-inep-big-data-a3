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


class FinancingByStageCharts(TypedDict):
    financing_programs_by_stage: Figure
    financing_fies_prouni_comparison: Figure


def _build_stage_table(df: DataFrame) -> pd.DataFrame:
    rows = []
    for stage in ("ingressantes", "matriculados", "concluintes"):
        prefix = STAGE_PREFIX[stage]
        stage_label = STAGE_LABEL[stage]
        for program_label, suffix in FINANCING_PROGRAMS:
            col = f"{prefix}_{suffix}"
            qty = float(df[col].fillna(0).sum()) if col in df.columns else 0.0
            for extra in FINANCING_PROGRAM_EXTRA.get(program_label, []):
                extra_col = f"{prefix}_{extra}"
                if extra_col in df.columns:
                    qty += float(df[extra_col].fillna(0).sum())
            rows.append([stage_label, program_label, qty])
    return pd.DataFrame(rows, columns=["Etapa", "Programa", "Quantidade"])


def getFinancingProgramsByStageCharts(df: DataFrame) -> FinancingByStageCharts:
    """Comparativo de programas por etapa e foco FIES x PROUNI."""
    table = _build_stage_table(df)

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

    fies_prouni = table[table["Programa"].isin(["FIES", "PROUNI Integral", "PROUNI Parcial"])]
    fig_fies_prouni = px.bar(
        fies_prouni,
        x="Etapa",
        y="Quantidade",
        color="Programa",
        barmode="group",
        title="FIES e PROUNI por Etapa (2024)",
        color_discrete_map=PROGRAM_COLORS,
        text_auto=".2s",
    )
    fig_fies_prouni.update_layout(
        xaxis_title="Etapa",
        yaxis_title="Quantidade de estudantes",
        legend_title="Programa",
    )

    return {
        "financing_programs_by_stage": fig_programs,
        "financing_fies_prouni_comparison": fig_fies_prouni,
    }
