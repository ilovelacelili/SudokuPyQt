import sys
from PyQt5.QtWidgets import QApplication

from MainApp import SudokuApp

if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet("""
        QWidget {
            background-color: #1E1E2E;
        }
        QPushButton {
            background-color: #6AAFE6;
            color: #1E1E2E;
            font-weight: bold;
            border-radius: 8px;
        }
        QLabel {
            color: #B4E1FA;
        }
        QLineEdit {
            background-color: #2B2B3D;
            color: #FFFFFF;
        }
    """)

    ventana = SudokuApp()
    ventana.show()
    sys.exit(app.exec_())
