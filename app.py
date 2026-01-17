import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="FII Assistente",
    page_icon="📊",
    layout="wide"
)

# =========================
# SIDEBAR
# =========================
st.sidebar.title("📊 FII Assistente")

st.sidebar.markdown(
    """
    **Plataforma profissional de FIIs**

    Funcionalidades:
    - 📈 Dashboard da carteira
    - 💰 Projeção de renda
    - 📊 Gráficos interativos
    - 📁 Importação de dados (em breve)
    """
)

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Projeção de Renda"]
)

# =========================
# DADOS MOCK (TEMPORÁRIOS)
# =========================
dados = {
    "FII": ["BTLG11", "VISC11", "KNCR11", "MXRF11"],
    "Quantidade": [100, 80, 120, 200],
    "Preço Atual": [102.50, 108.90, 105.20, 9.80],
    "DY (%)": [9.1, 8.8, 13.5, 12.4]
}

df = pd.DataFrame(dados)
df["Valor Investido"] = df["Quantidade"] * df["Preço Atual"]

# =========================
# DASHBOARD
# =========================
if menu == "Dashboard":
    st.title("📈 Dashboard da Carteira")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "💼 Patrimônio Total",
            f"R$ {df['Valor Investido'].sum():,.2f}"
        )

    with col2:
        st.metric(
            "📊 FIIs na Carteira",
            df.shape[0]
        )

    with col3:
        renda_mensal = (df["Valor Investido"] * df["DY (%)"] / 100 / 12).sum()
        st.metric(
            "💰 Renda Mensal Estimada",
            f"R$ {renda_mensal:,.2f}"
        )

    st.subheader("📋 Detalhes da Carteira")
    st.dataframe(df, use_container_width=True)

    # Gráfico de alocação
    fig_alocacao = go.Figure(
        data=[
            go.Pie(
                labels=df["FII"],
                values=df["Valor Investido"],
                hole=0.4
            )
        ]
    )

    fig_alocacao.update_layout(
        title="Distribuição da Carteira por FII"
    )

    st.plotly_chart(fig_alocacao, use_container_width=True)

# =========================
# PROJEÇÃO DE RENDA
# =========================
if menu == "Projeção de Renda":
    st.title("💰 Projeção de Renda")

    anos = st.slider(
        "Horizonte de projeção (anos)",
        min_value=1,
        max_value=10,
        value=5
    )

    crescimento_anual = st.slider(
        "Crescimento anual da renda (%)",
        min_value=0.0,
        max_value=15.0,
        value=5.0
    )

    renda_atual_mensal = (df["Valor Investido"] * df["DY (%)"] / 100 / 12).sum()

    datas = pd.date_range(
        start=datetime.today(),
        periods=anos * 12,
        freq="ME"
    )

    rendas = []
    renda = renda_atual_mensal

    for _ in range(_
