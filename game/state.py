import numpy as np

def get_position_signature(self):
        board = self.get_board_state()
        piece_rows = []
        for row in board:
            piece_rows.append("".join(piece or "." for piece in row))
        board_str = "/".join(piece_rows)
        
        castling = (
            f"{int(self.castling_rights['w']['kingside'])}"
            f"{int(self.castling_rights['w']['queenside'])}"
            f"{int(self.castling_rights['b']['kingside'])}"
            f"{int(self.castling_rights['b']['queenside'])}"
        )
        
        ep = self.en_passant_target or (-1, -1)
        
        return f"{board_str} {self.turn} {castling} {ep}"

def encode_board_state(chessboard):
    board = chessboard.get_board_state()
    tensor = np.zeros((8, 8, 18), dtype=np.float32)

    piece_to_channel = {
        "w_pawn": 0, "w_knight": 1, "w_bishop": 2,
        "w_rook": 3, "w_queen": 4, "w_king": 5,
        "b_pawn": 6, "b_knight": 7, "b_bishop": 8,
        "b_rook": 9, "b_queen": 10, "b_king": 11,
    }

    for row in range(8):
        for col in range(8):
            piece = board[row][col]
            if piece in piece_to_channel:
                tensor[row, col, piece_to_channel[piece]] = 1.0
    
    # Turn
    if chessboard.turn == "w":
        tensor[:, :, 12] = 1.0
    
    # Castling rights
    if chessboard.castling_rights["w"]["kingside"]:  tensor[:, :, 13] = 1.0
    if chessboard.castling_rights["w"]["queenside"]: tensor[:, :, 14] = 1.0
    if chessboard.castling_rights["b"]["kingside"]:  tensor[:, :, 15] = 1.0
    if chessboard.castling_rights["b"]["queenside"]: tensor[:, :, 16] = 1.0

    # En passant
    if chessboard.en_passant_target:
        row, col = chessboard.en_passant_target
        tensor[row, col, 17] = 1.0
    
    return tensor