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

# -------------------------------------------------
# CONFIGURAÇÃO
# -------------------------------------------------
st.set_page_config(
    page_title="FII Assistente - Dashboard Profissional",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="📊"
)

# Custom CSS para melhorar aparência
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .insight-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
    }
    .insight-success {
        background-color: #d4edda;
        border-left: 4px solid #28a745;
    }
    .insight-warning {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .insight-error {
        background-color: #f8d7da;
        border-left: 4px solid #dc3545;
    }
    .insight-info {
        background-color: #d1ecf1;
        border-left: 4px solid #17a2b8;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------------------------------------
# HEADER
# -------------------------------------------------
st.markdown('<p class="main-header">📊 Dashboard Profissional - FII Assistente</p>', unsafe_allow_html=True)
st.markdown("**Análise completa da carteira com KPIs, insights de IA e monitoramento de mercado**")

# -------------------------------------------------
# SIDEBAR
# -------------------------------------------------
st.sidebar.header("⚙️ Configurações")

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
    hovermode="x unified"
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
        legend=dict(yanchor="top", y=0.99, xanchor="left", x=0.01)
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
    fig_bar.update_layout(yaxis={'categoryorder': 'total ascending'}, height=400)
    st.plotly_chart(fig_bar, use_container_width=True)

st.divider()

# -------------------------------------------------
# TABELA DETALHADA
# -------------------------------------------------
st.markdown("### 📋 Detalhamento Completo da Carteira")

df_view = df.copy()
df_view["Pct_Patrimonio"] = (df_view["Valor_Investido"] / patrimonio) * 100
df_view["Yield (%)"] = df_view["Yield_Mensal"] * 100
df_view["Renda_Anual"] = df_view["Renda_Mensal"] * 12
df_view = df_view.sort_values("Valor_Investido", ascending=False)

st.dataframe(
    df_view[[
        "Ticker",
        "Quantidade",
        "Preco_Medio",
        "Dividendo_Mensal",
        "Valor_Investido",
        "Pct_Patrimonio",
        "Renda_Mensal",
        "Renda_Anual",
        "Yield (%)"
    ]].round(2),
    use_container_width=True,
    hide_index=True
)

# Resumo estatístico
st.markdown("#### 📊 Estatísticas da Carteira")
col_stat1, col_stat2, col_stat3, col_stat4 = st.columns(4)

with col_stat1:
    st.metric("Concentração Máxima", f"{df_view['Pct_Patrimonio'].max():.1f}%")

with col_stat2:
    st.metric("Yield Mínimo", f"{df_view['Yield (%)'].min():.2f}%")

with col_stat3:
    st.metric("Yield Máximo", f"{df_view['Yield (%)'].max():.2f}%")

with col_stat4:
    st.metric("Desvio Padrão Yield", f"{df_view['Yield (%)'].std():.2f}%")

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
