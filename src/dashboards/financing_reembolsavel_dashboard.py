from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px
import pandas as pd

from dashboards.financing_programs_constants import (
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

    # Mapeamento específico para as duas categorias usadas no pie ("Tipo").
    # (Evita depender de um dicionário com chaves de programas diferentes.)
    type_colors = {
        "Reembolsável": "#2C5E8A",
        "Não Reembolsável": "#88398A",
    }

    fig = px.pie(
        table,
        names="Tipo",
        values="Quantidade",
        color="Tipo",
        title=f"Financiamento Reembolsável x Não Reembolsável — {stage_label} (2024)",
        color_discrete_map=type_colors,
    )
    fig.update_traces(textposition="inside", textinfo="percent+label")
    return fig
