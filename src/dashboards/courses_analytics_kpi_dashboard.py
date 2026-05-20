from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.graph_objects as go

from dashboards.courses_analytics_constants import COURSE_COLUMN


def getCoursesAnalyticsKpiCharts(df: DataFrame) -> dict[str, Figure]:
    """Indicadores resumidos da análise de cursos."""
    distinct_courses = int(df[COURSE_COLUMN].nunique())
    total_mat = float(df["QT_MAT"].fillna(0).sum())
    total_ing = float(df["QT_ING"].fillna(0).sum())
    total_conc = float(df["QT_CONC"].fillna(0).sum())
    completion_rate = (total_conc / total_mat * 100) if total_mat > 0 else 0.0

    return {
        "courses_count_indicator": go.Figure(
            go.Indicator(
                mode="number",
                value=distinct_courses,
                number={"valueformat": ",.0f"},
                title={"text": "Cursos Distintos (CINE)"},
            )
        ),
        "courses_mat_indicator": go.Figure(
            go.Indicator(
                mode="number",
                value=total_mat,
                number={"valueformat": ",.0f"},
                title={"text": "Total de Matriculados"},
            )
        ),
        "courses_ing_indicator": go.Figure(
            go.Indicator(
                mode="number",
                value=total_ing,
                number={"valueformat": ",.0f"},
                title={"text": "Total de Ingressantes"},
            )
        ),
        "courses_completion_indicator": go.Figure(
            go.Indicator(
                mode="number",
                value=completion_rate,
                number={"valueformat": ".1f", "suffix": "%"},
                title={"text": "Taxa de Conclusão Geral"},
            )
        ),
    }
