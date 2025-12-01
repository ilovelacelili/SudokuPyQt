import random

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QLineEdit, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIntValidator

class PreviewGameWindow(QWidget):
    def __init__(self, parent):
        super().__init__()
        self.parent = parent
        self.puzzle = None
        self.steps = ""
        self.dificultad = "Medio"
        self.saveable = True # Controlar si el Sudoku fue resuelto sin usar RESOLVER o usar PISTA

        self.initUI()

    def initUI(self):
        self.setStyleSheet("""
            QWidget { background-color: #1E1E2E; }
            QLabel {
                color: #B4E1FA;
                font-size: 22px;
                font-weight: bold;
            }
            QLineEdit {
                background-color: #2B2B3D;
                color: #FFFFFF;
                font-size: 18px;
                qproperty-alignment: AlignCenter;
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

        main_layout = QVBoxLayout()
        main_layout.setAlignment(Qt.AlignCenter)

        # TÍTULO
        self.title = QLabel("🧩 Sudoku")
        self.title.setAlignment(Qt.AlignCenter)
        main_layout.addWidget(self.title)

        body_layout = QHBoxLayout()

        # CUADRÍCULA
        grid_layout = QGridLayout()
        grid_layout.setSpacing(0)

        self.cells = []
        for i in range(9):
            row = []
            for j in range(9):
                cell = QLineEdit()
                cell.setFixedSize(50, 50)
                #cell.setMaxLength(1)

                top = 3 if i % 3 == 0 else 1
                left = 3 if j % 3 == 0 else 1
                right = 3 if j == 8 else 1
                bottom = 3 if i == 8 else 1

                cell.setStyleSheet(f"""
                    QLineEdit {{
                        border-top: {top}px solid black;
                        border-left: {left}px solid black;
                        border-right: {right}px solid black;
                        border-bottom: {bottom}px solid black;
                        background-color: #A8C3BC;
                        font-size: 20px;
                    }}
                """)

                validator = QIntValidator(1, 9, self)
                cell.setValidator(validator)

                grid_layout.addWidget(cell, i, j)
                row.append(cell)
            self.cells.append(row)

        grid_widget = QWidget()
        grid_widget.setLayout(grid_layout)

        # ESTADÍSTICAS
        stats_layout = QVBoxLayout()
        stats_layout.setAlignment(Qt.AlignTop)

        stats_title = QLabel("📊 Estadísticas")
        stats_title.setAlignment(Qt.AlignCenter)

        self.time_label = QLabel("⏱️ Tiempo: 00:00")
        self.level_label = QLabel("🎯 Nivel: Medio")

        stats_layout.addWidget(stats_title)
        stats_layout.addSpacing(20)
        stats_layout.addWidget(self.time_label)
        stats_layout.addWidget(self.level_label)

        stats_widget = QWidget()
        stats_widget.setLayout(stats_layout)

        body_layout.addWidget(grid_widget)
        body_layout.addSpacing(30)
        body_layout.addWidget(stats_widget)

        main_layout.addLayout(body_layout)

        # TIMER
        self.timer = QTimer()
        self.timer.timeout.connect(self.siguiente_paso)
        self.timer.setInterval(1500)

        # BOTONES
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        # Timer buttons for previewing steps
        start_btn = QPushButton("Iniciar")
        pause_btn = QPushButton("Pausar")
        reset_btn = QPushButton("Reiniciar")

        start_btn.clicked.connect(self.timer.start)
        pause_btn.clicked.connect(self.timer.stop)
        reset_btn.clicked.connect(self.resetear_pasos)

        button_layout.addWidget(start_btn)
        button_layout.addWidget(pause_btn)
        button_layout.addWidget(reset_btn)

        exit_btn = QPushButton("Salir")

        exit_btn.clicked.connect(self.confirmar_salida)    
        button_layout.addWidget(exit_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)
    
    def resetear_pasos(self):
        self.timer.stop()
        for i in range(9):
            for j in range(9):
                cell = self.cells[i][j]
                val = self.puzzle[i][j]
                if val == 0:
                    cell.setText("")
                else:
                    cell.setText(str(val)) 

    def cargar_datos(self, game_data):
        if self.timer.isActive():
            self.timer.stop()

        name, puzzle, steps, time, dificultad = game_data

        self.name = name
        self.puzzle = puzzle
        self.steps = steps
        self.time = time
        self.dificultad = dificultad
        self.level_label.setText(f"🎯 Nivel: {dificultad}")

        for i in range(9):
            for j in range(9):
                val = puzzle[i][j]
                cell = self.cells[i][j]
                if val == 0:
                    cell.setStyleSheet(cell.styleSheet() + "QLineEdit { color: red; font-weight: bold; }")
                    cell.setText("")
                    cell.setReadOnly(True)
                else:
                    cell.setStyleSheet(cell.styleSheet() + "QLineEdit { color: black; font-weight: bold; }")
                    cell.setText(str(val))
                    cell.setReadOnly(True)
    
    def actualizar_tiempo(self):
        self.n_step += 1
        self.siguiente_paso(self.n_step)

    def siguiente_paso(self, n):
        if self.n_step >= len(self.steps):
            self.timer.stop()
            return
        
        step = self.steps[self.n_step: self.n_step + 3]
        x, y, val = int(step[0]), int(step[1]), int(step[2])
        self.cells[x][y].setText(str(val))
        
        return x, y, val

    def confirmar_salida(self):
        self.parent.ir_a("menu")
