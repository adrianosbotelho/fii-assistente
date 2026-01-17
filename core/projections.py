import pandas as pd

def projetar_renda(carteira, meses=60, reinvestir=True):
    patrimonio = carteira["valor"].sum()
    dy_medio = (carteira["valor"] * carteira["dy"]).sum() / patrimonio

    renda_mensal = patrimonio * dy_medio / 12

    historico = []

    for mes in range(1, meses + 1):
        historico.append({
            "Mês": mes,
            "Patrimônio": patrimonio,
            "Renda Mensal": renda_mensal
        })

        if reinvestir:
            patrimonio += renda_mensal
            renda_mensal = patrimonio * dy_medio / 12

    return pd.DataFrame(historico)
