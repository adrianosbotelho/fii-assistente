import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# ---------------- CONFIGURAÇÃO DA PÁGINA ----------------
st.set_page_config(
    page_title="FII Assistente | Dashboard Profissional",
    page_icon="📊",
    layout="wide"
)

# ---------------- FUNÇÕES AUXILIARES ----------------
def format_brl(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

# ---------------- DADOS MOCK (DEPOIS TROCAMOS PELOS REAIS) ----------------
datas = pd.date_range(start="2024-01-01", periods=24, freq="M")
patrimonio = np.cumsum(np.random.randint(600, 900, size=24)) + 70000
proventos = np.random.randint(600, 900, size=24)

df = pd.DataFrame({
    "Data": datas,
    "Patrimônio": patrimonio,
    "Proventos": proventos
})

# ---------------- TOPO / KPIs ----------------
st.markdown("## 📊 Dashboard de FIIs – Visão Geral")

col1, col2, col3, col4 = st.columns(4)

col1.metric("💰 Patrimônio Atual", format_brl(df["Patrimônio"].iloc[-1]), "+3,2%")
col2.metric("📥 Proventos Mensais", format_brl(df["Proventos"].iloc[-1]), "+1,8%")
col3.metric("📈 Proventos Anuais", format_brl(df["Proventos"].sum()))
col4.metric("🎯 Yield Médio", "0,87% a.m.")

st.markdown("---")

# ---------------- GRÁFICO PATRIMÔNIO ----------------
fig_patrimonio = go.Figure()

fig_patrimonio.add_trace(
    go.Scatter(
        x=df["Data"],
        y=df["Patrimônio"],
        mode="lines+markers",
        line=dict(color="#00E5FF", width=3),
        marker=dict(size=6),
        fill="tozeroy",
        fillcolor="rgba(0,229,255,0.15)",
        name="Patrimônio"
    )
)

fig_patrimonio.update_layout(
    title="📈 Evolução do Patrimônio",
    template="plotly_dark",
    height=420,
    margin=dict(l=40, r=40, t=60, b=40),
    yaxis=dict(tickprefix="R$ ", separatethousands=True),
    hovermode="x unified"
)

# ---------------- GRÁFICO PROVENTOS ----------------
fig_proventos = go.Figure()

fig_proventos.add_trace(
    go.Bar(
        x=df["Data"],
        y=df["Proventos"],
        marker_color="#00C853",
        name="Proventos"
    )
)

fig_proventos.update_layout(
    title="📥 Proventos Mensais",
    template="plotly_dark",
    height=420,
    margin=dict(l=40, r=40, t=60, b=40),
    yaxis=dict(tickprefix="R$ ", separatethousands=True),
)

# ---------------- LAYOUT DOS GRÁFICOS ----------------
col_g1, col_g2 = st.columns(2)

with col_g1:
    st.plotly_chart(fig_patrimonio, width="stretch")

with col_g2:
    st.plotly_chart(fig_proventos, width="stretch")

# ---------------- PROJEÇÃO ----------------
st.markdown("---")
st.markdown("## 🔮 Projeção de Patrimônio (12 meses)")

crescimento_medio = df["Proventos"].mean()
projecao = []

ultimo = df["Patrimônio"].iloc[-1]
for i in range(12):
    ultimo += crescimento_medio
    projecao.append(ultimo)

datas_proj = pd.date_range(start=df["Data"].iloc[-1], periods=12, freq="M")

fig_proj = go.Figure()

fig_proj.add_trace(
    go.Scatter(
        x=datas_proj,
        y=projecao,
        mode="lines+markers",
        line=dict(color="#FFD600", dash="dash", width=3),
        marker=dict(size=6),
        name="Projeção"
    )
)

fig_proj.update_layout(
    template="plotly_dark",
    height=420,
    yaxis=dict(tickprefix="R$ ", separatethousands=True),
    hovermode="x unified"
)

st.plotly_chart(fig_proj, width="stretch")
