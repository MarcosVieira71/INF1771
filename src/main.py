from map.Map import Map
from map.mapConstants import COLORS
from algorithm.pathFind import caminho_final

from interface.View import View
from PySide6.QtWidgets import QApplication
import sys


def main():
    mapa = Map("data/mapa_skyrim.txt")

    caminho = caminho_final(mapa, mapa.events)
    print(f"Caminho encontrado com {len(caminho)} passos:")

    app = QApplication(sys.argv)
    janela = View(mapa, COLORS)
    janela.show()
    sys.exit(app.exec())

if __name__ == "__main__":
    main()
