from pathlib import Path
from datetime import date, timedelta

import streamlit as st
import pandas as pd
import plotly.express as px

# Configurações
PERCENTUAL_COMISSAO = 0.08
COLUNAS_ANALISE = ['filial', 'vendedor', 'produto']

# Configurações da página
st.set_page_config(layout="wide", page_title="Dashboard de Vendas", page_icon="📊")

# Estilo CSS personalizado
st.markdown("""
    <style>
    .main {padding: 1rem 2rem;}
    .stMetric {background-color: #f0f2f6; padding: 1rem; border-radius: 10px;}
    </style>
""", unsafe_allow_html=True)

# Leitura dos datasets
pasta_datasets = Path(__file__).parent.parent / 'datasets'
df_vendas = pd.read_csv(pasta_datasets / 'vendas.csv', decimal=',', sep=';', index_col=0, parse_dates=True)
df_filiais = pd.read_csv(pasta_datasets / 'filiais.csv', decimal=',', sep=';', index_col=0)
df_produtos = pd.read_csv(pasta_datasets / 'produtos.csv', decimal=',', sep=';', index_col=0)

# Melhorando os filtros
with st.sidebar:
    st.title("📊 Filtros")
    data_inicio = st.date_input('Data inicial', df_vendas.index.date.min())
    data_final = st.date_input('Data final', df_vendas.index.date.max())
    analise_selecionada = st.selectbox('Analisar por:', COLUNAS_ANALISE)

# Pré-processamento
df_produtos = df_produtos.rename(columns={'nome': 'produto'})
df_vendas = pd.merge(df_vendas.reset_index(), df_produtos[['produto', 'preco']], on='produto').set_index('data')
df_vendas['comissao'] = df_vendas['preco'] * PERCENTUAL_COMISSAO

# Corte dos dados
df_vendas_cortado = df_vendas[(df_vendas.index.date >= data_inicio) & (df_vendas.index.date < data_final + timedelta(days=1))]
valor_vendas = f'R$ {df_vendas_cortado["preco"].sum():,.2f}'
qtd_vendas = df_vendas_cortado['preco'].count()

# Melhorando a apresentação dos números gerais
st.markdown('# 📈 Dashboard de Vendas')
col1, col2, col3 = st.columns([0.5, 0.25, 0.25])
with col1:
    st.subheader('Números Gerais')
    col11, col12 = st.columns(2)
    col11.metric("💰 Valor Total", valor_vendas)
    col12.metric("🛍️ Quantidade", qtd_vendas)

# Melhorando os gráficos
st.divider()
col21, col22 = st.columns(2)

with col21:
    # Análise de vendas por dia
    df_vendas_cortado['dia_venda'] = df_vendas_cortado.index.date
    vendas_dia = df_vendas_cortado.groupby('dia_venda').agg({'preco': 'sum'}).reset_index()
    fig = px.line(vendas_dia, 
                  y='preco', 
                  x='dia_venda', 
                  title='Vendas por dia',
                  labels={'preco': 'Valor (R$)', 'dia_venda': 'Data'},
                  template='plotly_white')
    fig.update_traces(line_color='#2E86C1', line_width=2)
    col21.plotly_chart(fig, use_container_width=True)

with col22:
    # Gráfico de análise selecionada
    df_analise = df_vendas_cortado.groupby(analise_selecionada)['preco'].sum().reset_index()
    fig2 = px.bar(df_analise, 
                  x=analise_selecionada, 
                  y='preco',
                  title=f'Vendas por {analise_selecionada.title()}',
                  labels={'preco': 'Valor (R$)', analise_selecionada: analise_selecionada.title()},
                  template='plotly_white')
    fig2.update_traces(marker_color='#2E86C1')
    st.plotly_chart(fig2, use_container_width=True)


