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

# Normaliza nomes: remove espaços, minúsculo
df.columns = (
    df.columns
    .str.strip()
    .str.lower()
)

# ===============================
# MAPA DE COLUNAS ACEITAS
# ===============================
COLUMN_ALIASES = {
    "quantidade": ["quantidade", "qtd", "cotas"],
    "preco_medio": ["preco_medio", "preço_médio", "preco medio", "pm"],
    "dividendo_mensal": ["dividendo_mensal", "dividendo", "rendimento", "dy_mensal"],
    "ticker": ["ticker", "ativo", "codigo", "fii"]
}

def resolve_column(df, aliases):
    for col in aliases:
        if col in df.columns:
            return col
    return None

col_quantidade = resolve_column(df, COLUMN_ALIASES["quantidade"])
col_preco = resolve_column(df, COLUMN_ALIASES["preco_medio"])
col_dividendo = resolve_column(df, COLUMN_ALIASES["dividendo_mensal"])
col_ticker = resolve_column(df, COLUMN_ALIASES["ticker"])

missing = []
if not col_quantidade:
    missing.append("Quantidade")
if not col_preco:
    missing.append("Preço Médio")
if not col_dividendo:
    missing.append("Dividendo Mensal")
if not col_ticker:
    missing.append("Ticker")

if missing:
    st.error(
        "❌ O CSV não contém as colunas obrigatórias:\n\n"
        + "\n".join(f"- {m}" for m in missing)
    )
    st.info(
        "💡 Dica: colunas aceitas:\n"
        "- Quantidade: quantidade, qtd, cotas\n"
        "- Preço médio: preco_medio, pm\n"
        "- Dividendo: dividendo, rendimento\n"
        "- Ticker: ticker, ativo, fii"
    )
    st.stop()

# ===============================
# PADRONIZA DATAFRAME
# ===============================
df = df.rename(columns={
    col_quantidade: "Quantidade",
    col_preco: "Preco_Medio",
    col_dividendo: "Dividendo_Mensal",
    col_ticker: "Ticker"
})

# ===============================
# CÁLCULOS
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
# KPIs
# ===============================
col1, col2, col3, col4 = st.columns(4)

def brl(v):
    return f"R$ {v:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

col1.metric("💰 Patrimônio Total", brl(patrimonio_total))
col2.metric("📥 Renda Mensal", brl(renda_mensal_total))
col3.metric("📈 Yield Mensal", f"{yield_mensal:.2f}%")
col4.metric("📅 Renda Anual Projetada", brl(renda_anual))

st.divider()

# ===============================
# TABELA
# ===============================
st.subheader("📋 Detalhamento da Carteira")

df_display = df.copy()
df_display["Valor_Investido"] = df_display["Valor_Investido"].apply(brl)
df_display["Renda_Mensal"] = df_display["Renda_Mensal"].apply(brl)

st.dataframe(
    df_display[
        ["Ticker", "Quantidade", "Preco_Medio", "Dividendo_Mensal", "Valor_Investido", "Renda_Mensal"]
    ],
    use_container_width=True,
    hide_index=True
)
