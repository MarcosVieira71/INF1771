from algorithm.Character import Character
from algorithm.pathFind import final_path, gerar_matriz_distancias
from algorithm.charactersSelection import genetic_algorithm

from map.Map import Map
from map.mapConstants import COLORS, CHARACTER_POWER

from interface.View import View
from PySide6.QtWidgets import QApplication
import sys



def main():
    map = Map("data/mapa_skyrim.txt")
    eventos = map.eventsCoord

    print("Gerando matriz de distâncias entre eventos (demora)")
    dist_a_estrela = gerar_matriz_distancias(map, eventos)
    print("Início da busca pelo melhor caminho")
    custoPath, caminho = final_path(map, eventos, dist_a_estrela)
    print(f"Caminho encontrado com {len(caminho)} passos e custo de {custoPath} Min.\n")

    characters = [Character(i) for i in list(CHARACTER_POWER.keys())]
    eventsFiltered = {key: eventos[key] for key in eventos if key != "0" and key != "P"}
    print("Início da busca por melhor combinatória de personagens (PARTE MAIS DEMORADA)")
    custoCombinatoria, population = genetic_algorithm(eventsFiltered, characters)
    print(f"\nMelhor combinatória encontrada: {population}")
    print(f"Custo de combinatória encontrado com valor de {custoCombinatoria} Min.")
    
    custoTotal = custoCombinatoria + custoPath
    print(f"custo final de todo trajeto: {custoTotal:.6f} Min.")

    #TODO passar custos e combinatória p view e exibir
    app = QApplication(sys.argv)
    janela = View(map, COLORS, caminho, (custoTotal, custoCombinatoria, custoPath))
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
