import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon

class ChessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goldfish V2")
        self.setFixedSize(800, 800)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = ChessMainWindow()
    window.show()
    sys.exit(app.exec())