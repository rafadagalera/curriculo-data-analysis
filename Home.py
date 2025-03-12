import streamlit as st
import pandas as pd
import numpy as np
# from streamlit_extras.app_logo import add_logo

# Configuração da página
st.set_page_config(page_title="Quem sou eu", layout="wide")
st.title("Olá! Meu nome é Rafael Nascimento")
st.write("Sou um estudante de Engenharia de Software apaixonado pela tecnologia.")

st.header("Um pouco sobre mim")
st.divider()
col1, col2, col3 = st.columns(3)
with col1:
    st.markdown("Hobbies")
    st.write("- Música")
    st.write("- Xadrez")
    st.write("- Futebol")
    st.write("- Jogos de estratégia")
    st.write("- Poker")
with col2:
    st.markdown("Áreas de interesse")
    st.write("- Análise de dados")
    st.write("- Desenvolvimento de scripts de automação")
    st.write("- Construir controladores MIDI customizáveis")
with col3:
    st.markdown("Infos de contato")
    st.write("- E-mail: dagalera.dev@gmail.com")
    st.write("- LinkedIn: https://www.linkedin.com/in/devdagalera/")
    st.write("- Github: https://github.com/rafadagalera")
    st.write("- Telefone: (11)97970 2758")

