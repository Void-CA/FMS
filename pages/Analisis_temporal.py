import streamlit as st
import plotly.express as px
from scripts.utils import configure_page, load_data

def comparing_means():
    st.subheader("Comparación de Medias por Año")
    st.write("Empezamos analizando cómo han cambiado los puntajes promedio de los MCs a lo largo de los años.")
    
    fms = load_data()
    fms["year"] = fms["year"].replace({"2023A": "2023", "2023B": "2023"})
    means_per_year = fms.groupby(["year"])["PTB"].mean().reset_index()
    
    st.plotly_chart(
        px.bar(
            means_per_year,
            x="year",
            y="PTB",
            title="Promedio de PTB respecto al Año",
            template="plotly_dark",
            width=600,
            height=500
        )
    )
    st.write("Nota: El año 2023 muestra una disminución aparente debido a la división en grupos A y B, pero los puntajes han sido estables en general.")

# Configuración de página
configure_page()

# Título
st.title("Análisis Temporal del Desempeño en la FMS")

# Secciones del análisis
st.markdown("## Introducción")
st.write("En esta sección exploramos cómo han cambiado los puntajes de batalla (PTB) de los MCs a lo largo del tiempo, considerando cambios en el formato y otras variables.")

# Análisis general
comparing_means()

# Observaciones finales
st.markdown("## Conclusiones")
st.write("""
- Los puntajes promedio han sido estables en general, pero el formato de votación influye en las apariencias.  
- La estandarización nos permite hacer comparaciones más objetivas entre años.  
- Próximamente, exploraremos quiénes han sido los MCs más consistentes en su desempeño.
""")
