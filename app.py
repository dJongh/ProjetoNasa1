import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ======================
# 🔧 CONFIGURAÇÃO INICIAL
# ======================
st.set_page_config(page_title="Visualizador de Dados", page_icon="📊", layout="wide")
st.title("📊 Visualizador de Dados TXT ou ZIP")

# Caminho local padrão
arquivo_local = r"C:\Users\diego\Downloads\train_FD001.txt.zip"

# Colunas esperadas (no caso do dataset ZIP)
colunas = [
    'id', 'cycle', 'setting1', 'setting2', 'setting3',
    'sensor1', 'sensor2', 'sensor3', 'sensor4', 'sensor5',
    'sensor6', 'sensor7', 'sensor8', 'sensor9', 'sensor10',
    'sensor11', 'sensor12', 'sensor13', 'sensor14', 'sensor15',
    'sensor16', 'sensor17', 'sensor18', 'sensor19', 'sensor20',
    'sensor21'
]

# =====================================
# 🗂️ UPLOAD DO ARQUIVO PELO USUÁRIO
# =====================================
uploaded_file = st.file_uploader("Carregue um arquivo .txt (ou deixe em branco para usar o padrão ZIP)", type=["txt"])

# =====================================
# 📥 CARREGAMENTO DOS DADOS
# =====================================
try:
    if uploaded_file is not None:
        # Usuário fez upload
        st.info("📁 Lendo arquivo enviado...")
        delimiter = st.selectbox("Selecione o delimitador do arquivo:", [",", ";", "\t", "|"])
        df = pd.read_csv(uploaded_file, delimiter=delimiter)
        origem = "arquivo carregado"
    else:
        # Usa o arquivo ZIP local
        st.info(f"📦 Lendo arquivo local: {arquivo_local}")
        df = pd.read_csv(arquivo_local, sep=r"\s+", header=None, names=colunas, compression="zip")
        origem = "arquivo local ZIP"

    # ==============================
    # 🔍 EXIBIÇÃO DOS DADOS
    # ==============================
    st.success(f"✅ Dados carregados com sucesso a partir do {origem}!")
    st.subheader("📋 Pré-visualização dos dados")
    st.dataframe(df.head())

    st.subheader("📊 Estatísticas descritivas")
    st.write(df.describe())

    # ==============================
    # 📈 GERAÇÃO DE GRÁFICOS
    # ==============================
    st.subheader("📈 Criação de gráficos interativos")

    colunas = df.columns.tolist()
    coluna_x = st.selectbox("Selecione o eixo X", colunas)
    coluna_y = st.selectbox("Selecione o eixo Y", colunas)

    # Gráfico de dispersão
    st.write("### Gráfico de Dispersão")
    fig, ax = plt.subplots()
    ax.scatter(df[coluna_x], df[coluna_y], alpha=0.7)
    ax.set_xlabel(coluna_x)
    ax.set_ylabel(coluna_y)
    st.pyplot(fig)

    # Gráfico de linha
    st.write("### Gráfico de Linha")
    fig, ax = plt.subplots()
    ax.plot(df[coluna_x], df[coluna_y])
    ax.set_xlabel(coluna_x)
    ax.set_ylabel(coluna_y)
    st.pyplot(fig)

    # Gráfico de barras interativo
    st.write("### Gráfico de Barras (interativo e ajustado)")
    grouped_data = df.groupby(coluna_x)[coluna_y].mean().reset_index()
    st.bar_chart(grouped_data, x=coluna_x, y=coluna_y)

except Exception as e:
    st.error(f"❌ Erro ao carregar ou processar o arquivo: {e}")
