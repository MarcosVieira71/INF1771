from PySide6.QtWidgets import QApplication, QWidget
from PySide6.QtGui import QPainter, QColor
from PySide6.QtCore import QTimer
import sys

from map import map, colors, events
from algorithm import caminho_final


class MapWidget(QWidget):
    def __init__(self, map, colors):
        super().__init__()
        self.map = map
        self.colors = colors
        self.cell_size = 3
        self.setWindowTitle('Mapa Skyrim')
        self.resize(1200, 450)
        self.caminho = caminho_final(self.map, events)

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
        for y, linha in enumerate(self.map):
            for x, celula in enumerate(linha):
                cor = self.colors.get(celula, QColor(255, 0, 0))

                painter.fillRect(
                    x * self.cell_size,
                    y * self.cell_size,
                    self.cell_size,
                    self.cell_size,
                    cor
                )

        painter.setBrush(QColor(255, 0, 0))
        for (x, y) in self.desenhar_caminho:
            painter.fillRect(
                x * self.cell_size,
                y * self.cell_size,
                self.cell_size,
                self.cell_size,
                QColor(255, 0, 0)
            )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    janela = MapWidget(map, colors)
    janela.show()
    sys.exit(app.exec())
