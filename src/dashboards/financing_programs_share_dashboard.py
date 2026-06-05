from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px

from dashboards.financing_programs_constants import (
    PROGRAM_COLORS,
    STAGE_LABEL,
    FinancingStage,
)
from dashboards.financing_programs_totals import get_program_totals_table


def getFinancingProgramsShareChart(df: DataFrame, stage: FinancingStage) -> Figure:
    """Participação nos programas de financiamento para uma etapa (ingresso, matrícula ou conclusão)."""
    table = get_program_totals_table(df, stage)
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
