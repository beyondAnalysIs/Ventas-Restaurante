Dashboard interactivo construido con Streamlit para análisis visual y exploración de datos de ventas de restaurante. Permite obtener insights clave como ventas totales, productos más vendidos, comparativas por ciudad, tendencias temporales, mapa de ventas y análisis por gerentes.

Tabla de Contenidos
- Demo
- Características
- Uso
- Autor

Demo

Incluye una vista previa del dashboard en funcionamiento:

https://ventas-restaurante-ahba.streamlit.app/

Características

- Filtrado dinámico por ciudades, productos y meses.
- KPIs visuales: ventas totales, promedio por orden, cantidad de pedidos y producto más popular.
- Gráficos interactivos generados con Matplotlib/Seaborn y Plotly:

    * Heatmap de tipos de compra por ciudad.

    * Ventas por día de la semana.

    * Distribución de productos, métodos de pago y ventas por ciudad.

    * Comparativas entre tipo de compra y días laborables vs fin de semana.

    * Mapa geoespacial de ventas por ciudad.

    * Análisis multivariable por gerentes y relación precio-cantidad.

- Caché de datos para rendimiento mejorado con @st.cache_data.

- Corrección de nombres de gerentes usando rapidfuzz.

- Visual styling personalizado con CSS para tarjetas KPI.


Uso

1. Filtra por ciudad, producto y mes desde la barra lateral.

2. Explora los KPIs principales visualizados como tarjetas interactivas.

3. Navega entre pestañas para ver análisis detallados y visualizaciones:

    * Tendencias (heatmap, ventas por día).

    * Distribución (productos, métodos de pago, ventas por ciudad).

    * Comparativa (tipo de compra, fin de semana vs día laboral).

    * Mapa geográfico de ventas.

    * Análisis de gerentes y relación precio-cantidad.

4. Expande la sección del mapa para ver los datos tabulados.


Autor

Desarrollado por: Anderson Hernández

Repositorio original: https://github.com/beyondAnalysIs/Ventas-Restaurante

Año: 2025
