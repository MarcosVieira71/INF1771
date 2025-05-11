from PySide6.QtWidgets import QWidget, QLabel, QVBoxLayout, QDialog, QPushButton
from PySide6.QtGui import QPainter, QColor, QPixmap
from PySide6.QtCore import QTimer, Qt

from map.Map import Map

from map.mapConstants import EVENT_SPRITES

class CustosDialog(QDialog):
    def __init__(self, custos, parent=None):
        super().__init__(parent)
        
        self.setWindowTitle("Custos do Trajeto")
        self.setFixedSize(300, 200) 
        self.setModal(True)  

        layout = QVBoxLayout(self)

        self.label_custos = QLabel(self)
        self.label_custos.setAlignment(Qt.AlignCenter)  
        layout.addWidget(self.label_custos)

        self.label_custos.setStyleSheet("""
            QLabel {
                background-color: white;
                color: red;
                font-weight: bold;
                font-size: 14px;
                border: 2px solid red;
                padding: 10px;
            }
        """)

        custoTotal, custoCombinatoria, custoPath = custos
        texto = (f"<b>Custo total: {custoTotal:.6f} Min.</b><br>"
                 f"<b>Custo combinatório: {custoCombinatoria:.6f} Min.</b><br>"
                 f"<b>Custo do caminho: {custoPath:.6f} Min.</b>")
        self.label_custos.setText(texto)

        button = QPushButton("Fechar", self)
        button.clicked.connect(self.accept)
        layout.addWidget(button)

class View(QWidget):
    def __init__(self, mapa: Map, colors: dict, caminho: list, custos: tuple):
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
        self.timer.start(20)

        self.sprite = QPixmap("assets/dragonborn.png")
        self.sprite_width = self.cell_width * 15
        self.sprite_height = self.cell_height * 15

        self.exibirCustosDialog(custos)

    def exibirCustosDialog(self, custos):
        custos_dialog = CustosDialog(custos, self)
        custos_dialog.exec()  

    def atualizar_caminho(self):
        if self.caminho and self.caminho_index < len(self.caminho):
            self.desenhar_caminho.append(self.caminho[self.caminho_index])
            self.caminho_index += 1
            self.update()  

    def paintEvent(self, event):
        painter = QPainter(self)

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

        painter.setBrush(QColor(255, 0, 0))  
        for (x, y) in self.desenhar_caminho[:-1]:
            painter.fillRect(
                x * self.cell_width,
                y * self.cell_height,
                self.cell_width,
                self.cell_height,
                QColor(255, 0, 0)
            )

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

        if self.desenhar_caminho:
            x, y = self.desenhar_caminho[-1]
            painter.drawPixmap(
                x * self.cell_width - (self.sprite_width - self.cell_width) // 2,
                y * self.cell_height - (self.sprite_height - self.cell_height) // 2,
                self.sprite_width,
                self.sprite_height,
                self.sprite
            )
