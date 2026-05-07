from pandas import DataFrame
from plotly.graph_objs import Figure
import plotly.express as px


def getTotalStudentsPerStateChart(df_education: DataFrame, select_regions: list) -> Figure:
  """ Função que retorna o grafico da distribuição do total de alunos por estado"""

  total_state = df_education.value_counts().reset_index()
  total_state.columns = ['Região', 'Estado','Total']

  total_state_filtered = total_state[total_state['Região'].isin(select_regions)]
  total_students_per_state_graphic = px.bar(total_state_filtered,
                 x='Estado',
                 y='Total',
                 title='Distribuição de Alunos por Estado (Censo 2024)',
                 labels={'Total': 'Quantidade de Pessoas', 'Estado': 'Estado'},
                 color='Total',
                 color_continuous_scale='Tempo',
                 text_auto=',.0f')

  return total_students_per_state_graphic
