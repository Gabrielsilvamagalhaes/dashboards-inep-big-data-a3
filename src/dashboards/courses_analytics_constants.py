"""Constantes e agregações para análise de cursos (Censo ES 2024)."""

from pandas import DataFrame
import pandas as pd

COURSE_COLUMN = "NO_CINE_ROTULO"
AREA_COLUMN = "NO_CINE_AREA_GERAL"
TOP_N_DEFAULT = 20
MIN_ENROLLMENT_FOR_RATE = 500

MODALITY_LABELS: dict[int | float, str] = {
    1: "Presencial",
    2: "Educação a Distância",
}

DEGREE_LABELS: dict[int | float, str] = {
    1: "Bacharelado",
    2: "Licenciatura",
    3: "Tecnológico",
    4: "Sequencial",
}

CHART_COLORS = {
    "matriculados": "#2C5E8A",
    "ingressantes": "#88398A",
    "concluintes": "#B07AB8",
    "taxa": "#2ca02c",
}


def prepare_courses_summary(df: DataFrame) -> DataFrame:
    """Agrega matrículas, ingressantes e concluintes por rótulo CINE do curso."""
    grouped = (
        df.groupby(COURSE_COLUMN, as_index=False)[["QT_MAT", "QT_ING", "QT_CONC"]]
        .sum()
        .rename(
            columns={
                "QT_MAT": "Matriculados",
                "QT_ING": "Ingressantes",
                "QT_CONC": "Concluintes",
            }
        )
    )
    mat = grouped["Matriculados"].replace(0, pd.NA)
    grouped["Taxa de Conclusão (%)"] = (grouped["Concluintes"] / mat * 100).fillna(0)
    return grouped
