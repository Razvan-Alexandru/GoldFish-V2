def get_pawn_moves(board, row, col, colour, en_passant_target):
    moves = []
    direction = -1 if colour == "w" else 1
    start_row = 6 if colour == "w" else 1

    # One forward
    if board[row + direction][col] == "":
        moves.append((row + direction, col))

        # Two forward
        if row == start_row and board[row + 2 * direction][col] == "":
            moves.append((row + 2 * direction, col))
    
    # Captures
    for to_col in [-1, 1]:
        new_col = col + to_col
        new_row = row + direction

        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target and target[0] != colour:
                moves.append((new_row, new_col))

            if (new_row, new_col) == en_passant_target:
                moves.append((new_row, new_col)) # en passant possible

    return moves

def get_knight_moves(board, row, col, colour):
    moves = []
    deltas = [(-2, -1), (-2, 1), (-1, -2), (-1, 2), (1, -2), (1, 2), (2, -1), (2, 1)]

    for to_row, to_col in deltas:
        new_row, new_col = row + to_row, col + to_col
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == "" or target[0] != colour:
                moves.append((new_row, new_col))

    return moves

def get_rook_moves(board, row, col, colour):
    moves = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    for to_row, to_col in directions:
        new_row, new_col = row + to_row, col + to_col
        while 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == "":
                moves.append((new_row, new_col)) # empty cell
            elif target[0] != colour:
                moves.append((new_row, new_col)) # enemy piece
                break
            else:
                break # friendly piece

            new_row += to_row
            new_col += to_col

    return moves

def get_bishop_moves(board, row, col, colour):
    moves = []
    directions = [(-1, -1), (-1, 1), (1, -1), (1, 1)]

    for to_row, to_col in directions:
        new_row, new_col = row + to_row, col + to_col
        while 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == "":
                moves.append((new_row, new_col)) # empty cell
            elif target[0] != colour:
                moves.append((new_row, new_col)) # enemy piece
                break
            else:
                break # friendly piece

            new_row += to_row
            new_col += to_col

    return moves

def get_queen_moves(board, row, col, colour):
    return get_rook_moves(board, row, col, colour) + get_bishop_moves(board, row, col, colour)

def get_king_moves(board, row, col, colour, castling_rights, is_in_check_pos_func):
    moves = []
    deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),           (0, 1),
        (1, -1),  (1, 0),  (1, 1)
    ]

    for to_row, to_col in deltas:
        new_row, new_col = row + to_row, col + to_col
        if 0 <= new_row < 8 and 0 <= new_col < 8:
            target = board[new_row][new_col]
            if target == "" or target[0] != colour:
                moves.append((new_row, new_col))

    # Castling (assume row 7 for white, 0 for black)
    if not is_in_check_pos_func(colour, row, col):
        back_row = 7 if colour == "w" else 0
        
        if castling_rights[colour]["kingside"]:
            if (board[back_row][5] == "" and board[back_row][6] == "" and 
                not is_in_check_pos_func(colour, back_row, 5) and not is_in_check_pos_func(colour, back_row, 6)):
                moves.append((back_row, 6))

        if castling_rights[colour]["queenside"]:
            if (board[back_row][1] == "" and board[back_row][2] == "" and board[back_row][3] == "" and
                not is_in_check_pos_func(colour, back_row, 2) and not is_in_check_pos_func(colour, back_row, 3)):
                moves.append((back_row, 2))


    return moves