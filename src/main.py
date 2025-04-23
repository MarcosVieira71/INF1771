from map.Map import Map
from map.mapConstants import COLORS
from algorithm.pathFind import caminho_final, gerar_matriz_distancias, floyd_warshall, validar_caminhos

from interface.View import View
from PySide6.QtWidgets import QApplication
import sys


def main():
    mapa = Map("data/mapa_skyrim.txt")

    eventos = mapa.events

    # print("Gerando matriz de distâncias entre eventos (demora)")
    # dist_a_estrela = gerar_matriz_distancias(mapa, eventos)

    # print("Rodando Floyd-Warshall")
    # dist_floyd = floyd_warshall(dist_a_estrela.copy())

    # print("Testando caminhos A* contra Floyd-Warshall")
    # validar_caminhos(mapa, eventos, dist_floyd)

    caminho = caminho_final(mapa, mapa.events)
    valor = 0
    for i in caminho:
        valor += mapa.get_value(i)
    print(f"Caminho encontrado com {len(caminho)} passos:  e valor {valor}")

    app = QApplication(sys.argv)
    janela = View(mapa, COLORS, caminho)
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
