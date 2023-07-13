#------------------------------------------------------------------------------------
# Bibliotecas Necessarias
#------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config (page_title='Cities', page_icon='🏙️', layout='wide')
#------------------------------------------------------------------------------------
# Importando Planilha
#------------------------------------------------------------------------------------
df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------
# Essa função tem a finalidade de selecionar e reproduzir em forma de gráfico de barras as 5 cidades com maior valor médio de prato para dois.
def prato_para_dois(df):    
    df_aux = df.loc[:, ['average_cost_for_two','city','country_code']].groupby(['city','country_code'])['average_cost_for_two'].mean().reset_index().sort_values(by='average_cost_for_two', ascending = False).reset_index(drop = True).head(5)
    df_aux.columns = ['Cidades','País','Custo Médio Prato para Dois']
    df_aux['Custo Médio Prato para Dois'] = np.round(df_aux['Custo Médio Prato para Dois'],2)
    fig = px.bar(df_aux, x='Cidades', y='Custo Médio Prato para Dois', color='País', text='Custo Médio Prato para Dois')
    return fig
#------------------------------------------------------------------------------
# Essa função tem a finalidade de selecionar e reproduzir em forma de gráfico de barras as 10 cidades com mais restaurantes com tipos culinários distintos.

def tipos_culinarios(df):
    df_aux = df.loc[:,['cuisines','city','country_code']].groupby(['city','country_code'])['cuisines'].nunique().reset_index().sort_values(by='cuisines', ascending = False).reset_index(drop = True).head(10)
    
    df_aux.columns = ['Cidades','País','Quantidade de Tipos de Culinária Únicos']
        
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de Tipos de Culinária Únicos', color='País', text='Quantidade de Tipos de Culinária Únicos')
    return fig
    
#------------------------------------------------------------------------------
# Essa função tem a finalidade de selecionar e exibir em forma de gráfico de barras as 7 cidades de acordo com a média de avaliação, pode receber dois valores no parâmetro 'valor', podendo ser 'maior_que_4' que filtra as 7 cidades que possuem mais restaurantes com média de avaliação acima de 4 ou 'menor_que_2.5' que filtra as 7 cidades que possuem mais restaurantes com média de avaliação abaixo de 2.5

def avaliacoes_cidade(df, valor):
    if valor == 'maior_que_4':
        df_aux = df.loc[:, ['restaurant_id','aggregate_rating','city','country_code']].groupby(['restaurant_id','city','country_code'])['aggregate_rating'].mean().reset_index()
        df_aux1 = df_aux.loc[df_aux['aggregate_rating'] > 4, ['city','restaurant_id','country_code']].groupby(['city','country_code']).count().reset_index().sort_values(by='restaurant_id', ascending = False).reset_index(drop = True).head(7)
        df_aux1.columns = ['Cidades','País','Quantidade de Restaurantes']
            
        fig = px.bar(df_aux1, x='Cidades', y='Quantidade de Restaurantes', color='País', text='Quantidade de Restaurantes')
        return fig
        
    elif valor == 'menor_que_2.5':
        df_aux = df.loc[:, ['restaurant_id','aggregate_rating','city','country_code']].groupby(['restaurant_id','city','country_code'])['aggregate_rating'].mean().reset_index()
        df_aux1 = df_aux.loc[df_aux['aggregate_rating'] < 2.5, ['city','restaurant_id','country_code']].groupby(['city','country_code']).count().reset_index().sort_values(by='restaurant_id', ascending = False).reset_index(drop = True).head(7)
        df_aux1.columns = ['Cidades','País','Quantidade de Restaurantes']       
        fig = px.bar(df_aux1, x='Cidades', y='Quantidade de Restaurantes', color='País', text='Quantidade de Restaurantes')
        return fig        
#---------------------------------------------------------------------------------
# Essa função tem a finalidade de selecionar e reproduzir em forma de gráfico de barras as cidades com mais restaurantes.
def cidades_mais_restaurantes(df):    
    df_aux = df.loc[:, ['restaurant_id','country_code','city']].groupby(['city','country_code'])['restaurant_id'].nunique().reset_index().sort_values(by='restaurant_id', ascending = False).reset_index(drop = True).head(10)

    
    df_aux.columns = ['Cidades','País','Quantidade de Restaurantes']
    fig = px.bar(df_aux, x='Cidades', y='Quantidade de Restaurantes', color='País', text='Quantidade de Restaurantes')
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
     

#-----------------------------------------------------------------------------------
# Limpeza
#---------------------------------------------------------------------------------
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

    countries_selected = st.sidebar.multiselect('Escolha os paises que deseja visualizar os restaurantes.', (list(df['country_code'].unique())), default = ('Brazil','England','Qatar','South Africa','Canada','Australia'))

linhas_selecionadas = df['country_code'].isin(countries_selected)
df = df.loc[linhas_selecionadas,:]
#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('🏙️ Visão Cidades')

with st.container():
    st.markdown('### Top 10 cidades com mais restaurantes na base de dados')
    fig = cidades_mais_restaurantes(df)
    st.plotly_chart(fig, use_container_width = True)

#----------------------------------------------------------------------------
    
with st.container():
    col1, col2 = st.columns(2)

    with col1:
        st.markdown('### Top 7 cidades com média de avaliação acima de 4')
        fig = avaliacoes_cidade(df, 'maior_que_4')
        st.plotly_chart(fig, use_container_width = True)

#----------------------------------------------------------------------------
    with col2:
        st.markdown('### Top 7 cidades com média de avaliação abaixo de 2.5')
        fig = avaliacoes_cidade(df, 'menor_que_2.5')
        st.plotly_chart(fig, use_container_width = True)          
#---------------------------------------------------------------------------       
with st.container():

    st.markdown('### Top 10 cidades com mais restaurantes com tipos culinários distintos')
    fig = tipos_culinarios(df)
    st.plotly_chart(fig, use_container_width = True)
    
#------------------------------------------------------------------------------
with st.container():
    st.markdown('### Top 5 cidades com maior valor médio de prato para dois')
    fig = prato_para_dois(df)
    st.plotly_chart(fig, use_container_width = True)
    

    
   
        