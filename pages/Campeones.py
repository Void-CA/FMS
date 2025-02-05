import plotly.express as px
import plotly.graph_objects as go
import streamlit as st
import scripts.utils as utils  
import pandas as pd
import numpy as np
import scipy.stats as stats

utils.configure_page()

def show_champions():
    fms = utils.load_data("FMS").sort_values(["year", "country"])
    fms = fms[fms["champion"] == 1]

    # Mostrar los campeones
    n_championships = fms.groupby("MC").agg({"champion": "sum", "country": "first"})
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
    country = st.selectbox("País", ["Todos"] + list(utils.country_colors.keys()))
    
    if country != "Todos":
        fms = utils.load_data("Scaled")
        fms = fms[fms["country"] == country]
    else:
        fms = utils.load_data("Scaled")

    fms["year"] = fms["year"].replace({"2023A": "2023", "2023B": "2023"})
    fms = fms.sort_values(["year", "PTS_scaled"], ascending=False)

    # Crear el gráfico
    fig = px.scatter(fms, x="PTS_scaled", y="PTB_scaled", color="champion", 
                     title="Comparación de Puntos de los Campeones", 
                     color_discrete_map={0: "gray", 1: "gold"}, 
                     facet_col="year", 
                     facet_col_wrap=3,
                     width=1200,
                     custom_data=[fms["MC"], fms["year"], fms["champion"]]
                     )
    
    fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>" +  # Nombre del MC
                        "Campeón: %{customdata[2]}<br>" +  # Campeón
                      "PTB: %{y:.2f}<br>" +  # PTB
                      "PTS: %{x:.2f}<extra></extra>"  # PTS
    )
    
    # Mostrar el gráfico
    st.plotly_chart(fig)

def proportion_champion_mvp():
    fms = utils.load_data("Scaled")
    fms["year"] = fms["year"].replace({"2023A": "2023", "2023B": "2023"})

    max_ptb = fms.groupby(["year", "country"]).agg({"PTB": "max"}).reset_index()
    for i, row in fms.iterrows():
        if row["PTB"] == max_ptb[(max_ptb["year"] == row["year"]) & (max_ptb["country"] == row["country"])]["PTB"].values[0]:
            fms.loc[i, "MVP"] = 1
        else:
            fms.loc[i, "MVP"] = 0
    

    champions = fms[fms["champion"] == 1]
    mvps = fms[fms["MVP"] == 1]

    st.subheader("Metricas claves")
    
    cols = st.columns(3)
    with cols[0]:
        st.metric("Número de campeones y MVPs", champions.shape[0])
        st.metric("Proporción de campeones que fueron MVPs", str(champions["MVP"].mean() * 100) + "%")
        st.metric("Correlacion entre PTS y PTB", round(stats.pearsonr(fms["PTS"], fms["PTB"])[0], 2))
    with cols[1]:
        st.metric("PTBs promedio de los campeones", champions["PTB"].mean())
        st.metric("PTBs promedio de los MVPs", mvps["PTB"].mean())
        st.metric("Diferencia de PTBs promedio", round(champions["PTB"].mean() - mvps["PTB"].mean(),2))
    with cols[2]:
        st.metric("PTS promedio de los campeones", champions["PTS"].mean())
        st.metric("PTS promedio de los MVPs", mvps["PTS"].mean())
        st.metric("Diferencia de PTS promedio", round(champions["PTS"].mean() - mvps["PTS"].mean(), 2))



# Título principal
st.title("Datos sobre los campeones de FMS")
st.write("En esta sección, analizaremos los datos de los campeones de FMS a lo largo de los años.")
st.subheader("Campeones de fms")
show_champions()

st.write("Una pregunta para empezar, un campeón de FMS ¿es siempre el MC con más puntos?")
st.write("Para responder a esta pregunta, analizaremos los campeones comparando sus puntos con los de los demas en MCs de esa misma temporada.")
compare_champions()
st.markdown("""
         En el gráfico anterior, los campeones están marcados en dorado, mientras que los demás MCs están en gris.
         Usamos los PTB y PTS escalados por año para comparar el desempeño relativo de los MCs. Los PTB miden el desempeño por batalla, 
         los PTS miden los puntos obtenidos a traves de las victorias en su temporada. Mientras el punto este mas a la derecha
         implicara que el MC obtuvo mas puntos en su temporada, mientras que si esta mas arriba implica que el MC obtuvo mas PTB en su temporada.
         """)


st.markdown(" #### Que podemos observar?")
st.write("""
         Como es esperado, los campeones suelen tener un mejor desempeño que los demás MCs en términos de PTB. Sin embargo,
            no siempre son los que más puntos obtienen. Por ejemplo, en la temporada 2020, el campeón de España, Bnet, tuvo muchos
            menos puntos que Gazir, ojo, esto no significa que Bnet no haya sido el mejor MC de esa temporada, ya que el PTB si bien
            es una metrica descriptiva de la calidad de las batallas, suele no ser suficiente reflejo de los highlights de la temporada.

         """)

proportion_champion_mvp()