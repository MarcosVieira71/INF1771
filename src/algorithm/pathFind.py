from queue import PriorityQueue
from utils import manhattan_distance
from map.Map import Map

import random
import math
import itertools

def calcular_custo(ordem, events):
    total = 0
    for i in range(len(ordem) - 1):
        total += manhattan_distance(events[ordem[i]], events[ordem[i + 1]])
    return total

def gerar_vizinho(ordem):
    i, j = random.sample(range(1, len(ordem) - 1), 2)
    vizinho = ordem[:]
    vizinho[i], vizinho[j] = vizinho[j], vizinho[i]
    return vizinho

def simulated_annealing(events, temp_inicial=100000, temp_final=1e-6, alpha=0.9999, iter_por_temp=500):
    ordem_atual = escolher_ordem(events)
    custo_atual = calcular_custo(ordem_atual, events)

    melhor_ordem = ordem_atual[:]
    melhor_custo = custo_atual

    temp = temp_inicial

    while temp > temp_final:
        for _ in range(iter_por_temp):
            vizinho = gerar_vizinho(ordem_atual)
            custo_vizinho = calcular_custo(vizinho, events)
            delta = custo_vizinho - custo_atual

            if delta < 0 or random.random() < math.exp(-delta / temp):
                ordem_atual = vizinho
                custo_atual = custo_vizinho

                if custo_atual < melhor_custo:
                    melhor_ordem = ordem_atual[:]
                    melhor_custo = custo_atual

        temp *= alpha

    return melhor_ordem


def escolher_ordem(events):
    ordem_visita = []
    visitados = set()

    start_event = '0'
    end_event = 'P'

    current_event = start_event
    current_pos = events[current_event]
    visitados.add(current_event)
    ordem_visita.append(current_event)

    while len(visitados) < len(events) - 1:
        proximo_evento = None
        menor_distancia = float('inf')

        for evento, pos in events.items():
            if evento not in visitados and evento != end_event:
                distancia = manhattan_distance(current_pos, pos)
                if distancia < menor_distancia:
                    menor_distancia = distancia
                    proximo_evento = evento

        if proximo_evento is None:
            break

        visitados.add(proximo_evento)
        ordem_visita.append(proximo_evento)
        current_pos = events[proximo_evento]

    ordem_visita.append(end_event)
    return ordem_visita


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


def caminho_final(mapa: Map, events, personagens=None):
    #ordem = simulated_annealing(events)
    #MELHOR ORDEM ENCONTRADA EM VARIAS RODADAS DE SIMULATED ANNEALING:
    ordem = ["0", "B", "K", "J", "I", "8", "6", "4", "7", "2", "1", "3", "G", "5", "C", "O", "D", "E", "H", "9", "P"]
    #print(ordem, "rodou simmulated")
    path_total = []

    for i in range(len(ordem) - 1):
        inicio = events[ordem[i]]
        fim = events[ordem[i + 1]]
        caminho = busca_a_estrela(mapa, inicio, fim)
        if caminho:
            if i != 0:
                path_total += caminho[1:]
            else: path_total += caminho
        else:
            print(f"Nenhum caminho encontrado de {ordem[i]} para {ordem[i+1]}")

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
