import streamlit as st
import pandas as pd
import plotly.graph_objects as go
from datetime import datetime

# =============================
# CONFIGURAÇÃO GERAL
# =============================
st.set_page_config(
    page_title="FII Assistente",
    page_icon="📊",
    layout="wide"
)

# =============================
# FUNÇÕES AUXILIARES
# =============================
def carregar_csv(uploaded_file):
    df = pd.read_csv(uploaded_file)
    df.columns = [c.lower().strip() for c in df.columns]

    colunas_obrigatorias = {"ticker", "quantidade", "preco_medio"}
    if not colunas_obrigatorias.issubset(set(df.columns)):
        raise ValueError(
            "O CSV precisa conter as colunas: ticker, quantidade, preco_medio"
        )

    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    df["preco_medio"] = pd.to_numeric(df["preco_medio"], errors="coerce")
    df["valor_investido"] = df["quantidade"] * df["preco_medio"]

    return df

def grafico_alocacao(df):
    fig = go.Figure(
        data=[
            go.Pie(
                labels=df["ticker"],
                values=df["valor_investido"],
                hole=0.5
            )
        ]
    )

    fig.update_layout(
        title="Distribuição da Carteira (R$)",
        legend_title="FIIs",
        template="plotly_dark"
    )

    return fig

# =============================
# SIDEBAR
# =============================
st.sidebar.markdown(
    "### 📊 FII Assistente\n"
    "Plataforma de acompanhamento\n"
    "e projeção de FIIs\n\n"
    "---\n"
    "**Etapa atual:**\n"
    "- Importação da carteira (CSV)\n"
)

# =============================
# CONTEÚDO PRINCIPAL
# =============================
st.title("📂 Importar Carteira de FIIs")

st.markdown(
    """
    Faça upload de um arquivo **CSV** com a sua carteira.

    **Formato esperado:**
    ```csv
    ticker,quantidade,preco_medio
    KNCR11,120,103.20
    CPTS11,200,94.50
    BTLG11,80,98.70
    ```
    """
)

uploaded_file = st.file_uploader(
    "Selecione o arquivo CSV da sua carteira",
    type=["csv"]
)

if uploaded_file is not None:
    try:
        carteira_df = carregar_csv(uploaded_file)

        st.success("Carteira importada com sucesso ✅")

        # =============================
        # MÉTRICAS
        # =============================
        total_investido = carteira_df["valor_investido"].sum()
        qtd_fiis = carteira_df.shape[0]

        col1, col2 = st.columns(2)
        col1.metric("💰 Total Investido", f"R$ {total_investido:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
        col2.metric("🏢 Quantidade de FIIs", qtd_fiis)

        st.markdown("---")

        # =============================
        # TABELA
        # =============================
        st.subheader("📋 Carteira Importada")
        st.dataframe(
            carteira_df.style.format(
                {
                    "preco_medio": "R$ {:.2f}",
                    "valor_investido": "R$ {:.2f}"
                }
            ),
            width="stretch"
        )

        st.markdown("---")

        # =============================
        # GRÁFICO
        # =============================
        st.subheader("📊 Alocação da Carteira")
        fig = grafico_alocacao(carteira_df)
        st.plotly_chart(fig, width="stretch")

        st.markdown("---")

        # =============================
        # PRÓXIMO PASSO
        # =============================
        st.info(
            "✅ Carteira carregada.\n\n"
            "Próximo passo: **persistir esses dados** e iniciar\n"
            "projeções reais de dividendos."
        )

    except Exception as e:
        st.error(f"Erro ao processar o CSV: {e}")

else:
    st.warning("Aguardando upload do arquivo CSV.")
