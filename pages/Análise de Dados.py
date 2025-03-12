import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import scipy.stats as stats
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression

if "data" not in st.session_state:
    df = pd.read_csv("car_prices.csv")
    st.session_state["data"] = df
    df.drop(["trim", "vin", "seller", "interior", "condition", "state"], axis=1, inplace=True)
    df.rename(columns={
        "year": "Ano",
        "make": "Fabricante",
        "model": "Modelo",
        "body": "Chassi",
        "transmission": "Câmbio",
        "odometer": "Quilometragem",
        "color": "Cor",
        "mmr": "Preço sugerido",
        "sellingprice": "Valor da venda",
        "saledate": "Data da venda"
    }, inplace=True)

    # Converter a coluna de data para formato datetime
# Converter a coluna para datetime, lidando com o formato específico
df["Data da venda"] = pd.to_datetime(df["Data da venda"], errors='coerce', utc=True)

# Remover valores nulos após a conversão
df = df.dropna(subset=["Data da venda"])

# Converter para horário local (opcional, depende do que você precisa)
df["Data da venda"] = df["Data da venda"].dt.tz_convert(None)  
    

# Filtrar os dados para considerar apenas os anos de 2012, 2013 e 2014
df_filtered = df[df["Ano"].isin([2012, 2013, 2014])]

# Filtrar apenas os dados da Ford de 2012 a 2014
df_ford = df[(df["Fabricante"] == "Ford") & (df["Ano"].isin([2012, 2013, 2014]))]

# Calcular o número de vendas por ano
df_vendas_ford = df_ford.groupby("Ano").size().reset_index(name="Quantidade de Vendas")


# Calcular a média de vendas por ano
df_media_vendas_por_ano = df_filtered.groupby("Ano")["Valor da venda"].mean().reset_index()

# Criar o gráfico
fig = px.line(df_media_vendas_por_ano, x="Ano", y="Valor da venda", title="Média de Vendas ao Longo dos Anos (2012-2014)")

# Restringir o eixo x para os anos de 2012 a 2014
fig.update_layout(
    xaxis_title="Ano",
    yaxis_title="Média de Vendas",
    template="plotly_dark",
    xaxis=dict(range=[2012, 2014])  # Restringir o eixo X ao intervalo entre 2012 e 2014
)

df_media_preco_sugerido_por_ano = df_filtered.groupby("Ano")["Preço sugerido"].mean().reset_index()

# Criar o gráfico
fig2 = px.line(df_media_preco_sugerido_por_ano, x="Ano", y="Preço sugerido", title="Média do Preço Sugerido ao Longo dos Anos (2012-2014)")

# Restringir o eixo x para os anos de 2012 a 2014
fig2.update_layout(
    xaxis_title="Ano",
    yaxis_title="Média do Preço Sugerido",
    template="plotly_dark",
    xaxis=dict(range=[2012, 2014])  # Restringir o eixo X ao intervalo entre 2012 e 2014
)

# Agora, ao invés de calcular a média por ano, vamos criar a correlação com os dados completos dos anos filtrados
df_correlacao = df_filtered[['Preço sugerido', 'Valor da venda']]

# Criar o gráfico de correlação (gráfico de dispersão)
fig3 = px.scatter(df_correlacao, x="Preço sugerido", y="Valor da venda", 
                 title="Correlação entre o Preço Sugerido e Valor da Venda",
                 labels={"Preço sugerido": "Preço sugerido", "Valor da venda": "Valor da venda"})

X = df_vendas_ford["Ano"].values.reshape(-1, 1)
y = df_vendas_ford["Quantidade de Vendas"].values

modelo = LinearRegression()
modelo.fit(X, y)

# Prever para os anos de 2015 a 2020
anos_futuros = np.array(range(2015, 2021)).reshape(-1, 1)
previsoes = modelo.predict(anos_futuros)

# Criar DataFrame com previsões
df_previsao = pd.DataFrame({"Ano": anos_futuros.flatten(), "Quantidade de Vendas": previsoes})

# Juntar dados reais e previstos
df_vendas_ford = pd.concat([df_vendas_ford, df_previsao], ignore_index=True)

# Criar gráfico
fig_ford = px.line(df_vendas_ford, x="Ano", y="Quantidade de Vendas", markers=True, title="Previsão de Vendas da Ford")
fig_ford.update_layout(template="plotly_dark")


# Calcular a quantidade de veículos vendidos por fabricante e ano
df_vendas_fabricante = df_filtered.groupby(["Ano", "Fabricante"]).size().reset_index(name="Quantidade de Vendas")

# Criar o gráfico
fig_fabricantes = px.bar(df_vendas_fabricante, 
                         x="Fabricante", 
                         y="Quantidade de Vendas", 
                         color="Ano", 
                         title="Fabricantes que Mais Venderam Veículos de 2012 a 2014",
                         labels={"Quantidade de Vendas": "Quantidade de Vendas", "Fabricante": "Fabricante"},
                         category_orders={"Ano": [2012, 2013, 2014]})

# Atualizar o layout do gráfico
fig_fabricantes.update_layout(
    xaxis_title="Fabricante",
    yaxis_title="Quantidade de Vendas",
    template="plotly_dark",
    xaxis_tickangle=-45
)

data_types = {
    "Ano": ["Variável quantitativa discreta", "Ano em que o veículo foi fabricado"],
    "Fabricante": ["Variável qualitativa nominal", "Marca fabricante do veículo"],
    "Modelo": ["Variável qualitativa nominal", "Modelo do veículo"],
    "Chassi": ["Variável qualitativa nominal", "Tipo do chassi do veículo"],
    "Câmbio": ["Variável qualitativa nominal", "Tipo de câmbio do veículo"],
    "Quilometragem": ["Variável quantitativa contínua", "Quantos quilômetros o odômetro do veículo contava no momento da venda"],
    "Cor": ["Variável qualitativa nominal", "Cor exterior do veículo"],
    "Preço sugerido": ["Variável quantitativa contínua", "FIPE do veículo em dólares"],
    "Valor da venda": ["Variável quantitativa contínua", "Preço pago pelo comprador do veículo em dólares"],
    "Data da venda": ["Variável qualitativa ordinal", "Data em que o veículo foi vendido"]
}
tipos_dados = pd.DataFrame.from_dict(data_types, orient='index', columns=["Tipo de Variável", "Descrição"])
tipos_dados.reset_index(inplace=True)
tipos_dados.rename(columns={"index": "Campo"}, inplace=True)

st.title("Análise de dados")
st.write("Nessa análise responderei trouxe dados de vendas de veículos nos Estados Unidos nos anos 2012-2014")
st.write("A intenção é analizar as tendências do mercado de vendas de automóveis para responder perguntas como:")
st.markdown("- Como a média de vendas mudou ao longo dos anos?")
st.markdown("- Como a média dos preços sugeridos do mercado mudou ao longo dos anos?")
st.markdown("- Quais fabricantes obtiveram o maior sucesso no mercado?")
st.markdown("- É possível prever o crescimento das vendas de uma marca ao longo dos anos apenas com esses dados?")
st.markdown("- E outras perguntas relevantes que descobriremos ao longo da análise")
st.divider()
st.title("0.1 Amostra dos dados")
st.dataframe(df)
st.divider()
st.title('1.0 Tabela de Tipos de Variáveis')
st.dataframe(tipos_dados)
st.divider()
st.header("2.0 Como a média de vendas mudou ao longo dos anos?")
st.plotly_chart(fig)
st.write("O gráfico a seguir considera o número de vendas registradas na base de dados e calcula a média de vendas para cada ano")
st.write("Nota-se que essa média cresce de maneira expressiva ao longo dos anos")
st.write("Essa análise pode ser útil para entender como a demanda por veículos tem crescido")
st.divider()
st.header("3.0 Como a média dos preços sugeridos do mercado mudou ao longo dos anos?")
st.plotly_chart(fig2)
st.write("Esses gráficos possuem uma semelhança notável, o que sugere que possa existir uma correlação entre eles")
st.header("3.1 Correlação entre o preço sugerido e o preço pago pelos consumidores")
st.plotly_chart(fig3)
st.divider()
st.title("4.0 Quais fabricantes obtiveram o maior sucesso no mercado?")
st.header("Fabricantes que Mais Venderam Veículos (2012-2014)")
st.plotly_chart(fig_fabricantes)
st.write("Nota-se que os veículos da fabricante Ford dominaram o mercado durante os anos analisados")
st.write("Isso sugere uma forte demanda popular por carros dessa marca")
st.write("É interessante analizarmos o que esses dados tem a dizer à respeito das vendas dessa marca nos próximos anos")
st.write("Utilizaremos a regressão linear para projetar um gráfico para prever se haverá um aumento nas vendas dos carros da Ford")
st.divider()
st.title("5.0 Previsão de Vendas da Ford")
st.plotly_chart(fig_ford)
st.write("Este gráfico mostra a evolução das vendas da Ford de 2012 a 2014 e a previsão para os anos seguintes usando regressão linear.")
st.write("Com isso podemos afirmar que é um bom negócio comprar os carros da Ford para revender, pois a demanda por esses carros tende a aumentar")
st.divider()
st.title("6.0 Aplicando distribuição para analizar os dados ")
st.divider()
def plot_normal_distribution(data, column_name):
    media = data.mean()
    desvio_padrao = data.std()
    
    x = np.linspace(min(data), min(60000, max(data)), 100)  # Limitando o eixo X a 60.000
    y = stats.norm.pdf(x, media, desvio_padrao)
    
    fig, ax = plt.subplots()
    ax.hist(data, bins=30, density=True, alpha=0.6, color='g', label='Histograma')
    ax.plot(x, y, label='Distribuição Normal', color='r', linewidth=2)
    
    ax.set_title(f"Histograma e Ajuste de Distribuição Normal para {column_name}")
    ax.set_xlabel(column_name)
    ax.set_ylabel("Densidade")
    ax.legend()
    
    ax.set_xlim(min(data), 60000)  # Definir os limites do eixo X

    st.pyplot(fig)

st.title("6.1 Análise de Distribuição Normal dos Preços de Venda")
plot_normal_distribution(df["Valor da venda"], "Valor da venda")
st.divider()
st.title("6.2 Análise da Distribuição de Poisson das Vendas Diárias")
df_vendas_diarias = df["Data da venda"].dt.date.value_counts().reset_index()
df_vendas_diarias.columns = ["Data", "Quantidade de Vendas"]
lambda_poisson = df_vendas_diarias["Quantidade de Vendas"].mean()
dias = np.arange(0, 50)  # Limitando o intervalo de 0 a 100
poisson_dist = stats.poisson.pmf(dias, lambda_poisson)
st.write("Podemos aplicar uma distribuição de Poisson para verificar a probabilidade de vendas diárias dos carros da marca Ford")
fig, ax = plt.subplots()
ax.hist(df_vendas_diarias["Quantidade de Vendas"], bins=range(0, 50, 5), density=True, alpha=0.6, color='g', label='Histograma')
ax.plot(dias, poisson_dist, marker='o', linestyle='None', color='r', label='Distribuição de Poisson')
ax.set_title("Distribuição de Poisson das Vendas Diárias")
ax.set_xlabel("Quantidade de Vendas por Dia")
ax.set_ylabel("Probabilidade")
ax.legend()
st.pyplot(fig)