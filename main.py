import streamlit as st
from scripts.utils import load_data
import plotly.express as px

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
    fig_0 = px.bar(filtered_table, x='PTB', y='MC', color='country', title='PTB by MC and Country')
    st.subheader("Top 5 MC's with the most PTB")
    st.dataframe(filtered_table[["MC", "PTB", "country", "BG", "PTS"]].sort_values(by='PTB', ascending=False).head(5))
    st.plotly_chart(fig_0)
with box_cols[1]:
    fig_1 = px.box(filtered_table, x='country', y='PTB', title='PTB by Country')
    
    st.plotly_chart(fig_1)
with box_cols[2]:
    fig_2 = px.histogram(filtered_table, x='PTB', title='PTB Distribution', template='plotly_dark')
    st.plotly_chart(fig_2)