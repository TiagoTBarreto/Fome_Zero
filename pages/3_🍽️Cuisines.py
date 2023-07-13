#------------------------------------------------------------------------------------
# Bibliotecas Necessarias
#------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image

st.set_page_config (page_title='Cuisines', page_icon='🍽️', layout='wide')
#------------------------------------------------------------------------------------
# Importando Planilha
#------------------------------------------------------------------------------------
df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------
# Essa função tem o objetivo de filtrar e exibir em forma de gráfico de barra o top dos tipos de culinárias, podendo ser os melhores ou os piores de acordo com o parâmetro passados. Podendo ser:
# 1. coluna
    # 1. 'nota' - Vai fazer o top pela nota média
    # 2. 'preço' - Vai fazer o top pelo preço médio de um prato para dois
# 2. ordenacao
    # 1. False - Vai selecionar os melhores
    # 2. True - Vai selecionar os piores

def top_tipos_culinarias(df1, coluna, ordenacao):
    if coluna == 'nota':
        df_aux = df1.loc[:,['aggregate_rating','cuisines_better_worst']].groupby('cuisines_better_worst')['aggregate_rating'].mean().reset_index().sort_values(by='aggregate_rating', ascending = ordenacao).reset_index(drop = True).head(quantidade_culinarias)
        df_aux['aggregate_rating'] = np.round(df_aux['aggregate_rating'], 2)
        df_aux.columns = ['Tipo de Culinária','Média de Avaliação']
        fig = px.bar(df_aux, x='Tipo de Culinária',y= 'Média de Avaliação', text='Média de Avaliação', color='Tipo de Culinária')
        return fig

    elif coluna == 'preço':
        df_aux = df1.loc[:,['average_cost_for_two','cuisines_better_worst']].groupby('cuisines_better_worst')['average_cost_for_two'].mean().reset_index().sort_values(by='average_cost_for_two', ascending = ordenacao).reset_index(drop = True).head(quantidade_culinarias)
        df_aux['average_cost_for_two'] = np.round(df_aux['average_cost_for_two'], 2)
        df_aux.columns = ['Tipo de Culinária','Preço Médio para Dois']
        fig = px.bar(df_aux, x='Tipo de Culinária',y= 'Preço Médio para Dois', text='Preço Médio para Dois', color='Tipo de Culinária')
        return fig

#----------------------------------------------------------------------
# Essa função tem o objetivo de filtrar e exibir em forma de tabela os melhores restaurantes de acordo com sua nota de avaliação, exibindo métricas de localização, culinário, custo e avaliações. 
def top_restaurantes(df):
    df_aux = df.loc[:, ['restaurant_id','aggregate_rating','restaurant_name','country_code','city','cuisines','average_cost_for_two','votes']].groupby(['restaurant_id','restaurant_name','country_code','city','cuisines','average_cost_for_two','votes'])['aggregate_rating'].mean().reset_index().sort_values(by=['aggregate_rating','restaurant_id'], ascending = [False, True]).reset_index(drop = True).head(quantidade_restaurantes)   
    df_aux = df_aux.reindex(columns=['restaurant_id','restaurant_name','country_code','city','cuisines','average_cost_for_two','aggregate_rating','votes'])
    return df_aux
#----------------------------------------------------------------------
# Essa função tem o objetivo de filtrar e exibir em forma de métrica o melhor restaurante por tipo de culinária junto com métricas de localização e preço para dois. Recebe dois parâmetros:
# 1. df1 - dataframe desejado
# 2. cuisines - O tipo de culinária desejado
def best_restaurant_for_cuisines(df1, cuisines): 
    df_aux = df1.loc[df1['cuisines_better_worst'] == cuisines, ['restaurant_id','aggregate_rating','restaurant_name','country','city','cuisines_better_worst','average_cost_for_two','votes','currency']].groupby(['restaurant_id','restaurant_name','country','city','cuisines_better_worst','average_cost_for_two','votes','currency'])['aggregate_rating'].mean().reset_index().sort_values(by=['aggregate_rating','restaurant_id'], ascending=[False, True]).reset_index(drop=True)
    metrics_better = st.metric( 
    label=f"{df_aux.loc[0, 'cuisines_better_worst']}: {df_aux.loc[0, 'restaurant_name']}",
    help=f"País: {df_aux.loc[0, 'country']}\n\nCidade: {df_aux.loc[0, 'city']}\n\nMédia Prato para Dois: {df_aux.loc[0, 'average_cost_for_two']} ({df_aux.loc[0, 'currency']})",
    value=f"{df_aux.loc[0, 'aggregate_rating']} / 5.0"
    )
    return metrics_better

#-------------------------------------------------------------------------
# Essa função tem o objetivo de filtrar e exibir em forma de métrica o pior restaurante por tipo de culinária junto com métricas de localização e preço para dois. Recebe dois parâmetros:
# 1. df1 - dataframe desejado
# 2. cuisines - O tipo de culinária desejado
def worst_restaurant_for_cuisines(df1, cuisines):
    df_aux = df1.loc[(df1['cuisines_better_worst'] == cuisines) & (df1['aggregate_rating'] != 0), ['restaurant_id','aggregate_rating','restaurant_name','country','city','cuisines_better_worst','average_cost_for_two','votes','currency']].groupby(['restaurant_id','restaurant_name','country','city','cuisines_better_worst','average_cost_for_two','votes','currency'])['aggregate_rating'].mean().reset_index().sort_values(by=['aggregate_rating','restaurant_id'], ascending=[True, True]).reset_index(drop=True)
    metrics_worst = st.metric( 
    label=f"{df_aux.loc[0, 'cuisines_better_worst']}: {df_aux.loc[0, 'restaurant_name']}",
    help=f"País: {df_aux.loc[0, 'country']}\n\nCidade: {df_aux.loc[0, 'city']}\n\nMédia Prato para Dois: {df_aux.loc[0, 'average_cost_for_two']} ({df_aux.loc[0, 'currency']})",
    value=f"{df_aux.loc[0, 'aggregate_rating']} / 5.0"
    )
    return metrics_worst
#-------------------------
#----------------------------------------------
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
#-----------------------------------------------------------------------------------
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

#copia colunas
df1 = df.copy()
df1['aggregate_rating'] = df['aggregate_rating']
df1['cuisines_better_worst'] = df['cuisines']
df1['country'] = df['country_code']
#----------------------------------------------------------------------------------
# Sidebar
#---------------------------------------------------------------------------------
with st.sidebar:


    st.markdown('# Filtros')

    countries_selected = st.sidebar.multiselect('Escolha os paises que deseja visualizar os restaurantes', (list(df['country_code'].unique())), default = ('Brazil','England','Qatar','South Africa','Canada','Australia'))
    
    quantidade_restaurantes = st.slider('Selecione a quantidade de Restaurantes que deseja visualizar', min_value = 0, max_value = 20, value = 10)

    quantidade_culinarias = st.slider('Selecione a quantidade de Tipos Culinários que deseja visualizar', min_value = 0, max_value = 10, value = 10)
    
    cuisines_selected = st.sidebar.multiselect('Escolha os Tipos de Culinária', (list(df['cuisines'].unique())), default = ('Home-made','BBQ','Japanese','Brazilian','Arabian','American','Italian'))



#filtro países
linhas_selecionadas = df['country_code'].isin(countries_selected)
df = df.loc[linhas_selecionadas,:]


#2 casas decimais aggregate_rating
df['aggregate_rating'] = np.round(df['aggregate_rating'], 2)
df1['aggregate_rating'] = np.round(df1['aggregate_rating'], 2)

#filtro culinárias
linhas_selecionadas = df['cuisines'].isin(cuisines_selected)
df = df.loc[linhas_selecionadas,:] 

#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('🍽️ Visão Tipos de Cozinha')
st.header('Melhores e Piores Restaurantes dos Principais tipos Culinários')

with st.container():
    col1, col2, col3, col4, col5 = st.columns(5)
    
    with col1:
        metrics_better = best_restaurant_for_cuisines(df1, 'Italian') 
        metrics_worst = worst_restaurant_for_cuisines(df1, 'Italian')
#--------------------------------------------------------------------------
    with col2:
        metrics_better = best_restaurant_for_cuisines(df1, 'American') 
        metrics_worst = worst_restaurant_for_cuisines(df1, 'American') 
#--------------------------------------------------------------------------       
    with col3:
        metrics_better = best_restaurant_for_cuisines(df1, 'Spanish') 
        metrics_worst = worst_restaurant_for_cuisines(df1, 'Spanish') 
#-----------------------------------------------------------------------
    with col4:
        metrics_better = best_restaurant_for_cuisines(df1, 'Japanese') 
        metrics_worst = worst_restaurant_for_cuisines(df1, 'Japanese')

#-----------------------------------------------------------------------
    with col5:
        metrics_better = best_restaurant_for_cuisines(df1, 'Brazilian') 
        metrics_worst = worst_restaurant_for_cuisines(df1, 'Brazilian')
        
#-------------------------------------------------------------------------        
with st.container():
    st.header(f'Top {quantidade_restaurantes} Restaurantes')
    df_aux = top_restaurantes(df)
    st.dataframe(df_aux, use_container_width = True)  

#-------------------------------------------------------------------------   
with st.container():
    col1, col2 = st.columns (2)
    
    with col1:
        st.subheader(f'Top {quantidade_culinarias} Melhores Tipos de Culinárias')
        fig = top_tipos_culinarias(df1, 'nota', False)
        st.plotly_chart(fig, use_container_width = True)
               
    with col2:
        
        st.subheader(f'Top {quantidade_culinarias} Piores Tipos de Culinárias')
        fig = top_tipos_culinarias(df1, 'nota', True)
        st.plotly_chart(fig, use_container_width = True)
#--------------------------------------------------------------------------
with st.container():
    col1, col2 = st.columns (2)
    with col1:
        st.subheader(f'Top {quantidade_culinarias} Tipos de Culinárias com Maior Valor Médio de um Prato para Duas Pessoas')
        fig = top_tipos_culinarias(df1, 'preço', False)
        st.plotly_chart(fig, use_container_width = True)
        
    with col2:
        st.subheader(f'Top {quantidade_culinarias} Tipos de Culinárias com Menor Valor Médio de um Prato para Duas Pessoas')
        fig = top_tipos_culinarias(df1, 'preço', True)
        st.plotly_chart(fig, use_container_width = True)