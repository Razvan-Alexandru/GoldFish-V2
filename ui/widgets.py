from PyQt6.QtWidgets import QLabel
from PyQt6.QtCore import pyqtSignal

class ClickableSqare(QLabel):
    clicked = pyqtSignal(int, int)

    def __init__(self, row, col):
        super().__init__()
        self.row = row
        self.col = col

    def mousePressEvent(self, ev):
        self.clicked.emit(self.row, self.col)