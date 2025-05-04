import random
import math
from queue import PriorityQueue
from utils import manhattan_distance
from map.Map import Map

def calcular_custo(ordem, dist_floyd):
    total = 0
    for i in range(len(ordem) - 1):
        a, b = ordem[i], ordem[i + 1]
        custo = dist_floyd[a][b]
        if custo == float('inf'):
            return float('inf')
        total += custo
    return total

def gerar_vizinho(ordem):
    vizinho = ordem[:]
    if random.random() < 0.5:
        i, j = random.sample(range(1, len(ordem) - 1), 2)
        vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
    else:
        i, j = sorted(random.sample(range(1, len(ordem) - 1), 2))
        vizinho[i:j+1] = list(reversed(vizinho[i:j+1]))
    return vizinho

def escolher_ordem(events):
    start_event = '0'
    end_event = 'P'
    meio = [e for e in events if e not in [start_event, end_event]]
    random.shuffle(meio)
    return [start_event] + meio + [end_event]

def simulated_annealing(events, dist_floyd, temp_inicial=100_000, temp_final=1e-3, alpha=0.9993, iter_por_temp=1500, log=True):
    ordem_atual = escolher_ordem(events)
    custo_atual = calcular_custo(ordem_atual, dist_floyd)

    melhor_ordem = ordem_atual[:]
    melhor_custo = custo_atual

    temp = temp_inicial
    iter_total = 0

    while temp > temp_final:
        for _ in range(iter_por_temp):
            iter_total += 1
            vizinho = gerar_vizinho(ordem_atual)
            custo_vizinho = calcular_custo(vizinho, dist_floyd)
            delta = custo_vizinho - custo_atual

            if delta < 0 or random.random() < math.exp(-delta / temp):
                ordem_atual = vizinho
                custo_atual = custo_vizinho

                if custo_atual < melhor_custo:
                    melhor_ordem = ordem_atual[:]
                    melhor_custo = custo_atual
                    if log:
                        print(f"[Iter {iter_total}] >>> NOVO MELHOR <<< custo={melhor_custo:.2f}")

        temp *= alpha

    if log:
        print("Busca encerrada.\nMelhor ordem encontrada:", melhor_ordem)
        print("Melhor custo final:", melhor_custo)

    return melhor_ordem

def busca_a_estrela(mapa: Map, start, end):
    open_list = PriorityQueue()
    open_list.put((0 + manhattan_distance(start, end), 0, start))
    came_from = {}
    g_score = {start: 0}
    f_score = {start: manhattan_distance(start, end)}

    while not open_list.empty():
        _, g, current = open_list.get()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for nb in mapa.get_neighbors(current):
            tentative_g_score = g + mapa.get_value(nb)

            if nb not in g_score or tentative_g_score < g_score[nb]:
                came_from[nb] = current
                g_score[nb] = tentative_g_score
                f_score[nb] = g_score[nb] + manhattan_distance(nb, end)
                open_list.put((f_score[nb], g_score[nb], nb))

    return None

def final_path(mapa: Map, events, dist_floyd, personagens=None):
    order = simulated_annealing(events, dist_floyd)
    print(order)
    path_total = []

    for i in range(len(order) - 1):
        inicio = events[order[i]]
        fim = events[order[i + 1]]
        caminho = busca_a_estrela(mapa, inicio, fim)
        if caminho:
            if i != 0:
                path_total += caminho[1:]
            else: path_total += caminho
        else:
            print(f"Nenhum caminho encontrado de {order[i]} para {order[i+1]}")

    return path_total[1:]

def calcular_custo_trajeto(path, mapa):
    if not path:
        return float('inf')
    
    return sum(mapa.get_value(pos) for pos in path[1:])

def gerar_matriz_distancias(mapa, eventos):
    dist = {i: {} for i in eventos}

    for i in eventos:
        for j in eventos:
            if i == j:
                dist[i][j] = 0
            else:
                caminho = busca_a_estrela(mapa, eventos[i], eventos[j])
                dist[i][j] = calcular_custo_trajeto(caminho, mapa)
    
    return dist

def floyd_warshall(dist):
    eventos = list(dist.keys())
    for k in eventos:
        for i in eventos:
            for j in eventos:
                if dist[i][j] > dist[i][k] + dist[k][j]:
                    dist[i][j] = dist[i][k] + dist[k][j]
    return dist

def validar_caminhos(mapa, eventos, dist_floyd):
    for i in eventos:
        for j in eventos:
            if i == j:
                continue
            caminho_a_estrela = busca_a_estrela(mapa, eventos[i], eventos[j])
            custo_a_estrela = calcular_custo_trajeto(caminho_a_estrela, mapa)
            if custo_a_estrela != dist_floyd[i][j]:
                print(f"Caminho {i} → {j} | A*: {custo_a_estrela} | Floyd: {dist_floyd[i][j]}")
