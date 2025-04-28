from algorithm.charactersSelection import genetic_algorithm
from algorithm.Character import Character
from algorithm.pathFind import final_path
from interface.View import View
from map.Map import Map
from map.mapConstants import CHARACTER_POWER, COLORS
from utils import event_cost

from PySide6.QtWidgets import QApplication

import sys


def main():
    map = Map("data/mapa_skyrim.txt")
    
    charactersIds = [
        "Dragonborn",
        "Ralof",
        "Lydia",
        "Farengar Secret Fire",
        "Balgruuf",
        "Delphine"
    ] 

    characters = [Character(i, CHARACTER_POWER[i]) for i in charactersIds]

    events = map.eventsCoord
    eventsFiltered = {key: events[key] for key in events if key != "0" and key != "P"}
    population = genetic_algorithm(eventsFiltered, characters)
                        
    print(population, "POPULACAO GERADA")

    sum = 0
    for idx, el in enumerate(eventsFiltered.keys()):
        sum += event_cost(el, population[idx])
    print(sum, "CUSTO PERSONAGENS")
    
    d = {}
    for i in population:
        for j in i:
            if j not in d:
                d[j] = 1
            else:
                d[j] += 1
    print(d, "DICIONARIO PERSONAGENS USADOS")

    path = final_path(map, events)

    valor = 0
    for i in path:
        valor += map.get_value(i)
    print(f"Caminho encontrado com {len(path)} passos:  e valor {valor}")

    app = QApplication(sys.argv)
    janela = View(map, COLORS, path)
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
