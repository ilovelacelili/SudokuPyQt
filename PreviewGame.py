# Preview a game from the leaderboard
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QListWidget, QMessageBox
from PyQt5.QtCore import Qt
from SudokuWindow import SudokuWindow
class PreviewGameWindow(QWidget):
    def __init__(self, parent, game_data):
        super().__init__()
        self.parent = parent
        self.game_data = game_data  # game_data is a tuple (name, puzzle, time, difficulty)
        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget { background-color: #1E1E2E; }
            QLabel {
                color: #B4E1FA;
                font-size: 28px;
                font-weight: bold;
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
                background-color: #8FC9F9;
            }
        """)
        
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        title = QLabel("👀 Vista Previa del Juego")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)
        
        name, puzzle, time, difficulty = self.game_data
        
        info_label = QLabel(f"Jugador: {name}\nDificultad: {difficulty}\nTiempo: {time} segundos")
        info_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(info_label)
        
        btn_start = QPushButton("Jugar este Juego")
        btn_start.clicked.connect(self.start_game)
        btn_back = QPushButton("Volver a la Tabla de Líderes")
        btn_back.clicked.connect(lambda: self.parent.ir_a("leaderboard"))
        
        layout.addWidget(btn_start)
        layout.addWidget(btn_back)
        self.setLayout(layout)
    
    def start_game(self):
        name, puzzle, time, difficulty = self.game_data
        sudoku_window = self.parent.ventanas["sudoku"]
        sudoku_window.cargar_puzzle_desde_datos(puzzle, difficulty)
        self.parent.ir_a("sudoku")