import time

class No:
    def __init__(self, estado, pai=None, acao=None, custo=0, heuristica=0, tipo_heuristica=""):
        self.estado = estado
        self.pai = pai
        self.acao = acao
        self.custo = custo
        self.heuristica = heuristica
        self.tipo_heuristica = tipo_heuristica

    def __repr__(self):
        return f"Estado final = {self.estado}, Custo = {self.custo}, Heuristica={self.tipo_heuristica}"


class Grafo:
    def __init__(self):
        self.grafo = {
            'Arad': {'Zerind': 75, 'Sibiu': 140, 'Timisoara': 118},
            'Zerind': {'Arad': 75, 'Oradea': 71},
            'Oradea': {'Zerind': 71, 'Sibiu': 151},
            'Sibiu': {'Arad': 140, 'Oradea': 151, 'Fagaras': 99, 'Rimnicu': 80},
            'Timisoara': {'Arad': 118, 'Lugoj': 111},
            'Lugoj': {'Timisoara': 111, 'Mehadia': 70},
            'Mehadia': {'Lugoj': 70, 'Drobeta': 75},
            'Drobeta': {'Mehadia': 75, 'Craiova': 120},
            'Craiova': {'Drobeta': 120, 'Rimnicu': 146, 'Pitesti': 138},
            'Rimnicu': {'Sibiu': 80, 'Craiova': 146, 'Pitesti': 97},
            'Fagaras': {'Sibiu': 99, 'Bucareste': 211},
            'Pitesti': {'Rimnicu': 97, 'Craiova': 138, 'Bucareste': 101},
            'Bucareste': {'Fagaras': 211, 'Pitesti': 101, 'Giurgiu': 90, 'Urziceni': 85},
            'Giurgiu': {'Bucareste': 90},
            'Urziceni': {'Bucareste': 85, 'Hirsova': 98, 'Vaslui': 142},
            'Hirsova': {'Urziceni': 98, 'Eforie': 86},
            'Eforie': {'Hirsova': 86},
            'Vaslui': {'Urziceni': 142, 'Iasi': 92},
            'Iasi': {'Vaslui': 92, 'Neamt': 87},
            'Neamt': {'Iasi': 87}
        }

    def acoes(self, estado):
        return list(self.grafo[estado].keys())

    def resultado(self, estado, acao):
        return acao

    def custo_caminho(self, custo_ate_agora, estado1, acao, estado2):
        return custo_ate_agora + self.grafo[estado1][estado2]

    def heuristica(self, estado, estado_objetivo, tipo_heuristica):
        coordenadas = {
            'Arad': (91, 492),
            'Zerind': (75, 385),
            'Oradea': (123, 365),
            'Sibiu': (207, 420),
            'Timisoara': (75, 375),
            'Lugoj': (45, 329),
            'Mehadia': (37, 297),
            'Drobeta': (39, 267),
            'Craiova': (115, 265),
            'Rimnicu': (195, 315),
            'Fagaras': (215, 385),
            'Pitesti': (225, 320),
            'Bucareste': (270, 385),
            'Giurgiu': (320, 375),
            'Urziceni': (350, 305),
            'Hirsova': (395, 305),
            'Eforie': (405, 335),
            'Vaslui': (470, 300),
            'Iasi': (510, 300),
            'Neamt': (590, 300)
        }
        x1, y1 = coordenadas[estado]
        x2, y2 = coordenadas[estado_objetivo]
        distancia = abs(x1 - x2) + abs(y1 - y2)
        if tipo_heuristica == "Manhattan":
            return distancia
        elif tipo_heuristica == "Euclidiana":
            return ((x1 - x2) ** 2 + (y1 - y2) ** 2) ** 0.5
        else:
            raise ValueError("Heurística não reconhecida")


def busca_largura(problema, estado_inicial, estado_objetivo, tipo_heuristica):
    fronteira = [No(estado_inicial, tipo_heuristica=tipo_heuristica)]
    explorado = set()

    while fronteira:
        no = fronteira.pop(0)
        estado = no.estado

        if estado == estado_objetivo:
            return no

        explorado.add(estado)

        for acao in problema.acoes(estado):
            estado_filho = problema.resultado(estado, acao)
            custo_filho = no.custo + problema.grafo[estado][estado_filho]
            filho = No(estado_filho, no, acao, custo=custo_filho, heuristica=problema.heuristica(estado_filho, estado_objetivo, no.tipo_heuristica), tipo_heuristica=no.tipo_heuristica)
            if estado_filho not in explorado and not any(n.estado == estado_filho for n in fronteira):
                fronteira.append(filho)

    return None


def busca_profundidade(problema, estado_inicial, estado_objetivo, tipo_heuristica):
    fronteira = [No(estado_inicial, tipo_heuristica=tipo_heuristica)]
    explorado = set()

    while fronteira:
        no = fronteira.pop()
        estado = no.estado

        if estado == estado_objetivo:
            return no

        explorado.add(estado)

        for acao in problema.acoes(estado):
            estado_filho = problema.resultado(estado, acao)
            custo_filho = no.custo + problema.grafo[estado][estado_filho]
            filho = No(estado_filho, no, acao, custo=custo_filho, heuristica=problema.heuristica(estado_filho, estado_objetivo, no.tipo_heuristica), tipo_heuristica=no.tipo_heuristica)
            if estado_filho not in explorado and not any(n.estado == estado_filho for n in fronteira):
                fronteira.append(filho)

    return None


def busca_profundidade_limitada(problema, estado_inicial, estado_objetivo, limite_profundidade, tipo_heuristica):
    def r_dls(no, problema, estado_objetivo, limite_profundidade):
        estado = no.estado

        if estado == estado_objetivo:
            return no

        if limite_profundidade == 0:
            return 'cutoff'

        cutoff_occurred = False

        for acao in problema.acoes(estado):
            estado_filho = problema.resultado(estado, acao)
            custo_filho = no.custo + problema.grafo[estado][estado_filho]
            filho = No(estado_filho, no, acao, custo=custo_filho, heuristica=problema.heuristica(estado_filho, estado_objetivo, no.tipo_heuristica), tipo_heuristica=no.tipo_heuristica)
            resultado = r_dls(filho, problema, estado_objetivo, limite_profundidade - 1)
            if resultado == 'cutoff':
                cutoff_occurred = True
            elif resultado is not None:
                return resultado

        return 'cutoff' if cutoff_occurred else None

    return r_dls(No(estado_inicial, tipo_heuristica=tipo_heuristica), problema, estado_objetivo, limite_profundidade)


def busca_aprofundamento_iterativo(problema, estado_inicial, estado_objetivo, tipo_heuristica):
    limite_maximo = 1000  # Define um limite máximo grande o suficiente
    for limite_profundidade in range(1, limite_maximo):
        resultado = busca_profundidade_limitada(problema, estado_inicial, estado_objetivo, limite_profundidade, tipo_heuristica)
        if resultado != 'cutoff':
            return resultado


def busca_custo_uniforme(problema, estado_inicial, estado_objetivo, tipo_heuristica):
    fronteira = [(0, No(estado_inicial, tipo_heuristica=tipo_heuristica))]
    explorado = set()

    while fronteira:
        custo, no = fronteira.pop(0)
        estado = no.estado

        if estado == estado_objetivo:
            return no

        explorado.add(estado)

        for acao in problema.acoes(estado):
            estado_filho = problema.resultado(estado, acao)
            custo_filho = no.custo + problema.grafo[estado][estado_filho]
            filho = No(estado_filho, no, acao, custo=custo_filho, heuristica=problema.heuristica(estado_filho, estado_objetivo, no.tipo_heuristica), tipo_heuristica=no.tipo_heuristica)
            if estado_filho not in explorado and not any((c, n.estado) in fronteira for c, n in fronteira):
                fronteira.append((custo_filho, filho))
            elif any((c, n.estado) in fronteira for c, n in fronteira):
                no_existente = next(n for c, n in fronteira if n.estado == estado_filho)
                if custo_filho < no_existente.custo:
                    no_existente.custo = custo_filho
                    no_existente.pai = no
                    no_existente.acao = acao

        fronteira.sort(key=lambda x: x[0])

    return None


def busca_gulosa(problema, estado_inicial, estado_objetivo, tipo_heuristica):
    fronteira = [(problema.heuristica(estado_inicial, estado_objetivo, tipo_heuristica), No(estado_inicial, tipo_heuristica=tipo_heuristica))]
    explorado = set()

    while fronteira:
        custo_heuristico, no = fronteira.pop(0)
        estado = no.estado

        if estado == estado_objetivo:
            return no

        explorado.add(estado)

        for acao in problema.acoes(estado):
            estado_filho = problema.resultado(estado, acao)
            custo_filho = no.custo + problema.grafo[estado][estado_filho]
            filho = No(estado_filho, no, acao, custo=custo_filho, heuristica=problema.heuristica(estado_filho, estado_objetivo, tipo_heuristica), tipo_heuristica=tipo_heuristica)
            if estado_filho not in explorado and not any((h, n.estado) in fronteira for h, n in fronteira):
                fronteira.append((custo_heuristico, filho))

        fronteira.sort(key=lambda x: x[0])

    return None


def busca_a_estrela(problema, estado_inicial, estado_objetivo, tipo_heuristica):
    fronteira = [(0, problema.heuristica(estado_inicial, estado_objetivo, tipo_heuristica), No(estado_inicial, tipo_heuristica=tipo_heuristica))]
    explorado = set()

    while fronteira:
        custo, custo_heuristico, no = fronteira.pop(0)
        estado = no.estado

        if estado == estado_objetivo:
            return no

        explorado.add(estado)

        for acao in problema.acoes(estado):
            estado_filho = problema.resultado(estado, acao)
            custo_caminho = no.custo + problema.grafo[estado][estado_filho]
            custo_heuristico = problema.heuristica(estado_filho, estado_objetivo, tipo_heuristica)
            custo_total = custo_caminho + custo_heuristico
            if estado_filho not in explorado and not any((c, h, n.estado) in fronteira for c, h, n in fronteira):
                filho = No(estado_filho, no, acao, custo=custo_caminho, heuristica=custo_heuristico, tipo_heuristica=tipo_heuristica)
                fronteira.append((custo_caminho, custo_heuristico, filho))
            elif any((c, h, n.estado) in fronteira for c, h, n in fronteira):
                no_existente = next(n for c, h, n in fronteira if n.estado == estado_filho)
                if custo_total < no_existente.custo + no_existente.heuristica:
                    no_existente.custo = custo_caminho
                    no_existente.pai = no
                    no_existente.acao = acao

        fronteira.sort(key=lambda x: x[0])

    return None


if __name__ == "__main__":
    grafo = Grafo()
    estado_inicial = 'Arad'
    estado_objetivo = 'Bucareste'

    print("Estado Inicial para todos:", estado_inicial)
    print("Estado Objetivo para todos:", estado_objetivo)

    # Busca em Largura
    
    print("\nBusca em Largura : ")
    solucao_bfs_manhattan = busca_largura(grafo, estado_inicial, estado_objetivo, tipo_heuristica="Manhattan")
    print(solucao_bfs_manhattan)

    # Busca em Profundidade

    print("\nBusca em Profundidade : ")
    solucao_dfs_euclidiana = busca_profundidade(grafo, estado_inicial, estado_objetivo, tipo_heuristica="Euclidiana")
    print(solucao_dfs_euclidiana)

    # Busca em Profundidade Limitada

    print("\nBusca em Profundidade Limitada (Limite de Profundidade = 5) : ")
    solucao_dls_manhattan = busca_profundidade_limitada(grafo, estado_inicial, estado_objetivo, 5, tipo_heuristica="Manhattan")
    print(solucao_dls_manhattan)

    # Busca em Aprofundamento Iterativo

    print("\nBusca em Aprofundamento Iterativo : ")
    solucao_ids_euclidiana = busca_aprofundamento_iterativo(grafo, estado_inicial, estado_objetivo, tipo_heuristica="Euclidiana")
    print(solucao_ids_euclidiana)

    #Busca de Custo Uniforme

    print("\nBusca de Custo Uniforme : ")
    solucao_ucs_manhattan = busca_custo_uniforme(grafo, estado_inicial, estado_objetivo, tipo_heuristica="Manhattan")
    print(solucao_ucs_manhattan)

    #Busca Gulosa

    print("\nBusca Gulosa : ")
    solucao_gulosa_euclidiana = busca_gulosa(grafo, estado_inicial, estado_objetivo, tipo_heuristica="Euclidiana")
    print(solucao_gulosa_euclidiana)

    #Busca A*

    print("\nBusca A* : ")
    solucao_a_estrela_manhattan = busca_a_estrela(grafo, estado_inicial, estado_objetivo, tipo_heuristica="Manhattan")
    print(solucao_a_estrela_manhattan)