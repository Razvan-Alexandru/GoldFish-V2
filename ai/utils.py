from game.board import ChessBoard

def get_all_legal_moves_4096(chessboard: ChessBoard):
    legal_moves_4096 = [0.0] * 4096
    for from_row in range(8):
        for from_col in range(8):
            piece = chessboard.board[from_row][from_col]
            if piece and piece[0] == chessboard.turn:
                for to_row, to_col in chessboard.get_legal_moves(from_row, from_col):
                    index = from_row * 512 + from_col * 64 + to_row * 8 + to_col
                    legal_moves_4096[index] = 1.0
    
    return legal_moves_4096

def decoder(encoded_index: int):
    from_row  = encoded_index // 512,
    from_col  = (encoded_index % 512) // 64,
    to_row    = (encoded_index % 64) // 8,
    to_col    = encoded_index % 8

    return from_row, from_col, to_row, to_col