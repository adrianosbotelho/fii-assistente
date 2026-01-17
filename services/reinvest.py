def sugestao_reinvestimento(dividendo, regras):
    total = sum(regras.values())
    sugestao = {}

    for ativo, peso in regras.items():
        sugestao[ativo] = round(dividendo * (peso / total), 2)

    return sugestao
