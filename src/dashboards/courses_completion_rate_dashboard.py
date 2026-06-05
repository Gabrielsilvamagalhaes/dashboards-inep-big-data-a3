from typing import Literal

import plotly.graph_objects as go
from pandas import DataFrame
from plotly.graph_objs import Figure

from dashboards.courses_analytics_constants import (
    MIN_ENROLLMENT_FOR_RATE,
    prepare_courses_summary,
)

CompletionRanking = Literal["highest", "lowest"]

MAX_LABEL_LEN = 30
_BAR_COLORS = {
    "highest": "#27ae60",
    "lowest": "#c0392b",
}


def _eligible_summary(df: DataFrame, min_enrollment: int) -> DataFrame:
    summary = prepare_courses_summary(df)
    return summary[summary["Matriculados"] >= min_enrollment]


def _format_course_label(name: str) -> str:
    name = str(name).strip()
    if len(name) <= MAX_LABEL_LEN:
        return name
    return f"{name[: MAX_LABEL_LEN - 1]}…"


def getCoursesCompletionRateChart(
    df: DataFrame,
    top_n: int = 10,
    min_enrollment: int = MIN_ENROLLMENT_FOR_RATE,
    ranking: CompletionRanking = "highest",
) -> Figure:
    """Top ou bottom cursos por taxa de conclusão (concluintes / matriculados)."""
    eligible = _eligible_summary(df, min_enrollment)
    ascending = ranking == "lowest"
    top = (
        eligible.nlargest(top_n, "Taxa de Conclusão (%)")
        if not ascending
        else eligible.nsmallest(top_n, "Taxa de Conclusão (%)")
    ).sort_values("Taxa de Conclusão (%)", ascending=ascending)

    labels = top["NO_CINE_ROTULO"].map(_format_course_label)
    rates = top["Taxa de Conclusão (%)"]
    bar_color = _BAR_COLORS[ranking]

    fig = go.Figure(
        go.Bar(
            y=labels,
            x=rates,
            orientation="h",
            marker={"color": bar_color, "line": {"width": 0}},
            text=[f"{v:.1f}%" for v in rates],
            textposition="outside",
            textfont={"size": 11, "color": "#FFFFFF"},
            cliponaxis=False,
            customdata=top[["NO_CINE_ROTULO", "Matriculados", "Concluintes"]].values,
            hovertemplate=(
                "<b>%{customdata[0]}</b><br>"
                "Taxa de conclusão: %{x:.1f}%<br>"
                "Matriculados: %{customdata[1]:,.0f}<br>"
                "Concluintes: %{customdata[2]:,.0f}"
                "<extra></extra>"
            ),
        )
    )

    title_suffix = "Maior" if not ascending else "Menor"
    x_max = max(rates.max() * 1.18, rates.max() + 2)

    fig.update_layout(
        title={
            "text": (
                f"Top {len(top)} — {title_suffix} Taxa de Conclusão<br>"
                f"<sup>Mín. {min_enrollment:,} matriculados · Censo ES 2024</sup>"
            ),
            "x": 0.5,
            "xanchor": "center",
            "font": {"size": 15},
        },
        template="plotly_white",
        height=max(380, len(top) * 36 + 120),
        margin={"l": 8, "r": 48, "t": 72, "b": 40},
        bargap=0.28,
        separators=",.",
        showlegend=False,
        xaxis={
            "title": "Taxa de Conclusão (%)",
            "range": [0, x_max],
            "gridcolor": "#e8e8e8",
            "zeroline": False,
            "ticksuffix": "%",
        },
        yaxis={
            "title": "",
            "categoryorder": "array",
            "categoryarray": list(labels),
            "tickfont": {"size": 11},
            "automargin": True,
        },
        hoverlabel={"bgcolor": "black", "font_size": 12},
    )

    return fig
