from game.rules import get_pawn_moves, get_knight_moves, get_rook_moves, get_bishop_moves, get_queen_moves, get_king_moves
from game.move import Move

class ChessBoard:
    def __init__(self):
        self.reset_board()
    
    def reset_board(self):
        self.board = [
            ["b_rook", "b_knight", "b_bishop", "b_queen", "b_king", "b_bishop", "b_knight", "b_rook"],
            ["b_pawn"] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            [""] * 8,
            ["w_pawn"] * 8,
            ["w_rook", "w_knight", "w_bishop", "w_queen", "w_king", "w_bishop", "w_knight", "w_rook"],
        ]
        self.turn = "w"

        self.white_king_pos = (7, 4)
        self.black_king_pos = (0, 4)

        self.en_passant_target = None

        self.move_history = []
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_board_state(self):
        return self.board
    
    def get_all_possible_moves(self, row, col):
        piece = self.get_piece(row, col)
        if not piece:
            return []

        piece_type = piece.split("_")[1]
        color = piece[0]

        if piece_type == "pawn":
            return get_pawn_moves(self.board, row, col, color, self.en_passant_target)
        elif piece_type == "knight":
            return get_knight_moves(self.board, row, col, color)
        elif piece_type == "rook":
            return get_rook_moves(self.board, row, col, color)
        elif piece_type == "bishop":
            return get_bishop_moves(self.board, row, col, color)
        elif piece_type == "queen":
            return get_queen_moves(self.board, row, col, color)
        elif piece_type == "king":
            return get_king_moves(self.board, row, col, color)

        return []
    
    def get_legal_moves(self, row, col):
        piece = self.get_piece(row, col)
        
        if not piece or piece[0] != self.turn:
            return []
    
        colour = piece[0]
        all_possible_moves = self.get_all_possible_moves(row, col)
        legal_moves = []

        for (r, c) in all_possible_moves:
            from_cell_temp = self.board[row][col]
            to_cell_temp = self.board[r][c]

            self.board[r][c] = from_cell_temp
            self.board[row][col] = ""

            if piece == "w_king":
                self.white_king_pos = (r, c)
            elif piece == "b_king":
                self.black_king_pos = (r, c)

            in_check = self.is_in_check(colour)

            if piece == "w_king":
                self.white_king_pos = (row, col)
            elif piece == "b_king":
                self.black_king_pos = (row, col)

            self.board[r][c] = to_cell_temp
            self.board[row][col] = from_cell_temp

            if not in_check:
                legal_moves.append((r, c))
        
        return legal_moves

    def move_piece(self, from_row, from_col, to_row, to_col, legal_moves):

        if (to_row, to_col) not in legal_moves:
            return False
        
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]

        # Update board
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""

        # King movement
        if piece == "w_king":
            self.white_king_pos = (to_row, to_col)
        elif piece == "b_king":
            self.black_king_pos = (to_row, to_col)

        # En passant 
        if piece.endswith("pawn") and (to_row, to_col) == self.en_passant_target:
            self.board[from_row][to_col] = ""

        # Handle en passant setting
        if piece.endswith("pawn") and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, to_col)
        else:
            self.en_passant_target = None

        # Save move
        self.move_history.append(Move(from_row, from_col, to_row, to_col, piece, captured))
    
        # Switch turn
        self.turn = "b" if self.turn == "w" else "w"
        return True
    
    def is_in_check(self, colour):
        king_pos = self.white_king_pos if colour == "w" else self.black_king_pos
        enemy_color = "b" if colour == "w" else "w"

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece[0] == enemy_color:
                    if king_pos in self.get_all_possible_moves(row, col):
                        print("check")
                        return True
                    
        return False