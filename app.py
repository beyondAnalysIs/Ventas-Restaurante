import streamlit as st  
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta

# Configuración de la pagina 
st.set_page_config(
    page_title='Dashboard de Ventas',
    page_icon='🍽☕',
    layout='wide', # Ancho completo
    initial_sidebar_state='expanded' # Barra lateral expandida
)

# cargar los datos
@st.cache_data
#función para cargar los datos
def load_data():
    df= pd.read_csv('sales_data.csv') # Cargar el archivo CSV y convertir la columna 'Date' a tipo datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce') # Convertir la columna 'Date' a tipo datetime
    df['Price'] = df['Price'].astype(float) # Convertir la columna 'Price' a tipo float
    df['Quiantity'] = df['Quantity'].astype(int) # Convertir la columna 'Quantity' a tipo int
    df['Total_Sales'] = df['Price'] * df['Quantity'] # Calcular el total de ventas
    df['Month'] = df['Date'].dt.month # Extraer el mes de la fecha
    df['Year'] = df['Date'].dt.year # Extraer el año de la fecha
    df['Day_ofWeek'] = df['Date'].dt.day_name() # Extraer el día de la semana
    df['Weekend'] = df['Date'].dt.dayofweek >= 5 # Identificar si es fin de semana
    return df

df = load_data()

# Slider para filtros
st.sidebar.markdown(
    """
    <div style="width: 2rem; text-align: center; margin: 0 auto;">
        <h1 style="font-size: 28px; text-aling:center;">Filtros</h1>
    </div>
    """, 
    unsafe_allow_html=True
)
                  


