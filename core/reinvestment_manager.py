"""
Módulo para gerenciar reinvestimento de dividendos e atualização de quantidades
"""
import pandas as pd
import numpy as np
from typing import Dict, List, Optional
from datetime import datetime
from pathlib import Path
from core.market_data import obter_preco_atual

def calcular_reinvestimento(df_carteira: pd.DataFrame, 
                           valores_reinvestir: Optional[Dict[str, float]] = None,
                           usar_precos_atuais: bool = True) -> pd.DataFrame:
    """
    Calcula quantas cotas podem ser compradas com os dividendos reinvestidos
    
    Args:
        df_carteira: DataFrame da carteira atual
        valores_reinvestir: Dict com {ticker: valor_a_reinvestir}. Se None, usa sugestão automática
        usar_precos_atuais: Se True, busca preços atuais do mercado
    
    Returns:
        DataFrame com informações de reinvestimento: cotas compradas, nova quantidade, etc.
    """
    df = df_carteira.copy()
    
    # Calcular renda mensal por fundo
    if "Renda_Mensal" not in df.columns:
        df["Renda_Mensal"] = df["Quantidade"] * df.get("Dividendo_Mensal", 0)
    
    renda_total = df["Renda_Mensal"].sum()
    
    # Se não especificar valores, distribuir proporcionalmente pela renda de cada fundo
    if valores_reinvestir is None:
        # Distribuir proporcionalmente à renda gerada por cada fundo
        valores_reinvestir = {}
        for _, row in df.iterrows():
            valores_reinvestir[row["Ticker"]] = row["Renda_Mensal"]
    
    # Buscar preços atuais se necessário
    if usar_precos_atuais:
        precos_atuais = {}
        for ticker in df["Ticker"].unique():
            preco = obter_preco_atual(ticker)
            if preco:
                precos_atuais[ticker] = preco
            else:
                # Se não conseguir preço atual, usar Preco_Medio
                preco_medio = df[df["Ticker"] == ticker]["Preco_Medio"].iloc[0]
                precos_atuais[ticker] = preco_medio
    else:
        precos_atuais = {row["Ticker"]: row["Preco_Medio"] for _, row in df.iterrows()}
    
    # Calcular reinvestimentos
    resultados = []
    
    for _, row in df.iterrows():
        ticker = row["Ticker"]
        valor_reinvestir = valores_reinvestir.get(ticker, 0)
        preco_atual = precos_atuais.get(ticker, row["Preco_Medio"])
        quantidade_atual = row["Quantidade"]
        
        # Calcular quantas cotas podem ser compradas
        cotas_compradas = np.floor(valor_reinvestir / preco_atual) if preco_atual > 0 else 0
        valor_utilizado = cotas_compradas * preco_atual
        valor_nao_utilizado = valor_reinvestir - valor_utilizado
        
        # Nova quantidade total
        nova_quantidade = quantidade_atual + cotas_compradas
        
        # Atualizar preço médio ponderado
        valor_investido_atual = quantidade_atual * row["Preco_Medio"]
        valor_investido_novo = cotas_compradas * preco_atual
        valor_total = valor_investido_atual + valor_investido_novo
        
        if nova_quantidade > 0:
            novo_preco_medio = valor_total / nova_quantidade
        else:
            novo_preco_medio = row["Preco_Medio"]
        
        resultados.append({
            "Ticker": ticker,
            "Quantidade_Atual": quantidade_atual,
            "Valor_Reinvestir": valor_reinvestir,
            "Preco_Atual": preco_atual,
            "Cotas_Compradas": int(cotas_compradas),
            "Valor_Utilizado": valor_utilizado,
            "Valor_Nao_Utilizado": valor_nao_utilizado,
            "Nova_Quantidade": nova_quantidade,
            "Preco_Medio_Anterior": row["Preco_Medio"],
            "Novo_Preco_Medio": novo_preco_medio,
            "Renda_Mensal_Atual": row["Renda_Mensal"]
        })
    
    return pd.DataFrame(resultados)


def gerar_carteira_atualizada(df_carteira: pd.DataFrame, 
                              df_reinvestimento: pd.DataFrame) -> pd.DataFrame:
    """
    Gera novo DataFrame da carteira com quantidades atualizadas após reinvestimento
    
    Args:
        df_carteira: DataFrame original da carteira
        df_reinvestimento: DataFrame resultante de calcular_reinvestimento()
    
    Returns:
        DataFrame da carteira atualizada
    """
    df_nova = df_carteira.copy()
    
    # Atualizar quantidades e preços médios
    for _, reinv in df_reinvestimento.iterrows():
        ticker = reinv["Ticker"]
        idx = df_nova[df_nova["Ticker"] == ticker].index[0]
        
        df_nova.at[idx, "Quantidade"] = reinv["Nova_Quantidade"]
        df_nova.at[idx, "Preco_Medio"] = reinv["Novo_Preco_Medio"]
    
    # Recalcular valores investidos e rendas
    df_nova["Valor_Investido"] = df_nova["Quantidade"] * df_nova["Preco_Medio"]
    if "Dividendo_Mensal" in df_nova.columns:
        df_nova["Renda_Mensal"] = df_nova["Quantidade"] * df_nova["Dividendo_Mensal"]
    
    return df_nova


def salvar_carteira_atualizada(df_carteira_atualizada: pd.DataFrame, 
                               caminho_original: str = "data/carteira.csv",
                               criar_backup: bool = True) -> str:
    """
    Salva carteira atualizada e opcionalmente cria backup
    
    Args:
        df_carteira_atualizada: DataFrame da carteira atualizada
        caminho_original: Caminho do arquivo original
        criar_backup: Se True, cria backup antes de sobrescrever
    
    Returns:
        Caminho do arquivo salvo
    """
    path_original = Path(caminho_original)
    
    # Criar backup se solicitado
    if criar_backup and path_original.exists():
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        backup_path = path_original.parent / f"{path_original.stem}_backup_{timestamp}{path_original.suffix}"
        import shutil
        shutil.copy(path_original, backup_path)
    
    # Preparar CSV simplificado (apenas Ticker e Quantidade)
    df_para_salvar = df_carteira_atualizada[["Ticker", "Quantidade"]].copy()
    
    # Salvar
    df_para_salvar.to_csv(path_original, index=False)
    
    return str(path_original)


def gerar_relatorio_reinvestimento(df_reinvestimento: pd.DataFrame) -> str:
    """
    Gera relatório em texto do reinvestimento realizado
    
    Args:
        df_reinvestimento: DataFrame resultante de calcular_reinvestimento()
    
    Returns:
        String com relatório formatado
    """
    total_cotas = df_reinvestimento["Cotas_Compradas"].sum()
    total_investido = df_reinvestimento["Valor_Utilizado"].sum()
    total_nao_utilizado = df_reinvestimento["Valor_Nao_Utilizado"].sum()
    
    relatorio = f"""
╔═══════════════════════════════════════════════════════════════╗
║         RELATÓRIO DE REINVESTIMENTO DE DIVIDENDOS            ║
╚═══════════════════════════════════════════════════════════════╝

📅 Data: {datetime.now().strftime("%d/%m/%Y %H:%M")}

💰 RESUMO GERAL:
   • Total em dividendos reinvestidos: R$ {total_investido:,.2f}
   • Total de cotas compradas: {int(total_cotas)}
   • Valor não utilizado (sobra): R$ {total_nao_utilizado:,.2f}

📊 DETALHAMENTO POR FUNDO:
"""
    
    for _, row in df_reinvestimento.iterrows():
        if row["Cotas_Compradas"] > 0 or row["Valor_Reinvestir"] > 0:
            relatorio += f"""
   {row['Ticker']}:
      • Quantidade anterior: {row['Quantidade_Atual']:.0f} cotas
      • Valor reinvestido: R$ {row['Valor_Reinvestir']:,.2f}
      • Cotas compradas: {int(row['Cotas_Compradas'])} (@ R$ {row['Preco_Atual']:,.2f})
      • Nova quantidade: {row['Nova_Quantidade']:.0f} cotas
      • Preço médio atualizado: R$ {row['Novo_Preco_Medio']:,.2f}
"""
    
    relatorio += "\n✅ Carteira atualizada com sucesso!\n"
    
    return relatorio


def calcular_distribuicao_reinvestimento(df_carteira: pd.DataFrame, 
                                        estrategia: str = "proporcional") -> Dict[str, float]:
    """
    Calcula distribuição sugerida dos dividendos para reinvestimento
    
    Args:
        df_carteira: DataFrame da carteira
        estrategia: "proporcional", "yield_alto", "diversificacao"
    
    Returns:
        Dict com {ticker: valor_a_reinvestir}
    """
    renda_total = df_carteira["Renda_Mensal"].sum()
    
    if estrategia == "proporcional":
        # Distribui proporcionalmente à renda gerada
        distribuicao = {}
        for _, row in df_carteira.iterrows():
            if renda_total > 0:
                distribuicao[row["Ticker"]] = row["Renda_Mensal"]
            else:
                distribuicao[row["Ticker"]] = 0
        return distribuicao
    
    elif estrategia == "yield_alto":
        # Prioriza fundos com maior yield
        df_sorted = df_carteira.sort_values("Yield_Mensal", ascending=False)
        pesos = df_sorted["Yield_Mensal"] / df_sorted["Yield_Mensal"].sum()
        distribuicao = {}
        for idx, (_, row) in enumerate(df_sorted.iterrows()):
            distribuicao[row["Ticker"]] = renda_total * pesos.iloc[idx]
        return distribuicao
    
    elif estrategia == "diversificacao":
        # Prioriza fundos com menor % do patrimônio (diversificar)
        df_carteira["Pct_Patrimonio"] = (df_carteira["Valor_Investido"] / df_carteira["Valor_Investido"].sum()) * 100
        pesos = 1 / (df_carteira["Pct_Patrimonio"] + 1)  # Inverso da concentração
        pesos_normalizados = pesos / pesos.sum()
        distribuicao = {}
        for _, row in df_carteira.iterrows():
            distribuicao[row["Ticker"]] = renda_total * pesos_normalizados[row.name]
        return distribuicao
    
    else:
        # Default: proporcional
        return calcular_distribuicao_reinvestimento(df_carteira, "proporcional")
