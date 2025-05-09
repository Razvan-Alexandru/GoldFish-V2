import os
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from ai.model import GoldfishModel
from ai.engine import Engine

def main():

    # Device setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Genereate training data with self-play
    print("Generating self-play game...")
    Engine(device)

    # Load data
    data = load_training_data()
    dataset = TrainingDataset(data)
    loader = DataLoader(dataset, batch_size=32, shuffle=True, pin_memory=True)

    # Load model
    model = GoldfishModel().to(device)

    # Optimizer
    optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

    # Train for 1 epoch
    train_one_epoch(model, loader, optimizer, device)

    # Save Model
    os.makedirs("model", exist_ok=True)
    torch.save(model.state_dict(), "model/goldfish_model.pt")
    print("Model saved to model/goldfish_model.pt")


def load_training_data(data_dir="data"):
    all_data = []
    for filename in os.listdir(data_dir):
        if filename.endswith(".pt"):
            filepath = os.path.join(data_dir, filename)
            game_data = torch.load(filepath)
            all_data.extend(game_data)

    print(f"Loaded {len(all_data)} training samples from {data_dir}")
    return all_data

class TrainingDataset(Dataset):
    def __init__(self, data_list):
        self.data = data_list

    def __len__(self):
        return len(self.data)
    
    def __getitem__(self, index):
        sample = self.data[index]
        state =  sample["state"].squeeze(0).float()
        policy = sample["policy"].float()
        value = torch.tensor([sample["value"]]).float()

        return state, policy, value



def train_one_epoch(model: GoldfishModel, dataloader: DataLoader, optimizer: torch.optim.Adam, device: torch.device):
    model.train()
    total_loss = 0.0

    for batch in dataloader:
        states, target_policies, target_values = batch
        states = states.to(device)
        target_policies = target_policies.to(device)
        target_values = target_values.to(device)

        output = model(states)
        pred_logits = output["policy"]
        pred_values = output["value"]

        # Losses
        log_probs = F.log_softmax(pred_logits, dim=1)
        policy_loss = -(target_policies * log_probs).sum(dim=1).mean()
        value_loss = F.mse_loss(pred_values, target_values)
        loss = policy_loss + value_loss

        # Backprop
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_loss = total_loss / len(dataloader) if len(dataloader) > 0 else 0.0
    print(f"Average training loss: {avg_loss:.4f}")