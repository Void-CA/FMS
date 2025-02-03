import streamlit as st
from scripts.utils import load_data, plot_bar_chart, plot_box_chart, display_champions, configure_page
import plotly.express as px  

configure_page()

final_table = load_data("FMS").query("year != '2023A' or country != 'COL'")
final_table["year"] = final_table["year"].replace({"2023A": "2023", "2023B": "2023"})
years = sorted(final_table["year"].unique())

# Título y bienvenida
st.title('Freestyle Master Series')
st.write('Welcome to the Freestyle Master Series! This is a simple web app that allows you see the FMS historical statistics.')

# Selección de año y filtrado de datos
selected_year = st.selectbox('Select a year:', years)
filtered_table = final_table[final_table["year"] == selected_year].sort_values(by='PTB', ascending=True)

# Definición de columnas para los tres gráficos
box_cols = st.columns(3)

# Top 5 MC's
with box_cols[0]:
    st.subheader("Top 5 MC's with the most PTB")
    st.dataframe(filtered_table[["MC", "PTB", "country", "BG", "PTS"]].sort_values(by='PTB', ascending=False).head(5))
    st.plotly_chart(plot_bar_chart(filtered_table, 'PTB', 'MC', 'PTB by MC and Country'))

# Gráfico de PTB por país
with box_cols[1]:
    st.plotly_chart(plot_box_chart(filtered_table, 'country', 'PTB', 'PTB by Country'))
    st.subheader("Top Countries with the most PTB")
    top_5 = filtered_table.groupby('country')['PTB'].sum().sort_values(ascending=False).head(5)
    for country, ptb in top_5.items():
        i = top_5.index.get_loc(country) + 1
        st.latex(f'\t{i}.\\quad {country}: {ptb}')

# Campeones del año
with box_cols[2]:
    st.subheader("Champions of the Year")
    display_champions(filtered_table)
    fig_2 = px.histogram(filtered_table, x='PTB', title='PTB Distribution', template='plotly_dark')
    fig_2.update_traces(marker=dict(line=dict(width=1.5, color='black')))
    st.plotly_chart(fig_2, use_container_width=True)
