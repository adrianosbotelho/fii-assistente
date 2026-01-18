import streamlit as st
import pandas as pd
import plotly.express as px
from datetime import datetime

# -------------------------------------------------
# CONFIGURAÇÃO
# -------------------------------------------------
st.set_page_config(
    page_title="FII Assistente",
    layout="wide"
)

st.title("📊 FII Assistente – Visão Geral da Carteira")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.header("📂 Importar Carteira")
uploaded_file = st.sidebar.file_uploader(
    "Importe o CSV da sua carteira",
    type=["csv"]
)

horizonte = st.sidebar.slider(
    "Horizonte de Projeção (meses)",
    min_value=12,
    max_value=60,
    value=24
)

# -------------------------------------------------
# LOAD CSV
# -------------------------------------------------
if uploaded_file is None:
    st.info("⬅️ Importe um arquivo CSV para começar.")
    st.stop()

df = pd.read_csv(uploaded_file)

# -------------------------------------------------
# VALIDAÇÃO
# -------------------------------------------------
cols = ["Ticker", "Quantidade", "Preco_Medio", "Dividendo_Mensal"]
for c in cols:
    if c not in df.columns:
        st.error(f"Coluna obrigatória ausente: {c}")
        st.stop()

df[cols[1:]] = df[cols[1:]].astype(float)

# -------------------------------------------------
# CÁLCULOS BASE
# -------------------------------------------------
df["Valor_Investido"] = df["Quantidade"] * df["Preco_Medio"]
df["Renda_Mensal"] = df["Quantidade"] * df["Dividendo_Mensal"]
df["Yield_Mensal"] = df["Renda_Mensal"] / df["Valor_Investido"]

patrimonio = df["Valor_Investido"].sum()
renda_mensal = df["Renda_Mensal"].sum()
yield_medio = renda_mensal / patrimonio

# -------------------------------------------------
# CARDS
# -------------------------------------------------
c1, c2, c3, c4 = st.columns(4)

c1.metric("💰 Patrimônio", f"R$ {patrimonio:,.2f}")
c2.metric("📥 Renda Mensal", f"R$ {renda_mensal:,.2f}")
c3.metric("📈 Yield Médio", f"{yield_medio*100:.2f}%")
c4.metric("📆 Renda Anual", f"R$ {renda_mensal*12:,.2f}")

st.divider()

# -------------------------------------------------
# PROJEÇÃO COM REINVESTIMENTO
# -------------------------------------------------
meses = []
rendas = []
patrimonios = []

pat = patrimonio
renda = renda_mensal

for i in range(horizonte):
    meses.append(i + 1)
    rendas.append(renda)
    patrimonios.append(pat)

    pat = pat + renda
    renda = pat * yield_medio

df_proj = pd.DataFrame({
    "Mês": meses,
    "Renda Mensal Projetada": rendas,
    "Patrimônio Projetado": patrimonios
})

fig_proj = px.line(
    df_proj,
    x="Mês",
    y="Renda Mensal Projetada",
    title="📈 Projeção de Renda Mensal com Reinvestimento",
    markers=True
)

fig_proj.update_layout(
    yaxis_title="R$",
    xaxis_title="Meses"
)

st.plotly_chart(fig_proj, use_container_width=True)

st.divider()

# -------------------------------------------------
# ALOCAÇÃO
# -------------------------------------------------
fig_pie = px.pie(
    df,
    names="Ticker",
    values="Valor_Investido",
    hole=0.45,
    title="Alocação da Carteira"
)

st.plotly_chart(fig_pie, use_container_width=True)

st.divider()

# -------------------------------------------------
# TABELA
# -------------------------------------------------
st.subheader("📋 Detalhamento da Carteira")

df_view = df.copy()
df_view["Yield (%)"] = df_view["Yield_Mensal"] * 100

st.dataframe(
    df_view[[
        "Ticker",
        "Quantidade",
        "Preco_Medio",
        "Dividendo_Mensal",
        "Valor_Investido",
        "Renda_Mensal",
        "Yield (%)"
    ]],
    use_container_width=True
)
