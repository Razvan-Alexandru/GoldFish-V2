class Move:
    def __init__(self, from_row, from_col, to_row, to_col, piece, captured=None, promotion=None, is_castling=None, is_en_passant=None):
        self.from_row = from_row
        self.from_col = from_col
        self.to_row = to_row
        self.to_col = to_col
        self.piece = piece
        self.captured = captured
        self.promotion = promotion
        self.is_castling = is_castling
        self.is_en_passant = is_en_passant
    
    def __repr__(self):
        return f"{self.piece}: {self.from_row}, {self.from_col} -> {self.to_row}, {self.to_col}"
        