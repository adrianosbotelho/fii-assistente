import streamlit as st
import pandas as pd
import numpy as np
import plotly.graph_objects as go
from datetime import datetime

# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(
    page_title="FII Assistente",
    layout="wide",
    initial_sidebar_state="expanded"
)

# =========================
# ESTILO GLOBAL (CSS)
# =========================
st.markdown(
    """
    <style>
    body {
        background-color: #0e1117;
        color: #e6e6e6;
    }
    .metric-container {
        background-color: #161b22;
        border-radius: 12px;
        padding: 20px;
        text-align: center;
        border: 1px solid #222;
    }
    .metric-title {
        font-size: 14px;
        color: #9da5b4;
    }
    .metric-value {
        font-size: 26px;
        font-weight: bold;
        color: #00e676;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =========================
# FUNÇÕES AUXILIARES
# =========================
def formatar_real(valor):
    return f"R$ {valor:,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")

def gerar_projecao(renda_atual, crescimento_mensal, meses):
    valores = []
    renda = renda_atual
    for _ in range(meses):
        valores.append(renda)
        renda *= (1 + crescimento_mensal)
    return valores

# =========================
# DADOS BASE (por enquanto mock, depois viram dinâmicos)
# =========================
RENDA_ATUAL = 730.00
CRESCIMENTO_MENSAL = 0.010  # 1% ao mês
PATRIMONIO = 73681.72

CDI_ANUAL = 0.105
IBOV_ANUAL = 0.085
IFIX_ANUAL = 0.095

# =========================
# SIDEBAR
# =========================
st.sidebar.title("⚙️ Configurações")

horizonte = st.sidebar.slider(
    "Horizonte de Projeção (meses)",
    min_value=6,
    max_value=120,
    value=36,
    step=6
)

st.sidebar.markdown("---")
st.sidebar.markdown("📌 **FII Assistente**")
st.sidebar.caption("Dashboard pessoal de renda e projeções")

# =========================
# TÍTULO
# =========================
st.title("📊 FII Assistente — Dashboard de Renda Inteligente")
st.caption("Visão estratégica de curto, médio e longo prazo")

# =========================
# MÉTRICAS TOPO
# =========================
col1, col2, col3, col4 = st.columns(4)

with col1:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-title">Renda Mensal Atual</div>
            <div class="metric-value">{formatar_real(RENDA_ATUAL)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col2:
    renda_12m = gerar_projecao(RENDA_ATUAL, CRESCIMENTO_MENSAL, 12)[-1]
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-title">Renda Projetada (12m)</div>
            <div class="metric-value">{formatar_real(renda_12m)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col3:
    renda_36m = gerar_projecao(RENDA_ATUAL, CRESCIMENTO_MENSAL, 36)[-1]
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-title">Renda Projetada (36m)</div>
            <div class="metric-value">{formatar_real(renda_36m)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

with col4:
    st.markdown(
        f"""
        <div class="metric-container">
            <div class="metric-title">Patrimônio Atual</div>
            <div class="metric-value">{formatar_real(PATRIMONIO)}</div>
        </div>
        """,
        unsafe_allow_html=True
    )

# =========================
# ABAS PRINCIPAIS
# =========================
aba1, aba2, aba3, aba4 = st.tabs(
    ["📈 Projeções", "⚖️ Comparativos", "🧠 Insight IA", "ℹ️ Visão Geral"]
)

# =========================
# ABA 1 — PROJEÇÕES
# =========================
with aba1:
    meses = list(range(1, horizonte + 1))
    renda_proj = gerar_projecao(RENDA_ATUAL, CRESCIMENTO_MENSAL, horizonte)

    fig = go.Figure()

    fig.add_trace(
        go.Scatter(
            x=meses,
            y=renda_proj,
            mode="lines+markers",
            name="Renda Projetada",
            line=dict(color="#00e676", width=3),
            hovertemplate="Mês %{x}<br>Renda: R$ %{y:,.2f}<extra></extra>",
        )
    )

    fig.update_layout(
        template="plotly_dark",
        title="📈 Projeção de Renda Mensal",
        xaxis_title="Meses",
        yaxis_title="Renda Mensal (R$)",
        hovermode="x unified",
        height=450,
    )

    st.plotly_chart(fig, width="stretch")

# =========================
# ABA 2 — COMPARATIVOS
# =========================
with aba2:
    anos = horizonte / 12

    rendimento_carteira = (1 + CRESCIMENTO_MENSAL) ** (12 * anos) - 1
    rendimento_cdi = (1 + CDI_ANUAL) ** anos - 1
    rendimento_ibov = (1 + IBOV_ANUAL) ** anos - 1
    rendimento_ifix = (1 + IFIX_ANUAL) ** anos - 1

    df_comp = pd.DataFrame({
        "Ativo": ["Carteira FIIs", "CDI", "IBOVESPA", "IFIX"],
        "Rentabilidade (%)": [
            rendimento_carteira * 100,
            rendimento_cdi * 100,
            rendimento_ibov * 100,
            rendimento_ifix * 100,
        ]
    })

    fig_comp = go.Figure(
        data=[
            go.Bar(
                x=df_comp["Ativo"],
                y=df_comp["Rentabilidade (%)"],
                marker_color=["#00e676", "#1f77b4", "#ff9800", "#9c27b0"],
                text=[f"{v:.2f}%" for v in df_comp["Rentabilidade (%)"]],
                textposition="auto",
            )
        ]
    )

    fig_comp.update_layout(
        template="plotly_dark",
        title="⚖️ Comparativo de Rentabilidade no Horizonte Selecionado",
        yaxis_title="Rentabilidade (%)",
        height=450,
    )

    st.plotly_chart(fig_comp, width="stretch")

# =========================
# ABA 3 — INSIGHT IA
# =========================
with aba3:
    st.subheader("🧠 Insight Inteligente (IA)")
    st.info(
        """
        **Estrutura pronta para IA.**  
        Aqui entrarão insights como:
        - Fundos com maior potencial de aumento de dividendos  
        - Alertas de risco (vacância, alavancagem, emissões)  
        - Sugestões de rebalanceamento  
        - Impacto de fatos relevantes no fluxo de caixa  

        👉 Próximo passo: integrar OpenAI para análise automática.
        """
    )

# =========================
# ABA 4 — VISÃO GERAL
# =========================
with aba4:
    st.markdown(
        """
        ### ℹ️ Visão Geral da Estratégia

        - Foco em **renda previsível**
        - Crescimento via **reinvestimento inteligente**
        - Comparação contínua com benchmarks
        - Decisão orientada a dados e não emoção

        Este dashboard é a base do seu **SaaS pessoal de investimentos**.
        """
    )
