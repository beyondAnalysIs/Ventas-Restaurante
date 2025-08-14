import streamlit as st  
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
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
    df['Quantity'] = df['Quantity'].astype(int) # Convertir la columna 'Quantity' a tipo int
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

#-------FILTROS-------
# Slider para filtros
st.sidebar.markdown(
    """
    <div style="width: 2.5rem; height:2.5rem; text-align: center; margin: 0 auto;">
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
# validación de los filtros
if not selected_cities or not selected_products or not selected_months:
    st.error("Por favor, selecciona al menos una ciudad, un producto y un mes.")
    st.stop()  # Detener la ejecución si no hay filtros válidos
    
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
 
#--------LAYOUT PRINCIPAL--------
st.markdown(
    """
    <div style="width: 100%; text-align: center; margin: 0 auto;">
        <h1 style="font-size: 24px; text-aling:center;">🍔🍗🍦Dashboard de Ventas - Restaurante 🍽 ☕ 🍻</h1>
    </div>
    
    <div style="width: 100%; text-align: center; margin: 0 auto; color: #6b7280;">
        <p style="font-size: 18px; text-aling:center;">
            Una herramienta centralizada que reúne en un solo lugar indicadores clave como ventas totales, productos más vendidos,
            comportamiento por ciudad y tipo de compra. Ideal para una visión rápida del negocio y la toma de decisiones estratégicas.
        </p>
    """,
    unsafe_allow_html=True # Permitir HTML
)
#--------KPIS--------
# Estilos CSS para los KPIs
st.markdown(
    """
    <style>
    .kpi-container {
        background: rgb(255, 75, 75);
        border-radius: 20px;
        padding: .1rem;
        box-shadow: 0 8px 32px 0 rgba(31, 38, 135, 0.37);
        backdrop-filter: blur(4px);
        border: 1px solid rgba(255, 255, 255, 0.18);
        margin: .2rem 0;
    }
    
    .kpi-card {
        background: transparent;
        padding: 1.5rem;
        border-radius: 20px !important;
        text-align: center;
        box-shadow: 0 4px 15px 0 rgba(0, 0, 0, 0.1);
        transition: transform 0.3s ease, box-shadow 0.3s ease, border 0.3s ease;
        margin: 0.5rem;
        min-height: 120px;
        display: flex;
        flex-direction: column;
        justify-content: center;
        border: 2px solid;
    }
    
    
    .kpi-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px 0 rgba(0, 0, 0, 0.15);
    }
    
    .kpi-title {
        font-size: 14px;
        font-weight: 600;
        color: #ffffff;
        text-transform: uppercase;
        letter-spacing: 0.5px;
        margin-bottom: 0.5rem;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-value {
        font-size: 24px;
        font-weight: 700;
        margin: 0;
        line-height: 1.2;
        background: linear-gradient(135deg, #10b981, #34d399, #6ee7b7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        background-clip: text;
        text-shadow: none;
    }
    
    .kpi-icon {
        font-size: 2rem;
        margin-bottom: 0.5rem;
        color: #ffffff;
        text-shadow: 0 2px 4px rgba(0, 0, 0, 0.3);
    }
    
    .kpi-card.sales { 
        border-image: linear-gradient(135deg, #10b981, #34d399, #6ee7b7) 1;
    }
    .kpi-card.average { 
        border-image: linear-gradient(135deg, #10b981, #34d399, #6ee7b7) 1;
    }
    .kpi-card.orders { 
        border-image: linear-gradient(135deg, #10b981, #34d399, #6ee7b7) 1;
    }
    .kpi-card.product { 
        border-image: linear-gradient(135deg, #10b981, #34d399, #6ee7b7) 1;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Contenedor principal de KPIs
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

#KPIs en columnas
col1,col2,col3,col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
            <div class="kpi-card sales">
                <div class="kpi-icon">💰</div>
                <div class="kpi-title">Ventas Totales</div>
                <div class="kpi-value">${total_sales:,.2f}</div>
            </div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    st.markdown(
        f"""
        <div class="kpi-card average">
            <div class="kpi-icon">📊</div>
            <div class="kpi-title">Promedio por Orden</div>
            <div class="kpi-value">${avg_sale_per_order:,.2f}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    st.markdown(
        f"""
        <div class="kpi-card orders">
            <div class="kpi-icon">📦</div>
            <div class="kpi-title">Total de Pedidos</div>
            <div class="kpi-value">{total_orders:,}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        
        f"""
        <div class="kpi-card product">
            <div class="kpi-icon">⭐</div>
            <div class="kpi-title">Producto Más Popular</div>
            <div class="kpi-value" style="font-size: 18px;">{most_popular_product}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# Cerrar contenedor principal
st.markdown('</div>', unsafe_allow_html=True)  
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

#----------GRÁFICOS----------
st.markdown(
    """
    <div style="width: 100%; text-align: center; margin: 0 auto;">
        <h2 style="font-size: 20px; text-aling:center;">📊Análisis de Ventas</h2>
    </div>
    """,
    unsafe_allow_html=True # Permitir HTML
)

# dataframe de coordenadas para las ciudades
city_coords = {
    'Madrid': {'lat': 40.416775, 'lon': -3.703790},
    'Lisbon': {'lat': 38.722252, 'lon': -9.139337},
    'London': {'lat': 51.507351, 'lon': -0.127758},
    'Berlin': {'lat': 52.520008, 'lon': 13.404954},
    'Paris': {'lat': 48.856613, 'lon': 2.352222},
}
# Contenedores de gráficas
tab1, tab2, tab3, tab4 = st.tabs(['Tendencias', 'Distribución', 'Comparativa de Ventas', 'Mapa de Ventas'])

# -----TENDENCIAS----- 
with tab1:
    # Layout horizontal para tendencias - 2 columnas lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        # heatmap de Purchase Type por City
        contingency_table = pd.crosstab(filtered_df['Purchase Type'],filtered_df['City'], normalize='index')
        scale = 1.0
        # grafica
        fig, ax = plt.subplots(figsize=(10 * scale, 6 * scale), facecolor='none')
        sns.set_theme(
            style="whitegrid",
            palette="coolwarm",
            font_scale=1.1 
        )
        
        sns.heatmap(
            contingency_table, 
            annot=True, 
            fmt=".2f", 
            cmap='Blues', 
            linewidths=.5, 
            ax=ax,
            annot_kws={"fontsize": scale * 15},  # Ajustar el tamaño de la fuente de los números
            
        )
        ax.set_title('Distribución de Tipo de Compra por Ciudad', fontsize=20,color='white', pad=30, fontweight='bold', loc='left')
        ax.set_xlabel('Ciudad', fontsize=16, color='white')
        ax.set_ylabel('Tipo de Compra', fontsize=16, color='white')
        ax.tick_params(axis='both', which='major', labelsize=14, colors='white')
        st.pyplot(fig, use_container_width=True)  # Mostrar la gráfica en Streamlit
        
    
    with col2:
        # ventas por día de la semana
        daily_sales = filtered_df.groupby('Day_ofWeek')['Total_Sales'].sum().reset_index()
        day_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
        daily_sales['Day_ofweek'] = pd.Categorical(daily_sales['Day_ofWeek'], categories=day_order, ordered=True)
        
        fig = px.bar(
            daily_sales, 
            x='Day_ofWeek', 
            y='Total_Sales', 
            title='Ventas por Día de la Semana',
            category_orders={'Day_ofWeek': day_order},
            color='Day_ofWeek'
        )
        fig.update_layout(
            xaxis_title='Día de la Semana',
            yaxis_title='Ventas Totales',
            template='plotly_white',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
# -----DISTRIBUCIÓN-----
with tab2:
    # Primera fila - 2 gráficos horizontales
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Distribución de productos vendidos
        product_dist = filtered_df['Product'].value_counts().reset_index(name='count')
        fig = px.pie(
            product_dist,
            values='count',
            names='Product',
            title='Productos Vendidos'
        )
        fig.update_layout(height=400)
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Métodos de pago
        payment_dist = filtered_df['Payment Method'].value_counts().reset_index(name='count')
        fig = px.bar(
            payment_dist,
            x='Payment Method',
            y='count',
            title='Métodos de Pago',
            color='Payment Method'
        )
        fig.update_layout(
            height=400,
            xaxis_title='Método de Pago',
            yaxis_title='Cantidad'
        )
        st.plotly_chart(fig, use_container_width=True)
        
    with col3:
        # Distribución de ventas por ciudad (centrada)
        city_sales = filtered_df.groupby('City')['Total_Sales'].sum().reset_index()
        fig = px.bar(
            city_sales,
            x='City',
            y='Total_Sales',
            title='Ventas por Ciudad',
            color='City',
        )
        fig.update_layout(
            xaxis_title='Ciudad',
            yaxis_title='Ventas Totales',
            height=400
        )
        st.plotly_chart(fig, use_container_width=True)
    
# -----COMPARATIVA DE VENTAS-----
with tab3:
    # Layout horizontal para comparativas - 2 columnas lado a lado
    col1, col2 = st.columns(2)
    
    with col1:
        # Distribución por tipo de compra
        purchase_sales = filtered_df.groupby('Purchase Type')['Total_Sales'].sum().reset_index()
        fig = px.bar(
            purchase_sales,
            x='Purchase Type',
            y='Total_Sales',
            title='Ventas por Tipo de Compra',
            color='Purchase Type'
        )
        fig.update_layout(
            height=400,
            xaxis_title='Tipo de Compra',
            yaxis_title='Ventas Totales'    
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Comparación fin de semana vs semana
        weekend_type = filtered_df.groupby('Weekend')['Total_Sales'].sum().reset_index()    
        weekend_type['Weekend']= weekend_type['Weekend'].map({True: 'Fin de Semana', False: 'Día de Semana'})
        fig = px.bar(
            weekend_type,
            x='Weekend',
            y='Total_Sales',
            title='Ventas entre Fin de Semana y Día de Semana',
            color='Weekend'
        )
        fig.update_layout(
            height=400,
            xaxis_title='Tipo de Día',
            yaxis_title='Ventas Totales',
        )
        st.plotly_chart(fig, use_container_width=True)
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

# -----MAPA DE VENTAS-----
with tab4:
    st.markdown(
        """
        <div style="width: 100%; text-align: center; margin: 0 auto;">
            <h2 style="font-size: 20px; text-aling:center;">🗺️ Ventas por Ciudad</h2>
        </div>
        """,
        unsafe_allow_html=True # Permitir HTML
    )
    # Mapa de ventas
    city_sales = filtered_df.groupby('City')['Total_Sales'].sum().reset_index().round(2)
    
    # Agregar coordenadas de las ciudades
    city_sales['lat'] = city_sales['City'].map(lambda x: city_coords.get(x,{}).get('lat'))
    city_sales['lon'] = city_sales['City'].map(lambda x: city_coords.get(x,{}).get('lon'))
    
    # Crear el mapa
    fig = px.scatter_geo(
        city_sales,
        lat='lat',
        lon='lon',
        size='Total_Sales',
        hover_name='City',
        projection='natural earth',
        size_max=50,
        color='City',
        locationmode='country names',
        text='Total_Sales'
    )
    
    # Texto del mapa
    fig.update_traces(
        textfont=dict(
            color='#000',
            size=12,
            family='Arial,bold'
        ),
        textposition='middle center'
    )
    # Personalizar el mapa
    fig.update_geos(
        resolution=50, # Resolución del mapa
        showcoastlines=True, # Mostrar costas
        coastlinecolor="RebeccaPurple", # Color de las costas
        showland=True, # Mostrar tierra
        landcolor="LightGreen", # Color de la tierra
        showocean=True,# Mostrar océanos
        oceancolor="LightBlue", # Color de los océanos
        showlakes=True,# Mostrar lagos
        lakecolor="LightBlue", # Color de los lagos
        showrivers=True, # Mostrar ríos
        rivercolor="LightBlue", # Color de los ríos
    )
    fig.update_layout(
        height=350,
        margin={"r": 0, "t": 40, "l": 0, "b": 0} ,
        geo=dict(
            center=dict(lat=48, lon=5), 
            showframe=False,# No mostrar el marco del mapa
            showcoastlines=False,# No mostrar las costas
            projection_type='natural earth',# Tipo de proyección del mapa
            bgcolor='rgba(0,0,0,0)',
            projection_scale=4, # Escala de la proyección
        )
    )
    st.plotly_chart(fig, use_container_width=True)
    
    # Montrar tabla de datos
    with st.expander('Ver Datos detallados por ciudad'):
        city_sales_display = city_sales[['City', 'Total_Sales']].copy()
        city_sales_display['Total_Sales'] = city_sales_display['Total_Sales'].apply(
            lambda x: f'€{x:,.2f}'  
        )
        st.dataframe(
            city_sales_display,
            column_config={
                'City': 'Ciudad',
                'Total_Sales':'Ventas Totales'
            },
            hide_index=True
        )
#-------- ANÁLISIS MULTIVARIABLES------    
col1, col2 = st.columns(2)
with col1:
    #top Managers por ventas
    manager_sales = filtered_df.groupby('Manager_clean')['Total_Sales'].sum().reset_index().sort_values(by='Total_Sales', ascending=False)
    fig = px.bar(
        manager_sales,
        x='Total_Sales',
        y='Manager_clean',
        title='Top Managers por Ventas',
    )
    fig.update_layout(
        xaxis_title='Ventas Totales',
        yaxis_title='Gerente',
        height=400,
        template='plotly_white'
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
    fig.update_traces(marker=dict(size=10, opacity=0.7), selector=dict(mode='markers'))
    fig.update_layout(
        xaxis_title='Precio',
        yaxis_title='Cantidad Vendida',
        template='plotly_white',
        height=400
    )
    
    st.plotly_chart(fig, use_container_width=True)
st.markdown('<div class="kpi-container">', unsafe_allow_html=True)

#--------FOOTER-------
st.markdown(
    """
    <div style="text-align: center; padding: 20px;">
        <p>Desarrollado por <strong>Anderson Hernández</strong> | <a href="https://github.com/beyondAnalysIs/Ventas-Restaurante" target="_blank">GitHub</a></p>
        <p>© 2025</p>
    </div>
    """,unsafe_allow_html=True) 