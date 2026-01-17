import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =========================================================
# CONFIGURAÇÃO DA PÁGINA
# =========================================================
st.set_page_config(
    page_title="FII Assistente",
    page_icon="📊",
    layout="wide"
)

# =========================================================
# SIDEBAR
# =========================================================
st.sidebar.title("📊 FII Assistente")

st.sidebar.markdown(
    """
    Plataforma profissional para análise de FIIs.

    **Funcionalidades atuais**
    - Dashboard da carteira
    - Projeção de renda
    - Gráficos interativos

    **Em breve**
    - Importação CSV
    - Integração B3 / Investidor10
    - Alertas inteligentes
    """
)

menu = st.sidebar.radio(
    "Menu",
    ["Dashboard", "Projeção de Renda"]
)

# =========================================================
# DADOS MOCK (ESTÁVEIS)
# =========================================================
dados = {
    "FII": ["BTLG11", "VISC11", "KNCR11", "MXRF11"],
    "Quantidade": [100, 80, 120, 200],
    "Preço Atual": [102.50, 108.90, 105.20, 9.80],
    "DY (%)": [9.1, 8.8, 13.5, 12.4]
}

df = pd.DataFrame(dados)
df["Valor Investido"] = df["Quantidade"] * df["Preço Atual"]

# =========================================================
# DASHBOARD
# =========================================================
if menu == "Dashboard":
    st.title("📈 Dashboard da Carteira")

    patrimonio_total = df["Valor Investido"].sum()
    renda_mensal = (df["Valor Investido"] * df["DY (%)"] / 100 / 12).sum()

    col1, col2, col3 = st.columns(3)

    col1.metric(
        "💼 Patrimônio Total",
        f"R$ {patrimonio_total:,.2f}"
    )

    col2.metric(
        "📊 FIIs na Carteira",
        df.shape[0]
    )

    col3.metric(
        "💰 Renda Mensal Estimada",
        f"R$ {renda_mensal:,.2f}"
    )

    st.subheader("📋 Detalhamento da Carteira")
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

# =========================================================
# PROJEÇÃO DE RENDA
# =========================================================
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

    renda_inicial = (df["Valor Investido"] * df["DY (%)"] / 100 / 12).sum()

    total_meses = anos * 12

    datas = pd.date_range(
        start=datetime.today(),
        periods=total_meses,
        freq="ME"
    )

    rendas = []
    renda_atual = renda_inicial

    for mes in range(total_meses):
        rendas.append(renda_atual)
        renda_atual = renda_atual * (1 + crescimento_anual / 100 / 12)

    df_projecao = pd.DataFrame(
        {
            "Data": datas,
            "Renda Mensal (R$)": rendas
        }
    )

    fig_renda = go.Figure()

    fig_renda.add_trace(
        go.Scatter(
            x=df_projecao["Data"],
            y=df_projecao["Renda Mensal (R$)"],
            mode="lines",
            name="Renda Projetada"
        )
    )

    fig_renda.update_layout(
        title="Projeção de Renda Mensal",
        xaxis_title="Data",
        yaxis_title="Renda (R$)",
        hovermode="x unified"
    )

    st.plotly_chart(fig_renda, use_container_width=True)

    st.subheader("📄 Dados da Projeção")
    st.dataframe(df_projecao, use_container_width=True)

# =========================================================
# RODAPÉ
# =========================================================
st.markdown("---")
st.caption(
    "Este dashboard é educacional e não constitui recomendação de investimento."
)
