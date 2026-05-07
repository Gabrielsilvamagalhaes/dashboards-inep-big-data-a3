from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px


def getTotalStudentsPerRegionChart(df_education: DataFrame, select_regions: list) -> Figure:
   """ Função que retorna o grafico da distribuição do total de alunos por região"""

   total_region = df_education.value_counts().reset_index()
   total_region.columns = ['Região', 'Total']

   total_region_filtered = total_region[total_region['Região'].isin(select_regions)]
   total_students_per_region_graphic = px.pie(total_region_filtered, 
      values='Total',
      names='Região',
      title='Distribuição de Alunos por Região (Censo 2024)')

   return total_students_per_region_graphic
