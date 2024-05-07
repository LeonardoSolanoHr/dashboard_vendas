import pandas as pd
import streamlit as st
import requests
import plotly.express as px
import time

@st.cache_data #converter para download
def converte_csv(df):
    return df.to_csv(index = False).encode('utf-8')

def mensagem_sucesso():
    sucesso = st.success('Arquivo baixado com sucesso!',icon="✅")
    time.sleep(5)
    sucesso.empty()

st.title('Dados Brutos') # titulo do dash

url = 'https://labdados.com/produtos' # leitura da api

response = requests.get(url) # recebendo e buscandos os dados da url
dados= pd.DataFrame.from_dict(response.json()) # recebendo o json
dados['Data da Compra'] = pd.to_datetime(dados['Data da Compra'],format='%d/%m/%Y')

with st.expander('Colunas'):
    colunas = st.multiselect('Selecione as colunas',list(dados.columns), list(dados.columns))

st.sidebar.title('Filtros')
with st.sidebar.expander('Nome do produto'):
    produtos = st.multiselect('Selecione os produtos',dados['Produto'].unique(),dados['Produto'].unique())
with st.sidebar.expander('Preço do produto'):
    preco = st.slider('Selecione o preço',0,5000,(0,5000))
with st.sidebar.expander('Data da compra'):
    data_compra = st.date_input('Selecione a data',(dados['Data da Compra'].min(),dados['Data da Compra'].max()))


## Colunas ## 
with st.sidebar.expander('Categoria do Produto'):
    categoria = st.multiselect('Selecione as categorias',dados['Categoria do Produto'].unique(),dados['Categoria do Produto'].unique())
with st.sidebar.expander('Frete'):
    frete = st.slider('Selecione o valor do frete',0, 250,(0,250))
with st.sidebar.expander('Vendedor'):
    vendedor = st.multiselect('Selecione o vendedor', dados['Vendedor'].unique(),dados['Vendedor'].unique())
with st.sidebar.expander('Local da Compra'):
    local_compra = st.multiselect('Selecione o local da compra',dados['Local da compra'].unique(),dados['Local da compra'].unique())
with st.sidebar.expander('Avaliacao da compra'):
    avaliacao = st.slider('Seleciona a avaliaçao da compra',1,5,value=(1,5))
with st.sidebar.expander('Tipo de pagamento'):
    tipo_pagamento = st.multiselect('Selecione o tipo de pagamento',dados['Tipo de pagamento'].unique(),dados['Tipo de pagamento'].unique())
with st.sidebar.expander('Qtde de parcelas'):
    parcelas = st.slider('Selecione qtde de parcelas',0,24,(0,24))

query = '''
Produto in @produtos and \
@preco[0] <= Preço <= @preco[1] and \
@data_compra[0] <= `Data da Compra` <= @data_compra[1] and \
`Categoria do Produto` in @categoria and \
@frete[0] <= Frete <= @frete[1] and \
Vendedor in @vendedor and \
`Local da compra`in @local_compra and \
@avaliacao[0]<= `Avaliação da compra` <= @avaliacao[1] and \
`Tipo de pagamento` in @tipo_pagamento and \
@parcelas[0] <= `Quantidade de parcelas` <= @parcelas[1]
'''

dados_filtrados= dados.query(query)
dados_filtrados= dados_filtrados[colunas]

st.dataframe(dados_filtrados)

st.markdown(f'A tabela possui :blue[{dados_filtrados.shape[0]}] linhas e :blue[{dados_filtrados.shape[1]}]')

st.markdown('Escreva um nome para o arquivo')
coluna1,coluna2 = st.columns(2)
with coluna1:
    nome_arquivo = st.text_input('Nome do arquivo:',value='dados')
    nome_arquivo+='.csv'
with coluna2:
    st.download_button('Fazer download da tabela em csv',data = converte_csv(dados_filtrados),file_name = nome_arquivo,mime='text/csv',on_click=mensagem_sucesso)
