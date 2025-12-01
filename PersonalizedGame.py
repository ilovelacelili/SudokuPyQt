# Personalized game window
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton
from PyQt5.QtCore import Qt
from SudokuWindow import SudokuWindow

class VentanaPersonalizada(QWidget):
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
        label = QLabel("Configuración Personalizada")
        label.setAlignment(Qt.AlignCenter)
        
        btn_start = QPushButton("Iniciar Juego Personalizado")
        btn_start.clicked.connect(self.iniciar_juego_personalizado)
        
        layout.addWidget(label)
        layout.addSpacing(25)
        layout.addWidget(btn_start)
        self.setLayout(layout)
    
    def iniciar_juego_personalizado(self):
        # Aquí puedes agregar la lógica para configurar y comenzar un juego personalizado
        self.parent.iniciar_juego("Personalizado")
        self.parent.ir_a("sudoku")
    
