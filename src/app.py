import streamlit as st
import plotly.express as px
from colorama import init

from dashboards.total_students_per_region_dashboard import getTotalStudentsPerRegionChart
from dashboards.total_students_per_state_dashboard import getTotalStudentsPerStateChart
from services.extract_csv_service import extractCsv
from pathlib import Path


init(autoreset=True) # Função para inicializar a lib colorama 
st.set_page_config(layout='wide') # Para ocupar todo o espaço horizontal da pagina

_root_url = Path(__file__).resolve().parent.parent
_csv_path = _root_url / "samples" / "MICRODADOS_CADASTRO_CURSOS_2024.csv"


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