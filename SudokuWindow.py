import random

from PyQt5.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QHBoxLayout, QGridLayout, QPushButton,
    QLabel, QLineEdit, QInputDialog, QMessageBox
)
from PyQt5.QtCore import Qt, QTimer
from PyQt5.QtGui import QIntValidator

from DBConnector import DBConnector

class SudokuWindow(QWidget):
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

        # BOTONES
        button_layout = QHBoxLayout()
        button_layout.setSpacing(20)

        solve_btn = QPushButton("Resolver")
        check_btn = QPushButton("Verificar")
        hint_btn = QPushButton("Pista")
        exit_btn = QPushButton("Salir")

        exit_btn.clicked.connect(self.confirmar_salida)
        hint_btn.clicked.connect(self.dar_pista)
        solve_btn.clicked.connect(self.resolver_sudoku)
        check_btn.clicked.connect(self.verificar_sudoku)

        button_layout.addWidget(solve_btn)
        button_layout.addWidget(check_btn)
        button_layout.addWidget(hint_btn)
        button_layout.addWidget(exit_btn)

        main_layout.addLayout(button_layout)
        self.setLayout(main_layout)

        # TIMER
        self.timer = QTimer()
        self.timer.timeout.connect(self.actualizar_tiempo)
        self.timer.setInterval(1000)
        self.segundos = 0

    # ======================================================
    #                   FUNCIONES DE CONTROL
    # ======================================================
    def cargar_tablero(self, grid, puzzle, dificultad):
        if self.timer.isActive():
            self.timer.stop()

        self.grid = grid
        self.puzzle = puzzle
        self.dificultad = dificultad
        self.level_label.setText(f"🎯 Nivel: {dificultad}")

        self.segundos = 0
        self.time_label.setText("⏱️ Tiempo: 00:00")
        self.timer.start()

        for i in range(9):
            for j in range(9):
                val = puzzle[i][j]
                cell = self.cells[i][j]
                if val == 0:
                    cell.setStyleSheet(cell.styleSheet() + "QLineEdit { color: red; font-weight: bold; }")
                    cell.setText("")
                    cell.setReadOnly(False)
                    cell.textChanged.connect(self.verificar_completo)
                    cell.textChanged.connect(lambda _, x=i, y=j: self.guardar_pasos(x, y))
                else:
                    cell.setStyleSheet(cell.styleSheet() + "QLineEdit { color: black; font-weight: bold; }")
                    cell.setText(str(val))
                    cell.setReadOnly(True)

    def actualizar_tiempo(self):
        self.segundos += 1
        minutos = self.segundos // 60
        segundos = self.segundos % 60
        self.time_label.setText(f"⏱️ Tiempo: {minutos:02}:{segundos:02}")

    def verificar_sudoku(self):
        self.saveable = False
        try:
            for i in range(9):
                for j in range(9):
                    t = self.cells[i][j].text()
                    if t != str(self.grid[i][j]):
                        raise ValueError
            
            QMessageBox.information(self, "¡Vas Bien!", "✔ Todo parece válido hasta ahora.")
            return True
        
        except:
            QMessageBox.warning(self, "Hay algún error", "Casi lo logras, pero hay errores en el Sudoku.")
            return False
        
    def verificar_completo(self):
        for i in range(9):
            for j in range(9):
                t = self.cells[i][j].text()
                if t == "" or not t.isdigit() or int(t) != self.grid[i][j]:
                    return False
        
        self.timer.stop()
        QMessageBox.information(self, "¡Felicidades!", f"🎉 ¡Has completado el Sudoku!\n Tiempo: {self.segundos // 60}m {self.segundos % 60}s")
        return True

    def resolver_sudoku(self):
        self.saveable = False

        for i in range(9):
            for j in range(9):
                self.cells[i][j].setText(str(self.grid[i][j]))

        self.timer.stop()

    def dar_pista(self):
        if self.verificar_completo():
            return
        
        self.saveable = False
        
        i = random.randint(0, 8)
        j = random.randint(0, 8)
        while self.cells[i][j].text() == str(self.grid[i][j]):
            i = random.randint(0, 8)
            j = random.randint(0, 8)
            print('Choosing new cell for hint...', i, j)
        
        self.cells[i][j].setText(str(self.grid[i][j]))
        self.cells[i][j].setStyleSheet(self.cells[i][j].styleSheet() + "QLineEdit { color: green; font-weight: bold; }")
        self.cells[i][j].setReadOnly(True)
        
    def guardar_pasos(self, i, j):
        current_value = self.cells[i][j].text() if self.cells[i][j].text() != "" else 0
        self.steps += f"{i}{j}{current_value}"
        print(self.steps)

    def confirmar_salida(self):
        '''No permite guardar si el Sudoku no está completo o se ha usado resolver/pista'''
        if not self.saveable or not self.verificar_completo():
            self.parent.ir_a("menu")
            return

        msg = QMessageBox()
        msg.setWindowTitle("Confirmar salida")
        msg.setText("¿Deseas guardar antes de salir?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)
        r = msg.exec_()

        if r == QMessageBox.Yes:
            name, ok = QInputDialog.getText(self, "Guardar Juego", "Ingresa tu nombre:")
            if ok and name:
                self.guardar_progreso(name)
                QMessageBox.information(self, "Guardar", "Guardado exitosamente.")
            
        self.parent.ir_a("menu")

    def guardar_progreso(self, name='Player'):
        self.db = DBConnector()
        current_puzzle = []
        for i in range(9):
            row = []
            for j in range(9):
                t = str(self.puzzle[i][j])
                if t == "" or not t.isdigit():
                    row.append(0)
                else:
                    row.append(int(t))
            current_puzzle.append(row)
        self.db.guardar_juego(name, current_puzzle, self.steps, self.segundos, self.dificultad)
        self.db.close()