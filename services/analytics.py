import yfinance as yf

def calcular_renda(carteira):
    renda = 0

    for _, row in carteira.iterrows():
        ticker = row["ticker"] + ".SA"
        qtd = row["quantidade"]

        ativo = yf.Ticker(ticker)
        info = ativo.info

        dy = info.get("dividendYield") or 0
        preco = ativo.history(period="1d")["Close"].iloc[-1]

        renda += qtd * preco * dy / 12

    return round(renda, 2)
