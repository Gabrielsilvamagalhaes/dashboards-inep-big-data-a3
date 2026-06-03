"""
Helpers de UI reutilizáveis para deixar todas as páginas mais profissionais.

Objetivos:
- aplicar um tema escuro consistente (sem depender do tema do usuário);
- padronizar cabeçalhos (título + subtítulo);
- garantir que os gráficos Plotly usem `plotly_dark` com boa legibilidade.
"""

from __future__ import annotations

from typing import Optional

import streamlit as st
from plotly.graph_objs import Figure


_GLOBAL_DARK_CSS = """
<style>
/* Fundo e texto do app para consistência visual (tema escuro "hard") */
body {
  background-color: #0b0f17;
  color: #e8eaf0;
}

/* Container principal do Streamlit */
div[data-testid="stAppViewContainer"] {
  background-color: #0b0f17;
  color: #e8eaf0;
}

/* Cabeçalhos do Streamlit */
h1, h2, h3, h4, h5 {
  color: #e8eaf0 !important;
}

/* Divisores suaves */
.a3-section-divider {
  border: none;
  height: 1px;
  background: rgba(255, 255, 255, 0.10);
  margin: 1rem 0;
}

/* Cards de insight (texto curto) */
.a3-insight {
  border-radius: 12px;
  padding: 0.9rem 1rem;
  border: 1px solid rgba(255, 255, 255, 0.12);
  background: rgba(255, 255, 255, 0.04);
}
</style>
"""


def apply_dark_theme() -> None:
    """Aplica um CSS global para consistência visual no tema escuro."""

    # Obs: `unsafe_allow_html=True` é necessário para injetar CSS na página.
    st.markdown(_GLOBAL_DARK_CSS, unsafe_allow_html=True)


def render_page_header(title: str, subtitle: Optional[str] = None) -> None:
    """Renderiza um cabeçalho padronizado para a página."""

    st.markdown(
        f"""
        <div style="margin-top: 0.2rem; margin-bottom: 0.5rem;">
          <h2 style="text-align: center; font-size: 30px; margin-bottom: 0.25rem;">
            {title}
          </h2>
          {(
              f"<p style='text-align:center; color: rgba(255,255,255,0.72); margin:0;'>{subtitle}</p>"
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
    Garante que o gráfico Plotly fique legível em fundo escuro.

    Alguns dashboards já setam template; mesmo assim, atualizamos para manter
    consistência entre todos os gráficos.
    """

    # `update_layout` é seguro para Figuras Plotly.
    fig.update_layout(template="plotly_dark")
    # Reforço de cor de fonte para alguns temas que não herdam bem.
    fig.update_layout(font={"color": "#e8eaf0"})
    return fig
