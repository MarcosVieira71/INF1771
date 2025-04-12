from queue import PriorityQueue
from utils import *
from map import map, time, events


x = len(map[0]) 
y = len(map)


def get_value(c):
    
    if c in time:
        return time[c]
    elif c in events:
        return 1
    else:
        return -1

def get_char_from_map(mapa, coord):
    return mapa[coord[1]][coord[0]]

def get_value_from_map(mapa, coord):
    return get_value(get_char_from_map(mapa, coord))


def add_valid_pos(nb, mapa, coord):        
    if get_value_from_map(mapa, coord) > -1:
        nb.append(coord)

def get_neighborhood(mapa, coord):
    
    nb = []
    if coord[0] == 0:
        add_valid_pos(nb, mapa, (coord[0] + 1, coord[1]))
    
    elif coord[0] == x - 1:
        add_valid_pos(nb, mapa, (coord[0] - 1, coord[1]))
    
    else:    
        add_valid_pos(nb, mapa, (coord[0] + 1, coord[1]))
        add_valid_pos(nb, mapa, (coord[0] - 1, coord[1]))
    

    if coord[1] == 0:
        add_valid_pos(nb, mapa, (coord[0], coord[1] + 1))
    
    elif coord[1] == y - 1:
        add_valid_pos(nb, mapa, (coord[0], coord[1] - 1))
    
    else:    
        add_valid_pos(nb, mapa, (coord[0], coord[1] + 1))
        add_valid_pos(nb, mapa, (coord[0], coord[1] - 1))
    
    return nb

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


def busca_a_estrela(mapa, start, end):

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

        for nb in get_neighborhood(mapa, current):
            tentative_g_score = g + get_value_from_map(mapa, nb)

            if nb not in g_score or tentative_g_score < g_score[nb]:
                came_from[nb] = current
                g_score[nb] = tentative_g_score
                f_score[nb] = g_score[nb] + manhattan_distance(nb, end)
                open_list.put((f_score[nb], g_score[nb], nb))

    return None

def caminho_final(mapa, events, personagens= None):
    ordem = escolher_ordem(events)
    path_total = []
    for i in range(len(ordem) - 1):
        inicio = events[ordem[i]]
        fim = events[ordem[i + 1]]
        path_total += busca_a_estrela(mapa, inicio, fim)
    return path_total