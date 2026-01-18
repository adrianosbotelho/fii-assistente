"""
Módulo avançado para carregar carteira de múltiplas fontes
Suporta: CSV, Google Sheets, e dados automáticos do mercado
"""
import pandas as pd
import yfinance as yf
from typing import Optional, Dict
from pathlib import Path
import os

def carregar_carteira_csv(caminho: str = "data/carteira.csv") -> pd.DataFrame:
    """Carrega carteira de arquivo CSV"""
    return pd.read_csv(caminho)


def atualizar_dados_mercado(df_carteira: pd.DataFrame, atualizar_precos: bool = True, 
                            atualizar_dividendos: bool = True) -> pd.DataFrame:
    """
    Atualiza preços atuais e dividendos dos FIIs via Yahoo Finance
    
    Args:
        df_carteira: DataFrame com colunas: Ticker, Quantidade, Preco_Medio (opcional), Dividendo_Mensal (opcional)
        atualizar_precos: Se True, atualiza preços atuais
        atualizar_dividendos: Se True, busca dividendos recentes
    
    Returns:
        DataFrame atualizado
    """
    df = df_carteira.copy()
    
    # Se não tiver preço médio, assumir que quer usar preço atual
    if "Preco_Medio" not in df.columns:
        df["Preco_Medio"] = 0
    
    precos_atuais = {}
    dividendos_mensais = {}
    
    for ticker in df["Ticker"].unique():
        try:
            t = yf.Ticker(f"{ticker}.SA")
            info = t.info
            
            # Obter preço atual
            if atualizar_precos:
                hist = t.history(period="1d")
                if len(hist) > 0:
                    preco_atual = hist["Close"].iloc[-1]
                    precos_atuais[ticker] = preco_atual
            
            # Obter dividend yield e calcular dividendo mensal
            if atualizar_dividendos:
                dy = info.get("dividendYield", 0)
                if dy and dy > 0:
                    preco_ref = precos_atuais.get(ticker, info.get("regularMarketPrice", 0))
                    if preco_ref and preco_ref > 0:
                        # Dividendo mensal = (DY anual / 12) * preço
                        dividendo_mensal = (dy / 12) * preco_ref
                        dividendos_mensais[ticker] = dividendo_mensal
                
                # Alternativa: buscar últimos dividendos pagos
                try:
                    div_history = t.dividends
                    if len(div_history) > 0:
                        # Média dos últimos 3 dividendos pagos (geralmente mensais para FIIs)
                        div_recentes = div_history.tail(3).mean()
                        if div_recentes > 0:
                            dividendos_mensais[ticker] = div_recentes
                except:
                    pass
                    
        except Exception as e:
            print(f"Erro ao atualizar {ticker}: {e}")
            continue
    
    # Atualizar DataFrame
    if atualizar_precos and precos_atuais:
        # Criar coluna com preço atual (manter Preco_Medio para histórico)
        df["Preco_Atual"] = df["Ticker"].map(precos_atuais).fillna(df.get("Preco_Medio", 0))
        # Se Preco_Medio não existir ou for 0, usar preço atual
        if "Preco_Medio" not in df.columns or df["Preco_Medio"].sum() == 0:
            df["Preco_Medio"] = df["Preco_Atual"]
    
    if atualizar_dividendos and dividendos_mensais:
        df["Dividendo_Mensal"] = df["Ticker"].map(dividendos_mensais).fillna(
            df.get("Dividendo_Mensal", 0)
        )
    
    return df


def carregar_carteira_completa(caminho_csv: Optional[str] = None, 
                               atualizar_dados: bool = True,
                               usar_preco_medio: bool = False) -> pd.DataFrame:
    """
    Carrega carteira e opcionalmente atualiza dados do mercado
    
    Args:
        caminho_csv: Caminho para arquivo CSV. Se None, usa data/carteira.csv
        atualizar_dados: Se True, busca preços e dividendos atuais do mercado
        usar_preco_medio: Se True, mantém Preco_Medio do CSV. Se False, usa preços atuais
    
    Returns:
        DataFrame da carteira processada
    """
    if caminho_csv is None:
        caminho_csv = "data/carteira.csv"
    
    # Carregar CSV base
    df = carregar_carteira_csv(caminho_csv)
    
    # Atualizar dados do mercado se solicitado
    if atualizar_dados:
        df = atualizar_dados_mercado(
            df, 
            atualizar_precos=not usar_preco_medio,
            atualizar_dividendos=True
        )
    
    # Garantir colunas necessárias
    if "Quantidade" not in df.columns:
        raise ValueError("CSV deve conter coluna 'Quantidade'")
    
    if "Preco_Medio" not in df.columns or df["Preco_Medio"].sum() == 0:
        if "Preco_Atual" in df.columns:
            df["Preco_Medio"] = df["Preco_Atual"]
        else:
            raise ValueError("CSV deve conter 'Preco_Medio' ou ativar atualizar_dados=True")
    
    if "Dividendo_Mensal" not in df.columns:
        raise ValueError("CSV deve conter 'Dividendo_Mensal' ou ativar atualizar_dados=True")
    
    return df


def carregar_carteira_minima(tickers_quantidades: Dict[str, float], 
                             atualizar_dados: bool = True) -> pd.DataFrame:
    """
    Cria carteira a partir de dicionário simples {ticker: quantidade}
    Útil para testes ou entrada manual
    
    Args:
        tickers_quantidades: Dict com {ticker: quantidade}
        atualizar_dados: Se True, busca preços e dividendos automaticamente
    
    Returns:
        DataFrame da carteira
    """
    df = pd.DataFrame([
        {"Ticker": ticker, "Quantidade": qtd}
        for ticker, qtd in tickers_quantidades.items()
    ])
    
    if atualizar_dados:
        df = atualizar_dados_mercado(df, atualizar_precos=True, atualizar_dividendos=True)
    
    return df


# Exemplo de integração com Google Sheets (requer gspread)
def carregar_carteira_google_sheets(sheet_id: str, worksheet_name: str = "Carteira",
                                    credenciais_path: Optional[str] = None) -> pd.DataFrame:
    """
    Carrega carteira do Google Sheets
    
    Requer: pip install gspread google-auth
    
    Args:
        sheet_id: ID da planilha Google (da URL)
        worksheet_name: Nome da aba
        credenciais_path: Caminho para arquivo JSON de credenciais
    
    Returns:
        DataFrame da carteira
    """
    try:
        import gspread
        from google.oauth2.service_account import Credentials
        
        scope = ['https://spreadsheets.google.com/feeds',
                 'https://www.googleapis.com/auth/drive']
        
        if credenciais_path is None:
            credenciais_path = os.getenv("GOOGLE_CREDENTIALS_PATH", "credentials.json")
        
        creds = Credentials.from_service_account_file(credenciais_path, scopes=scope)
        client = gspread.authorize(creds)
        
        sheet = client.open_by_key(sheet_id).worksheet(worksheet_name)
        data = sheet.get_all_records()
        
        df = pd.DataFrame(data)
        return atualizar_dados_mercado(df, atualizar_precos=True, atualizar_dividendos=True)
        
    except ImportError:
        raise ImportError("Para usar Google Sheets, instale: pip install gspread google-auth")
    except Exception as e:
        raise Exception(f"Erro ao carregar do Google Sheets: {e}")
