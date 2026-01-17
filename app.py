import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# -------------------------------------------------
# CONFIGURAÇÃO DA PÁGINA
# -------------------------------------------------
st.set_page_config(
    page_title="FII Assistente",
    page_icon="📊",
    layout="wide"
)

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.markdown(
    """
    ## 📊 FII Assistente

    Plataforma profissional para análise de FIIs.

    **Funcionalidades:**
    - Diagnóstico de carteira
    - Projeção de renda
    - Dashboard visual
    - Reinvestimento inteligente

    ---
    **Origem da carteira**
    """
)

origem = st.sidebar.radio(
    "Como deseja importar sua carteira?",
    [
        "Manual",
        "CSV",
        "Integração B3",
        "Investidor10"
    ]
)

st.sidebar.markdown("---")
st.sidebar.caption("© 2026 • FII Assistente")

# -------------------------------------------------
# DADOS (EXEMPLO)
# -------------------------------------------------
dados = {
    "FII": ["BTLG11", "KNCR11", "VISC11", "MXRF11"],
    "Valor Investido": [10462, 8765, 9795, 7096],
    "Renda Mensal": [80, 100, 75, 85]
}

df = pd.DataFrame(dados)

total_investido = df["Valor Investido"].sum()
renda_mensal = df["Renda Mensal"].sum()
renda_anual = renda_mensal * 12

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.title("📊 Dashboard da Carteira de FIIs")
st.caption(f"Última atualização: {datetime.now().strftime('%d/%m/%Y %H:%M')}")

# -------------------------------------------------
# KPIs
# -------------------------------------------------
col1, col2, col3 = st.columns(3)

col1.metric("💰 Total Investido", f"R$ {total_investido:,.2f}")
col2.metric("📥 Renda Mensal", f"R$ {renda_mensal:,.2f}")
col3.metric("📈 Renda Anual", f"R$ {renda_anual:,.2f}")

st.markdown("---")

# -------------------------------------------------
# GRÁFICO 1 - DISTRIBUIÇÃO DA CARTEIRA
# -------------------------------------------------
fig_pie = go.Figure(
    data=[
        go.Pie(
            labels=df["FII"],
            values=df["Valor Investido"],
            hole=0.45
        )
    ]
)

fig_pie.update_layout(
    title="Distribuição da Carteira por FII",
    margin=dict(t=60, b=20, l=20, r=20)
)

st.plotly_chart(fig_pie, width="stretch")

# -------------------------------------------------
# GRÁFICO 2 - PROJEÇÃO DE RENDA
# -------------------------------------------------
meses = pd.date_range(start="2026-01-01", periods=12, freq="ME")
renda_proj = [renda_mensal] * 12

fig_renda = go.Figure()

fig_renda.add_trace(
    go.Scatter(
        x=meses,
        y=renda_proj,
        mode="lines+markers",
        name="Renda Mensal Projetada"
    )
)

fig_renda.update_layout(
    title="Projeção de Renda Mensal (12 meses)",
    xaxis_title="Mês",
    yaxis_title="R$",_
