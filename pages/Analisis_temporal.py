import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from scripts.utils import configure_page, load_data

def comparing_means():
    st.subheader("Comparación de Medias por Año")
    st.write("Empezamos analizando cómo han cambiado los puntajes promedio de los MCs a lo largo de los años.")
    
    fms = load_data("FMS")
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
    st.write("Nota: El año 2023 muestra una disminución aparente debido a la división en grupos A y B, lo que reduce las batallas a la mitad, en general los puntajes han disminuido ligeramente a medida que pasan los años.")


def ptb_development():
    st.subheader("Desarrollo de PTB por MC")
    st.write("A continuación, analizamos cómo ha cambiado el desempeño de los MCs a lo largo de los años.")

    fms = load_data("Scaled")
    cols = st.columns(2)
    filtered_mcs = st.multiselect("Selecciona MCs para comparar", fms["MC"].unique(), default=["Aczino", "Chuty", "Teorema", "Jaze"])
    important_mcs = fms[fms["MC"].isin(filtered_mcs)]

    fixed_years = sorted(important_mcs['year'].unique())

    # Crear el gráfico inicial con Plotly Express
    fig = px.line(
        important_mcs,
        x="year",
        y="PTB_scaled",
        color="MC",
        title="Desarrollo de PTB por MC (Escalado)",
        template="plotly_dark",
        width=800,
        height=600,
        markers=True,
        category_orders={"year": fixed_years}
    )

    # Convertir el gráfico de Plotly Express a un objeto de Plotly Graph Objects
    fig = go.Figure(fig)

    # Añadir líneas horizontales para indicar los márgenes
    fig.add_hline(y=0, line_dash="dash", line_color="white", annotation_text="Desempeño Promedio", annotation_position="top left")
    fig.add_hline(y=1.5, line_dash="dash", line_color="green", annotation_text="Desempeño Sobresaliente", annotation_position="top left")
    fig.add_hline(y=-1.5, line_dash="dash", line_color="red", annotation_text="Desempeño Bajo", annotation_position="bottom left")

    # Mostrar el gráfico en Streamlit
    st.plotly_chart(fig)

    st.write("Los puntajes estan escalados por año para comparar el desempeño relativo de los MCs. Un puntaje de 0 indica el promedio, mientras que 1.5 y -1.5 son los límites para desempeños sobresalientes y bajos, respectivamente.")


# Configuración de página
configure_page()

# Título
st.title("Análisis Temporal del Desempeño en la FMS")

# Secciones del análisis
st.markdown("## Introducción")
st.write("En esta sección exploramos cómo han cambiado los puntajes de batalla (PTB) de los MCs a lo largo del tiempo, considerando cambios en el formato y otras variables.")

# Análisis general
comparing_means()

ptb_development()

# Observaciones finales
st.markdown("## Conclusiones")
st.write("""
- Los puntajes promedio han sido estables en general, pero el formato de votación influye en las apariencias.  
- La estandarización nos permite hacer comparaciones más objetivas entre años.  
- Próximamente, exploraremos quiénes han sido los MCs más consistentes en su desempeño.
""")
