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
    
    def get_piece(self, row, col):
        return self.board[row][col]
    
    def move_piece(self, from_row, from_col, to_row, to_col):
        piece = self.board[from_row][from_col]
        if piece == "":
            return False
        
        self.board[to_row][to_col] = piece
        self.board[from_row][from_col] = ""

        self.turn = "b" if self.turn == "w" else "w"
        return True
    
    def get_board_state(self):
        return self.board