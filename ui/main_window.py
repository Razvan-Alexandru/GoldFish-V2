import os
from PyQt6.QtWidgets import (
    QMainWindow, QWidget, QPushButton, QVBoxLayout, QHBoxLayout, QGridLayout, QInputDialog
)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPixmap

from ui.widgets import ClickableSquare
from ui.promotion_dialog import PromotionDialog

from game.board import ChessBoard

class ChessMainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Goldfish V2")
        self.setFixedSize(1024, 1024)
        self._setup_ui()

    def _setup_ui(self):
        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        main_layout = QVBoxLayout()
        central_widget.setLayout(main_layout)

        top_button_layout =  QHBoxLayout()
        self._add_mode_button(top_button_layout)
        main_layout.addLayout(top_button_layout)

        board_widget = QWidget()
        board_widget.setFixedSize(640, 640)
        self.board_layout = QGridLayout()
        self._init_chessboard(self.board_layout)
        board_widget.setLayout(self.board_layout)

        main_layout.addWidget(board_widget, alignment=Qt.AlignmentFlag.AlignCenter)

    def _add_mode_button(self, layout):
        self.pvp_btn = QPushButton("Player vs Player")
        self.pvai_btn = QPushButton("Player vs AI")
        self.aivai_btn = QPushButton("AI vs AI")

        layout.addWidget(self.pvp_btn)
        layout.addWidget(self.pvai_btn)
        layout.addWidget(self.aivai_btn)
        
        self.pvai_btn.clicked.connect(self._show_colour_options)

    def _show_colour_options(self):
        print("PvAI selected - placeholder")

    def _init_chessboard(self, layout):
        self.game_logic = ChessBoard()

        self.squares = [[None for _ in range(8)] for _ in range(8)]
        self.selected_from = None

        layout.setSpacing(0)
        layout.setContentsMargins(0, 0, 0, 0)
        for row in range(8):
            for col in range(8):
                square = ClickableSquare(row, col)
                square.setFixedSize(80,80)
                square.clicked.connect(self._on_square_clicked)

                colour = "#f0d9b5" if (row + col) % 2 == 0 else "#b58863"
                square.setStyleSheet(f"background-color: {colour}; border: none;")
                layout.addWidget(square, row, col)
                self.squares[row][col] = square

        self._update_board_ui()
        
    def _update_board_ui(self):
        board_state = self.game_logic.get_board_state()
        for row in range(8):
            for col in range(8):
                piece = board_state[row][col]
                square = self.squares[row][col]
                if(piece):
                    image_path = os.path.join("assets", "pieces", f"{piece}.png")
                    pixmap = QPixmap(image_path)
                    square.setPixmap(pixmap.scaled(80, 80, Qt.AspectRatioMode.KeepAspectRatio))
                else:
                    square.clear()

    def _on_square_clicked(self, row, col):
        if self.selected_from is None:
            print(self.game_logic.get_piece(row, col))
            if self.game_logic.get_piece(row, col) != "":
                self.legal_moves = self.game_logic.get_legal_moves(row, col)
                self.selected_from = (row, col)
                print(f"Selected from square: {row}, {col}")
        else:
            from_row, from_col = self.selected_from
            print(f"Selected to square: {row}, {col}")

            piece = self.game_logic.get_piece(from_row, from_col)
            colour = piece[0]

            # Detect promotion
            is_pawn = piece and piece.endswith("pawn")
            final_rank = 0 if piece[0] == "w" else 7
            promotion = None

            if colour == self.game_logic.turn and is_pawn and row == final_rank:
                dialog = PromotionDialog(colour, self)
                dialog.exec()  # blocks until user clicks
                promotion = dialog.piece_choice

            moved = self.game_logic.make_move(from_row, from_col, row, col, self.legal_moves, promotion)

            if moved:
                self._update_board_ui()
                result = self.game_logic.is_game_over()
                if result == "Checkmate":
                    winner = "White" if self.chess_logic.turn == "b" else "Black"
                    print(f"Checkmate! {winner} wins.")
                elif result:
                    print(result.capitalize())
            else:
                print("Invalid Move")

            self.selected_from = None
            self.legal_moves = None
            self._update_board_ui()