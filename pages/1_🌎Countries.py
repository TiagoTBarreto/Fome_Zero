#------------------------------------------------------------------------------------
# Bibliotecas Necessarias
#------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config (page_title='Countries', page_icon='🌎', layout='wide')
#------------------------------------------------------------------------------------
# Importando Planilha
#------------------------------------------------------------------------------------
df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------

#Essa função tem o objetivo de calcular uma variável por país, variando de acordo com o valor recebido no parâmetro 'info', podendo ser:
# 1.'restaurant' - Quantidade de Restaurantes por País
# 2.'city' - Quantidade de Cidades por país
# 3.'gourmet' - Quantidade de Restaurantes gourmet por país
# 4.'votes' - Quantidade Média de Avaliações por país
# 5.'cost_for_two' - Preço de comida para dois por país
#

def quantidade_por_pais(df, info):
    if info == 'restaurant':
        df_aux = df.groupby('country_code')['restaurant_name'].nunique().reset_index().sort_values(by='restaurant_name', ascending = False).reset_index(drop = True)
        df_aux.columns = ['Países', 'Quantidade de Restaurantes']
        fig = px.bar (df_aux, x='Países', y='Quantidade de Restaurantes', text='Quantidade de Restaurantes', color='Países')
        return fig
        
    elif info == 'city':
        df_aux = df.groupby('country_code')['city'].nunique().reset_index().sort_values(by='city', ascending=False).reset_index(drop = True)
        df_aux.columns = ['Países', 'Quantidade de Cidades']
        fig = px.bar(df_aux, x='Países',y='Quantidade de Cidades', text= 'Quantidade de Cidades', color='Países')
        return fig

    elif info == 'gourmet':
        df_aux = df.loc[df['price_range'] == 'gourmet', ['restaurant_name','price_range', 'country_code']].groupby(['country_code','price_range'])['restaurant_name'].nunique().reset_index().sort_values(by='restaurant_name', ascending = False).reset_index(drop = True)
        df_aux.columns = ['Países','Classificação da Comida','Quantidade de Restaurantes']
    
        fig = px.bar(df_aux, x='Países', y='Quantidade de Restaurantes', color='Países', text='Quantidade de Restaurantes')
        return fig
    
    elif info == 'votes':
        df_aux = df.loc[:, ['country_code','votes']].groupby('country_code')['votes'].mean().reset_index().sort_values(by='votes', ascending = False).reset_index(drop = True)
        df_aux.columns = ['Países', 'Quantidade de Avaliações']
        df_aux['Quantidade de Avaliações'] = np.round(df_aux['Quantidade de Avaliações'], 2)
        fig = px.bar(df_aux, x='Países',y='Quantidade de Avaliações', text='Quantidade de Avaliações', color='Países')
        return fig

    elif info == 'cost_for_two':
        df_aux = df.loc[:, ['average_cost_for_two','country_code']].groupby('country_code')['average_cost_for_two'].mean().reset_index().sort_values(by='average_cost_for_two', ascending = False).reset_index(drop = True)
        df_aux.columns = ['Países', 'Preço Médio para Dois']
        df_aux['Preço Médio para Dois'] = np.round(df_aux['Preço Médio para Dois'], 2)
        fig = px.bar(df_aux, x='Países', y='Preço Médio para Dois', text='Preço Médio para Dois', color='Países')
        return fig

    
#----------------------------------------------------------------------------
# Essa função tem como objetivo renomear o nome das colunas
def rename_columns(dataframe):
    df = dataframe.copy()
    title = lambda x: inflection.titleize(x)
    snakecase = lambda x: inflection.underscore(x)
    spaces = lambda x: x.replace(" ", "")
    cols_old = list(df.columns)
    cols_old = list(map(title, cols_old))
    cols_old = list(map(spaces, cols_old))
    cols_new = list(map(snakecase, cols_old))
    df.columns = cols_new
    return df


#----------------------------------------------------------------------------------------------------------------------------------------------------
# Essa função tem como objetivo substituir o código na coluna de país pelo nome do país respectivo a cada código.
COUNTRIES = {
    1: "India",
    14: "Australia",
    30: "Brazil",
    37: "Canada",
    94: "Indonesia",
    148: "New Zeland",
    162: "Philippines",
    166: "Qatar",
    184: "Singapure",
    189: "South Africa",
    191: "Sri Lanka",
    208: "Turkey",
    214: "United Arab Emirates",
    215: "England",
    216: "United States of America"
    }

def country_name(country_id):
    return COUNTRIES[country_id]
     
#----------------------------------------------------------------------------------------------------------------------------------------------------
#Essa função tem como objetivo substituir o número na coluna pela classificação dos preços em cheap, normal, expensive ou gourmet
def create_price_type(price_range):
    if price_range == 1:
        return "cheap"
    elif price_range == 2:
        return "normal"
    elif price_range == 3:
        return "expensive"
    else:
        return "gourmet"
      

    
#----------------------------------------------------------------------------------------------------------------------------------------------------
# Essa função tem como objetivo substituir o código na coluna de cores pelo nome da cor respectiva a cada código.
COLORS = {
"3F7E00": "darkgreen",
"5BA829": "green",
"9ACD32": "lightgreen",
"CDD614": "orange",
"FFBA00": "red",
"CBCBC8": "darkred",
"FF7800": "darkred"
}
def color_name(color_code):
    return COLORS[color_code]
    
#------------------------------------------------------------------------------------
# Limpeza
#------------------------------------------------------------------------------------
df = rename_columns(df)

df['country_code'] = df.loc[:, 'country_code'].apply(lambda x: country_name(x))

df['price_range'] = df.loc[:, 'price_range'].apply(lambda x: create_price_type(x))

df['rating_color'] = df.loc[:, 'rating_color'].apply(lambda x: color_name(x))   

df = df.loc[~df['cuisines'].apply(lambda x: isinstance(x, float)), :]
df["cuisines"] = df.loc[:, "cuisines"].apply(lambda x: x.split(",")[0])

linhas_vazias = df['cuisines'] != 'Drinks Only'
df = df.loc [linhas_vazias, :]
linhas_vazias = df['cuisines'] != 'Mineira'
df = df.loc [linhas_vazias, :]

#----------------------------------------------------------------------------------
# Sidebar
#---------------------------------------------------------------------------------
with st.sidebar:

    st.markdown('# Filtros')
    
#Filtro de países na barra lateral
    countries_selected = st.sidebar.multiselect('Escolha os paises que deseja visualizar os restaurantes.', (list(df['country_code'].unique())), default = ('Brazil','England','Qatar','South Africa','Canada','Australia'))


linhas_selecionadas = df['country_code'].isin(countries_selected)
df = df.loc[linhas_selecionadas,:]
#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('🌎 Visão Países')

with st.container():
    st.subheader('Restaurantes por País')
    fig = quantidade_por_pais(df, 'restaurant')
    st.plotly_chart(fig, use_container_width = True)
    
with st.container():
    st.subheader('Cidades por País')
    fig = quantidade_por_pais(df, 'city')
    st.plotly_chart(fig, use_container_width = True)  

with st.container():
    st.subheader('Quantidade de Restaurantes Gourmet por País')
    fig = quantidade_por_pais(df, 'gourmet')
    st.plotly_chart(fig, use_container_width = True)
    
   
    
with st.container():
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader('Média de Avaliações Feitas por País')
        fig = quantidade_por_pais(df, 'votes')
        st.plotly_chart(fig, use_container_width = True) 
    
    with col2:
        st.subheader('Média de Preço de um prato para duas pessoas por País')
        fig = quantidade_por_pais(df, 'cost_for_two')
        st.plotly_chart(fig, use_container_width = True)   
