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
                moves.append((new_row, new_col))

    print(f"valid voves: {len(moves)}")
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

    print(f"valid voves: {len(moves)}")
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

    print(f"valid voves: {len(moves)}")
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

    print(f"valid voves: {len(moves)}")
    return moves

def get_queen_moves(board, row, col, colour):
    return get_rook_moves(board, row, col, colour) + get_bishop_moves(board, row, col, colour)