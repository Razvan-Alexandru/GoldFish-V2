import os
import uuid
import torch

from game.board import ChessBoard
from game.state import encode_board_state
from ai.model import GoldfishModel
from ai.utils import *

class Engine():

    def __init__(self, device: torch.device, debug=False):
        self.debug = debug
        self.device = device
        self.game = ChessBoard() # Starts new board
        self.model = GoldfishModel().to(self.device)
        self.play_data = []

        self.self_play()
        self.save_game_data()

    def self_play(self):
        while not self.game.is_game_over():

            # Encode board
            with torch.no_grad():
                tensor = torch.tensor(encode_board_state(self.game)).permute(2, 0, 1).unsqueeze(0).float().to(self.device)

                # Run the Goldfish model
                output = self.model.forward(tensor)

            # Mask logits, get probabilities
            legal_mask = get_all_legal_moves_4096(self.game)
            logits = output["policy"].squeeze(0)

            mask_tensor = torch.tensor(legal_mask, dtype=torch.bool, device=logits.device)
            masked_logits = torch.full_like(logits, float('-inf'))
            masked_logits[mask_tensor] = logits[mask_tensor]

            probabilities = torch.softmax(masked_logits, dim=0)

            # argmax or multinominal, uncomment the to use
            move_index = torch.argmax(probabilities).item()
            # move_index = torch.multinomial(probabilities, num_samples=1).item()

            # Play move and store the move
            from_row, from_col, to_row, to_col = decoder(move_index)
            legal_moves = self.game.get_legal_moves(from_row, from_col)
            if (to_row, to_col) in legal_moves:
                self.play_data.append({
                    "player": self.game.turn,
                    "state": tensor.detach().cpu(),
                    "policy": probabilities.detach().cpu()
                })
                self.game.make_move(from_row, from_col, to_row, to_col, legal_moves)
            else:
                print("Illigal move!")
                break
            
        # Game ended, compute result
        result = self.game.result

        if result == "checkmate":
            winner = "b" if self.game.turn == "w" else "w"
        elif result == "stalemate" or (result and result.startswith("draw")):
            winner = None
        else:
            raise ValueError("Unexpected game result format: " + str(result))
        
        if self.debug: print(f"Game result: {result}, Winner: {winner}")
        
        # Attach value to each data in stored game
        for data in self.play_data:
            if winner is None:
                data["value"] = 0 # Draw
            else:
                data["value"] = 1 if data["player"] == winner else -1

    def save_game_data(self, max_games=1000):
        os.makedirs("data", exist_ok=True)
        filename = f"data/training_game_{uuid.uuid4().hex}.pt"
        torch.save(self.play_data, filename)
        if self.debug: print(f"Saved {len(self.play_data)} training samples to {filename}")

        # Cleanup
        cleanup_data(max_files=max_games)