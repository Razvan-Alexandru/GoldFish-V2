import os
from PyQt6.QtWidgets import QDialog, QVBoxLayout, QPushButton, QLabel, QHBoxLayout
from PyQt6.QtGui import QPixmap, QIcon

class PromotionDialog(QDialog):
    def __init__(self, colour, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Choose Promotion")
        self.setFixedSize(360, 140)
        self.piece_choice = None
        self.setModal(True)

        layout = QVBoxLayout()
        label = QLabel("Promote pawn to:")
        layout.addWidget(label)

        piece_options = ["queen", "rook", "bishop", "knight"]

        button_layout = QHBoxLayout()
        for piece in piece_options:
            btn = QPushButton()
            btn.setFixedSize(64, 64)

            img_path = os.path.join("assets", "pieces", f"{colour}_{piece}.png")
            icon = QIcon(QPixmap(img_path))
            btn.setIcon(icon)
            btn.setIconSize(btn.size())

            btn.clicked.connect(lambda checked, p=piece: self._select_piece(p))
            button_layout.addWidget(btn)

        layout.addLayout(button_layout)
        self.setLayout(layout)

    def _select_piece(self, piece):
        self.piece_choice = piece
        self.accept()