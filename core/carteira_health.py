"""
Módulo de análise de saúde da carteira com insights de IA
"""
import pandas as pd
import numpy as np
from typing import Dict, List

def analisar_saude_carteira(df_carteira: pd.DataFrame) -> Dict:
    """
    Analisa a saúde da carteira e retorna insights e recomendações
    """
    insights = []
    alertas = []
    score_saude = 100
    
    # Calcular métricas base
    patrimonio_total = df_carteira["Valor_Investido"].sum()
    yield_medio = (df_carteira["Yield_Mensal"] * df_carteira["Valor_Investido"]).sum() / patrimonio_total
    
    # 1. Análise de concentração
    df_carteira["Pct_Patrimonio"] = (df_carteira["Valor_Investido"] / patrimonio_total) * 100
    max_concentracao = df_carteira["Pct_Patrimonio"].max()
    num_ativos = len(df_carteira)
    
    # Índice de Herfindahl (concentração)
    hhi = (df_carteira["Pct_Patrimonio"] ** 2).sum()
    
    if max_concentracao > 30:
        alertas.append({
            "tipo": "warning",
            "titulo": "Alta Concentração",
            "mensagem": f"Maior posição representa {max_concentracao:.1f}% da carteira. Considere diversificar."
        })
        score_saude -= 10
    elif max_concentracao < 10 and num_ativos < 8:
        insights.append({
            "tipo": "info",
            "titulo": "Carteira Bem Diversificada",
            "mensagem": f"Distribuição equilibrada entre {num_ativos} ativos."
        })
    
    if hhi > 2000:
        alertas.append({
            "tipo": "warning",
            "titulo": "Concentração Elevada (HHI)",
            "mensagem": f"Índice de Herfindahl: {hhi:.0f}. Ideal abaixo de 1500."
        })
    
    # 2. Análise de Yield
    yield_min = df_carteira["Yield_Mensal"].min() * 100
    yield_max = df_carteira["Yield_Mensal"].max() * 100
    desvio_yield = df_carteira["Yield_Mensal"].std() * 100
    
    if yield_medio * 100 < 0.8:
        alertas.append({
            "tipo": "error",
            "titulo": "Yield Médio Baixo",
            "mensagem": f"Yield médio de {yield_medio*100:.2f}% a.m. pode estar abaixo do objetivo de renda."
        })
        score_saude -= 15
    else:
        insights.append({
            "tipo": "success",
            "titulo": "Yield Adequado",
            "mensagem": f"Yield médio de {yield_medio*100:.2f}% a.m. está alinhado com objetivo de renda."
        })
    
    if desvio_yield > 3:
        insights.append({
            "tipo": "info",
            "titulo": "Disparidade de Yields",
            "mensagem": f"Grande variação entre yields ({yield_min:.2f}% a {yield_max:.2f}%). Considere balancear."
        })
    
    # 3. Análise de Quantidade de Ativos
    if num_ativos < 5:
        alertas.append({
            "tipo": "warning",
            "titulo": "Carteira Pouco Diversificada",
            "mensagem": f"Apenas {num_ativos} ativos. Considere adicionar mais FIIs para reduzir risco."
        })
        score_saude -= 10
    elif num_ativos >= 10:
        insights.append({
            "tipo": "success",
            "titulo": "Diversificação Adequada",
            "mensagem": f"Carteira com {num_ativos} ativos oferece boa diversificação."
        })
    
    # 4. Identificar ativos subperformantes (yield muito abaixo da média)
    media_yield = df_carteira["Yield_Mensal"].mean()
    ativos_fracos = df_carteira[df_carteira["Yield_Mensal"] < media_yield * 0.7]
    
    if len(ativos_fracos) > 0:
        tickers_fracos = ativos_fracos["Ticker"].tolist()
        alertas.append({
            "tipo": "warning",
            "titulo": "Ativos Subperformantes",
            "mensagem": f"Revisar: {', '.join(tickers_fracos)} com yield abaixo da média."
        })
    
    # 5. Crescimento orgânico projetado
    renda_mensal = df_carteira["Renda_Mensal"].sum()
    taxa_reinvestimento = yield_medio
    
    # Calcular tempo para dobrar patrimônio
    meses_dobrar = np.log(2) / np.log(1 + taxa_reinvestimento) if taxa_reinvestimento > 0 else 0
    
    insights.append({
        "tipo": "info",
        "titulo": "Crescimento Orgânico",
        "mensagem": f"Com reinvestimento, patrimônio dobra em aproximadamente {meses_dobrar:.0f} meses ({meses_dobrar/12:.1f} anos)."
    })
    
    # Normalizar score
    score_saude = max(0, min(100, score_saude))
    
    # Classificar saúde
    if score_saude >= 80:
        status_saude = "Excelente"
        cor_status = "green"
    elif score_saude >= 60:
        status_saude = "Boa"
        cor_status = "blue"
    elif score_saude >= 40:
        status_saude = "Atenção"
        cor_status = "orange"
    else:
        status_saude = "Crítica"
        cor_status = "red"
    
    return {
        "score": score_saude,
        "status": status_saude,
        "cor_status": cor_status,
        "insights": insights,
        "alertas": alertas,
        "metricas": {
            "num_ativos": num_ativos,
            "hhi": hhi,
            "max_concentracao": max_concentracao,
            "yield_medio": yield_medio * 100,
            "meses_dobrar": meses_dobrar
        }
    }


def gerar_recomendacoes(df_carteira: pd.DataFrame, dados_mercado: Dict = None) -> List[Dict]:
    """
    Gera recomendações baseadas na análise da carteira e mercado
    """
    recomendacoes = []
    
    patrimonio_total = df_carteira["Valor_Investido"].sum()
    yield_medio = (df_carteira["Yield_Mensal"] * df_carteira["Valor_Investido"]).sum() / patrimonio_total
    
    # 1. Recomendação de diversificação
    num_ativos = len(df_carteira)
    if num_ativos < 8:
        recomendacoes.append({
            "prioridade": "alta",
            "categoria": "Diversificação",
            "titulo": "Aumentar Diversificação",
            "descricao": f"Adicionar mais {8 - num_ativos} FIIs para reduzir risco específico.",
            "acao": "Considerar novos aportes em setores diferentes"
        })
    
    # 2. Análise de setores (simplificado - baseado em ticker)
    # FIIs de tijolo vs papel
    # Esta é uma análise simplificada - idealmente teria dados de classificação
    
    # 3. Recomendação baseada em yield
    if yield_medio * 100 < 1.0:
        recomendacoes.append({
            "prioridade": "media",
            "categoria": "Rentabilidade",
            "titulo": "Otimizar Yield",
            "descricao": f"Yield atual {yield_medio*100:.2f}% pode ser melhorado com rebalanceamento.",
            "acao": "Revisar ativos com menor yield e considerar substituições"
        })
    
    # 4. Recomendação de reinvestimento
    renda_mensal = df_carteira["Renda_Mensal"].sum()
    if renda_mensal > 0:
        recomendacoes.append({
            "prioridade": "baixa",
            "categoria": "Estratégia",
            "titulo": "Reinvestimento Automático",
            "descricao": f"Com R$ {renda_mensal:.2f}/mês de dividendos, manter estratégia de reinvestimento.",
            "acao": "Continuar reinvestindo dividendos para crescimento orgânico"
        })
    
    return recomendacoes
