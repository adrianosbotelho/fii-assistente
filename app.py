import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="FII Assistente",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 FII Assistente – Visão Geral da Carteira")

# ===============================
# SIDEBAR – IMPORTAÇÃO CSV
# ===============================
st.sidebar.header("📁 Importar Carteira")

uploaded_file = st.sidebar.file_uploader(
    "Importe o CSV da sua carteira",
    type=["csv"]
)

if uploaded_file is None:
    st.info("👉 Importe um arquivo CSV para visualizar sua carteira.")
    st.stop()

# ===============================
# LEITURA DO CSV
# ===============================
df = pd.read_csv(uploaded_file)

# Esperado no CSV:
# Ticker | Quantidade | Preco_Medio | Dividendo_Mensal

df.columns = [c.strip() for c in df.columns]

# ===============================
# CÁLCULOS DA CARTEIRA
# ===============================
df["Valor_Investido"] = df["Quantidade"] * df["Preco_Medio"]
df["Renda_Mensal"] = df["Quantidade"] * df["Dividendo_Mensal"]

patrimonio_total = df["Valor_Investido"].sum()
renda_mensal_total = df["Renda_Mensal"].sum()
renda_anual = renda_mensal_total * 12

yield_mensal = (
    (renda_mensal_total / patrimonio_total) * 100
    if patrimonio_total > 0 else 0
)

# ===============================
# KPIs – CARDS SUPERIORES
# ===============================
col1, col2, col3, col4 = st.columns(4)

col1.metric(
    "💰 Patrimônio Total",
    f"R$ {patrimonio_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

col2.metric(
    "📥 Renda Mensal",
    f"R$ {renda_mensal_total:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

col3.metric(
    "📈 Yield Mensal",
    f"{yield_mensal:.2f}%"
)

col4.metric(
    "📅 Renda Anual Projetada",
    f"R$ {renda_anual:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

st.divider()

# ===============================
# TABELA DA CARTEIRA
# ===============================
st.subheader("📋 Detalhamento da Carteira")

df_display = df.copy()
df_display["Valor_Investido"] = df_display["Valor_Investido"].map(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)
df_display["Renda_Mensal"] = df_display["Renda_Mensal"].map(
    lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")
)

st.dataframe(
    df_display,
    use_container_width=True,
    hide_index=True
)
