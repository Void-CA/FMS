import streamlit as st
import pandas as pd
import scripts.utils as utils
import plotly.express as px
import numpy as np

utils.configure_page()

fms = utils.load_data("Scaled")

def mean_per_country(fms:pd.DataFrame)->pd.DataFrame:
    fms_copy = fms.copy()
    return fms_copy.groupby(["country", "year"]).agg({"PTB": "mean"}).reset_index()

def means_bar_chart(fms:pd.DataFrame, year:str)->px.bar:
    means = mean_per_country(fms)
    means = means[means["year"] == year]

    return px.bar(means, x="country", y="PTB", color="country", 
                  title="Promedio de PTB por país",
                  color_discrete_map=utils.country_colors,
                  text_auto=True)

def battles_outcomes(fms:pd.DataFrame)->pd.DataFrame:
    fms_copy = fms.copy()
    return fms_copy.groupby(["year","country"]).agg({"BG": "sum", "BGR": "sum", "BPR":"sum", "BP": "sum"}).reset_index()

def battles_outcomes_bar_chart(fms:pd.DataFrame, year:str)->px.bar:
    outcomes = battles_outcomes(fms)
    outcomes = outcomes[outcomes["year"] == year]

    return px.bar(outcomes, x="country", y=["BG", "BGR", "BPR", "BP"],
                  title="Desenlace de las batallas por país",
                  text_auto=True,
                  barmode="group",
                  labels={"BG": "Batallas Ganadas", "BGR": "Batallas Ganadas con Réplica", "country": "País"})

st.title("Diferencias por Liga")
st.write("En esta página se muestran las diferencias entre las ligas de FMS en cuanto a los puntajes obtenidos por los competidores.")
st.markdown("## Puntajes por país")
st.write("Una de las cosas mas interesantes a mi parecer es analizar como los votos de los jurados varian por país. A continuación se muestra un gráfico de dispersión que muestra los puntajes obtenidos por los MCs de cada país en cada temporada de FMS.")


year = st.selectbox("Selecciona un año", fms["year"].sort_values().unique())
st.plotly_chart(means_bar_chart(fms, year))

st.subheader("Desenvolvimiento de las batallas")
st.markdown("""
            Otra cosa interesante a analizar es como se desenvuelven las batallas en cada liga. 
            Los enfrentamientos pueden tener 4 desenlaces posibles: victoria, victoria por réplica, derrota por réplica y derrota.
            """)

st.plotly_chart(battles_outcomes_bar_chart(fms, year))
st.write("""
         Nota: Aqui me di cuenta que Urban Roosters tiene mal la informacion de las batallas, 
         ya que el numero de batallas ganadas no coincide con el numero de batallas perdidas.
         Por lo que los datos presentados en este grafico pueden no ser correctos. Gracias UR.
         """)

st.dataframe(battles_outcomes(fms))

st.markdown("## Conclusiones")
st.markdown("""
            Dejando de lado los errores de Urban Roosters, podemos observar una diferencia clave entre las ligas de FMS.
            Es complicado discernir si estas diferencias se deben a la calidad de los MCs, a la calidad de los jurados o a la calidad de las batallas.
            Pero a simple vista podemos observar que los MCs de Argentina y España suelen obtener puntajes mas altos que los de Colombia y Caribe.
            España tuvo un bajon de PTB en el 2020, lo cual se alinea con la baja de Chuty y Skone de la liga en este año. En lineas generales este patron observable
            es comprobable por opiniones de fans y analistas de FMS. Quienes suelen decir que la liga de España es la mas competitiva y la de Colombia la menos competitiva.
            Luego tenemos casos donde es mas dificil discernir, como el caso de Peru, que tuvo un bajon en el 2020, pero que en el 2022 tuvo un repunte.
            Repunte que en mi opinion puede ser una correccion de votacion, debido a que en mi opinion, la liga peruana en 2020 obtuvo puntajes muy bajos 
            a comparacion de la calidad de las batallas.
            """)
st.markdown("""
            Si bien me gustaria poder realizar un analisis mas profundo tales como sesgos de votacion, paises que sobrevaloren o infravaloren a sus competidores, etc.
            no cuento con la informacion necesaria para poder afirmar algo con certeza. Sin embargo, es un tema que me gustaria investigar en el futuro.
            Con un poco de suerte Urban Rooster o alguna otra organizacion de FMS publique mas informacion sobre las votaciones de los jurados.
            """)