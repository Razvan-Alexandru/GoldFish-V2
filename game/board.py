from collections import defaultdict
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
    
    def get_all_possible_moves(self, row, col):
        piece = self.get_piece(row, col)
        if not piece:
            return []

        piece_type = piece.split("_")[1]
        colour = piece[0]

        if piece_type == "pawn":
            return get_pawn_moves(self.board, row, col, colour, self.en_passant_target)
        elif piece_type == "knight":
            return get_knight_moves(self.board, row, col, colour)
        elif piece_type == "rook":
            return get_rook_moves(self.board, row, col, colour)
        elif piece_type == "bishop":
            return get_bishop_moves(self.board, row, col, colour)
        elif piece_type == "queen":
            return get_queen_moves(self.board, row, col, colour)
        elif piece_type == "king":
            return get_king_moves(self.board, row, col, colour, self.castling_rights, self.is_in_check_pos)

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

    def move_piece(self, from_row, from_col, to_row, to_col, legal_moves, promotion=None):

        if self.game_over:
            return False

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
            self.castling_rights["w"]["kingside"] = False
            self.castling_rights["w"]["queenside"] = False
        elif piece == "b_king":
            self.black_king_pos = (to_row, to_col)
            self.castling_rights["b"]["kingside"] = False
            self.castling_rights["b"]["queenside"] = False

        # Castle settings for rooks
        if piece.endswith("rook"):
            if from_row == 7:
                self.castling_rights[self.turn]["kingside"] = False
            if from_row == 0:
                self.castling_rights[self.turn]["queenside"] = False

        # Handle Castling
        is_castling = False
        if piece.endswith("king"):
            if abs(to_col - from_col) == 2:
                is_castling = True
                if to_col == 6: # kingside
                    self.board[from_row][5] = self.board[from_row][7]
                    self.board[from_row][7] = ""
                if to_col == 2: # queenside
                    self.board[from_row][3] = self.board[from_row][0]
                    self.board[from_row][0] = ""

                self.castling_rights[self.turn]["kingside"] = False
                self.castling_rights[self.turn]["queenside"] = False

        # En passant 
        is_en_passant = False
        if piece.endswith("pawn") and (to_row, to_col) == self.en_passant_target:
            self.board[from_row][to_col] = ""
            is_en_passant = True

        # Handle en passant setting
        if piece.endswith("pawn") and abs(to_row - from_row) == 2:
            self.en_passant_target = ((from_row + to_row) // 2, to_col)
        else:
            self.en_passant_target = None

        # Promotion
        if piece.endswith("pawn"):
            final_rank = 0 if piece[0] == "w" else 7
            if to_row == final_rank:
                if promotion not in ("queen", "rook", "bishop", "knight"):
                    promotion = "queen"
                self.board[to_row][to_col] = f"{piece[0]}_{promotion}"

        # Save move
        self.move_history.append(Move(from_row, from_col, to_row, to_col, piece, captured, promotion, is_castling, is_en_passant))

        if captured != "" or piece.endswith("pawn"):
            self.halfmove_clock = 0
        else:
            self.halfmove_clock += 1

        if self.turn == "b":
            self.fullmove_number += 1

        # Track FEN for repetition
        fen = self.generate_fen(include_clocks=False)
        self.position_history[fen] = self.position_history.get(fen, 0) + 1
        print(fen)
    
        # Switch turn
        self.turn = "b" if self.turn == "w" else "w"
        return True
    
    def is_in_check(self, colour):
        king_pos = self.white_king_pos if colour == "w" else self.black_king_pos
        enemy_colour = "b" if colour == "w" else "w"

        for row in range(8):
            for col in range(8):
                piece = self.get_piece(row, col)
                if piece and not piece.endswith("king") and piece[0] == enemy_colour:
                    if king_pos in self.get_all_possible_moves(row, col):
                        return True
                    
        return False
    
    def is_in_check_pos(self, colour, row, col):
        enemy_colour = "b" if colour == "w" else "w"

        for r in range(8):
            for c in range(8):
                piece = self.get_piece(r, c)
                if piece and not piece.endswith("king") and piece[0] == enemy_colour:
                    if (row, col) in self.get_all_possible_moves(r, c):
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
        
    def generate_fen(self, include_clocks=True):
        fen_rows = []
        for row in self.board:
            empty_count = 0
            fen_row = ""
            for piece in row:
                if piece == "":
                    empty_count += 1
                else:
                    if empty_count > 0:
                        fen_row += str(empty_count)
                        empty_count = 0
                    symbol = self._piece_to_fen_symbol(piece)
                    fen_row += symbol
            if empty_count > 0:
                fen_row += str(empty_count)
            fen_rows.append(fen_row)

        piece_placement = "/".join(fen_rows)
        active_color = self.turn
        castling = ""
        if self.castling_rights["w"]["kingside"]: castling += "K"
        if self.castling_rights["w"]["queenside"]: castling += "Q"
        if self.castling_rights["b"]["kingside"]: castling += "k"
        if self.castling_rights["b"]["queenside"]: castling += "q"
        castling = castling or "-"
        en_passant = self._coord_to_alg(self.en_passant_target) if self.en_passant_target else "-"

        if include_clocks:
            return f"{piece_placement} {active_color} {castling} {en_passant} {self.halfmove_clock} {self.fullmove_number}"
        else:
            return f"{piece_placement} {active_color} {castling} {en_passant}"
        
    def _piece_to_fen_symbol(self, piece):
        symbol = piece.split("_")[1][0]
        symbol_map = {
            "p": "p", "r": "r", "n": "n", "b": "b", "q": "q", "k": "k"
        }
        s = symbol_map.get(symbol, "?")
        return s.upper() if piece[0] == "w" else s

    def _coord_to_alg(self, coord):
        if not coord:
            return "-"
        row, col = coord
        return chr(ord('a') + col) + str(8 - row)

    def is_draw(self):
        if self.halfmove_clock >= 100:
            return "50-move rule"
        for fen, count in self.position_history.items():
            if count >= 3:
                return "threefold repetition"
        if self._is_insufficient_material():
            return "insufficient material"
        return None  
    
    def _is_insufficient_material(self):
        pass