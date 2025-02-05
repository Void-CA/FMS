import streamlit as st
import pandas as pd
import scripts.utils as utils

utils.configure_page()

matches = utils.load_data("Matches")
st.title("Enfrentamientos")
for year, matrix in matches.items():
    st.markdown(f"## {year}")
    st.write(matrix[1])