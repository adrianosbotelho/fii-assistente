import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================
# CONFIGURAÇÃO GERAL
# =========================
st.set_page_config(
    page_title="FII Assistente – Dashboard Profissional",
    layout="wide",
    initial_sidebar_state="collapsed"
)

st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
    }
    .metric-label {
        font-size: 14px;
        color: #aaaaaa;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# DADOS DA CARTEIRA (BASE REAL)
# =========================
valor_carteira = 73681.72
renda_mensal_atual = 720.00
dy_mensal = renda_mensal_atual / valor_carteira
meta_renda = 1000

# =========================
# CONTROLES
# =========================
st.title("📊 FII Assistente — Plataforma Profissional")

aba = st.tabs(["📌 Visão Geral", "📈 Projeções", "⚖️ Comparativos", "🧠 Insight IA"])

# =========================
# 📌 VISÃO GERAL
# =========================
with aba[0]:
    col1, col2, col3, col4 = st.columns(4)

    col1.metric("💼 Patrimônio", f"R$ {valor_carteira:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col2.metric("💸 Renda Mensal", f"R$ {renda_mensal_atual:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
    col3.metric("📈 Yield Mensal", f"{dy_mensal*100:.2f}%")
    col4.metric("🎯 Meta", f"R$ {meta_renda:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))

    st.divider()

    st.subheader("📌 Diagnóstico Rápido")
    st.write(
        """
        • Carteira bem posicionada para crescimento orgânico  
        • Reinvestimento tem impacto direto na aceleração da renda  
        • Concentração saudável entre papel e tijolo  
        """
    )

# =========================
# 📈 PROJEÇÕES
# =========================
with aba[1]:
    horizonte = st.slider("Horizonte de projeção (meses)", 6, 60, 36)

    meses = np.arange(0, horizonte + 1)
    renda_sem_reinvest = np.full(len(meses), renda_mensal_atual)

    renda_com_reinvest = []
    renda = renda_mensal_atual
    for _ in meses:
        renda_com_reinvest.append(renda)
        renda += renda * dy_mensal

    fig = go.Figure()

    fig.add_trace(go.Scatter(
        x=meses,
        y=renda_com_reinvest,
        mode="lines+markers",
        name="Com Reinvestimento",
        line=dict(color="#00ff88", width=3)
    ))

    fig.add_trace(go.Scatter(
        x=meses,
        y=renda_sem_reinvest,
        mode="lines",
        name="Sem Reinvestimento",
        line=dict(color="#ff4d4d", width=2, dash="dash")
    ))

    fig.add_hline(
        y=meta_renda,
        line_dash="dot",
        line_color="gold",
        annotation_text="Meta R$ 1.000",
        annotation_position="top left"
    )

    fig.update_layout(
        template="plotly_dark",
        title="📈 Projeção de Renda Mensal (R$)",
        xaxis_title="Meses",
        yaxis_title="Renda Mensal (R$)",
        yaxis_tickprefix="R$ ",
        height=500,
        legend=dict(orientation="h", y=-0.2)
    )

    st.plotly_chart(fig, use_container_width=True)

# =========================
# ⚖️ COMPARATIVOS
# =========================
with aba[2]:
    meses = np.arange(0, 36)

    carteira = valor_carteira * (1 + dy_mensal) ** meses
    cdi = valor_carteira * (1 + 0.009) ** meses  # CDI ~0,9% a.m
    ifix = valor_carteira * (1 + 0.006) ** meses

    fig2 = go.Figure()

    fig2.add_trace(go.Scatter(x=meses, y=carteira, name="Carteira FIIs", line=dict(width=3)))
    fig2.add_trace(go.Scatter(x=meses, y=cdi, name="CDI", line=dict(dash="dot")))
    fig2.add_trace(go.Scatter(x=meses, y=ifix, name="IFIX", line=dict(dash="dash")))

    fig2.update_layout(
        template="plotly_dark",
        title="⚖️ Crescimento do Patrimônio (R$)",
        xaxis_title="Meses",
        yaxis_title="Valor (R$)",
        yaxis_tickprefix="R$ ",
        height=500
    )

    st.plotly_chart(fig2, use_container_width=True)

# =========================
# 🧠 INSIGHT IA
# =========================
with aba[3]:
    meses_meta = 0
    renda_temp = renda_mensal_atual
    while renda_temp < meta_renda:
        renda_temp += renda_temp * dy_mensal
        meses_meta += 1

    st.subheader("🧠 Insights Inteligentes")

    st.markdown(
        f"""
        ✅ **Meta de R$ {meta_renda:,.2f} atingida em aproximadamente {meses_meta} meses**  
        ✅ **Reinvestimento acelera a renda em ~{int((meta_renda/renda_mensal_atual-1)*100)}% no longo prazo**  
        ⚠️ **Sem reinvestir, sua renda ficaria estagnada**  
        💡 **Cada R$ 100 reinvestido hoje gera efeito composto permanente**
        """.replace(",", "X").replace(".", ",").replace("X", ".")
    )

    st.info("📌 Próximo upgrade: alertas automáticos + leitura de fatos relevantes + recomendação mensal de reinvestimento.")

# =========================
# RODAPÉ
# =========================
st.divider()
st.caption("FII Assistente • Dashboard profissional • Uso pessoal")
