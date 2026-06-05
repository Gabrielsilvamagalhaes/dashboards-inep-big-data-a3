from pandas import DataFrame

from plotly.graph_objs import Figure

import plotly.express as px


from dashboards.financing_programs_constants import (
    PROGRAM_COLORS,
    STAGE_LABEL,
    FinancingStage,
)

from dashboards.financing_programs_totals import get_reembolsavel_totals_table


def getFinancingReembolsavelChart(df: DataFrame, stage: FinancingStage) -> Figure:
    """Distribuição entre financiamento reembolsável e não reembolsável."""

    table = get_reembolsavel_totals_table(df, stage)

    stage_label = STAGE_LABEL[stage]

    fig = px.pie(
        table,
        names="Tipo",
        values="Quantidade",
        color="Tipo",
        title=f"Financiamento Reembolsável x Não Reembolsável — {stage_label} (2024)",
        color_discrete_map={
            "Reembolsável": PROGRAM_COLORS["Reembolsável"],
            "Não Reembolsável": PROGRAM_COLORS["Não Reembolsável"],
        },
    )

    fig.update_traces(textposition="inside", textinfo="percent+label")

    return fig
