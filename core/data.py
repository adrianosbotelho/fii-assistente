import pandas as pd

def carregar_carteira():
    data = [
        {"ticker": "BTLG11", "valor": 10462.14, "dy": 0.0917},
        {"ticker": "VISC11", "valor": 9795.60, "dy": 0.0888},
        {"ticker": "KNCR11", "valor": 8765.63, "dy": 0.1376},
        {"ticker": "CPTS11", "valor": 8569.00, "dy": 0.1320},
        {"ticker": "XPML11", "valor": 7700.00, "dy": 0.1004},
        {"ticker": "GARE11", "valor": 7241.40, "dy": 0.1114},
        {"ticker": "MXRF11", "valor": 7096.95, "dy": 0.1238},
        {"ticker": "VGIA11", "valor": 6831.00, "dy": 0.1561},
        {"ticker": "XPCA11", "valor": 5022.00, "dy": 0.1541},
        {"ticker": "CPUR11", "valor": 2198.00, "dy": 0.0949},
    ]
    return pd.DataFrame(data)
