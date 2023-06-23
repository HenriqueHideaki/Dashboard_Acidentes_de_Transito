import streamlit as st
import pandas as pd
import plotly.express as px

df = pd.read_csv("datatran2022.csv", encoding="latin1", sep=';')

st.title("Dashboard de Acidentes de Trânsito")

st.sidebar.title("Filtros")
filtro_uf = st.sidebar.selectbox("UF", df['uf'].unique())
df_filtrado = df[df['uf'] == filtro_uf]

municipios_uf = df_filtrado['municipio'].unique()
filtro_municipio = st.sidebar.selectbox("Município", municipios_uf)
df_filtrado = df_filtrado[df_filtrado['municipio'] == filtro_municipio]

tipos_acidente = df_filtrado['tipo_acidente'].unique()

opcoes_fase_dia = ['Todos', 'Plena Noite', 'Pleno dia', 'Amanhecer']

fase_dia_selecionada = st.selectbox('Selecione uma fase do dia', opcoes_fase_dia)

if fase_dia_selecionada != 'Todos':
    df_filtrado = df_filtrado[df_filtrado['fase_dia'] == fase_dia_selecionada]
    st.write('Fase do dia selecionada:', fase_dia_selecionada)
else:
    st.write('Fase do dia não selecionada')

contagem_acidentes = {}

for tipo in tipos_acidente:
    contagem_acidentes[tipo] = df_filtrado[df_filtrado['tipo_acidente'] == tipo].shape[0]


fig_bar = px.bar(x=list(contagem_acidentes.keys()), y=list(contagem_acidentes.values()),
                 labels={'x': 'Tipo de Acidente', 'y': 'Quantidade de Acidentes'},
                 title='Quantidade de Acidentes por Tipo')

fig_bar.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_bar)

fig_histograma = px.histogram(df_filtrado, x='dia_semana',
                              title='Quantidade de Acidentes por Dia da Semana',
                              category_orders={'dia_semana': ['Domingo', 'Segunda-feira', 'Terça-feira',
                                                            'Quarta-feira', 'Quinta-feira', 'Sexta-feira',
                                                            'Sábado']})
fig_histograma.update_layout(xaxis={'categoryorder': 'total descending'})
st.plotly_chart(fig_histograma)

causas_acidentes = df_filtrado['causa_acidente'].value_counts().nlargest(10)

fig_pizza_causas = px.pie(causas_acidentes, names=causas_acidentes.index, values=causas_acidentes.values,
                          title='Top 10 Causas de Acidentes')
st.plotly_chart(fig_pizza_causas)


condicoes_meteorologicas = df_filtrado['condicao_metereologica'].unique()

pivot_table = pd.pivot_table(df_filtrado, values='id', index='condicao_metereologica', columns='dia_semana', aggfunc='count', fill_value=0)

fig_heatmap = px.imshow(pivot_table.values, x=pivot_table.columns, y=pivot_table.index, color_continuous_scale='Viridis')

fig_heatmap.update_layout(
    title='Quantidade de Acidentes por Condição Meteorológica e Dia da Semana',
    xaxis=dict(title='Dia da Semana'),
    yaxis=dict(title='Condição Meteorológica')
)


st.plotly_chart(fig_heatmap)

classificacao_acidentes = df_filtrado['classificacao_acidente'].value_counts()
fig_pizza_classificacao = px.pie(classificacao_acidentes, names=classificacao_acidentes.index,
                                 values=classificacao_acidentes.values, title='Classificação dos Acidentes')
st.plotly_chart(fig_pizza_classificacao)

