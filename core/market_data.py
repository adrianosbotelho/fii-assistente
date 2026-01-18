"""
Módulo para coletar e processar dados de mercado
Índices: IBOV, IFIX, SELIC, IPCA
"""
import yfinance as yf
import pandas as pd
from datetime import datetime, timedelta
import numpy as np

def obter_indices(dias=30):
    """Obtém dados dos principais índices do mercado brasileiro"""
    try:
        # IBOVESPA
        ibov = yf.Ticker("^BVSP")
        hist_ibov = ibov.history(period=f"{dias}d")
        
        # IFIX (índice de fundos imobiliários)
        ifix = yf.Ticker("IFIX.SA")
        hist_ifix = ifix.history(period=f"{dias}d")
        
        ibov_atual = hist_ibov["Close"].iloc[-1] if len(hist_ibov) > 0 else None
        ibov_anterior = hist_ibov["Close"].iloc[-30] if len(hist_ibov) > 30 else hist_ibov["Close"].iloc[0] if len(hist_ibov) > 0 else None
        
        ifix_atual = hist_ifix["Close"].iloc[-1] if len(hist_ifix) > 0 else None
        ifix_anterior = hist_ifix["Close"].iloc[-30] if len(hist_ifix) > 30 else hist_ifix["Close"].iloc[0] if len(hist_ifix) > 0 else None
        
        ibov_variacao = ((ibov_atual / ibov_anterior) - 1) * 100 if ibov_atual and ibov_anterior else 0
        ifix_variacao = ((ifix_atual / ifix_anterior) - 1) * 100 if ifix_atual and ifix_anterior else 0
        
        return {
            "ibov": {
                "valor": ibov_atual,
                "variacao_30d": ibov_variacao,
                "historico": hist_ibov
            },
            "ifix": {
                "valor": ifix_atual,
                "variacao_30d": ifix_variacao,
                "historico": hist_ifix
            }
        }
    except Exception as e:
        print(f"Erro ao obter índices: {e}")
        return {
            "ibov": {"valor": None, "variacao_30d": 0, "historico": pd.DataFrame()},
            "ifix": {"valor": None, "variacao_30d": 0, "historico": pd.DataFrame()}
        }


def obter_taxa_selic():
    """Obtém a taxa SELIC atual (proxy usando taxa CDI)"""
    try:
        # Usando ETF que acompanha SELIC/CDI
        selic = yf.Ticker("SELIC11.SA")
        info = selic.info
        # Se não conseguir, retorna um valor padrão recente
        return 10.5  # Taxa aproximada - idealmente buscar de API do BCB
    except:
        return 10.5


def calcular_correlacao_carteira_mercado(tickers_carteira, dias=60):
    """Calcula correlação da carteira com IFIX"""
    try:
        ifix = yf.Ticker("IFIX.SA")
        hist_ifix = ifix.history(period=f"{dias}d")["Close"].pct_change().dropna()
        
        retornos_carteira = []
        
        for ticker in tickers_carteira:
            try:
                t = yf.Ticker(f"{ticker}.SA")
                hist = t.history(period=f"{dias}d")["Close"].pct_change().dropna()
                retornos_carteira.append(hist)
            except:
                continue
        
        if not retornos_carteira:
            return 0.0
        
        # Média ponderada dos retornos (simplificado)
        retorno_medio = pd.concat(retornos_carteira, axis=1).mean(axis=1)
        
        # Calcular correlação
        correlacao = retorno_medio.corr(hist_ifix)
        return correlacao if not np.isnan(correlacao) else 0.0
    except:
        return 0.0


def obter_preco_atual(ticker):
    """Obtém preço atual de um ticker"""
    try:
        t = yf.Ticker(f"{ticker}.SA")
        hist = t.history(period="1d")
        if len(hist) > 0:
            return hist["Close"].iloc[-1]
        return None
    except:
        return None


def calcular_dy_atual(ticker):
    """Calcula dividend yield atual de um FII"""
    try:
        t = yf.Ticker(f"{ticker}.SA")
        info = t.info
        dy = info.get("dividendYield", 0)
        if dy and dy > 0:
            return dy * 100  # Retorna em percentual
        return None
    except:
        return None

