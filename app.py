import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ================= CONFIG =================
st.set_page_config(
    page_title="FII Assistente",
    layout="wide",
    page_icon="📊"
)

st.title("📊 FII Assistente — Dashboard de Renda Real")

# ================= FUNÇÕES =================
def brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ================= DADOS DA CARTEIRA =================
df = pd.read_csv("carteira.csv")

df["renda_mensal"] = df["quantidade"] * df["provento_mensal"]
renda_total = df["renda_mensal"].sum()

# ================= KPIs =================
col1, col2, col3 = st.columns(3)

col1.metric("💰 Renda Mensal Atual", brl(renda_total))
col2.metric("📆 Renda Anual", brl(renda_total * 12))
col3.metric("📦 Nº de FIIs", len(df))

st.markdown("---")

# ================= TABELA DETALHADA =================
st.subheader("📋 Detalhamento da Carteira")

df_show = df.copy()
df_show["renda_mensal"] = df_show["renda_mensal"].apply(brl)
df_show["provento_mensal"] = df_show["provento_mensal"].apply(brl)

st.dataframe(df_show, use_container_width=True)

# ================= GRÁFICO RENDA POR FII =================
fig = go.Figure()

fig.add_trace(
    go.Bar(
        x=df["ticker"],
        y=df["renda_mensal"],
        marker_color="#00E5FF",
        text=[brl(v) for v in df["renda_mensal"]],
        textposition="auto"
    )
)

fig.update_layout(
    title="📊 Renda Mensal por FII",
    template="plotly_dark",
    yaxis=dict(tickprefix="R$ ", separatethousands=True),
    height=420
)

st.plotly_chart(fig, width="stretch")

# ================= PROJEÇÃO =================
st.markdown("---")
st.subheader("🔮 Projeção com Reinvestimento (Conservador)")

meses = st.slider("Horizonte (meses)", 6, 120, 36)

renda = renda_total
projecao = []

for _ in range(meses):
    projecao.append(renda)
    renda += renda * 0.01  # crescimento conservador (1% ao mês)

fig_proj = go.Figure()

fig_proj.add_trace(
    go.Scatter(
        y=projecao,
        mode="lines+markers",
        line=dict(color="#00C853", width=3),
        name="Renda Projetada"
    )
)

fig_proj.update_layout(
    title="📈 Projeção de Renda Mensal",
    template="plotly_dark",
    yaxis=dict(tickprefix="R$ ", separatethousands=True),
    height=420
)

st.plotly_chart(fig_proj, width="stretch")
