# Leaderboard Window
from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QComboBox, QListWidgetItem)
from PyQt5.QtCore import Qt
from DBConnector import DBConnector

from PreviewGame import PreviewGameWindow

class LeaderBoardWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.db = DBConnector()
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget { background-color: #1E1E2E; }
            QLabel {
                color: #B4E1FA;
                font-size: 28px;
                font-weight: bold;
            }
            QListWidget {
                background-color: #2B2B3D;
                color: #FFFFFF;
                font-size: 18px;
                font-family: monospace;
            }
            QListWidget::item {
                padding: 10px;
                font-family: monospace;
            }
            QPushButton {
                background-color: #6AAFE6;
                color: #1E1E2E;
                font-size: 16px;
                font-weight: bold;
                padding: 10px 20px;
                border-radius: 10px;
            }
            QPushButton:hover {
                font-family: monospace;
                background-color: #8FC9F9;
            }
        """)
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("🏆 Tabla de Líderes")
        title.setAlignment(Qt.AlignCenter)

        # add drop down to select difficulty

        self.difficulty_dropdown = QComboBox()
        self.difficulty_dropdown.addItems(["Fácil", "Medio", "Difícil"])
        self.difficulty_dropdown.currentTextChanged.connect(self.cargar_leaderboard)
        layout.addWidget(self.difficulty_dropdown)

        self.leaderboard_list = QListWidget()
        btn_back = QPushButton("Volver al Menú")
        btn_back.clicked.connect(lambda: (self.db.close(), self.parent.ir_a("menu")))
        
        layout.addWidget(title)
        layout.addWidget(self.leaderboard_list)
        layout.addWidget(btn_back)
        self.setLayout(layout)
        self.cargar_leaderboard(self.difficulty_dropdown.currentText())
    
    def cargar_leaderboard(self, difficulty):
        self.leaderboard_list.clear()
        scores = self.db.cargar_juegos(difficulty)
        
        if not scores:
            self.leaderboard_list.addItem("No hay puntajes registrados aún.")
        else:
            for name, puzzle, time in scores:
                minutes, seconds = divmod(time, 60)
                item = QListWidgetItem(f"{name} - {minutes}m {seconds}s")
                item.setTextAlignment(Qt.AlignCenter)
                self.leaderboard_list.addItem(item)
                self.leaderboard_list.item(self.leaderboard_list.count() - 1).setToolTip(f"Puzzle:\n{self.format(puzzle)}")
    
    def format(self, puzzle):
        board_str = ""
        for row in puzzle:
            for i, r in enumerate(row):
                board_str += str(r) + " "
                if (i + 1) % 3 == 0 and i < 8:
                    board_str += "| "
            board_str += "\n"
            if (puzzle.index(row) + 1) % 3 == 0 and puzzle.index(row) < 8:
                board_str += "--------+--------+--------\n" 
        return board_str
        