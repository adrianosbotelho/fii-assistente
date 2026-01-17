import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go

st.set_page_config(page_title="FII Assistente", layout="wide")

st.title("📊 FII Assistente — Dashboard Profissional")

# =========================
# Dados simulados
# =========================
datas = pd.date_range(start="2024-01-01", periods=24, freq="ME")
proventos = np.cumsum(np.random.uniform(500, 900, size=len(datas)))
patrimonio = 70000 + np.cumsum(np.random.uniform(-500, 1200, size=len(datas)))

df = pd.DataFrame({
    "Data": datas,
    "Proventos Acumulados": proventos,
    "Patrimônio": patrimonio
})

# =========================
# Gráfico de Proventos
# =========================
fig_prov = go.Figure()
fig_prov.add_trace(go.Scatter(
    x=df["Data"],
    y=df["Proventos Acumulados"],
    mode="lines+markers",
    name="Proventos"
))

fig_prov.update_layout(
    title="Evolução dos Proventos",
    xaxis_title="Data",
    yaxis_title="R$",
    template="plotly_white"
)

# =========================
# Gráfico de Patrimônio
# =========================
fig_patr = go.Figure()
fig_patr.add_trace(go.Scatter(
    x=df["Data"],
    y=df["Patrimônio"],
    mode="lines+markers",
    name="Patrimônio"
))

fig_patr.update_layout(
    title="Evolução do Patrimônio",
    xaxis_title="Data",
    yaxis_title="R$",
    template="plotly_white"
)

# =========================
# Layout
# =========================
col1, col2 = st.columns(2)

with col1:
    st.plotly_chart(fig_prov, width="stretch")

with col2:
    st.plotly_chart(fig_patr, width="stretch")

st.markdown("---")
st.success("Aplicação estável e pronta para evolução 🚀")
