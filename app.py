import sys
from PyQt6.QtWidgets import QApplication, QMainWindow
from PyQt6.QtGui import QIcon
from ui.main_window import ChessMainWindow
from ai.train import main as train_main

def main():

    if len(sys.argv) > 1 and sys.argv[1] == "train":
        train_main()
    else:
        app = QApplication(sys.argv)
        window = ChessMainWindow()
        window.show()
        sys.exit(app.exec())

if __name__ == '__main__':
    main()