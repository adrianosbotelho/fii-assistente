import streamlit as st
import altair as alt

from core.data import carregar_carteira
from core.projections import projetar_renda
from core.benchmarks import simular_benchmark

st.set_page_config(page_title="FII Assistente", layout="wide")

st.title("📊 FII Assistente — Visão Inteligente")

carteira = carregar_carteira()

patrimonio = carteira["valor"].sum()
dy_medio = (carteira["valor"] * carteira["dy"]).sum() / patrimonio
renda_atual = patrimonio * dy_medio / 12

aba1, aba2, aba3, aba4 = st.tabs([
    "📌 Visão Geral",
    "📈 Projeções",
    "⚖️ Comparativos",
    "🧠 Insight IA"
])

# --- VISÃO GERAL ---
with aba1:
    col1, col2, col3 = st.columns(3)
    col1.metric("Patrimônio", f"R$ {patrimonio:,.2f}")
    col2.metric("Renda Mensal Atual", f"R$ {renda_atual:,.2f}")
    col3.metric("DY Médio", f"{dy_medio*100:.2f}%")

    st.subheader("Composição da Carteira")
    st.dataframe(carteira, use_container_width=True)

# --- PROJEÇÕES ---
with aba2:
    meses = st.slider("Horizonte (meses)", 12, 120, 60)

    sem = projetar_renda(carteira, meses, reinvestir=False)
    com = projetar_renda(carteira, meses, reinvestir=True)

    base = alt.Chart(sem).encode(x="Mês")

    linha_sem = base.mark_line(color="red").encode(y="Renda Mensal")
    linha_com = alt.Chart(com).mark_line(color="green").encode(x="Mês", y="Renda Mensal")

    st.altair_chart(linha_sem + linha_com, use_container_width=True)

# --- COMPARATIVOS ---
with aba3:
    cdi = simular_benchmark(patrimonio, 0.10, meses)
    ibov = simular_benchmark(patrimonio, 0.08, meses)

    st.subheader("Carteira vs CDI vs IBOV (simples)")

    st.line_chart({
        "Carteira (reinv.)": com["Patrimônio"].values,
        "CDI": [x["Valor"] for x in cdi],
        "IBOV": [x["Valor"] for x in ibov]
    })

# --- INSIGHT IA ---
with aba4:
    st.subheader("Insight do Mês")

    if renda_atual < 1000:
        st.info(
            "A renda ainda depende fortemente do reinvestimento. "
            "Manter consistência agora tem impacto exponencial no médio prazo."
        )
    else:
        st.success(
            "A carteira já apresenta autonomia de renda. "
            "Rebalanceamentos passam a ser mais importantes que crescimento."
        )
