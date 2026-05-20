from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.graph_objects as go


def getFinancingKpiCharts(df: DataFrame) -> dict[str, Figure]:
    """Indicadores resumidos do impacto dos programas de financiamento."""
    total_mat_financ = float(df["QT_MAT_FINANC"].fillna(0).sum())
    total_mat = float(df["QT_MAT"].fillna(0).sum()) if "QT_MAT" in df.columns else 0.0
    total_fies = float(df["QT_MAT_FIES"].fillna(0).sum())
    total_prouni = float(df["QT_MAT_PROUNII"].fillna(0).sum()) + float(
        df["QT_MAT_PROUNIP"].fillna(0).sum()
    )

    fig_total = go.Figure(
        go.Indicator(
            mode="number",
            value=total_mat_financ,
            number={"valueformat": ",.0f"},
            title={"text": "Matriculados em Programas de Financiamento"},
        )
    )

    fig_fies = go.Figure(
        go.Indicator(
            mode="number",
            value=total_fies,
            number={"valueformat": ",.0f"},
            title={"text": "Matriculados via FIES"},
        )
    )

    fig_prouni = go.Figure(
        go.Indicator(
            mode="number",
            value=total_prouni,
            number={"valueformat": ",.0f"},
            title={"text": "Matriculados via PROUNI (Integral e Parcial)"},
        )
    )

    return {
        "financing_total_indicator": fig_total,
        "financing_fies_indicator": fig_fies,
        "financing_prouni_indicator": fig_prouni,
    }
