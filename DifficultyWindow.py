import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QLineEdit, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

class VentanaDificultad(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget { background-color: #1E1E2E; }
            QPushButton {
                background-color: #6AAFE6;
                color: #1E1E2E;
                font-size: 18px;
                font-weight: bold;
                padding: 14px 30px;
                border-radius: 12px;
            }
            QPushButton:hover {
                background-color: #8FC9F9;
            }
            QLabel {
                color: #B4E1FA;
                font-size: 28px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Selecciona dificultad")
        label.setAlignment(Qt.AlignCenter)

        btn_easy = QPushButton("Fácil")
        btn_med = QPushButton("Medio")
        btn_hard = QPushButton("Difícil")
        btn_personalized = QPushButton("Personalizado")
        btn_back = QPushButton("Volver al Menú")

        btn_easy.clicked.connect(lambda: self.parent.iniciar_juego("Fácil"))
        btn_med.clicked.connect(lambda: self.parent.iniciar_juego("Medio"))
        btn_hard.clicked.connect(lambda: self.parent.iniciar_juego("Difícil"))
        btn_personalized.clicked.connect(lambda: self.parent.iniciar_juego("Personalizado"))
        btn_back.clicked.connect(lambda: self.parent.ir_a("menu"))

        layout.addWidget(label)
        layout.addSpacing(25)
        layout.addWidget(btn_easy)
        layout.addWidget(btn_med)
        layout.addWidget(btn_hard)
        layout.addWidget(btn_personalized)
        layout.addSpacing(15)
        layout.addWidget(btn_back)

        self.setLayout(layout)