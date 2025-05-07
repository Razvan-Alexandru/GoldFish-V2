from game.rules import get_pawn_moves, get_knight_moves, get_rook_moves, get_bishop_moves
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
        self.en_passant_target = None
        self.move_history = []
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_board_state(self):
        return self.board
    
    def get_legal_moves(self, row, col):
        piece = self.get_piece(row, col)
        
        if not piece or piece[0] != self.turn:
            return []
        
        piece_type = piece.split("_")[1]
        colour = piece[0]

        if piece_type == "pawn":
            return get_pawn_moves(self.board, row, col, colour, self.en_passant_target)
        if piece_type == "knight":
            return get_knight_moves(self.board, row, col, colour)
        if piece_type == "rook":
            return get_rook_moves(self.board, row, col, colour)
        if piece_type == "bishop":
            return get_bishop_moves(self.board, row, col, colour)
        
        return []

    def move_piece(self, from_row, from_col, to_row, to_col, legal_moves):
        # legal_moves = self.get_legal_moves(from_row, from_col)

        if (to_row, to_col) not in legal_moves:
            return False
        
        piece = self.board[from_row][from_col]
        captured = self.board[to_row][to_col]

        # Update board
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""

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