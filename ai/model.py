import torch, torch.nn as nn, torch.nn.functional as F

class Goldfish(nn.Module):

    def __init__(self):
        super().__init__()

        # Convolutional layers
        self.conv1 = nn.Conv2d(18, 64, 3, padding=1)
        self.conv2 = nn.Conv2d(64, 64, 3, padding=1)
        self.conv3 = nn.Conv2d(64, 64, 3, padding=1)

        # Policy Head
        self.policy_conv = nn.Conv2d(64, 2, kernel_size=1)
        self.policy_fc = nn.Linear(2 * 8 * 8, 4096)

        # Value Head
        self.value_conv = nn.Conv2d(64, 1, kernel_size=1)
        self.value_fc1 = nn.Linear(8 * 8, 64)
        self.value_fc2 = nn.Linear(64, 1)

    def forward(self, x):

        # Shared convolutional layers
        x = F.relu(self.conv1(x))
        x = F.relu(self.conv2(x))
        x = F.relu(self.conv3(x))

        # Policy Head
        p = F.relu(self.policy_conv(x))
        p = p.view(p.size(0), -1)
        p = self.policy_fc(p)

        # Value Head
        v = F.relu(self.value_conv(x))
        v = v.view(v.size(0), -1)
        v = F.relu(self.value_fc1(v))
        v = torch.tanh(self.value_fc2(v))

        return {
            "policy": p, # softmax later
            "value": v
        }