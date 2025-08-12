import streamlit as st  
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
from rapidfuzz import process, fuzz

# Configuración de la pagina 
st.set_page_config(
    page_title='Dashboard de Ventas',
    page_icon='☕',
    layout='wide', # Ancho completo
    initial_sidebar_state='expanded' # Barra lateral expandida
)

# cargar los datos
@st.cache_data
#función para cargar los datos
def load_data():
    correct_names= ['remy monet', 'pablo perez', 'tom jackson', 'joao silva', 'walter muller']
    df= pd.read_csv('sales_data.csv') # Cargar el archivo CSV y convertir la columna 'Date' a tipo datetime
    df['Date'] = pd.to_datetime(df['Date'], dayfirst=True, errors='coerce') # Convertir la columna 'Date' a tipo datetime
    df['Price'] = df['Price'].astype(float) # Convertir la columna 'Price' a tipo float
    df['Quiantity'] = df['Quantity'].astype(int) # Convertir la columna 'Quantity' a tipo int
    df['Total_Sales'] = df['Price'] * df['Quantity'] # Calcular el total de ventas
    df['Month'] = df['Date'].dt.month # Extraer el mes de la fecha
    df['Year'] = df['Date'].dt.year # Extraer el año de la fecha
    df['Day_ofWeek'] = df['Date'].dt.day_name() # Extraer el día de la semana
    df['Weekend'] = df['Date'].dt.dayofweek >= 5 # Identificar si es fin de semana
    df['Manager_clean'] = df['Manager'].apply(
        lambda x: process.extractOne(x, correct_names, scorer=fuzz.token_sort_ratio)[0]
    )
    return df

df = load_data()

# Slider para filtros
st.sidebar.markdown(
    """
    <div style="width: 4rem; text-align: center; margin: 0 auto;">
        <h1 style="font-size: 28px; text-aling:center;">Filtros</h1>
    </div>
    """, 
    unsafe_allow_html=True # Permitir HTML
)
                  
# ciudades
selected_cities = st.sidebar.multiselect(
    'Ciudades',
    options=df['City'].unique(),
    default=df['City'].unique().tolist(), # Por defecto todas las ciudades
    key='city_filter' # Clave para el filtro de ciudades
)

selected_products = st.sidebar.multiselect(
    'Productos',
    options=df['Product'].unique(),
    default=df['Product'].unique().tolist(), # Por defecto todos los productos
    key='product_filter' # Clave para el filtro de productos
)

selected_months = st.sidebar.multiselect(
    'Meses',
    options=df['Month'].unique(),
    default=df['Month'].unique().tolist(), # Por defecto todos los meses
    key='month_filter' # Clave para el filtro de meses
)

# filtrar los datos
filtered_df = df[
    (df['City'].isin(selected_cities)) &
    (df['Product'].isin(selected_products)) &
    (df['Month'].isin(selected_months))
]

# KPIs principales
total_sales = filtered_df['Total_Sales'].sum()
avg_sale_per_order = filtered_df['Total_Sales'].mean()
total_orders= filtered_df['Order ID'].nunique()
most_popular_product = filtered_df['Product'].mode()[0]
 
# Layout Principal
st.markdown(
    """
    <div style="width: 100%; text-align: center; margin: 0 auto;">
        <h1 style="font-size: 48px; text-aling:center;">🍽☕🍻Dashboard de Ventas - Restaurante</h1>
    </div>
    
    <div style="width: 100%; text-align: center; margin: 0 auto;">
        <h2 style="font-size: 32px; text-aling:center;">Análisis de Ventas basado en EDA aplicado</h2>
    """,
    unsafe_allow_html=True # Permitir HTML
)

#KPIs en columnas
col1,col2,col3,col4 = st.columns(4)
col1.metric("Ventas Totales", f"${total_sales:,.2f}", delta=f"${total_sales - filtered_df['Total_Sales'].sum():,.2f}" if filtered_df['Total_Sales'].sum() else "$0.00")
col2.metric("Promedio de Ventas por Orden", f"${avg_sale_per_order:,.2f}", delta=f"${avg_sale_per_order - filtered_df['Total_Sales'].mean():,.2f}" if filtered_df['Total_Sales'].mean() else "$0.00")
col3.metric("Total de Pedidos", total_orders, delta=total_orders - filtered_df['Order ID'].nunique() if filtered_df['Order ID'].nunique() else 0)
col4.metric("Producto Más Popular", most_popular_product)  

# Gráficos 
st.markdown(
    """
    <div style="width: 100%; text-align: center; margin: 0 auto;">
        <h2 style="font-size: 32px; text-aling:center;">Análisis de Ventas</h2>
    </div>
    """,
    unsafe_allow_html=True # Permitir HTML
)

tab1, tab2, tab3 = st.tabs(['Tendencias', 'Distribución', 'Comparativa de Ventas'], width=400)
 
with tab1:
    # ventas por mes
    montly_sales = filtered_df.groupby(['Year', 'Month'])['Total_Sales'].sum().reset_index()
    fig = px.line(
        montly_sales, 
        x='Month', 
        y='Total_Sales', 
        color='Year', 
        title='Ventas por Mes'
    )
    fig.update_layout(
        xaxis_title='Mes',
        yaxis_title='Ventas Totales',
        legend_title='Año',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # ventas por día de la semana
    daily_sales = filtered_df.groupby('Day_ofWeek')['Total_Sales'].sum().reset_index()
    day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    daily_sales['Day_ofweek'] = pd.Categorical(daily_sales['Day_ofWeek'], categories=day_order, ordered=True)
    
    fig = px.bar(
        daily_sales, 
        x='Day_ofWeek', 
        y='Total_Sales', 
        title='Ventas por Día de la Semana',
        category_orders={'Day_ofWeek': day_order}
    )
    fig.update_layout(
        xaxis_title='Día de la Semana',
        yaxis_title='Ventas Totales',
        template='plotly_white'
    )
    st.plotly_chart(fig, use_container_width=True)

with tab2:
    # Distribución de productos vendidos
    product_dist = filtered_df['Product'].value_counts().reset_index(name='count')
    fig = px.pie(
        product_dist,
        values='count',
        names='Product',
        title='Distribución de Productos Vendidos'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Métodos de pago
    payment_dist = filtered_df['Payment Method'].value_counts().reset_index(name='count')
    fig = px.bar(
        payment_dist,
        x='Payment Method',
        y='count',
        title='Distribución de Métodos de Pago',
        color='Payment Method'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Distribución de ventas por ciudad
    city_sales = filtered_df.groupby('City')['Total_Sales'].sum().reset_index()
    fig = px.bar(
        city_sales,
        x='City',
        y='Total_Sales',
        title='Distribución de Ventas por Ciudad',
        color='City',
    )
    st.plotly_chart(fig, use_container_width=True)
    
with tab3:
    # Distribución por tipo de compra
    purchase_sales = filtered_df.groupby('Purchase Type')['Total_Sales'].sum().reset_index()
    fig = px.bar(
        purchase_sales,
        x='Purchase Type',
        y='Total_Sales',
        title='Distribución de Ventas por Tipo de Compra',
        color='Purchase Type'
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Comparación fin de semana vs semana
    weekend_type = filtered_df.groupby('Weekend')['Total_Sales'].sum().reset_index()    
    weekend_type['Weekend']= weekend_type['Weekend'].map({True: 'Fin de Semana', False: 'Día de Semana'})
    fig = px.bar(
        weekend_type,
        x='Weekend',
        y='Total_Sales',
        title='Comparación de Ventas entre Fin de Semana y Día de Semana',
        color='Weekend'
    )
    st.plotly_chart(fig, use_container_width=True)

# Hallazgos y Conclusiones
st.subheader('👀🔎Hallazgos claves para el Análisis')
st.markdown(
    """
    - **Tendencias de Ventas**: Se observa una tendencia clara de ventas a lo largo de los meses, con picos en los meses de enero y febrero, y bajos en los meses de marzo, abril y mayo.
    - **Distribución de Ventas**: La mayoría de las ventas se concentran en productos como café, té y bebidas calientes, seguidos por platos fuertes y postres.
    - **Métodos de Pago**: La mayoría de las ventas se realizan con tarjetas de crédito, seguidas por tarjetas de débito y efectivo.
    - **Comparación de Ventas**: La mayoría de las ventas se realizan en días de semana, con una pequeña influencia de fin de semana.
    - **Distribución por Tipo de Compra**: La mayoría de las ventas se realizan en línea, seguidas por en tienda.
    - **Distribución por Ciudad**: La mayoría de las ventas se realizan en la ciudad de Nueva York, seguidas por la ciudad de San Francisco.
    """
)
# Análisis Detallado
st.subheader('📊 Análisis Detallado de Ventas')
col1, col2 = st.columns(2)
with col1:
    #top managers por ventas
    manager_sales = filtered_df.groupby('Manager_clean')['Total_Sales'].sum().reset_index().sort_values(by='Total_Sales', ascending=False)
    fig = px.bar(
        manager_sales,
        x='Total_Sales',
        y='Manager_clean',
        title='Top 10 Managers por Ventas',
    )
    st.plotly_chart(fig, use_container_width=True) 
    
with col2:
    # Relacion cantidad vs precio
    fig= px.scatter(
        filtered_df, 
        x='Price', 
        y='Quantity', 
        color='Product', 
        title='Relación entre Precio y Cantidad Vendida por Producto',
        trendline='ols' # Agregar línea de tendencia
    )
    st.plotly_chart(fig, use_container_width=True)

# Footer
st.markdown('---')
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <p>Desarrollado por <strong>Anderson Hernández</strong> | <a href="https://github.com/beyondAnalysIs/Ventas-Restaurante" target="_blank">GitHub</a></p>
        <p>© 2025</p>
    </div>
    """,unsafe_allow_html=True) # Permitir HTML