"""Colunas do microdado INEP usadas pelos dashboards (sem carregar o CSV inteiro)."""

from dashboards.financing_programs_constants import (
    FINANCING_PROGRAMS,
    FINANCING_PROGRAM_EXTRA,
    STAGE_PREFIX,
)

_AGE_SUFFIXES = ("0_17", "18_24", "25_29", "35_39", "40_49", "50_59", "60_MAIS")

_STATIC_COLUMNS = frozenset(
    {
        "NO_REGIAO",
        "NO_CURSO",
        "NO_UF",
        "NU_ANO_CENSO",
        "NO_CINE_ROTULO",
        "NO_CINE_AREA_GERAL",
        "TP_MODALIDADE_ENSINO",
        "CO_IES",
        "QT_MAT",
        "QT_ING",
        "QT_CONC",
        "QT_INSCRITO_TOTAL",
        "QT_INSCRITO_TOTAL_DIURNO",
        "QT_INSCRITO_TOTAL_NOTURNO",
        "QT_INSCRITO_TOTAL_EAD",
        "QT_ING_FEM",
        "QT_MAT_FEM",
        "QT_CONC_FEM",
        "QT_ING_MASC",
        "QT_MAT_MASC",
        "QT_CONC_MASC",
        "QT_MAT_FINANC",
        "QT_MAT_FIES",
        "QT_MAT_PROUNII",
        "QT_MAT_PROUNIP",
        "QT_ING_BRANCA",
        "QT_ING_PRETA",
        "QT_ING_PARDA",
        "QT_ING_AMARELA",
        "QT_ING_INDIGENA",
        "QT_ING_CORND",
        "QT_MAT_BRANCA",
        "QT_MAT_PRETA",
        "QT_MAT_PARDA",
        "QT_MAT_AMARELA",
        "QT_MAT_INDIGENA",
        "QT_MAT_CORND",
        "QT_CONC_BRANCA",
        "QT_CONC_PRETA",
        "QT_CONC_PARDA",
        "QT_CONC_AMARELA",
        "QT_CONC_INDIGENA",
        "QT_CONC_CORND",
        "QT_ING_DEFICIENTE",
        "QT_MAT_DEFICIENTE",
        "QT_CONC_DEFICIENTE",
    }
)

_CATEGORY_COLUMNS = frozenset(
    {
        "NO_REGIAO",
        "NO_UF",
        "NO_CINE_ROTULO",
        "NO_CINE_AREA_GERAL",
    }
)

_INTEGER_ID_COLUMNS = frozenset(
    {
        "NU_ANO_CENSO",
        "CO_IES",
        "TP_MODALIDADE_ENSINO",
    }
)


def get_required_csv_columns() -> list[str]:
    """Lista de colunas necessárias para todos os gráficos do app."""
    cols = set(_STATIC_COLUMNS)

    for stage_prefix in ("QT_ING", "QT_MAT", "QT_CONC"):
        for suffix in _AGE_SUFFIXES:
            cols.add(f"{stage_prefix}_{suffix}")

    for prefix in STAGE_PREFIX.values():
        cols.add(f"{prefix}_FINANC")
        cols.add(f"{prefix}_FINANC_REEMB")
        cols.add(f"{prefix}_FINANC_NREEMB")
        for _, program_suffix in FINANCING_PROGRAMS:
            cols.add(f"{prefix}_{program_suffix}")
        for extra_cols in FINANCING_PROGRAM_EXTRA.values():
            for extra in extra_cols:
                cols.add(f"{prefix}_{extra}")

    return sorted(cols)


def get_category_columns() -> frozenset[str]:
    return _CATEGORY_COLUMNS


def get_integer_id_columns() -> frozenset[str]:
    return _INTEGER_ID_COLUMNS
