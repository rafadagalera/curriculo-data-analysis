import streamlit as st
import pandas as pd
import numpy as np

st.title("Skills")
st.write("Ao longo da minha jornada profissional, desenvolvi as seguintes habilidades relevantes ao mercado de trabalho:")
st.divider()
col1, col2 = st.columns(2)

with col1:
    st.header("Soft skills")
    st.write("Comunicação")
    st.write("Trabalho em equipe")
    st.write("Resolução de problemas")
    st.write("Raciocínio lógico")
    st.write("Metodologia Agile")
with col2:
    st.header("Hard skills")
    st.write("Python")
    st.write("Java")
    st.write("JavaScript")
    st.write("SQL")
    st.write("Excel")
    st.write("HTML/CSS")
    st.write("Bootstrap")
    st.write("Tailwind CSS")
    st.write("Sass")
    st.write("React")
    st.write("Análise de dados")
    st.write("Microcontroladores Arduino/ESP32")

