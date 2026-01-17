import streamlit as st
import yaml
from services.loader import carregar_carteira
from services.analytics import calcular_renda
from services.reinvest import sugestao_reinvestimento

st.set_page_config(page_title="FII Assistente", layout="wide")

st.title("📊 FII Assistente Pessoal")

carteira = carregar_carteira()

with open("config/regras.yaml") as f:
    regras = yaml.safe_load(f)["meta_percentual"]

renda = calcular_renda(carteira)

st.metric("Renda mensal estimada", f"R$ {renda}")

st.subheader("Sugestão de reinvestimento")
sugestao = sugestao_reinvestimento(renda, regras)

st.table(
    [{"Ativo": k, "Valor (R$)": v} for k, v in sugestao.items()]
)
