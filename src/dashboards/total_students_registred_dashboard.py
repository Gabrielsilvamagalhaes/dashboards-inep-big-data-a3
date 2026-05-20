from pandas import DataFrame
import plotly.express as px
from plotly.graph_objs import Figure


def getTotalStudentsRegistredChart(df: DataFrame, years: int) -> Figure:
    """Função que retorna gráfico de inscritos totais"""

    # Seleciona apenas as colunas relevantes para o gráfico: ano do censo e total de inscritos por modalidade (diurno, noturno, e EAD)
    df_education = df[
        [
            "NU_ANO_CENSO",
            "QT_INSCRITO_TOTAL_DIURNO",
            "QT_INSCRITO_TOTAL_NOTURNO",
            "QT_INSCRITO_TOTAL_EAD",
        ]
    ]

    # Calcula o total geral de inscritos somando a coluna 'QT_INSCRITO_TOTAL' do DataFrame original
    total_students_registred = df["QT_INSCRITO_TOTAL"].sum()

    # Agrupa os dados por ano do censo, somando o total de inscritos por modalidade para cada ano
    stack_df = df_education.groupby("NU_ANO_CENSO", as_index=False)[
        ["QT_INSCRITO_TOTAL_DIURNO", "QT_INSCRITO_TOTAL_NOTURNO", "QT_INSCRITO_TOTAL_EAD"]
    ].sum()

    # Garante que o ano do censo esteja no formato inteiro
    stack_df["NU_ANO_CENSO"] = stack_df["NU_ANO_CENSO"].astype(int)

    # Renomeia as colunas para nomes mais amigáveis e claros para o gráfico
    stack_df = stack_df.rename(
        columns={
            "QT_INSCRITO_TOTAL_DIURNO": "Diurno",
            "QT_INSCRITO_TOTAL_NOTURNO": "Noturno",
            "QT_INSCRITO_TOTAL_EAD": "EAD",
            "NU_ANO_CENSO": "Ano do Censo",
        }
    )

    # Transforma o DataFrame de formato largo para longo, facilitando a visualização empilhada das modalidades
    stack_long = stack_df.melt(id_vars="Ano do Censo", var_name="Turno", value_name="Quantidade")

    # Converte os anos para string para garantir a correta ordenação no eixo X do gráfico
    stack_long["Ano do Censo"] = stack_long["Ano do Censo"].astype(str)
    year_labels = [str(year) for year in years]

    # Cria o gráfico de barras empilhadas usando Plotly Express, detalhando inscritos por modalidade e ano
    fig = px.bar(
        stack_long,
        x="Ano do Censo",
        y="Quantidade",
        color="Turno",
        title="Inscritos totais por modalidade e ano",
        text="Quantidade",
        category_orders={"Ano do Censo": year_labels},
        color_discrete_map={
            "Diurno": "#1f77b4",
            "Noturno": "#ff7f0e",
            "EAD": "#2ca02c",
        },
        text_auto=",.0f",  # pyright: ignore[reportArgumentType]
    )

    # Atualiza o layout do gráfico para usar barras empilhadas e configura títulos dos eixos e legenda
    fig.update_layout(
        barmode="stack",
        yaxis_title="Quantidade de inscritos",
        xaxis_title="Ano do censo",
        legend_title="Modalidade",
    )

    # Adiciona uma anotação no gráfico mostrando o total geral de inscritos
    fig.add_annotation(
        x="Inscritos",
        y=total_students_registred,
        text=f"Total: {total_students_registred}",
        showarrow=False,
        yshift=10,
    )

    # Define a largura das barras no gráfico
    fig.update_traces(width=0.3)

    # Retorna o objeto Figure criado
    return fig
