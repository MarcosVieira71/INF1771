from PySide6.QtWidgets import QWidget
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtCore import QTimer

from map.Map import Map
from map.mapConstants import EVENT_SPRITES
from algorithm.pathFind import caminho_final


class View(QWidget):
    def __init__(self, mapa: Map, colors: dict, caminho: list):
        super().__init__()
        self.mapa = mapa
        self.colors = colors
        self.cell_width = 4
        self.cell_height = 5
        self.setWindowTitle('Mapa Skyrim')
        self.resize(1200, 450)
        self.showMaximized()

        self.caminho = caminho
        self.caminho_index = 0
        self.desenhar_caminho = []

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.atualizar_caminho)
        self.timer.start(0.1)

        self.sprite = QPixmap("assets/dragonborn.png")
        self.sprite_width = self.cell_width * 15
        self.sprite_height = self.cell_height * 15

    def atualizar_caminho(self):
        if self.caminho and self.caminho_index < len(self.caminho):
            self.desenhar_caminho.append(self.caminho[self.caminho_index])
            self.caminho_index += 1
            self.update()
        else:
            self.timer.stop()
    
    """def resizeEvent(self, event):
        cols = len(self.mapa.grid[0])
        rows = len(self.mapa.grid)
        self.cell_width = self.width()
        self.cell_height = self.height()

        self.sprite_width = self.cell_width * 15
        self.sprite_height = self.cell_height * 15

        self.update()"""

    def paintEvent(self, event):
        painter = QPainter(self)

        # Desenha o mapa
        for y, linha in enumerate(self.mapa.grid):
            for x, celula in enumerate(linha):
                cor = self.colors.get(celula, QColor(255, 0, 0))
                painter.fillRect(
                    x * self.cell_width,
                    y * self.cell_height,
                    self.cell_width,
                    self.cell_height,
                    cor
                )

        # Desenha o caminho percorrido (menos o ponto atual)
        painter.setBrush(QColor(255, 0, 0))
        for (x, y) in self.desenhar_caminho[:-1]:
            painter.fillRect(
                x * self.cell_width,
                y * self.cell_height,
                self.cell_width,
                self.cell_height,
                QColor(255, 0, 0)
            )

        # Desenha os eventos com sprites
        for k, v in self.mapa.eventsCoord.items():
            if k not in EVENT_SPRITES:
                continue
            x, y = v
            evento_sprite = QPixmap(EVENT_SPRITES[k])
            painter.drawPixmap(
                x * self.cell_width - (self.sprite_width - self.cell_width) // 2,
                y * self.cell_height - (self.sprite_height - self.cell_height) // 2,
                self.sprite_width,
                self.sprite_height,
                evento_sprite
            )

        # Desenha o sprite do personagem no ponto atual
        if self.desenhar_caminho:
            x, y = self.desenhar_caminho[-1]
            painter.drawPixmap(
                x * self.cell_width - (self.sprite_width - self.cell_width) // 2,
                y * self.cell_height - (self.sprite_height - self.cell_height) // 2,
                self.sprite_width,
                self.sprite_height,
                self.sprite
            )
