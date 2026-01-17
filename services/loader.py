import pandas as pd

def carregar_carteira():
    return pd.read_csv("config/carteira.csv")
