"""Tokens de cor para tema claro e escuro, detectados via preferência do Streamlit."""

from __future__ import annotations

from dataclasses import dataclass
from typing import Literal

import streamlit as st

ThemeMode = Literal["light", "dark"]


@dataclass(frozen=True)
class ThemeColors:
    bg: str
    text: str
    text_muted: str
    divider: str
    card_border: str
    card_bg: str
    plotly_template: str
    plotly_font: str
    hover_bg: str
    hover_font: str
    bar_label: str


_DARK = ThemeColors(
    bg="#0b0f17",
    text="#e8eaf0",
    text_muted="rgba(255,255,255,0.72)",
    divider="rgba(255, 255, 255, 0.10)",
    card_border="rgba(255, 255, 255, 0.12)",
    card_bg="rgba(255, 255, 255, 0.04)",
    plotly_template="plotly_dark",
    plotly_font="#e8eaf0",
    hover_bg="#1a1a1a",
    hover_font="#e8eaf0",
    bar_label="#FFFFFF",
)

_LIGHT = ThemeColors(
    bg="#ffffff",
    text="#262730",
    text_muted="rgba(38,39,48,0.72)",
    divider="rgba(0, 0, 0, 0.10)",
    card_border="rgba(0, 0, 0, 0.12)",
    card_bg="rgba(0, 0, 0, 0.03)",
    plotly_template="plotly_white",
    plotly_font="#262730",
    hover_bg="#ffffff",
    hover_font="#262730",
    bar_label="#FFFFFF",
)

_THEMES: dict[ThemeMode, ThemeColors] = {
    "dark": _DARK,
    "light": _LIGHT,
}


def get_theme_mode() -> ThemeMode:
    theme_type = getattr(getattr(st.context, "theme", None), "type", None)
    return "dark" if theme_type == "dark" else "light"


def get_theme_colors() -> ThemeColors:
    return _THEMES[get_theme_mode()]


def plotly_hoverlabel(font_size: int | None = None) -> dict:
    colors = get_theme_colors()
    hover: dict = {
        "bgcolor": colors.hover_bg,
        "font_color": colors.hover_font,
    }
    if font_size is not None:
        hover["font_size"] = font_size
    return hover
