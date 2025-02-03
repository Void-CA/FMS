import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import scripts.utils as utils  

def show_champions():
    fms = utils.load_data("FMS")

    # Mostrar los campeones
    n_championships = fms.groupby("MC").agg({"champion": "sum", "country": "first"}).query("champion > 0")
    n_championships = n_championships.rename(columns={"champion": "championships"})
    # Treemap
    fig = px.treemap(n_championships, path=["country", n_championships.index], 
                     values="championships", title="Número de Campeonatos Ganados",
                     color="country", color_discrete_map=utils.country_colors,
                     template="plotly_dark",
                     custom_data=[n_championships.index, n_championships["country"], n_championships["championships"]]
                     )
    
    fig.update_traces(
    hovertemplate="<b>%{customdata[0]}</b><br>" +  # Nombre del MC
                 "País: %{customdata[1]}<br>" +  # País
                 "Títulos: %{customdata[2]}<extra></extra>"  # Número de títulos
                )


    fig.update_traces(
        textfont=dict(
            family="Arial, sans-serif",  # Tipo de letra
            size=14,  # Tamaño de fuente
            color="white",  # Color del texto
            weight="bold"  # Negrita
        )
        
    )


    st.plotly_chart(fig)

def compare_champions():
    cols = st.columns(2)
    fms = utils.load_data("FMS")
    fms["year"] = fms["year"].replace({"2023A": "2023", "2023B": "2023"})
    
    with cols[0]:
        # Selecciona un país
        country = st.selectbox("Selecciona un país", fms["country"].sort_values().unique())
        
    # Filtrar los años disponibles para el país seleccionado
    years_for_country = fms.query(f"country == '{country}'")["year"].sort_values().unique()
    
    with cols[1]:
        # Selecciona un año basado en el país
        year = st.selectbox("Selecciona un año", years_for_country)
    
    # Filtrar los datos para ese país y año
    filtered_fms = fms[(fms["year"] == year) & (fms["country"] == country)]
    
    # Crear el gráfico
    fig = px.scatter(filtered_fms, x="PTB", y="PTS", color="champion", title="Comparación de Puntos de los Campeones", color_discrete_map={0: "gray", 1: "gold"})
    
    # Mostrar el gráfico
    st.plotly_chart(fig)

# Título principal
st.title("Datos sobre los campeones de FMS")
st.write("En esta sección, analizaremos los datos de los campeones de FMS a lo largo de los años.")
st.subheader("Campeones de fms")
show_champions()

st.write("Una pregunta para empezar, un campeón de FMS ¿es siempre el MC con más puntos?")
st.write("Para responder a esta pregunta, analizaremos los campeones comparando sus puntos con los de los demas en MCs de esa misma temporada.")
compare_champions()