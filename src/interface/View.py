from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QTimer

from map.Map import Map
from map.mapConstants import COLORS



class View(QWidget):
    def __init__(self, mapa: Map, colors: dict, caminho:list):
        super().__init__()
        self.mapa = mapa
        self.colors = colors
        self.cell_size = 3
        self.setWindowTitle('Mapa Skyrim')
        self.resize(1200, 450)

        self.caminho = caminho
        self.caminho_index = 0
        self.desenhar_caminho = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_caminho)
        self.timer.start(0.1)

    def atualizar_caminho(self):
        if self.caminho and self.caminho_index < len(self.caminho):
            self.desenhar_caminho.append(self.caminho[self.caminho_index])
            self.caminho_index += 1
            self.update()
        else:
            self.timer.stop()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Desenha o mapa
        for y, linha in enumerate(self.mapa.grid):
            for x, celula in enumerate(linha):
                cor = self.colors.get(celula, QColor(255, 0, 0))
                painter.fillRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    cor
                )

        # Desenha o caminho percorrido
        painter.setBrush(QColor(255, 0, 0))
        for (x, y) in self.desenhar_caminho:
            painter.fillRect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size,
                QColor(255, 0, 0)
            )

