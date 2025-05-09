import os
import csv
import torch
import torch.nn.functional as F
from torch.utils.data import Dataset, DataLoader

from ai.model import GoldfishModel
from ai.engine import Engine

def main():

    # Device setup
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    epoch = 10
    games_per_epoch = 10

    # Train N epochs (100 for now) and save to file
    for epoch in range (epoch):

        # Genereate training data with self-play
        for _ in range(games_per_epoch):
            Engine(device)

        # Load data
        data = load_training_data()
        dataset = TrainingDataset(data)
        loader = DataLoader(dataset, batch_size=32, shuffle=True, pin_memory=True)

        # Load model
        if epoch == 0:
            model = GoldfishModel().to(device)
            if os.path.exists("model/goldfish_model.pt"):
                model.load_state_dict(torch.load("model/goldfish_model.pt", map_location=device))
                print("Loaded existing model.")

            # Optimizer
            optimizer = torch.optim.Adam(model.parameters(), lr=0.001)

        
        os.makedirs("model", exist_ok=True)
        
        train_one_epoch(model, loader, optimizer, device, epoch)
        torch.save(model.state_dict(), "model/goldfish_model.pt")
        # print("Model saved to model/goldfish_model.pt")


def load_training_data(data_dir="data", max_files=50):
    all_files = sorted(
        [f for f in os.listdir(data_dir) if f.endswith(".pt")],
        key=lambda x: os.path.getmtime(os.path.join(data_dir, x)),
        reverse=True
    )[:max_files]

    all_data = []
    for filename in all_files:
        if filename.endswith(".pt"):
            filepath = os.path.join(data_dir, filename)
            game_data = torch.load(filepath)
            all_data.extend(game_data)

    # print(f"Loaded {len(all_data)} training samples from {data_dir}")
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

def train_one_epoch(model: GoldfishModel, dataloader: DataLoader, optimizer: torch.optim.Adam, device: torch.device, epoch: int):
    model.train()
    total_policy_loss = 0.0
    total_value_loss = 0.0
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
        total_policy_loss += policy_loss.item()

        value_loss = F.mse_loss(pred_values, target_values)
        total_value_loss += value_loss.item()

        loss = policy_loss + value_loss

        # Backprop
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        total_loss += loss.item()

    avg_policy_loss = total_policy_loss / len(dataloader) if len(dataloader) > 0 else 0.0
    avg_value_loss = total_value_loss / len(dataloader) if len(dataloader) > 0 else 0.0
    avg_loss = total_loss / len(dataloader) if len(dataloader) > 0 else 0.0
    print(f"Average training loss: {avg_loss:.4f}")

    # Log to CSV
    os.makedirs("logs", exist_ok=True)
    log_file = "logs/training_loss.csv"
    write_header = not os.path.exists(log_file)

    with open(log_file, mode="a", newline="") as file:
        writer = csv.writer(file)
        if write_header:
            writer.writerow([
            epoch,
            avg_loss,
            avg_policy_loss,
            avg_value_loss,
            # avg_top1_acc,
            # avg_value_output
        ])
            
        writer.writerow([epoch,avg_loss,avg_policy_loss,avg_value_loss,
            # avg_top1_acc,
            # avg_value_output
        ])