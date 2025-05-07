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

    return moves