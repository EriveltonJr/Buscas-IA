def mochila(pesos, valores, capacidade):
    n = len(pesos)
    #Inicializa uma matriz (tabela) para armazenar os valores máximos alcançáveis com diferentes capacidades e diferentes números de itens.
    #A linha i e a coluna "j" representam a capacidade "j" e os primeiros "i" itens.
    dp = [[0] * (capacidade + 1) for _ in range(n + 1)]

    #Preenche a matriz dp usando programação dinâmica
    for i in range(1, n + 1):
        for j in range(1, capacidade + 1):
            #Se o peso do item for maior que a capacidade da mochila, não podemos incluí-lo, então o valor máximo até agora é o mesmo do valor máximo obtido sem este item.
            if pesos[i - 1] > j:
                dp[i][j] = dp[i - 1][j]
            else:
                #Caso contrário, temos duas opções:
                #1. Incluir o item, adicionando seu valor ao valor máximo alcançável com a capacidade restante "(j - pesos[i - 1]").
                #2. Não incluir o item e manter o valor máximo alcançável sem este item.
                dp[i][j] = max(dp[i - 1][j], valores[i - 1] + dp[i - 1][j - pesos[i - 1]])

    #O valor máximo alcançável com a capacidade total é armazenado em "dp[n][capacidade]".
    return dp[n][capacidade]

#Teste
pesos = [2, 3, 4, 5]
valores = [3, 4, 5, 6]
capacidade = 5
print("O maior valor possível que pode ser colocado na mochila é:", mochila(pesos, valores, capacidade))