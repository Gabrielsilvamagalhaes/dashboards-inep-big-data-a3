"""Colunas e rótulos dos programas de financiamento (Censo ES 2024)."""

from typing import Literal

FinancingStage = Literal["ingressantes", "matriculados", "concluintes"]

STAGE_PREFIX: dict[FinancingStage, str] = {
    "ingressantes": "QT_ING",
    "matriculados": "QT_MAT",
    "concluintes": "QT_CONC",
}

STAGE_LABEL: dict[FinancingStage, str] = {
    "ingressantes": "Calouros",
    "matriculados": "Veteranos",
    "concluintes": "Formandos",
}

# (rótulo exibição, sufixo da coluna sem prefixo QT_ING/MAT/CONC)
FINANCING_PROGRAMS: list[tuple[str, str]] = [
    ("FIES", "FIES"),
    ("PROUNI Integral", "PROUNII"),
    ("PROUNI Parcial", "PROUNIP"),
    ("Outros Reembolsáveis", "FINANC_REEMB_OUTROS"),
    ("Outros Não Reembolsáveis", "FINANC_NREEMB_OUTROS"),
]

# Complementos agregados em "Outros"
FINANCING_PROGRAM_EXTRA: dict[str, list[str]] = {
    "Outros Reembolsáveis": ["RPFIES"],
    "Outros Não Reembolsáveis": ["NRPFIES"],
}

# Agrupamento usado no gráfico reembolsável x não reembolsável (coerente com share_pie)
REEMBOLSAVEL_PROGRAM_LABELS = frozenset({"FIES", "Outros Reembolsáveis"})

PROGRAM_COLORS: dict[str, str] = {
    "FIES": "#2C5E8A",
    "PROUNI Integral": "#88398A",
    "PROUNI Parcial": "#B07AB8",
    "Outros Reembolsáveis": "#ff7f0e",
    "Outros Não Reembolsáveis": "#2ca02c",
    "Reembolsável": "#2C5E8A",
    "Não Reembolsável": "#88398A",
}
