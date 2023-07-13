#------------------------------------------------------------------------------------
# Bibliotecas Necessarias
#------------------------------------------------------------------------------------
import pandas as pd
import numpy as np
import inflection
import plotly.express as px
import streamlit as st
from PIL import Image
import folium
from streamlit_folium import folium_static
from folium.plugins import MarkerCluster

st.set_page_config(
    page_title="Main Page",
    page_icon="🏠",
    layout= 'wide'
)
#------------------------------------------------------------------------------------
# Importando Planilha
#------------------------------------------------------------------------------------
df = pd.read_csv('dataset/zomato.csv')
df1 = df.copy()

#------------------------------------------------------------------------------------
# Funções
#------------------------------------------------------------------------------------
# Essa função tem como objetivo gerar um mapa com pontos nos locais do restaurantes de acordo com sua latitude e longitude. Todos os pontos possuem: 
# 1. Clusterização através do comando MarkerCluster
# 2. Ícone de uma casa branca e em volta a cor é de acordo com a avaliação (quanto mais verde melhor avaliado é o restaurante), dentro desse ícone tem:
    # 1. Nome do Restaurante
    # 2. Preço médio para dois e a moeda
    # 3. Tipo de culinária
    # 4. Nota de avaliação

def country_maps(df):
    
    df_aux = df1.loc[:, ["rating_color","latitude","longitude","restaurant_name","country_code",'average_cost_for_two','currency','cuisines','aggregate_rating']]

 
    map= folium.Map()

    marker_cluster = MarkerCluster().add_to(map)
    
    for index, row in df_aux.iterrows():
        icon = folium.map.Icon(color= row["rating_color"], icon_color='white', icon='home', angle=0, prefix='glyphicon')

        conteudo_popup = f"<strong>{row['restaurant_name']}</strong><br><br>"
        conteudo_popup += f"Price: {row['average_cost_for_two']: .2f} {row['currency']} para dois<br>"
        conteudo_popup += f"Type: {row['cuisines']}<br>"
        conteudo_popup += f"Aggregate Rating: {row['aggregate_rating']}/5.0"
        
        
        folium.Marker([row["latitude"], row["longitude"]], popup = folium.Popup(conteudo_popup, max_width=250), icon = icon).add_to(marker_cluster)
            
    folium_static (map, width=1024, height=600)
#-----------------------------------------------------------------
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
    

#--------------------------------------------------------------------------
# Limpeza
#--------------------------------------------------------------------------
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

    st.title('Fome Zero')

    st.markdown('# Filtro')

    countries_options = st.sidebar.multiselect('Escolha os paises que deseja visualizar os restaurantes', ('India','Australia','Brazil','Canada','Indonesia','New Zeland','Philippines','Qatar','Singapure','South Africa','Sri Lanka','Turkey','United Arab Emirates','England','United States of America'), default = ('Brazil','England','Qatar','South Africa','Canada','Australia'))

df1 = df.copy()
linhas_selecionadas = df1['country_code'].isin( countries_options )
df1 = df1.loc[linhas_selecionadas,:]

#---------------------------------------------------------------------------------
# Layout
#---------------------------------------------------------------------------------
st.title('Fome Zero!')
st.header('Ache seu novo restaurante favorito na nossa plataforma!')
st.subheader('Nossa plataforma tem as seguintes métricas gerais:')
with st.container():
    col1, col2, col3, col4, col5, col6 = st.columns (6)
    with col1:
        restaurante_unico = len(df['restaurant_id'].unique())
        col1.metric('Restaurantes', restaurante_unico)
        
    with col2:
        paises_unicos = len(df['country_code'].unique())
        col2.metric('Países Cadastrados', paises_unicos)
        
    with col3:
        cidades_unicas = len(df['city'].unique())
        col3.metric('Cidades Cadastrados', cidades_unicas)
        
    with col4:
        total_avaliacoes = df['votes'].sum()
        col4.metric('Avaliações Feitas', total_avaliacoes)
    with col5:
        total_culinaria = len(df['cuisines'].unique())
        col5.metric('Tipos de Culinárias', total_culinaria)
        
with st.container():
    st.title('Mapa')   
    country_maps(df)







    