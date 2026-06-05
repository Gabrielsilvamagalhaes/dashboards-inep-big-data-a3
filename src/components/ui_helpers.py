"""
Helpers de UI reutilizáveis para deixar todas as páginas mais profissionais.

Objetivos:
- aplicar um tema consistente com a preferência do usuário (claro ou escuro);
- padronizar cabeçalhos (título + subtítulo);
- garantir que os gráficos Plotly usem template e cores legíveis no tema ativo.
"""

from __future__ import annotations

from typing import Optional

import streamlit as st
from plotly.graph_objs import Figure

from components.theme_constants import ThemeColors, get_theme_colors


def _build_global_css(colors: ThemeColors) -> str:
    return f"""
<style>
/* Fundo e texto do app para consistência visual */
body {{
  background-color: {colors.bg};
  color: {colors.text};
}}

/* Container principal do Streamlit */
div[data-testid="stAppViewContainer"] {{
  background-color: {colors.bg};
  color: {colors.text};
}}

/* Cabeçalhos do Streamlit */
h1, h2, h3, h4, h5 {{
  color: {colors.text} !important;
}}

/* Divisores suaves */
.a3-section-divider {{
  border: none;
  height: 1px;
  background: {colors.divider};
  margin: 1rem 0;
}}

/* Cards de insight (texto curto) */
.a3-insight {{
  border-radius: 12px;
  padding: 0.9rem 1rem;
  border: 1px solid {colors.card_border};
  background: {colors.card_bg};
}}
</style>
"""


def apply_app_theme() -> None:
    """Aplica CSS global alinhado ao tema ativo (claro ou escuro)."""

    colors = get_theme_colors()
    st.markdown(_build_global_css(colors), unsafe_allow_html=True)


apply_dark_theme = apply_app_theme


def render_page_header(title: str, subtitle: Optional[str] = None) -> None:
    """Renderiza um cabeçalho padronizado para a página."""

    colors = get_theme_colors()
    st.markdown(
        f"""
        <div style="margin-top: 0.2rem; margin-bottom: 0.5rem;">
          <h2 style="text-align: center; font-size: 30px; margin-bottom: 0.25rem;">
            {title}
          </h2>
          {(
              f"<p style='text-align:center; color: {colors.text_muted}; margin:0;'>{subtitle}</p>"
              if subtitle
              else ""
          )}
        </div>
        """,
        unsafe_allow_html=True,
    )


def render_section_divider() -> None:
    """Insere um divisor visual para separar blocos de conteúdo."""

    st.markdown('<hr class="a3-section-divider" />', unsafe_allow_html=True)


def render_insight(text: str) -> None:
    """Mostra um insight textual curto e bem legível."""

    st.markdown(f'<div class="a3-insight">{text}</div>', unsafe_allow_html=True)


def apply_plotly_dark(fig: Figure) -> Figure:
    """
    Garante que o gráfico Plotly fique legível no tema ativo (claro ou escuro).

    Alguns dashboards já setam template; mesmo assim, atualizamos para manter
    consistência entre todos os gráficos.
    """

    colors = get_theme_colors()
    fig.update_layout(template=colors.plotly_template)
    fig.update_layout(font={"color": colors.plotly_font})
    return fig
