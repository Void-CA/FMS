import streamlit as st
from data_processor import final_table

st.title('Freestyle Master Series')
st.write('Welcome to the Freestyle Master Series! This is a simple web app that allows you see the FMS historical statistics.')
st.table(final_table.head(10))