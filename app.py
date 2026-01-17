import streamlit as st
import yaml
import pandas as pd

from services.loader import carregar_carteira
from services.analytics import calcular_renda

st.set_page_config(page_title="FII Assistente", layout="wide")

st.title("📊 FII Assistente — Diagnóstico da Carteira")

# =====================
# Carregamento de dados
# =====================
carteira = carregar_carteira()

with open("config/regras.yaml") as f:
    regras = yaml.safe_load(f)["meta_percentual"]

# =====================
# Cálculo de valores
# =====================
# Preços atuais
import yfinance as yf

dados = []

valor_total = 0
for _, row in carteira.iterrows():
    ticker = row["ticker"]
    qtd = row["quantidade"]

    ativo = yf.Ticker(ticker + ".SA")
    preco = ativo.history(period="1d")["Close"].iloc[-1]

    valor = preco * qtd
    valor_total += valor

    dados.append({
        "Ativo": ticker,
        "Quantidade": qtd,
        "Preço": round(preco, 2),
        "Valor": valor
    })

df = pd.DataFrame(dados)

# =====================
# Diagnóstico
# =====================
diagnostico = []

for _, row in df.iterrows():
    ativo = row["Ativo"]
    valor = row["Valor"]

    pct_real = (valor / valor_total) * 100
    pct_ideal = regras.get(ativo, 0)
    desvio = pct_real - pct_ideal

    if abs(desvio) <= 2:
        status = "🟢 OK"
    elif desvio > 2 and desvio <= 4:
        status = "🟡 Atenção"
    elif desvio > 4:
        status = "🔴 Desbalanceado"
    else:
        status = "🔵 Oportunidade"

    diagnostico.append({
        "Ativo": ativo,
        "% Carteira": round(pct_real, 2),
        "% Ideal": pct_ideal,
        "Desvio": round(desvio, 2),
        "Status": status
    })

df_diag = pd.DataFrame(diagnostico)

# =====================
# Visão Executiva
# =====================
renda = calcular_renda(carteira)

col1, col2, col3 = st.columns(3)

col1.metric("💰 Renda mensal estimada", f"R$ {renda}")
col2.metric("📦 Ativos fora do peso", len(df_diag[df_diag["Status"] != "🟢 OK"]))
col3.metric("🎯 Total da carteira", f"R$ {round(valor_total, 2)}")

st.divider()

# =====================
# Tabela de Diagnóstico
# =====================
st.subheader("🔍 Diagnóstico de Alocação")

st.dataframe(
    df_diag.sort_values("Desvio", ascending=False),
    use_container_width=True
)

# =====================
# Resumo em linguagem humana
# =====================
st.subheader("🧠 Leitura Gerencial")

problemas = df_diag[df_diag["Status"] == "🔴 Desbalanceado"]
oportunidades = df_diag[df_diag["Status"] == "🔵 Oportunidade"]

if problemas.empty and oportunidades.empty:
    st.success("Carteira bem equilibrada. Nenhuma ação necessária no momento.")
else:
    if not problemas.empty:
        st.warning(
            f"Ativos acima do peso: {', '.join(problemas['Ativo'].tolist())}"
        )
    if not oportunidades.empty:
        st.info(
            f"Oportunidade de reforço: {', '.join(oportunidades['Ativo'].tolist())}"
        )


st.divider()
st.subheader("🔁 Reinvestimento Inteligente (Próximo Aporte)")

# Selecionar oportunidades reais
candidatos = df_diag[df_diag["Status"] == "🔵 Oportunidade"].copy()

if candidatos.empty:
    st.info("Nenhum ativo abaixo do peso no momento. Reinvestimento não recomendado.")
else:
    # Limitar aos top 3 maiores desvios negativos
    candidatos = candidatos.sort_values("Desvio").head(3)

    total_abs = candidatos["Desvio"].abs().sum()

    sugestao = []
    for _, row in candidatos.iterrows():
        percentual = abs(row["Desvio"]) / total_abs * 100
        sugestao.append({
            "Ativo": row["Ativo"],
            "Motivo": "Abaixo do peso ideal",
            "% do Aporte": round(percentual, 1)
        })

    st.table(sugestao)

    ativos = ", ".join([s["Ativo"] for s in sugestao])
    st.success(
        f"Priorize o próximo reinvestimento em: {ativos}. "
        "Essa alocação melhora o equilíbrio da carteira sem aumentar risco."
    )
        
