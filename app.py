import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots
from datetime import datetime, timedelta
import numpy as np

# Importar módulos personalizados
import sys
from pathlib import Path
sys.path.append(str(Path(__file__).parent))

from core.market_data import obter_indices, calcular_correlacao_carteira_mercado, obter_taxa_selic
from core.carteira_health import analisar_saude_carteira, gerar_recomendacoes
from core.news_analyzer import analisar_sentimento_carteira, buscar_noticias_mercado
from core.benchmarks import simular_benchmark
from core.carteira_loader import carregar_carteira_completa, carregar_carteira_csv
from core.reinvestment_manager import (
    calcular_reinvestimento, gerar_carteira_atualizada, 
    salvar_carteira_atualizada, gerar_relatorio_reinvestimento,
    calcular_distribuicao_reinvestimento
)

# -------------------------------------------------
# CONFIGURAÇÃO
# -------------------------------------------------
st.set_page_config(
    page_title="FII Assistente - Dashboard Profissional",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Inicializar dark mode no session state
if "dark_mode" not in st.session_state:
    st.session_state.dark_mode = True  # Default: dark mode

# Função para obter template de gráfico baseado no tema
def get_plot_template():
    """Retorna template do Plotly baseado no tema ativo"""
    if st.session_state.dark_mode:
        return "plotly_dark"
    else:
        return "plotly_white"

# Função para obter cores do tema
def get_theme_colors():
    """Retorna cores do tema atual"""
    if st.session_state.dark_mode:
        return {
            "primary": "#00d4aa",
            "secondary": "#ff6b9d",
            "success": "#00e676",
            "warning": "#ffb74d",
            "error": "#ef5350",
            "info": "#29b6f6",
            "background": "#0e1117",
            "card": "#1e1e2e",
            "text": "#fafafa",
            "text_secondary": "#b0b0b0"
        }
    else:
        return {
            "primary": "#1f77b4",
            "secondary": "#ff7f0e",
            "success": "#2ca02c",
            "warning": "#ff9800",
            "error": "#d32f2f",
            "info": "#0288d1",
            "background": "#ffffff",
            "card": "#f5f5f5",
            "text": "#1e1e1e",
            "text_secondary": "#666666"
        }

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.header("⚙️ Configurações")

# Toggle Dark Mode (deve estar no topo para atualizar CSS)
dark_mode = st.sidebar.toggle(
    "🌙 Dark Mode",
    value=st.session_state.dark_mode,
    help="Alternar entre tema escuro e claro (estilo Grafana)"
)
st.session_state.dark_mode = dark_mode

st.sidebar.markdown("---")

# Atualizar cores baseado no estado atual do dark mode (após toggle)
colors = get_theme_colors()

# Custom CSS estilo Grafana (dinâmico baseado no tema)
css = f"""
    <style>
    /* Reset e base */
    .main {{
        background-color: {colors['background']};
    }}
    
    /* Header principal */
    .main-header {{
        font-size: 2.5rem;
        font-weight: 600;
        color: {colors['primary']};
        margin-bottom: 0.5rem;
        letter-spacing: -0.5px;
    }}
    
    .sub-header {{
        color: {colors['text_secondary']};
        font-size: 1rem;
        margin-bottom: 2rem;
    }}
    
    /* Cards e métricas estilo Grafana */
    .metric-card {{
        background: linear-gradient(135deg, {colors['card']} 0%, {colors['card']} 100%);
        padding: 1.25rem;
        border-radius: 8px;
        border-left: 3px solid {colors['primary']};
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
        transition: transform 0.2s;
    }}
    
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.15);
    }}
    
    /* Insight boxes */
    .insight-box {{
        padding: 1rem 1.25rem;
        border-radius: 6px;
        margin: 0.75rem 0;
        border-left: 4px solid;
        box-shadow: 0 1px 3px rgba(0,0,0,0.1);
    }}
    
    .insight-success {{
        background-color: {colors['success']}15;
        border-left-color: {colors['success']};
        color: {colors['text']};
    }}
    
    .insight-warning {{
        background-color: {colors['warning']}20;
        border-left-color: {colors['warning']};
        color: {colors['text']};
    }}
    
    .insight-error {{
        background-color: {colors['error']}15;
        border-left-color: {colors['error']};
        color: {colors['text']};
    }}
    
    .insight-info {{
        background-color: {colors['info']}15;
        border-left-color: {colors['info']};
        color: {colors['text']};
    }}
    
    /* Divider estilo Grafana */
    hr {{
        border: none;
        height: 1px;
        background: linear-gradient(to right, transparent, {colors['primary']}40, transparent);
        margin: 2rem 0;
    }}
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {{
        background-color: {colors['card']};
    }}
    
    /* Botões estilo Grafana */
    .stButton > button {{
        background: linear-gradient(135deg, {colors['primary']} 0%, {colors['secondary']} 100%);
        color: white;
        border: none;
        border-radius: 6px;
        font-weight: 500;
        transition: all 0.3s;
    }}
    
    .stButton > button:hover {{
        transform: translateY(-1px);
        box-shadow: 0 4px 12px {colors['primary']}40;
    }}
    
    /* Dataframe styling */
    .dataframe {{
        border-radius: 8px;
        overflow: hidden;
    }}
    
    /* Tabs estilo Grafana */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 0.5rem;
    }}
    
    .stTabs [data-baseweb="tab"] {{
        background-color: {colors['card']};
        border-radius: 6px 6px 0 0;
        padding: 0.75rem 1.5rem;
    }}
    
    /* Scrollbar personalizado */
    ::-webkit-scrollbar {{
        width: 8px;
        height: 8px;
    }}
    
    ::-webkit-scrollbar-track {{
        background: {colors['card']};
    }}
    
    ::-webkit-scrollbar-thumb {{
        background: {colors['primary']};
        border-radius: 4px;
    }}
    
    ::-webkit-scrollbar-thumb:hover {{
        background: {colors['secondary']};
    }}
    </style>
"""
st.markdown(css, unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown('<p class="main-header">📊 Dashboard Profissional - FII Assistente</p>', unsafe_allow_html=True)
st.markdown('<p class="sub-header">Análise completa da carteira com KPIs, insights de IA e monitoramento de mercado</p>', unsafe_allow_html=True)

# Carregar carteira
carteira_path = "data/carteira.csv"
uploaded_file = st.sidebar.file_uploader(
    "📂 Importar Carteira (opcional)",
    type=["csv"],
    help="Se não importar, será usado data/carteira.csv"
)

horizonte = st.sidebar.slider(
    "📅 Horizonte de Projeção (meses)",
    min_value=12,
    max_value=120,
    value=60
)

# Opção para atualização automática de dados
atualizar_dados_auto = st.sidebar.checkbox(
    "🔄 Atualizar preços e dividendos automaticamente",
    value=False,
    help="Busca preços atuais e dividendos do mercado via API"
)

atualizar_mercado = st.sidebar.button("🔄 Atualizar Dados de Mercado", type="primary")

# -------------------------------------------------
# LOAD CSV
# -------------------------------------------------
try:
    if uploaded_file is not None:
        # Se foi feito upload, usar arquivo temporário
        import tempfile
        with tempfile.NamedTemporaryFile(delete=False, suffix=".csv") as tmp:
            tmp.write(uploaded_file.getvalue())
            tmp_path = tmp.name
        
        if atualizar_dados_auto:
            df = carregar_carteira_completa(tmp_path, atualizar_dados=True, usar_preco_medio=False)
        else:
            df_temp = pd.read_csv(tmp_path)
            # Se CSV tem apenas Ticker e Quantidade, tentar usar loader automático
            if set(df_temp.columns) <= {"Ticker", "Quantidade"}:
                st.info("💡 CSV simplificado detectado. Ativando atualização automática de dados...")
                df = carregar_carteira_completa(tmp_path, atualizar_dados=True, usar_preco_medio=False)
            else:
                df = df_temp
    else:
        # Usar arquivo padrão
        if atualizar_dados_auto:
            df = carregar_carteira_completa(carteira_path, atualizar_dados=True, usar_preco_medio=False)
        else:
            df_temp = pd.read_csv(carteira_path)
            # Se CSV tem apenas Ticker e Quantidade, tentar usar loader automático
            if set(df_temp.columns) <= {"Ticker", "Quantidade"}:
                st.info("💡 CSV simplificado detectado. Ativando atualização automática de dados...")
                df = carregar_carteira_completa(carteira_path, atualizar_dados=True, usar_preco_medio=False)
            else:
                df = df_temp
except FileNotFoundError:
    st.error(f"❌ Arquivo não encontrado: {carteira_path}")
    st.info("⬅️ Por favor, importe um arquivo CSV na sidebar ou coloque data/carteira.csv")
    st.stop()
except Exception as e:
    st.error(f"❌ Erro ao carregar arquivo: {e}")
    if atualizar_dados_auto:
        st.info("💡 Dica: Tente desativar 'Atualizar automaticamente' se houver problema de conexão")
    st.stop()

# -------------------------------------------------
# VALIDAÇÃO
# -------------------------------------------------
cols = ["Ticker", "Quantidade", "Preco_Medio", "Dividendo_Mensal"]
for c in cols:
    if c not in df.columns:
        st.error(f"❌ Coluna obrigatória ausente: {c}")
        st.stop()

df[cols[1:]] = df[cols[1:]].astype(float)

# -------------------------------------------------
# CÁLCULOS BASE
# -------------------------------------------------
df["Valor_Investido"] = df["Quantidade"] * df["Preco_Medio"]
df["Renda_Mensal"] = df["Quantidade"] * df["Dividendo_Mensal"]
df["Yield_Mensal"] = df["Renda_Mensal"] / df["Valor_Investido"]

patrimonio = df["Valor_Investido"].sum()
renda_mensal = df["Renda_Mensal"].sum()
yield_medio = renda_mensal / patrimonio
renda_anual = renda_mensal * 12

# -------------------------------------------------
# KPIs PRINCIPAIS
# -------------------------------------------------
st.markdown("### 📈 Indicadores Principais (KPIs)")

kpi1, kpi2, kpi3, kpi4, kpi5 = st.columns(5)

with kpi1:
    st.metric(
        "💰 Patrimônio Total",
        f"R$ {patrimonio:,.2f}",
        help="Valor total investido na carteira"
    )

with kpi2:
    st.metric(
        "📥 Renda Mensal",
        f"R$ {renda_mensal:,.2f}",
        help="Dividendos recebidos mensalmente"
    )

with kpi3:
    st.metric(
        "📊 Yield Médio",
        f"{yield_medio*100:.2f}%",
        delta=f"{(yield_medio*100 - 1.0):.2f}% vs meta",
        help="Rentabilidade média mensal da carteira"
    )

with kpi4:
    st.metric(
        "📆 Renda Anual Projetada",
        f"R$ {renda_anual:,.2f}",
        help="Renda anual com base nos dividendos mensais"
    )

with kpi5:
    num_ativos = len(df)
    st.metric(
        "🎯 Número de Ativos",
        f"{num_ativos}",
        help="Quantidade de FIIs na carteira"
    )

st.divider()

# -------------------------------------------------
# ANÁLISE DE SAÚDE DA CARTEIRA (IA)
# -------------------------------------------------
st.markdown("### 🤖 Insights de IA - Saúde da Carteira")

with st.spinner("Analisando saúde da carteira..."):
    saude = analisar_saude_carteira(df)

# Score de Saúde
col_score, col_status = st.columns([3, 1])

with col_score:
    st.markdown(f"**Score de Saúde:** {saude['score']:.0f}/100")
    st.progress(saude['score'] / 100)

with col_status:
    cores = {"green": "🟢", "blue": "🔵", "orange": "🟠", "red": "🔴"}
    st.markdown(f"**{cores.get(saude['cor_status'], '⚪')} {saude['status']}**")

# Insights e Alertas
if saude['insights'] or saude['alertas']:
    col_insights, col_alertas = st.columns(2)
    
    with col_insights:
        if saude['insights']:
            st.markdown("#### ✅ Insights Positivos")
            for insight in saude['insights']:
                st.markdown(f"""
                <div class="insight-box insight-{insight['tipo']}">
                    <strong>{insight['titulo']}</strong><br>
                    {insight['mensagem']}
                </div>
                """, unsafe_allow_html=True)
    
    with col_alertas:
        if saude['alertas']:
            st.markdown("#### ⚠️ Alertas e Atenções")
            for alerta in saude['alertas']:
                st.markdown(f"""
                <div class="insight-box insight-{alerta['tipo']}">
                    <strong>{alerta['titulo']}</strong><br>
                    {alerta['mensagem']}
                </div>
                """, unsafe_allow_html=True)

# Recomendações
recomendacoes = gerar_recomendacoes(df)
if recomendacoes:
    st.markdown("#### 💡 Recomendações Estratégicas")
    for rec in recomendacoes:
        prioridade_icon = {"alta": "🔴", "media": "🟡", "baixa": "🟢"}
        st.markdown(f"""
        **{prioridade_icon.get(rec['prioridade'], '⚪')} {rec['titulo']}** ({rec['categoria']})
        - {rec['descricao']}
        - 💼 Ação sugerida: {rec['acao']}
        """)

# -------------------------------------------------
# ANÁLISE DE NOTÍCIAS E SENTIMENTOS
# -------------------------------------------------
st.markdown("### 📰 Análise de Sentimentos e Notícias")

with st.spinner("Analisando sentimentos da carteira..."):
    try:
        sentimentos_carteira = analisar_sentimento_carteira(df["Ticker"].tolist())
        noticias_mercado = buscar_noticias_mercado()
    except Exception as e:
        st.warning(f"⚠️ Erro ao analisar sentimentos: {e}")
        sentimentos_carteira = {"sentimento_geral": "neutro", "score_medio": 0, "resumo": "Análise indisponível"}
        noticias_mercado = []

col_sent1, col_sent2 = st.columns(2)

with col_sent1:
    st.markdown("#### 🤖 Sentimento da Carteira")
    
    sentimento_icon = {
        "positivo": "🟢",
        "neutro": "🟡",
        "negativo": "🔴"
    }
    
    st.markdown(f"""
    **{sentimento_icon.get(sentimentos_carteira['sentimento_geral'], '⚪')} {sentimentos_carteira['sentimento_geral'].upper()}**
    
    {sentimentos_carteira.get('resumo', 'Análise em andamento')}
    """)
    
    if 'score_medio' in sentimentos_carteira:
        score_sent = (sentimentos_carteira['score_medio'] + 1) / 2 * 100  # Normalizar -1 a 1 para 0 a 100
        st.progress(score_sent / 100)

with col_sent2:
    if noticias_mercado:
        st.markdown("#### 📰 Notícias do Mercado")
        for noticia in noticias_mercado[:3]:  # Mostrar 3 primeiras
            st.markdown(f"""
            **{noticia.get('titulo', 'Sem título')}**  
            *{noticia.get('fonte', 'Fonte desconhecida')} - {noticia.get('data', 'N/A')}*
            """)
    else:
        st.info("📰 Notícias serão carregadas em atualização futura")

st.divider()

# -------------------------------------------------
# DADOS DE MERCADO
# -------------------------------------------------
st.markdown("### 📊 Indicadores de Mercado")

with st.spinner("Carregando dados de mercado..."):
    try:
        indices = obter_indices()
        correlacao = calcular_correlacao_carteira_mercado(df["Ticker"].tolist())
    except Exception as e:
        st.warning(f"⚠️ Erro ao carregar dados de mercado: {e}")
        indices = {"ibov": {"valor": None, "variacao_30d": 0}, "ifix": {"valor": None, "variacao_30d": 0}}
        correlacao = 0.0

col_mkt1, col_mkt2, col_mkt3 = st.columns(3)

with col_mkt1:
    if indices["ibov"]["valor"]:
        variacao_ibov = indices["ibov"]["variacao_30d"]
        st.metric(
            "📈 IBOVESPA",
            f"{indices['ibov']['valor']:,.0f}" if indices['ibov']['valor'] else "N/A",
            delta=f"{variacao_ibov:.2f}%",
            delta_color="normal" if variacao_ibov >= 0 else "inverse"
        )

with col_mkt2:
    if indices["ifix"]["valor"]:
        variacao_ifix = indices["ifix"]["variacao_30d"]
        st.metric(
            "🏢 IFIX",
            f"{indices['ifix']['valor']:,.2f}" if indices['ifix']['valor'] else "N/A",
            delta=f"{variacao_ifix:.2f}%",
            delta_color="normal" if variacao_ifix >= 0 else "inverse",
            help="Índice de Fundos Imobiliários"
        )

with col_mkt3:
    st.metric(
        "🔗 Correlação com IFIX",
        f"{correlacao:.2f}",
        help="Correlação da carteira com o índice IFIX"
    )

st.divider()

# -------------------------------------------------
# PROJEÇÕES E GRÁFICOS
# -------------------------------------------------
st.markdown("### 📈 Projeções de Crescimento Orgânico")

# Projeção com reinvestimento
meses = []
rendas = []
patrimonios = []

pat = patrimonio
renda = renda_mensal

for i in range(horizonte):
    meses.append(i + 1)
    rendas.append(renda)
    patrimonios.append(pat)
    
    pat = pat + renda
    renda = pat * yield_medio

df_proj = pd.DataFrame({
    "Mês": meses,
    "Renda Mensal Projetada": rendas,
    "Patrimônio Projetado": patrimonios
})

# Gráfico de projeção duplo
fig_proj = make_subplots(
    rows=2, cols=1,
    subplot_titles=("Renda Mensal Projetada", "Patrimônio Projetado"),
    vertical_spacing=0.15,
    row_heights=[0.5, 0.5]
)

fig_proj.add_trace(
    go.Scatter(
        x=df_proj["Mês"],
        y=df_proj["Renda Mensal Projetada"],
        mode="lines+markers",
        name="Renda Mensal",
        line=dict(color="#2E86AB", width=3),
        marker=dict(size=4)
    ),
    row=1, col=1
)

fig_proj.add_trace(
    go.Scatter(
        x=df_proj["Mês"],
        y=df_proj["Patrimônio Projetado"],
        mode="lines+markers",
        name="Patrimônio",
        line=dict(color="#A23B72", width=3),
        marker=dict(size=4)
    ),
    row=2, col=1
)

fig_proj.update_xaxes(title_text="Mês", row=2, col=1)
fig_proj.update_yaxes(title_text="R$", row=1, col=1)
fig_proj.update_yaxes(title_text="R$", row=2, col=1)
fig_proj.update_layout(
    height=700,
    showlegend=True,
    hovermode="x unified",
    template=get_plot_template()
)

st.plotly_chart(fig_proj, use_container_width=True)

# Métricas de projeção
col_proj1, col_proj2, col_proj3 = st.columns(3)

renda_final = rendas[-1]
patrimonio_final = patrimonios[-1]
crescimento_renda = ((renda_final / renda_mensal) - 1) * 100
crescimento_patrimonio = ((patrimonio_final / patrimonio) - 1) * 100

with col_proj1:
    st.metric(
        f"💰 Patrimônio em {horizonte} meses",
        f"R$ {patrimonio_final:,.2f}",
        delta=f"{crescimento_patrimonio:.1f}%",
        help="Com crescimento orgânico via reinvestimento"
    )

with col_proj2:
    st.metric(
        f"📥 Renda Mensal em {horizonte} meses",
        f"R$ {renda_final:,.2f}",
        delta=f"{crescimento_renda:.1f}%",
        help="Renda mensal projetada"
    )

with col_proj3:
    meses_dobrar = saude['metricas'].get('meses_dobrar', 0)
    st.metric(
        "⏱️ Tempo para Dobrar",
        f"{meses_dobrar:.0f} meses",
        help="Tempo estimado para dobrar patrimônio com reinvestimento"
    )

# -------------------------------------------------
# COMPARAÇÃO COM BENCHMARKS
# -------------------------------------------------
st.markdown("### ⚖️ Comparação com Benchmarks de Mercado")

try:
    taxa_selic = obter_taxa_selic()
    taxa_selic_anual = taxa_selic / 100  # Converter para decimal
    
    # Simular carteira vs benchmarks
    benchmark_selic = simular_benchmark(patrimonio, taxa_selic_anual, horizonte)
    benchmark_ifix = simular_benchmark(patrimonio, 0.10, horizonte)  # Assumindo ~10% ao ano para IFIX
    benchmark_poupanca = simular_benchmark(patrimonio, 0.085, horizonte)  # ~8.5% ao ano
    
    # Converter para DataFrame para facilitar plotagem
    df_bench = pd.DataFrame({
        "Mês": range(1, horizonte + 1),
        "Carteira (Reinvestimento)": patrimonios,
        "SELIC": [b["Valor"] for b in benchmark_selic],
        "IFIX (Estimado)": [b["Valor"] for b in benchmark_ifix],
        "Poupança": [b["Valor"] for b in benchmark_poupanca]
    })
    
    # Gráfico comparativo
    fig_bench = go.Figure()
    
    fig_bench.add_trace(go.Scatter(
        x=df_bench["Mês"],
        y=df_bench["Carteira (Reinvestimento)"],
        mode="lines",
        name="Carteira (Reinvestimento)",
        line=dict(color="#2E86AB", width=3)
    ))
    
    fig_bench.add_trace(go.Scatter(
        x=df_bench["Mês"],
        y=df_bench["SELIC"],
        mode="lines",
        name=f"SELIC ({taxa_selic}% a.a.)",
        line=dict(color="#A23B72", width=2, dash="dash")
    ))
    
    fig_bench.add_trace(go.Scatter(
        x=df_bench["Mês"],
        y=df_bench["IFIX (Estimado)"],
        mode="lines",
        name="IFIX (~10% a.a.)",
        line=dict(color="#F18F01", width=2, dash="dot")
    ))
    
    fig_bench.add_trace(go.Scatter(
        x=df_bench["Mês"],
        y=df_bench["Poupança"],
        mode="lines",
        name="Poupança (~8.5% a.a.)",
        line=dict(color="#C73E1D", width=2, dash="dashdot")
    ))
    
    fig_bench.update_layout(
        title="Crescimento do Patrimônio: Carteira vs Benchmarks",
        xaxis_title="Mês",
        yaxis_title="Patrimônio (R$)",
        hovermode="x unified",
        height=500,
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01),
        template=get_plot_template()
    )
    
    st.plotly_chart(fig_bench, use_container_width=True)
    
    # Comparação no período final
    valor_final_carteira = patrimonios[-1]
    valor_final_selic = benchmark_selic[-1]["Valor"]
    valor_final_ifix = benchmark_ifix[-1]["Valor"]
    valor_final_poupanca = benchmark_poupanca[-1]["Valor"]
    
    diff_selic = ((valor_final_carteira / valor_final_selic) - 1) * 100
    diff_ifix = ((valor_final_carteira / valor_final_ifix) - 1) * 100
    diff_poupanca = ((valor_final_carteira / valor_final_poupanca) - 1) * 100
    
    col_bench1, col_bench2, col_bench3, col_bench4 = st.columns(4)
    
    with col_bench1:
        st.metric(
            f"💰 Carteira ({horizonte}m)",
            f"R$ {valor_final_carteira:,.2f}",
            help="Com reinvestimento de dividendos"
        )
    
    with col_bench2:
        st.metric(
            f"SELIC ({horizonte}m)",
            f"R$ {valor_final_selic:,.2f}",
            delta=f"{diff_selic:+.1f}%",
            delta_color="normal" if diff_selic > 0 else "inverse"
        )
    
    with col_bench3:
        st.metric(
            f"IFIX ({horizonte}m)",
            f"R$ {valor_final_ifix:,.2f}",
            delta=f"{diff_ifix:+.1f}%",
            delta_color="normal" if diff_ifix > 0 else "inverse"
        )
    
    with col_bench4:
        st.metric(
            f"Poupança ({horizonte}m)",
            f"R$ {valor_final_poupanca:,.2f}",
            delta=f"{diff_poupanca:+.1f}%",
            delta_color="normal" if diff_poupanca > 0 else "inverse"
        )
    
    # Análise
    if diff_selic > 0:
        st.success(f"✅ Sua carteira supera a SELIC em {diff_selic:.1f}% no período projetado!")
    else:
        st.warning(f"⚠️ Sua carteira está abaixo da SELIC em {abs(diff_selic):.1f}% - considere revisar os ativos.")
    
except Exception as e:
    st.warning(f"⚠️ Erro ao calcular benchmarks: {e}")

st.divider()

# -------------------------------------------------
# ANÁLISE DE ALOCAÇÃO
# -------------------------------------------------
st.markdown("### 🎯 Análise de Alocação")

col_alloc1, col_alloc2 = st.columns(2)

with col_alloc1:
    # Gráfico de pizza
    fig_pie = px.pie(
        df,
        names="Ticker",
        values="Valor_Investido",
        hole=0.4,
        title="Distribuição do Patrimônio",
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
    fig_pie.update_layout(template=get_plot_template())
    st.plotly_chart(fig_pie, use_container_width=True)

with col_alloc2:
    # Gráfico de barras - Yield por ativo
    df_yield = df.copy()
    df_yield["Yield (%)"] = df_yield["Yield_Mensal"] * 100
    df_yield = df_yield.sort_values("Yield (%)", ascending=True)
    
    fig_bar = px.bar(
        df_yield,
        x="Yield (%)",
        y="Ticker",
        orientation='h',
        title="Yield Mensal por Ativo",
        color="Yield (%)",
        color_continuous_scale="Greens",
        labels={"Yield (%)": "Yield Mensal (%)"}
    )
    fig_bar.update_layout(
        yaxis={'categoryorder': 'total ascending'}, 
        height=400,
        template=get_plot_template()
    )
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -------------------------------------------------
# TABELA DETALHADA E COMPARAÇÃO
# -------------------------------------------------
st.markdown("### 📋 Análise Detalhada e Comparação de Fundos")

# Preparar DataFrame para visualização
df_view = df.copy()
df_view["Pct_Patrimonio"] = (df_view["Valor_Investido"] / patrimonio) * 100
df_view["Yield (%)"] = df_view["Yield_Mensal"] * 100
df_view["Renda_Anual"] = df_view["Renda_Mensal"] * 12
df_view["Dividendo_Anual"] = df_view["Dividendo_Mensal"] * 12

# Adicionar métricas comparativas
yield_medio_geral = df_view["Yield (%)"].mean()
df_view["Yield_vs_Media"] = df_view["Yield (%)"] - yield_medio_geral
df_view["Prioridade_Reinvestimento"] = df_view.apply(
    lambda row: "Alta" if row["Yield (%)"] > yield_medio_geral * 1.1 
    else "Média" if row["Yield (%)"] > yield_medio_geral * 0.9 
    else "Baixa", axis=1
)

# Tabs para diferentes visualizações
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "📊 Tabela Interativa", 
    "🔄 Comparação de Fundos", 
    "💡 Sugestão de Reinvestimento", 
    "📈 Análise Comparativa",
    "💰 Calcular e Aplicar Reinvestimento"
])

with tab1:
    st.markdown("#### Tabela Completa da Carteira")
    
    # Filtros e ordenação
    col_filt1, col_filt2 = st.columns(2)
    
    with col_filt1:
        ordenar_por = st.selectbox(
            "Ordenar por:",
            ["Valor_Investido", "Yield (%)", "Renda_Mensal", "Pct_Patrimonio", "Ticker"],
            index=0
        )
    
    with col_filt2:
        ordem = st.selectbox("Ordem:", ["Decrescente", "Crescente"], index=0)
    
    df_sorted = df_view.sort_values(
        ordenar_por, 
        ascending=(ordem == "Crescente")
    )
    
    # Formatação profissional da tabela
    df_display = df_sorted[[
        "Ticker",
        "Quantidade",
        "Preco_Medio",
        "Dividendo_Mensal",
        "Valor_Investido",
        "Pct_Patrimonio",
        "Renda_Mensal",
        "Renda_Anual",
        "Yield (%)",
        "Prioridade_Reinvestimento"
    ]].copy()
    
    # Formatar valores monetários e percentuais
    df_display["Preco_Medio"] = df_display["Preco_Medio"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Dividendo_Mensal"] = df_display["Dividendo_Mensal"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Valor_Investido"] = df_display["Valor_Investido"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Renda_Mensal"] = df_display["Renda_Mensal"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Renda_Anual"] = df_display["Renda_Anual"].apply(lambda x: f"R$ {x:,.2f}")
    df_display["Pct_Patrimonio"] = df_display["Pct_Patrimonio"].apply(lambda x: f"{x:.2f}%")
    df_display["Yield (%)"] = df_display["Yield (%)"].apply(lambda x: f"{x:.2f}%")
    
    # Renomear colunas para exibição
    df_display.columns = [
        "Ticker", "Qtd", "Preço Médio", "Dividendo Mensal",
        "Valor Investido", "% Patrimônio", "Renda Mensal",
        "Renda Anual", "Yield %", "Prioridade Reinvest."
    ]
    
    st.dataframe(
        df_display,
        use_container_width=True,
        hide_index=True,
        height=400
    )
    
    # Estatísticas resumidas
    st.markdown("#### 📊 Estatísticas Resumidas")
    col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)
    
    with col_stat1:
        st.metric("Concentração Máxima", f"{df_view['Pct_Patrimonio'].max():.1f}%")
    
    with col_stat2:
        st.metric("Yield Médio", f"{yield_medio_geral:.2f}%")
    
    with col_stat3:
        st.metric("Yield Mínimo", f"{df_view['Yield (%)'].min():.2f}%")
    
    with col_stat4:
        st.metric("Yield Máximo", f"{df_view['Yield (%)'].max():.2f}%")

with tab2:
    st.markdown("#### 🔄 Comparação Lado a Lado entre Fundos")
    
    col_comp1, col_comp2 = st.columns(2)
    
    with col_comp1:
        fundo1 = st.selectbox("Selecione o primeiro fundo:", df_view["Ticker"].tolist(), key="fundo1")
    
    with col_comp2:
        fundo2 = st.selectbox("Selecione o segundo fundo:", df_view["Ticker"].tolist(), key="fundo2")
    
    if fundo1 != fundo2:
        df1 = df_view[df_view["Ticker"] == fundo1].iloc[0]
        df2 = df_view[df_view["Ticker"] == fundo2].iloc[0]
        
        # Tabela comparativa
        comparacao = pd.DataFrame({
            "Métrica": [
                "Ticker",
                "Quantidade",
                "Preço Médio",
                "Valor Investido",
                "% do Patrimônio",
                "Dividendo Mensal",
                "Dividendo Anual",
                "Renda Mensal",
                "Renda Anual",
                "Yield Mensal (%)"
            ],
            fundo1: [
                df1["Ticker"],
                f"{df1['Quantidade']:.0f}",
                f"R$ {df1['Preco_Medio']:,.2f}",
                f"R$ {df1['Valor_Investido']:,.2f}",
                f"{df1['Pct_Patrimonio']:.2f}%",
                f"R$ {df1['Dividendo_Mensal']:,.2f}",
                f"R$ {df1['Dividendo_Anual']:,.2f}",
                f"R$ {df1['Renda_Mensal']:,.2f}",
                f"R$ {df1['Renda_Anual']:,.2f}",
                f"{df1['Yield (%)']:.2f}%"
            ],
            fundo2: [
                df2["Ticker"],
                f"{df2['Quantidade']:.0f}",
                f"R$ {df2['Preco_Medio']:,.2f}",
                f"R$ {df2['Valor_Investido']:,.2f}",
                f"{df2['Pct_Patrimonio']:.2f}%",
                f"R$ {df2['Dividendo_Mensal']:,.2f}",
                f"R$ {df2['Dividendo_Anual']:,.2f}",
                f"R$ {df2['Renda_Mensal']:,.2f}",
                f"R$ {df2['Renda_Anual']:,.2f}",
                f"{df2['Yield (%)']:.2f}%"
            ]
        })
        
        st.dataframe(comparacao, use_container_width=True, hide_index=True)
        
        # Gráfico de comparação
        fig_comp = go.Figure()
        
        metricas_numericas = {
            "Valor Investido": (df1["Valor_Investido"], df2["Valor_Investido"]),
            "Renda Mensal": (df1["Renda_Mensal"], df2["Renda_Mensal"]),
            "Dividendo Mensal": (df1["Dividendo_Mensal"], df2["Dividendo_Mensal"]),
            "Yield (%)": (df1["Yield (%)"], df2["Yield (%)"])
        }
        
        for metrica, (valor1, valor2) in metricas_numericas.items():
            fig_comp.add_trace(go.Bar(
                name=fundo1 if metrica != "Yield (%)" else f"{fundo1} ({valor1:.2f}%)",
                x=[metrica],
                y=[valor1],
                text=[f"R$ {valor1:,.2f}" if "R$" not in str(valor1) else f"{valor1:.2f}%"],
                textposition="auto"
            ))
            fig_comp.add_trace(go.Bar(
                name=fundo2 if metrica != "Yield (%)" else f"{fundo2} ({valor2:.2f}%)",
                x=[metrica],
                y=[valor2],
                text=[f"R$ {valor2:,.2f}" if "R$" not in str(valor2) else f"{valor2:.2f}%"],
                textposition="auto"
            ))
        
        fig_comp.update_layout(
            title=f"Comparação: {fundo1} vs {fundo2}",
            barmode="group",
            height=400,
            template=get_plot_template()
        )
        
        st.plotly_chart(fig_comp, use_container_width=True)
    else:
        st.warning("⚠️ Selecione dois fundos diferentes para comparação.")

with tab3:
    st.markdown("#### 💡 Sugestões de Reinvestimento de Dividendos")
    
    # Calcular renda total disponível para reinvestimento
    renda_total_mensal = df_view["Renda_Mensal"].sum()
    
    st.markdown(f"""
    **💰 Renda Mensal Total Disponível para Reinvestimento:** R$ {renda_total_mensal:,.2f}
    
    **💡 Estratégia Recomendada:** Baseada em yield, diversificação e priorização de ativos de alta performance.
    """)
    
    # Ordenar por prioridade de reinvestimento
    df_reinvest = df_view.copy()
    df_reinvest = df_reinvest.sort_values("Yield (%)", ascending=False)
    
    # Calcular sugestão de alocação
    sugestoes = []
    for _, row in df_reinvest.iterrows():
        # Proporção baseada em yield relativo
        peso_yield = row["Yield (%)"] / df_reinvest["Yield (%)"].sum()
        # Proporção inversa à concentração (para diversificar)
        peso_diversificacao = 1 / (row["Pct_Patrimonio"] + 1)
        # Peso combinado
        peso_final = (peso_yield * 0.7) + (peso_diversificacao * 0.3)
        sugestoes.append({
            "Ticker": row["Ticker"],
            "Yield (%)": row["Yield (%)"],
            "Peso Sugerido": peso_final,
            "Valor Sugerido (R$)": renda_total_mensal * peso_final,
            "Prioridade": row["Prioridade_Reinvestimento"]
        })
    
    df_sugestao = pd.DataFrame(sugestoes)
    df_sugestao["Peso Sugerido (%)"] = (df_sugestao["Peso Sugerido"] / df_sugestao["Peso Sugerido"].sum()) * 100
    df_sugestao["Valor Sugerido (R$)"] = df_sugestao["Valor Sugerido (R$)"] * (df_sugestao["Peso Sugerido"] / df_sugestao["Peso Sugerido"].sum())
    df_sugestao = df_sugestao.sort_values("Valor Sugerido (R$)", ascending=False)
    
    # Formatação
    df_sugestao_display = df_sugestao.copy()
    df_sugestao_display["Yield (%)"] = df_sugestao_display["Yield (%)"].apply(lambda x: f"{x:.2f}%")
    df_sugestao_display["Peso Sugerido (%)"] = df_sugestao_display["Peso Sugerido (%)"].apply(lambda x: f"{x:.1f}%")
    df_sugestao_display["Valor Sugerido (R$)"] = df_sugestao_display["Valor Sugerido (R$)"].apply(lambda x: f"R$ {x:,.2f}")
    df_sugestao_display = df_sugestao_display[["Ticker", "Yield (%)", "Prioridade", "Peso Sugerido (%)", "Valor Sugerido (R$)"]]
    
    st.dataframe(df_sugestao_display, use_container_width=True, hide_index=True)
    
    # Gráfico de sugestão
    fig_reinvest = px.bar(
        df_sugestao,
        x="Ticker",
        y="Valor Sugerido (R$)",
        color="Prioridade",
        color_discrete_map={"Alta": "#28a745", "Média": "#ffc107", "Baixa": "#dc3545"},
        title="Distribuição Sugerida de Reinvestimento",
        text="Valor Sugerido (R$)"
    )
    fig_reinvest.update_traces(texttemplate="R$ %{text:,.2f}", textposition="outside")
    fig_reinvest.update_layout(
        height=400,
        template=get_plot_template()
    )
    st.plotly_chart(fig_reinvest, use_container_width=True)
    
    st.info("💡 **Dica:** Priorize fundos com yield acima da média para maximizar retorno, mas mantenha diversificação.")

with tab4:
    st.markdown("#### 📈 Análise Comparativa de Dividendos e Yield")
    
    # Gráfico de dividendos vs yield
    fig_scatter = px.scatter(
        df_view,
        x="Dividendo_Mensal",
        y="Yield (%)",
        size="Valor_Investido",
        color="Prioridade_Reinvestimento",
        hover_data=["Ticker", "Renda_Mensal", "Pct_Patrimonio"],
        color_discrete_map={"Alta": "#28a745", "Média": "#ffc107", "Baixa": "#dc3545"},
        title="Dividendo Mensal vs Yield (%)",
        labels={
            "Dividendo_Mensal": "Dividendo Mensal (R$)",
            "Yield (%)": "Yield Mensal (%)"
        }
    )
    fig_scatter.update_layout(
        height=500,
        template=get_plot_template()
    )
    st.plotly_chart(fig_scatter, use_container_width=True)
    
    # Gráfico comparativo de renda
    fig_renda = go.Figure()
    
    df_view_sorted = df_view.sort_values("Renda_Mensal", ascending=True)
    
    fig_renda.add_trace(go.Bar(
        y=df_view_sorted["Ticker"],
        x=df_view_sorted["Renda_Mensal"],
        orientation='h',
        name="Renda Mensal",
        marker_color=df_view_sorted["Yield (%)"],
        marker_showscale=True,
        marker_colorbar=dict(title="Yield %"),
        text=[f"R$ {x:,.2f}" for x in df_view_sorted["Renda_Mensal"]],
        textposition="outside"
    ))
    
    fig_renda.update_layout(
        title="Renda Mensal por Fundo (Cor = Yield)",
        xaxis_title="Renda Mensal (R$)",
        height=400,
        template=get_plot_template()
    )
    
    st.plotly_chart(fig_renda, use_container_width=True)
    
    # Ranking de melhor yield
    st.markdown("#### 🏆 Ranking por Yield")
    df_ranking = df_view[["Ticker", "Yield (%)", "Dividendo_Mensal", "Renda_Mensal"]].copy()
    df_ranking = df_ranking.sort_values("Yield (%)", ascending=False)
    df_ranking["Rank"] = range(1, len(df_ranking) + 1)
    df_ranking["Dividendo_Mensal"] = df_ranking["Dividendo_Mensal"].apply(lambda x: f"R$ {x:,.2f}")
    df_ranking["Renda_Mensal"] = df_ranking["Renda_Mensal"].apply(lambda x: f"R$ {x:,.2f}")
    df_ranking["Yield (%)"] = df_ranking["Yield (%)"].apply(lambda x: f"{x:.2f}%")
    df_ranking = df_ranking[["Rank", "Ticker", "Yield (%)", "Dividendo_Mensal", "Renda_Mensal"]]
    
    st.dataframe(df_ranking, use_container_width=True, hide_index=True)

with tab5:
    st.markdown("#### 💰 Calcular e Aplicar Reinvestimento Mensal")
    
    renda_total_mensal = df_view["Renda_Mensal"].sum()
    
    st.markdown(f"""
    **💰 Renda Mensal Total Disponível:** R$ {renda_total_mensal:,.2f}
    
    Esta ferramenta calcula quantas cotas podem ser compradas com os dividendos recebidos 
    e gera a carteira atualizada com as novas quantidades.
    """)
    
    # Seleção de estratégia
    estrategia = st.radio(
        "📋 Estratégia de Distribuição:",
        ["proporcional", "yield_alto", "diversificacao"],
        format_func=lambda x: {
            "proporcional": "🔄 Proporcional à Renda Gerada",
            "yield_alto": "📈 Priorizar Maior Yield",
            "diversificacao": "🎯 Priorizar Diversificação"
        }[x],
        help="Escolha como distribuir os dividendos entre os fundos"
    )
    
    # Calcular distribuição
    distribuicao = calcular_distribuicao_reinvestimento(df, estrategia)
    
    # Calcular reinvestimento
    with st.spinner("Calculando reinvestimento..."):
        df_reinvestimento = calcular_reinvestimento(df, distribuicao, usar_precos_atuais=True)
    
    # Mostrar resultados
    st.markdown("#### 📊 Resultado do Reinvestimento")
    
    # Resumo
    total_cotas = df_reinvestimento["Cotas_Compradas"].sum()
    total_investido = df_reinvestimento["Valor_Utilizado"].sum()
    total_nao_utilizado = df_reinvestimento["Valor_Nao_Utilizado"].sum()
    
    col_res1, col_res2, col_res3 = st.columns(3)
    with col_res1:
        st.metric("Cotas Compradas", f"{int(total_cotas)}")
    with col_res2:
        st.metric("Valor Investido", f"R$ {total_investido:,.2f}")
    with col_res3:
        st.metric("Sobra (não utilizada)", f"R$ {total_nao_utilizado:,.2f}")
    
    # Tabela detalhada
    df_reinvest_display = df_reinvestimento.copy()
    df_reinvest_display = df_reinvest_display[df_reinvest_display["Cotas_Compradas"] > 0]
    
    if len(df_reinvest_display) > 0:
        # Selecionar apenas as colunas que queremos exibir (em ordem específica)
        colunas_exibir = [
            "Ticker", "Quantidade_Atual", "Valor_Reinvestir", "Preco_Atual",
            "Cotas_Compradas", "Valor_Utilizado", "Valor_Nao_Utilizado",
            "Nova_Quantidade", "Preco_Medio_Anterior", "Novo_Preco_Medio"
        ]
        
        # Filtrar apenas colunas que existem no DataFrame
        colunas_disponiveis = [col for col in colunas_exibir if col in df_reinvest_display.columns]
        df_reinvest_display = df_reinvest_display[colunas_disponiveis].copy()
        
        # Formatação
        if "Quantidade_Atual" in df_reinvest_display.columns:
            df_reinvest_display["Quantidade_Atual"] = df_reinvest_display["Quantidade_Atual"].apply(lambda x: f"{x:.0f}")
        if "Valor_Reinvestir" in df_reinvest_display.columns:
            df_reinvest_display["Valor_Reinvestir"] = df_reinvest_display["Valor_Reinvestir"].apply(lambda x: f"R$ {x:,.2f}")
        if "Preco_Atual" in df_reinvest_display.columns:
            df_reinvest_display["Preco_Atual"] = df_reinvest_display["Preco_Atual"].apply(lambda x: f"R$ {x:,.2f}")
        if "Cotas_Compradas" in df_reinvest_display.columns:
            df_reinvest_display["Cotas_Compradas"] = df_reinvest_display["Cotas_Compradas"].apply(lambda x: f"{int(x)}")
        if "Valor_Utilizado" in df_reinvest_display.columns:
            df_reinvest_display["Valor_Utilizado"] = df_reinvest_display["Valor_Utilizado"].apply(lambda x: f"R$ {x:,.2f}")
        if "Valor_Nao_Utilizado" in df_reinvest_display.columns:
            df_reinvest_display["Valor_Nao_Utilizado"] = df_reinvest_display["Valor_Nao_Utilizado"].apply(lambda x: f"R$ {x:,.2f}")
        if "Nova_Quantidade" in df_reinvest_display.columns:
            df_reinvest_display["Nova_Quantidade"] = df_reinvest_display["Nova_Quantidade"].apply(lambda x: f"{x:.0f}")
        if "Preco_Medio_Anterior" in df_reinvest_display.columns:
            df_reinvest_display["Preco_Medio_Anterior"] = df_reinvest_display["Preco_Medio_Anterior"].apply(lambda x: f"R$ {x:,.2f}")
        if "Novo_Preco_Medio" in df_reinvest_display.columns:
            df_reinvest_display["Novo_Preco_Medio"] = df_reinvest_display["Novo_Preco_Medio"].apply(lambda x: f"R$ {x:,.2f}")
        
        # Renomear colunas - mapear exatamente o número de colunas que temos
        nomes_colunas_map = {
            "Ticker": "Ticker",
            "Quantidade_Atual": "Qtd Atual",
            "Valor_Reinvestir": "Valor Reinvestir",
            "Preco_Atual": "Preço Atual",
            "Cotas_Compradas": "Cotas Compradas",
            "Valor_Utilizado": "Valor Utilizado",
            "Valor_Nao_Utilizado": "Sobra",
            "Nova_Quantidade": "Nova Qtd",
            "Preco_Medio_Anterior": "Preço Médio Ant.",
            "Novo_Preco_Medio": "Novo Preço Médio"
        }
        
        # Renomear usando dicionário (mais seguro)
        df_reinvest_display = df_reinvest_display.rename(columns=nomes_colunas_map)
        
        st.dataframe(df_reinvest_display, use_container_width=True, hide_index=True)
    else:
        st.info("ℹ️ Nenhuma cota será comprada com a estratégia selecionada. Ajuste os valores ou tente outra estratégia.")
    
    # Mostrar relatório
    with st.expander("📄 Ver Relatório Completo"):
        relatorio = gerar_relatorio_reinvestimento(df_reinvestimento)
        st.text(relatorio)
    
    # Botão para gerar e salvar carteira atualizada
    st.markdown("---")
    st.markdown("#### 💾 Atualizar Carteira")
    
    col_btn1, col_btn2 = st.columns(2)
    
    with col_btn1:
        if st.button("📥 Gerar CSV Atualizado", type="primary"):
            try:
                df_atualizada = gerar_carteira_atualizada(df, df_reinvestimento)
                
                # Criar CSV para download
                csv_updated = df_atualizada[["Ticker", "Quantidade"]].to_csv(index=False)
                
                st.download_button(
                    label="⬇️ Baixar CSV Atualizado",
                    data=csv_updated,
                    file_name=f"carteira_atualizada_{datetime.now().strftime('%Y%m%d')}.csv",
                    mime="text/csv",
                    type="primary"
                )
                
                st.success("✅ CSV gerado com sucesso! Baixe o arquivo e substitua o data/carteira.csv")
            except Exception as e:
                st.error(f"❌ Erro ao gerar CSV: {e}")
    
    with col_btn2:
        if st.button("💾 Salvar Diretamente (Backup Automático)", help="Atualiza data/carteira.csv e cria backup"):
            try:
                df_atualizada = gerar_carteira_atualizada(df, df_reinvestimento)
                caminho_salvo = salvar_carteira_atualizada(
                    df_atualizada, 
                    caminho_original=carteira_path,
                    criar_backup=True
                )
                st.success(f"✅ Carteira atualizada e salva em {caminho_salvo}")
                st.info("💡 Recarregue a página para ver a carteira atualizada")
            except Exception as e:
                st.error(f"❌ Erro ao salvar: {e}")
    
    # Instruções
    st.markdown("---")
    st.markdown("""
    ### 📝 Como Funciona:
    
    1. **Calcular**: O sistema calcula quantas cotas podem ser compradas com os dividendos
    2. **Revisar**: Verifique a tabela acima com os resultados
    3. **Atualizar**: 
       - **Opção 1**: Baixe o CSV atualizado e substitua manualmente o arquivo `data/carteira.csv`
       - **Opção 2**: Clique em "Salvar Diretamente" para atualizar automaticamente (backup é criado)
    
    ⚠️ **Importante**: Após cada reinvestimento mensal, atualize a carteira usando esta ferramenta.
    """)

# -------------------------------------------------
# FOOTER
# -------------------------------------------------
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <small>📊 Dashboard FII Assistente | Análise profissional de carteira de fundos imobiliários</small><br>
    <small>Última atualização: {}</small>
</div>
""".format(datetime.now().strftime("%d/%m/%Y %H:%M")), unsafe_allow_html=True)
