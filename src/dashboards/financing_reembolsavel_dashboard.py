from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd

from dashboards.financing_programs_constants import (
    PROGRAM_COLORS,
    STAGE_LABEL,
    STAGE_PREFIX,
    FinancingStage,
)


def _reembolsavel_table(df: DataFrame, stage: FinancingStage) -> pd.DataFrame:
    prefix = STAGE_PREFIX[stage]
    reembolsavel = float(df[f"{prefix}_FINANC_REEMB"].fillna(0).sum())
    nao_reembolsavel = float(df[f"{prefix}_FINANC_NREEMB"].fillna(0).sum())
    return pd.DataFrame(
        [
            ["Reembolsável", reembolsavel],
            ["Não Reembolsável", nao_reembolsavel],
        ],
        columns=["Tipo", "Quantidade"],
    )


def getFinancingReembolsavelChart(df: DataFrame, stage: FinancingStage) -> Figure:
    """Distribuição entre financiamento reembolsável e não reembolsável."""
    table = _reembolsavel_table(df, stage)
    stage_label = STAGE_LABEL[stage]

    fig = px.pie(
        table,
        names="Tipo",
        values="Quantidade",
        color="Tipo",
        title=f"Financiamento Reembolsável x Não Reembolsável — {stage_label} (2024)",
        color_discrete_map=PROGRAM_COLORS,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig


def getFinancingReembolsavelByStageChart(df: DataFrame) -> Figure:
    """Comparativo reembolsável x não reembolsável nas três etapas."""
    rows = []
    for stage in ("ingressantes", "matriculados", "concluintes"):
        prefix = STAGE_PREFIX[stage]
        stage_label = STAGE_LABEL[stage]
        rows.append([stage_label, "Reembolsável", float(df[f"{prefix}_FINANC_REEMB"].fillna(0).sum())])
        rows.append(
            [stage_label, "Não Reembolsável", float(df[f"{prefix}_FINANC_NREEMB"].fillna(0).sum())]
        )
    table = pd.DataFrame(rows, columns=["Etapa", "Tipo", "Quantidade"])

    fig = px.bar(
        table,
        x="Etapa",
        y="Quantidade",
        color="Tipo",
        barmode="group",
        title="Reembolsável x Não Reembolsável por Etapa (2024)",
        color_discrete_map=PROGRAM_COLORS,
        text_auto=".2s",
    )
    fig.update_layout(
        xaxis_title="Etapa",
        yaxis_title="Quantidade de estudantes",
        legend_title="Tipo de financiamento",
    )
    return fig
