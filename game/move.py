from dataclasses import dataclass

@dataclass
class Move:
    from_row: int
    from_col: int
    to_row: int
    to_col: int
    piece: str
    captured: str = None
    promotion: str = None
    is_castling: bool = False
    is_en_passant: bool = False

    def __repr__(self):
        move_type = ""
        if self.is_castling:
            move_type = " (castling)"
        elif self.is_en_passant:
            move_type = " (en passant)"
        elif self.promotion:
            move_type = f" (promotion to {self.promotion})"
        return f"{self.piece}: ({self.src_row}, {self.src_col}) -> ({self.dest_row}, {self.dest_col}){move_type}"
