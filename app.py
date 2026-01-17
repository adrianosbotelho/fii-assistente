import streamlit as st
import pandas as pd
import plotly.graph_objects as go

# ===============================
# CONFIGURAÇÃO DA PÁGINA
# ===============================
st.set_page_config(
    page_title="FII Assistente | Dashboard Profissional",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.title("📊 FII Assistente — Dashboard Profissional")
st.caption("Carteira real • Projeções • Renda passiva • Reinvestimento")

# ===============================
# UPLOAD DA CARTEIRA
# ===============================
st.sidebar.header("📂 Importar Carteira")
uploaded_file = st.sidebar.file_uploader(
    "Importe sua carteira em CSV",
    type=["csv"]
)

st.sidebar.markdown("""
**Formato esperado do CSV:**
