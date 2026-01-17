import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------
st.set_page_config(
    page_title="FII Assistente",
    layout="wide",
    initial_sidebar_state="expanded"
)

# -------------------------------------------------
# SIDEBAR - IMPORTAÇÃO CSV
# -------------------------------------------------
st.sidebar.title("📂 Importar Carteira")
uploaded_file = st.sidebar.file_uploader(
    "Importe o CSV da sua carteira",
    type=["csv"]
)

# -------------------------------------------------
# TÍTULO PRINCIPAL
# -------------------------------------------------
st.title("📊 FII Assistente – Visão Geral da Carteira")

# -------------------------------------------------
# CARREGAMENTO DO CSV
# -------------------------------------------------
if uploaded_file is None:
    st.info("⬅️ Importe um arquivo CSV para visualizar sua carteira.")
    st.stop()

df = pd.read_csv(uploaded_file)

# -------------------------------------------------
# VALIDAÇÃO DE COLUNAS
# -------------------------------------------------
colunas_esperadas = [
    "Ticker",
    "Quantidade",
    "Preco_Medio",
    "Dividendo_Mensal"
]

for col in colunas_esperadas:
    if col not in df.columns:
        st.error(f"Coluna obrigatória ausente no CSV: {col}")
        st.stop()

# -------------------------------------------------
# NORMALIZAÇÃO E CÁLCULOS
# -------------------------------------------------
df["Quantidade"] = df["Quantidade"].astype(float)
df["Preco_Medio"] = df["Preco_Medio"].astype(float)
df["Dividendo_Mensal"] = df["Dividendo_Mensal"].astype(float)

df["Valor_Investido"] = df["Quantidade"] * df["Preco_Medio"]
df["Renda_Mensal"] = df["Quantidade"] * df["Dividendo_Mensal"]
df["Yield_Mensal"] = df["Renda_Mensal"] / df["Valor_Investido"]

patrimonio_total = df["Valor_Investido"].sum()
renda_mensal_total = df["Renda_Mensal"].sum()
yield_mensal_total = renda_mensal_total / patrimonio_total
renda_anual_projetada = renda_mensal_total * 12

# -------------------------------------------------
# CARDS EXECUTIVOS
# -------------------------------------------------
col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Patrimônio Total", f"R$ {patrimonio_total:,.2f}")
col2.metric("📥 Renda Mensal", f"R$ {renda_mensal_total:,.2f}")
col3.metric("📈 Yield Mensal", f"{yield_mensal_total*100:.2f}%")
col4.metric("📆 Renda Anual Projetada", f"R$ {renda_anual_projetada:,.2f}")

st.divider()

# -------------------------------------------------
# GRÁFICO - ALOCAÇÃO DA CARTEIRA
# -------------------------------------------------
fig_alocacao = px.pie(
    df,
    names="Ticker",
    values="Valor_Investido",
    hole=0.45,
    title="Alocação da Carteira (%)"
)

st.plotly_chart(fig_alocacao, use_container_width=True)

# -------------------------------------------------
# GRÁFICOS EM GRID
# -------------------------------------------------
col_g1, col_g2 = st.columns(2)

# Renda mensal por FII
fig_renda = px.bar(
    df,
    x="Ticker",
    y="Renda_Mensal",
    title="Renda Mensal por FII",
    text_auto=".2f"
)

fig_renda.update_layout(
    yaxis_title="R$ / mês",
    xaxis_title="FII"
)

col_g1.plotly_chart(fig_renda, use_container_width=True)

# Yield por FII
fig_yield = px.bar(
    df,
    x="Ticker",
    y="Yield_Mensal",
    title="Yield Mensal por FII",
    text_auto=".2%"
)

fig_yield.update_layout(
    yaxis_title="Yield (%)",
    xaxis_title="FII"
)

col_g2.plotly_chart(fig_yield, use_container_width=True)

# -------------------------------------------------
# PROJEÇÃO DE RENDA (12 MESES)
# -------------------------------------------------
meses = pd.date_range(
    start=datetime.today(),
    periods=12,
    freq="ME"
)

df_proj = pd.DataFrame({
    "Mes": meses,
    "Renda_Projetada": [renda_mensal_total] * 12
})

fig_proj = px.line(
    df_proj,
    x="Mes",
    y="Renda_Projetada",
    title="Projeção de Renda Mensal – 12 Meses"
)

st.plotly_chart(fig_proj, use_container_width=True)

st.divider()

# -------------------------------------------------
# TABELA DETALHADA
# -------------------------------------------------
st.subheader("📋 Detalhamento da Carteira")

df_exibicao = df.copy()
df_exibicao["Yield_Mensal (%)"] = df_exibicao["Yield_Mensal"] * 100

st.dataframe(
    df_exibicao[[
        "Ticker",
        "Quantidade",
        "Preco_Medio",
        "Dividendo_Mensal",
        "Valor_Investido",
        "Renda_Mensal",
        "Yield_Mensal (%)"
    ]],
    use_container_width=True
)
