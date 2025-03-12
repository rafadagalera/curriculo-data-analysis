import streamlit as st
import pandas as pd
import numpy as np

st.set_page_config(page_title="Formação e experiências", layout="wide")

st.title("Minha formação e experiências profissionais")

st.write("Estou cursando o quarto semestre de Engenharia de Software na FIAP")

st.write("Em colaboração com meus colegas de faculdade, desenvolvi projetos para diversas empresas parceiras da FIAP")

st.title("Saiba mais:")

st.header("Projeto em parceria com a Ocean20")
st.write("Nesse projeto, exploramos a possibilidade do uso de sensores metereológicos para a previsão de chuvas e tempestades em áreas urbanas com o intuito de identificar os dias ótimos para realizar a coleta de lixo, evitando assim que os ventos e a água da chuva carreguem o lixo para os rios e oceanos.")
st.write("https://github.com/rafadagalera/wave.clear")

st.header("Projeto em parceria com o Hospital das Clínicas")
st.write("Nesse projeto, implementamos a cultura da gameficação para atrair a atenção dos pacientes do Icr, a divisão pediátrica do Hospital das Clínicas com o intuito de espalhar informações sobre os processos hospitalares de maneira lúdica e interativa, visando um maior engajamento com as crianças.")
st.write("https://github.com/rafadagalera/Amigos-da-Saude")

st.divider()
st.title("Formações")
st.write("Aqui estão alguns certificados de cursos que concluí ao longo de minha jornada profissional")

st.image("certificado1.png", width= 400)
st.image("certificado2.png", width= 400)