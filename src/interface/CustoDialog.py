from PySide6.QtWidgets import QLabel, QVBoxLayout, QDialog, QPushButton
from PySide6.QtCore import Qt


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