import random
from PyQt5.QtWidgets import QStackedWidget

from DifficultyWindow import VentanaDificultad
from SudokuWindow import SudokuWindow
from MainMenu import MenuInicial
from LeaderBoardWindow import LeaderBoardWindow
from PreviewGame import PreviewGameWindow

class SudokuApp(QStackedWidget):
    def __init__(self):
        super().__init__()

        self.menu = MenuInicial(self)
        self.dificultad = VentanaDificultad(self)
        self.juego = SudokuWindow(self)
        self.leaderboard = LeaderBoardWindow(self)
        self.preview = PreviewGameWindow(self)

        self.addWidget(self.menu)
        self.addWidget(self.dificultad)
        self.addWidget(self.juego)
        self.addWidget(self.leaderboard)
        self.addWidget(self.preview)

        self.setFixedSize(850, 750)
        self.ir_a("menu")

    def ir_a(self, destino):
        if destino == "menu":
            self.setCurrentWidget(self.menu)
        elif destino == "dificultad":
            self.setCurrentWidget(self.dificultad)
        elif destino == "juego":
            self.setCurrentWidget(self.juego)
        elif destino == "leaderboard":
            self.setCurrentWidget(self.leaderboard)
        elif destino == "preview":
            self.setCurrentWidget(self.preview)

    def vista_previa(self, game_data):
        self.preview.cargar_datos(game_data)
        self.ir_a("preview")

    def iniciar_juego(self, dificultad):     
        base = self.generar_sudoku_completo()
        puzzle = self.remover_celdas(base, dificultad)
        self.juego.cargar_tablero(base, puzzle, dificultad)
        self.ir_a("juego")

    def iniciar_personalizado(self, base, puzzle, dificultad):
        self.juego.cargar_tablero(base, puzzle, dificultad + " - Personalizado")
        self.ir_a("juego")

    def generar_sudoku_completo(self):
        """Genera un tablero de Sudoku completo y válido, usando backtracking."""
        grid = [[0]*9 for _ in range(9)]

        def es_valido(num, row, col):
            if num in grid[row]:
                return False
            if num in [grid[i][col] for i in range(9)]:
                return False
            sr, sc = 3 * (row // 3), 3 * (col // 3)
            for r in range(sr, sr + 3):
                for c in range(sc, sc + 3):
                    if grid[r][c] == num:
                        return False
            return True
    
        def resolver():
            for i in range(9):
                for j in range(9):
                    if grid[i][j] == 0:
                        nums = list(range(1, 10))
                        random.shuffle(nums)
                        for n in nums:
                            if es_valido(n, i, j):
                                grid[i][j] = n
                                if resolver():
                                    return True
                                grid[i][j] = 0
                        return False
            return True

        resolver()
        return grid


    def remover_celdas(self, grid, dificultad):
        """Elimina celdas según la dificultad elegida."""
        niveles = {
            "Fácil": 35,
            "Medio": 45,
            "Difícil": 55
        }
        remov = niveles[dificultad]
        puzzle = [row[:] for row in grid]
        count = 0
        while count < remov:
            r = random.randint(0, 8)
            c = random.randint(0, 8)
            if puzzle[r][c] != 0:
                puzzle[r][c] = 0
                count += 1
        return puzzle