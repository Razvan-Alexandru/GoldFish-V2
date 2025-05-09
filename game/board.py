from game.rules import *
from game.move import Move
from game.state import get_position_signature, encode_board_state

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

        self.castling_rights = {
            "w": {"kingside": True, "queenside": True},
            "b": {"kingside": True, "queenside": True}
        }

        self.en_passant_target = None

        self.move_history = []

        self.position_history = {}
        self.halfmove_clock = 0
        self.fullmove_number = 1

        self.game_over = False
        self.result = None

    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def get_board_state(self):
        return self.board
    
    def generate_piece_moves(self, row, col):
        piece = self.get_piece(row, col)
        if not piece:
            return []

        piece_type = piece.split("_")[1]
        colour = piece[0]

        if piece_type == "pawn":        return get_pawn_moves(self.board, row, col, colour, self.en_passant_target)
        elif piece_type == "knight":    return get_knight_moves(self.board, row, col, colour)
        elif piece_type == "rook":      return get_rook_moves(self.board, row, col, colour)
        elif piece_type == "bishop":    return get_bishop_moves(self.board, row, col, colour)
        elif piece_type == "queen":     return get_queen_moves(self.board, row, col, colour)
        elif piece_type == "king":      return get_king_moves(self.board, row, col, colour, self.castling_rights, self.is_in_check_pos)

        return []
    
    def get_legal_moves(self, row, col):
        piece = self.get_piece(row, col)
        
        if not piece or piece[0] != self.turn:
            return []
    
        legal_moves = []

        for r, c in self.generate_piece_moves(row, col):
            from_cell_temp = self.board[row][col]
            to_cell_temp = self.board[r][c]

            # Simulate Move
            self.board[r][c]     = from_cell_temp
            self.board[row][col] = ""
            if   piece == "w_king": self.white_king_pos = (r, c)
            elif piece == "b_king": self.black_king_pos = (r, c)

            if not self.is_in_check(self.turn):
                legal_moves.append((r, c))

            # Undo
            self.board[r][c]     = to_cell_temp
            self.board[row][col] = from_cell_temp
            if   piece == "w_king": self.white_king_pos = (row, col)
            elif piece == "b_king": self.black_king_pos = (row, col)

        
        return legal_moves

    def make_move(self, from_row, from_col, to_row, to_col, legal_moves, promotion=None):

        if self.game_over:
            return False

        if (to_row, to_col) not in legal_moves:
            return False
        
        piece = self.get_piece(from_row, from_col)
        target = self.get_piece(to_row, to_col)
        move = Move(from_row, from_col, to_row, to_col, piece, target)

        # Handle Castling
        if piece.endswith("king"):
            if abs(to_col - from_col) == 2:
                move.is_castling = True
                if to_col == 6: # kingside
                    self.board[from_row][5] = self.board[from_row][7]
                    self.board[from_row][7] = ""
                if to_col == 2: # queenside
                    self.board[from_row][3] = self.board[from_row][0]
                    self.board[from_row][0] = ""

                self.castling_rights[self.turn]["kingside"]  = False
                self.castling_rights[self.turn]["queenside"] = False
            
        # Handle en passant 
        if piece.endswith("pawn") and (to_row, to_col) == self.en_passant_target:
            move.is_en_passant = True
            self.board[from_row][to_col] = ""
        
        # Handle promotion
        if piece.endswith("pawn"):
            final_rank = 0 if piece[0] == "w" else 7
            if to_row == final_rank:
                move.promotion = promotion if promotion in ("queen", "rook", "bishop", "knight") else "queen"
                piece = f"{piece[0]}_{promotion}"

        # Execute Move
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""

        # Update castling rights and king position
        if piece == "w_king":
            self.white_king_pos = (to_row, to_col)
            self.castling_rights["w"]["kingside"]  = False
            self.castling_rights["w"]["queenside"] = False
        elif piece == "b_king":
            self.black_king_pos = (to_row, to_col)
            self.castling_rights["b"]["kingside"]  = False
            self.castling_rights["b"]["queenside"] = False

        # Update castling rights for rooks
        if piece.endswith("rook"):
            if from_row == 7:
                self.castling_rights[self.turn]["kingside"]  = False
            if from_row == 0:
                self.castling_rights[self.turn]["queenside"] = False

        # Update en passant target
        if piece.endswith("pawn") and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, to_col)
        else:
            self.en_passant_target = None

        # Update clocks
        self.halfmove_clock = 0 if target or piece.endswith("pawn") else self.halfmove_clock + 1
        if self.turn == "b": self.fullmove_number += 1

        # Switch turn
        self.turn = "b" if self.turn == "w" else "w"

        # Update FEN and position history
        signature = get_position_signature(self)
        self.position_history[signature] = self.position_history.get(signature, 0) + 1
    
        # Save move
        self.move_history.append(move)

        return True
    
    def is_in_check(self, colour):
        king_pos = self.white_king_pos if colour == "w" else self.black_king_pos
        enemy_colour = "b" if colour == "w" else "w"

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and not piece.endswith("king") and piece[0] == enemy_colour:
                    if king_pos in self.generate_piece_moves(row, col):
                        return True
                    
        return False
    
    def is_in_check_pos(self, colour, row, col):
        enemy_colour = "b" if colour == "w" else "w"

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and not piece.endswith("king") and piece[0] == enemy_colour:
                    if (row, col) in self.generate_piece_moves(r, c):
                        return True
                    
        return False
    
    def is_game_over(self):
        draw_reason = self.is_draw()
        if draw_reason:
            self.game_over = True
            return f"draw: {draw_reason}"
    
        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and piece[0] == self.turn:
                    if self.get_legal_moves(row, col):
                        return False
        
        if self.is_in_check(self.turn):
            self.result = "checkmate"
        else:
            self.result = "stalemate" # Not tested, assuming this works LOL
        self.game_over = True
        return self.result

    def is_draw(self):
        if self.halfmove_clock >= 100:
            return "50-move rule"
        for fen, count in self.position_history.items():
            if count >= 3:
                return "threefold repetition"
        if self._is_insufficient_material():
            return "insufficient material"
        return None  
    
    def _is_insufficient_material(self): # Not tested yet lol
        pieces = []
        bishop_colors = []

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece:
                    pieces.append((piece, row, col))

        if len(pieces) == 2:
            return True  # King vs King

        if len(pieces) == 3:
            for p, _, _ in pieces:
                if p.endswith("bishop") or p.endswith("knight"):
                    return True  # King + minor vs King

        if len(pieces) == 4:
            bishops = [p for p, r, c in pieces if p.endswith("bishop")]
            if len(bishops) == 2:
                colors = []
                for p, r, c in pieces:
                    if p.endswith("bishop"):
                        color = (r + c) % 2  # 0: light square, 1: dark square
                        colors.append(color)
                if colors[0] == colors[1]:
                    return True  # Same color bishops

        return False
