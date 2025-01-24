import streamlit as st
from scripts.utils import load_data
import plotly.express as px


country_colors = {
    'ESP': '#ff0404',  # Rojo de la bandera de España
    'MEX': '#006847',  # Verde de la bandera de México
    'ARG': '#75AADB',  # Celeste de la bandera de Argentina
    'CHILE': '#0033A0',  # Azul de la bandera de Chile
    'PERU': '#9c0000',  # Rojo de la bandera de Perú
    'COL': '#FCD116',  # Amarillo de la bandera de Colombia
    'CAR': '#66ffc5 '
}

# Usar CSS para modificar el tamaño del contenedor del gráfico
st.markdown(
    """
    <style>
        .block-container {
            max-width: 1300px;  # Ajusta el ancho según lo desees
        }
    </style>
    """, unsafe_allow_html=True)


final_table = load_data()
years = list(final_table["year"].sort_values().unique())
countries = list(final_table["country"].sort_values().unique())


st.title('Freestyle Master Series')
st.write('Welcome to the Freestyle Master Series! This is a simple web app that allows you see the FMS historical statistics.')

selected_year = st.selectbox('Select a year:', years)
box_cols = st.columns(3)

filtered_table = final_table[final_table["year"] == selected_year].sort_values(by='PTB', ascending=True)
with box_cols[0]:
    st.subheader("Top 5 MC's with the most PTB")
    st.dataframe(filtered_table[["MC", "PTB", "country", "BG", "PTS"]].sort_values(by='PTB', ascending=False).head(5))

    fig_0 = px.bar(filtered_table, x='PTB', y='MC', color='country', title='PTB by MC and Country',
                   color_discrete_map=country_colors)
    st.plotly_chart(fig_0)


with box_cols[1]:
    fig_1 = px.box(filtered_table, x='country', y='PTB', title='PTB by Country', color="country", 
                   color_discrete_map=country_colors)
    st.plotly_chart(fig_1)
    st.subheader("Top Countries with the most PTB")
    top_5 = filtered_table.groupby('country')['PTB'].sum().sort_values(ascending=False).head(5)
    for country, ptb in top_5.items():
        st.latex(f'\t{country}: {ptb}')
    
with box_cols[2]:
    st.subheader("Champions of the Year")
    champions = filtered_table[filtered_table["champion"] == 1][["MC", "country", "PTS"]].sort_values(by='PTS', ascending=False)
    
    # Crear una tabla más estilizada
    champion_table = champions[['MC', 'country', 'PTS']]
    cols = st.columns(len(champions))  # Crear tantas columnas como campeones
    for i, (index, row) in enumerate(champions.iterrows()):
        # Obtener el color correspondiente al país
        country_color = country_colors.get(row["country"], "#FFFFFF")  # Color predeterminado blanco si no se encuentra en el diccionario

        # Usar HTML para cambiar el color del texto
        champion_name = f"<p style='font-weight: bold; color: {country_color};'>{row['MC']}</p> from <p style='color: {country_color}; font-weight: bold;'>{row['country']}</p>"
        points_text = f"Points: {row['PTS']}"

        with cols[i]:
            st.markdown(champion_name, unsafe_allow_html=True)
            st.markdown(points_text, unsafe_allow_html=True)
            st.markdown("---")  # Separador entre campeones
    
    # Gráfico con formato mejorado
    fig_2 = px.histogram(filtered_table, x='PTB', title='PTB Distribution', template='plotly_dark')
    # Actualizar el estilo de los bins para agregar bordes
    fig_2.update_traces(marker=dict(line=dict(width=1.5, color='black')))
    st.plotly_chart(fig_2, use_container_width=True)
