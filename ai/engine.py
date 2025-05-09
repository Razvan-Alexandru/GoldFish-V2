import torch

from game.board import ChessBoard
from game.state import encode_board_state
from ai.model import GoldfishModel
from ai.utils import *

class Engine():

    def __init__(self):
        self.game = ChessBoard() # Starts new board
        self.board = self.game.get_board_state
        self.model = GoldfishModel()
        self.self_play()

    def self_play(self):
        while not self.game.is_game_over():
            tensor = encode_board_state(self.game)
            policy, value = self.model.forward(tensor)

            legal_mask = get_all_legal_moves_4096(self.game)
            logits = policy.squeeze(0)

            mask_tensor = torch.tensor(legal_mask, dtype=torch.bool, device=logits.device)
            masked_logits = torch.full_like(logits, float('-inf'))
            masked_logits[mask_tensor] = logits[mask_tensor]

            probabilities = torch.softmax(masked_logits, dim=0)

            # argmax or multinominal, uncomment the to use
            move_index = torch.argmax(probabilities).item()
            # move_index = torch.multinomial(probabilities, num_samples=1).item()

            from_row, from_col, to_row, to_col = decoder(move_index)
            legal_moves = self.game.get_legal_moves(from_row, from_col)
            if (to_row, to_col) in legal_moves:
                self.game.make_move(from_row, from_col, to_row, to_col, legal_moves)