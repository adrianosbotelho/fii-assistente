def simular_benchmark(valor_inicial, taxa_anual, meses):
    mensal = (1 + taxa_anual) ** (1/12) - 1
    valores = []
    valor = valor_inicial

    for mes in range(1, meses + 1):
        valor *= (1 + mensal)
        valores.append({"Mês": mes, "Valor": valor})

    return valores
