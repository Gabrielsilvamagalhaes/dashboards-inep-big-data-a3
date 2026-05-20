import streamlit as st
import plotly.express as px
import pandas as pd

from colorama import init
from dashboards.total_students_per_region_dashboard import getTotalStudentsPerRegionChart
from dashboards.total_students_per_state_dashboard import getTotalStudentsPerStateChart
from services.extract_csv_service import extractCsv
from pathlib import Path


init(autoreset=True) # Função para inicializar a lib colorama 
st.set_page_config(layout='wide') # Para ocupar todo o espaço horizontal da pagina

_root_url = Path(__file__).resolve().parent.parent
_csv_path = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"

_csv_path = 'https://drive.google.com/file/d/1DDt40eAzPweMlXh-Z4pg5Lp9Up85U0HL/view?usp=sharing'

df = extractCsv(_csv_path)

df['Region'] = df['NO_REGIAO'].apply(lambda x: x)
region = st.sidebar.selectbox('Região', df['Region'].unique())


df_filtered_per_region = df[df['Region'] == region]
df_filtered_per_region

df_education = df['NO_REGIAO']
regions = sorted(df_education.unique())

# Estilizando label do multiselect
st.markdown(
    "<h4 style='text-align: center; font-size: 28px;' title='Filtrar por Regiões'>Filtrar por Regiões</h4>",
    unsafe_allow_html=True,
)
select_regions = st.multiselect('Filtrar por regiões', regions, default=regions, label_visibility='hidden')
col1, col2 = st.columns(2)

total_students_per_region_graphic = getTotalStudentsPerRegionChart(df_education, select_regions)
col1.plotly_chart(total_students_per_region_graphic, width='stretch', on_select='rerun')


df_education = df[['NO_REGIAO','NO_UF']]
total_students_per_state_graphic = getTotalStudentsPerStateChart(df_education, select_regions) 
col2.plotly_chart(total_students_per_state_graphic)


col3, col4, col5 = st.columns(3)

df_education = df[['NU_ANO_CENSO', 'QT_INSCRITO_TOTAL_DIURNO', 'QT_INSCRITO_TOTAL_NOTURNO', 'QT_INSCRITO_TOTAL_EAD']]
years = sorted(df_education['NU_ANO_CENSO'].dropna().astype(int).unique().tolist())

total_students_registred = df['QT_INSCRITO_TOTAL'].sum()

stack_df = (
    df_education
    .groupby('NU_ANO_CENSO', as_index=False)[['QT_INSCRITO_TOTAL_DIURNO', 'QT_INSCRITO_TOTAL_NOTURNO', 'QT_INSCRITO_TOTAL_EAD']]
    .sum()
)
stack_df['NU_ANO_CENSO'] = stack_df['NU_ANO_CENSO'].astype(int)
stack_df = stack_df.rename(
    columns={
        'QT_INSCRITO_TOTAL_DIURNO': 'Diurno',
        'QT_INSCRITO_TOTAL_NOTURNO': 'Noturno',
        'QT_INSCRITO_TOTAL_EAD': 'EAD',
        'NU_ANO_CENSO': 'Ano do Censo'
    }
)

stack_long = stack_df.melt(
    id_vars='Ano do Censo',
    var_name='Turno',
    value_name='Quantidade'
)
stack_long['Ano do Censo'] = stack_long['Ano do Censo'].astype(str)
year_labels = [str(year) for year in years]

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
    text_auto=',.0f'
)

fig.update_layout(
    barmode="stack",
    yaxis_title="Quantidade de inscritos",
    xaxis_title="Ano do censo",
    legend_title="Modalidade",
)

fig.add_annotation(x='Inscritos', y=total_students_registred,
            text=f"Total: {total_students_registred}",
            showarrow=False,
            yshift=10)

fig.update_traces(width=0.3)

col3.plotly_chart(fig)
