from pathlib import Path

import streamlit as st
import pandas as pd

# Caminho para o arquivo Excel
pasta_datasets = Path(__file__).parent / 'datasets'
caminho_vendas = pasta_datasets / 'vendas.xlsx'

df_vendas = pd.read_excel(caminho_vendas, sep=';', decimal=',')

st.dataframe(df_vendas)