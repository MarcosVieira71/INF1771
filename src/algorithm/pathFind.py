import random
import math
from queue import PriorityQueue
from utils import manhattan_distance
from map.Map import Map

def calcular_custo(ordem, distanceMatrix):
    total = 0
    for i in range(len(ordem) - 1):
        a, b = ordem[i], ordem[i + 1]
        custo = distanceMatrix[a][b]
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

def simulated_annealing(events, distanceMatrix, temp_inicial=100_000, temp_final=1e-3, alpha=0.9993, iter_por_temp=100):
    ordem_atual = escolher_ordem(events)
    custo_atual = calcular_custo(ordem_atual, distanceMatrix)

    melhor_ordem = ordem_atual[:]
    melhor_custo = custo_atual

    temp = temp_inicial
    iter_total = 0

    while temp > temp_final:
        for _ in range(iter_por_temp):
            iter_total += 1
            vizinho = gerar_vizinho(ordem_atual)
            custo_vizinho = calcular_custo(vizinho, distanceMatrix)
            delta = custo_vizinho - custo_atual

            if delta < 0 or random.random() < math.exp(-delta / temp):
                ordem_atual = vizinho
                custo_atual = custo_vizinho

                if custo_atual < melhor_custo:
                    melhor_ordem = ordem_atual[:]
                    melhor_custo = custo_atual
                    print(f"[Iter {iter_total}] >>> NOVO MELHOR <<< custo = {melhor_custo:.2f}")

        temp *= alpha

    print("Busca encerrada.\n\nMelhor ordem encontrada:", melhor_ordem)

    return melhor_ordem

def busca_a_estrela(map, start, end):
    queue = PriorityQueue()
    queue.put((0 + manhattan_distance(start, end), 0, start))
    came_from = {}
    realCost = {start: 0}

    while not queue.empty():
        _, cost, current = queue.get()

        if current == end:
            path = []
            while current in came_from:
                path.append(current)
                current = came_from[current]
            path.append(start)
            path.reverse()
            return path

        for nb in map.get_neighbors(current):
            newRealCost = cost + map.get_value(nb)

            if nb not in realCost or newRealCost < realCost[nb]:
                came_from[nb] = current
                realCost[nb] = newRealCost
                priority = newRealCost + manhattan_distance(nb, end)
                queue.put((priority, newRealCost, nb))

    return None


def final_path(mapa: Map, events, distanceMatrix):
    order = simulated_annealing(events, distanceMatrix)
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
    
    custo = calcular_custo_trajeto(path_total, mapa)

    return custo, path_total[1:]

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
