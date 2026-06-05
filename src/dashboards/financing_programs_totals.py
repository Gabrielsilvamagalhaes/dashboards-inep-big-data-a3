"""Agregações compartilhadas dos programas de financiamento."""

from pandas import DataFrame
import pandas as pd

from dashboards.financing_programs_constants import (
    FINANCING_PROGRAMS,
    FINANCING_PROGRAM_EXTRA,
    REEMBOLSAVEL_PROGRAM_LABELS,
    STAGE_PREFIX,
    FinancingStage,
)


def program_quantity(
    df: DataFrame, stage: FinancingStage, program_label: str, suffix: str
) -> float:
    prefix = STAGE_PREFIX[stage]
    suffixes = [suffix, *FINANCING_PROGRAM_EXTRA.get(program_label, [])]
    total = 0.0
    for program_suffix in suffixes:
        col = f"{prefix}_{program_suffix}"
        if col in df.columns:
            total += float(df[col].fillna(0).sum())
    return total


def get_program_totals_table(
    df: DataFrame, stage: FinancingStage, *, drop_zero: bool = True
) -> pd.DataFrame:
    rows = []
    for label, suffix in FINANCING_PROGRAMS:
        qty = program_quantity(df, stage, label, suffix)
        rows.append([label, qty])
    table = pd.DataFrame(rows, columns=["Programa", "Quantidade"])
    if drop_zero:
        return table[table["Quantidade"] > 0]
    return table


def get_reembolsavel_totals_table(df: DataFrame, stage: FinancingStage) -> pd.DataFrame:
    """Agrupa os mesmos programas do gráfico de participação em reembolsável x não reembolsável."""
    reembolsavel = 0.0
    nao_reembolsavel = 0.0
    for label, suffix in FINANCING_PROGRAMS:
        qty = program_quantity(df, stage, label, suffix)
        if label in REEMBOLSAVEL_PROGRAM_LABELS:
            reembolsavel += qty
        else:
            nao_reembolsavel += qty
    return pd.DataFrame(
        [
            ["Reembolsável", reembolsavel],
            ["Não Reembolsável", nao_reembolsavel],
        ],
        columns=["Tipo", "Quantidade"],
    )


def get_official_reembolsavel_totals(df: DataFrame, stage: FinancingStage) -> tuple[float, float]:
    """Totais agregados publicados pelo INEP (colunas FINANC_REEMB / FINANC_NREEMB)."""
    prefix = STAGE_PREFIX[stage]
    reemb_col = f"{prefix}_FINANC_REEMB"
    nreemb_col = f"{prefix}_FINANC_NREEMB"
    reembolsavel = float(df[reemb_col].fillna(0).sum()) if reemb_col in df.columns else 0.0
    nao_reembolsavel = (
        float(df[nreemb_col].fillna(0).sum()) if nreemb_col in df.columns else 0.0
    )
    return reembolsavel, nao_reembolsavel


def get_reembolsavel_discrepancy(df: DataFrame, stage: FinancingStage) -> dict[str, float]:
    """Compara a soma por programas com os totais oficiais do INEP."""
    from_programs = get_reembolsavel_totals_table(df, stage)
    reembolsavel_programs = float(from_programs.loc[0, "Quantidade"])
    nao_reembolsavel_programs = float(from_programs.loc[1, "Quantidade"])
    reembolsavel_official, nao_reembolsavel_official = get_official_reembolsavel_totals(
        df, stage
    )
    return {
        "reembolsavel_programs": reembolsavel_programs,
        "nao_reembolsavel_programs": nao_reembolsavel_programs,
        "reembolsavel_official": reembolsavel_official,
        "nao_reembolsavel_official": nao_reembolsavel_official,
        "delta_reembolsavel": reembolsavel_official - reembolsavel_programs,
        "delta_nao_reembolsavel": nao_reembolsavel_official - nao_reembolsavel_programs,
    }
