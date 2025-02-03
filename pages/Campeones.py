import streamlit as st
import scripts.utils as utils
import plotly.express as px

# Título principal
st.title("Datos sobre los campeones de FMS")
st.write("En esta sección, analizaremos los datos de los campeones de FMS a lo largo de los años.")

st.write("Una pregunta para empezar, un campeón de FMS ¿es siempre el MC con más puntos?")
st.write("Para responder a esta pregunta, primero cargaremos los datos y luego analizaremos los campeones de cada temporada.")
fms = utils.load_data("FMS")
champions = fms[fms["champion"] == 1][["MC", "year", "PTS", "PTB"]].sort_values(by='PTB', ascending=False)

# Mostrar los campeones
n_championships = fms.groupby("MC").agg({"champion":"sum", "country": "first"}).query("champion > 0")
fig = px.bar(n_championships, y=n_championships.index, x="champion", 
             title="Número de Campeonatos Ganados", 
             template="plotly_dark", 
             color="country",
             color_discrete_map=utils.country_colors)
st.plotly_chart(fig)