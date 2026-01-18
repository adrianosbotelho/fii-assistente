"""
Módulo para análise de notícias e sentimentos relacionados aos FIIs da carteira
"""
import pandas as pd
from typing import List, Dict
import re

def analisar_noticias_fii(ticker: str, noticias: List[Dict] = None) -> Dict:
    """
    Analisa notícias de um FII específico e retorna sentimento
    Esta é uma implementação simplificada - idealmente usaria NLP/AI real
    """
    if not noticias:
        return {
            "sentimento": "neutro",
            "score": 0,
            "resumo": "Sem notícias disponíveis",
            "relevancia": []
        }
    
    # Palavras-chave positivas e negativas (simplificado)
    palavras_positivas = [
        "crescimento", "expansão", "aumento", "alta", "lucro", "receita",
        "performance", "resultado positivo", "dividendo", "aluguel",
        "vacância baixa", "novo contrato", "ocupação"
    ]
    
    palavras_negativas = [
        "queda", "perda", "dificuldade", "risco", "incerteza", "vacância",
        "inquilino", "cancelamento", "problema", "investigação", "suspensão"
    ]
    
    score_total = 0
    relevancias = []
    
    for noticia in noticias:
        titulo = noticia.get("titulo", "").lower()
        conteudo = noticia.get("conteudo", "").lower()
        texto_completo = f"{titulo} {conteudo}"
        
        positivas = sum(1 for palavra in palavras_positivas if palavra in texto_completo)
        negativas = sum(1 for palavra in palavras_negativas if palavra in texto_completo)
        
        score_noticia = positivas - negativas
        score_total += score_noticia
        
        if abs(score_noticia) > 0:
            relevancias.append({
                "titulo": noticia.get("titulo", ""),
                "score": score_noticia,
                "relevancia": "alta" if abs(score_noticia) >= 2 else "media"
            })
    
    # Normalizar score (-1 a 1)
    if len(noticias) > 0:
        score_normalizado = score_total / (len(noticias) * 2)  # Normalização simples
        score_normalizado = max(-1, min(1, score_normalizado))
    else:
        score_normalizado = 0
    
    # Determinar sentimento
    if score_normalizado > 0.2:
        sentimento = "positivo"
    elif score_normalizado < -0.2:
        sentimento = "negativo"
    else:
        sentimento = "neutro"
    
    # Gerar resumo
    if sentimento == "positivo":
        resumo = f"Sentimento geral positivo para {ticker}. Tendência de crescimento identificada."
    elif sentimento == "negativo":
        resumo = f"Atenção necessária para {ticker}. Alguns sinais negativos detectados."
    else:
        resumo = f"Sentimento neutro para {ticker}. Nenhum sinal significativo detectado."
    
    return {
        "sentimento": sentimento,
        "score": score_normalizado,
        "resumo": resumo,
        "relevancia": relevancias[:5]  # Top 5 mais relevantes
    }


def buscar_noticias_mercado() -> List[Dict]:
    """
    Busca notícias gerais do mercado de FIIs
    Retorna lista de notícias simuladas - idealmente usaria API de notícias real
    """
    # Esta é uma implementação mock - idealmente usaria:
    # - API do Google News
    # - RSS feeds de sites financeiros
    # - API do Yahoo Finance
    # - Web scraping (com permissões)
    
    noticias_mock = [
        {
            "titulo": "Mercado de FIIs registra alta em 2024",
            "fonte": "InfoMoney",
            "data": "2024-01-15",
            "relevancia": "alta"
        },
        {
            "titulo": "Taxa SELIC impacta atratividade dos fundos imobiliários",
            "fonte": "Valor Econômico",
            "data": "2024-01-10",
            "relevancia": "alta"
        }
    ]
    
    return noticias_mock


def analisar_sentimento_carteira(tickers: List[str], noticias_por_ticker: Dict[str, List] = None) -> Dict:
    """
    Analisa sentimento geral da carteira baseado em notícias
    """
    sentimentos = []
    
    for ticker in tickers:
        noticias = noticias_por_ticker.get(ticker, []) if noticias_por_ticker else []
        analise = analisar_noticias_fii(ticker, noticias)
        sentimentos.append({
            "ticker": ticker,
            "sentimento": analise["sentimento"],
            "score": analise["score"]
        })
    
    if not sentimentos:
        return {
            "sentimento_geral": "neutro",
            "score_medio": 0,
            "resumo": "Insuficientes dados de notícias para análise"
        }
    
    score_medio = sum(s["score"] for s in sentimentos) / len(sentimentos)
    
    if score_medio > 0.2:
        sentimento_geral = "positivo"
        resumo = "Sentimento geral positivo na carteira. Ambiente favorável."
    elif score_medio < -0.2:
        sentimento_geral = "negativo"
        resumo = "Atenção: Sentimento negativo detectado em alguns ativos."
    else:
        sentimento_geral = "neutro"
        resumo = "Sentimento neutro na carteira. Nenhum alerta crítico."
    
    return {
        "sentimento_geral": sentimento_geral,
        "score_medio": score_medio,
        "resumo": resumo,
        "detalhes": sentimentos
    }
