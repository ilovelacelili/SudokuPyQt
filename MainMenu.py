import sys
import random
from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QLineEdit, QStackedWidget, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer

class MenuInicial(QWidget):
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
                font-size: 20px;
                font-weight: bold;
                padding: 12px 24px;
                border-radius: 10px;
            }
            QPushButton:hover {
                background-color: #8FC9F9;
            }
            QLabel {
                color: #B4E1FA;
                font-size: 32px;
                font-weight: bold;
            }
        """)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel(" Sudoku Python ")
        title.setAlignment(Qt.AlignCenter)

        btn_play = QPushButton("Jugar")
        btn_leaderboard = QPushButton("Tabla de Líderes")
        btn_exit = QPushButton("Salir")

        btn_play.clicked.connect(lambda: self.parent.ir_a("dificultad"))
        btn_leaderboard.clicked.connect(lambda: self.parent.ir_a("leaderboard"))
        btn_exit.clicked.connect(sys.exit)

        layout.addWidget(title)
        layout.addSpacing(40)
        layout.addWidget(btn_play)
        layout.addWidget(btn_leaderboard)
        layout.addWidget(btn_exit)

        self.setLayout(layout)