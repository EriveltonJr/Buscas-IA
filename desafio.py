def mochila_gulosa(pesos, valores, capacidade):
    n = len(pesos)
    #Calcula a taxa de valor por peso para cada item
    taxa = [(valores[i] / pesos[i], pesos[i], valores[i]) for i in range(n)]
    #Ordena os itens pela taxa em ordem decrescente
    taxa.sort(reverse=True)

    valor_total = 0 
    peso_total = 0   

    # Percorre os itens ordenados pela taxa
    for taxa_valor_peso, peso, valor in taxa:
        if peso_total + peso <= capacidade:
            #Se ainda houver espaço na mochila, adiciona o item
            valor_total += valor
            peso_total += peso

    return valor_total

# Teste
pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidade = 5
print("O maior valor possível que pode ser colocado na mochila é:", mochila_gulosa(pesos, valores, capacidade))