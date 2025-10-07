'''
cls == 0 → horizontalna traka koja se pomiče dolje

cls == 1 → vertikalna traka koja se pomiče desno

cls == 2 → dijagonalna točka koja se pomiče

cls == 3 → “bouncing” kvadrat
'''
!pip install torch torchvision torchaudio
!pip install matplotlib
!pip install snntorch


# ---------- IMPORTS ----------
import torch
import torch.nn as nn
import matplotlib.pyplot as plt
import random
import snntorch as snn
from snntorch import surrogate

# ---------- HYPERPARAMS ----------
T = 16
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
img_size = 32
num_classes = 4

# ---------- SYNTHETIC EVENT DATASET ----------
class SyntheticEventDataset(torch.utils.data.Dataset):
    def __init__(self, length=5, T=16, img_size=32):
        self.length = length
        self.T = T
        self.H = img_size
        self.W = img_size

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        cls = random.randrange(num_classes)
        seq = torch.zeros(self.T, 1, self.H, self.W, dtype=torch.float32)

        if cls == 0:  # horizontal bar moving down
            bar_h = 3
            start = random.randint(0, self.H - bar_h - 1)
            velocity = random.choice([1, 2])
            for t in range(self.T):
                pos = (start + t*velocity) % (self.H - bar_h)
                seq[t, 0, pos:pos+bar_h, :] = 1.0
        elif cls == 1:  # vertical bar moving right
            bar_w = 3
            start = random.randint(0, self.W - bar_w - 1)
            velocity = random.choice([1, 2])
            for t in range(self.T):
                pos = (start + t*velocity) % (self.W - bar_w)
                seq[t, 0, :, pos:pos+bar_w] = 1.0
        elif cls == 2:  # diagonal moving dot
            x0 = random.randint(0, self.W-1)
            y0 = random.randint(0, self.H-1)
            vx = random.choice([1, -1])
            vy = random.choice([1, -1])
            for t in range(self.T):
                x = (x0 + t*vx) % self.W
                y = (y0 + t*vy) % self.H
                seq[t, 0, y, x] = 1.0
        else:  # bouncing square
            size = 5
            x = random.randint(0, self.W-size-1)
            y = random.randint(0, self.H-size-1)
            vx = random.choice([1, -1])
            vy = random.choice([1, -1])
            for t in range(self.T):
                x = (x + vx) % (self.W - size)
                y = (y + vy) % (self.H - size)
                seq[t, 0, y:y+size, x:x+size] = 1.0

        spikes = torch.bernoulli(seq)
        label = torch.tensor(cls, dtype=torch.long)
        return spikes, label

class ComplexSyntheticEventDataset(torch.utils.data.Dataset):
    def __init__(self, length=5, T=16, img_size=32):
        self.length = length
        self.T = T
        self.H = img_size
        self.W = img_size

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        cls = random.randrange(num_classes)
        seq = torch.zeros(self.T, 1, self.H, self.W, dtype=torch.float32)

        if cls == 0:
            # Horizontalna traka koja se pomiče, ali mijenja brzinu i smjer
            bar_h = random.randint(2, 4)
            pos = random.randint(0, self.H - bar_h - 1)
            velocity = random.choice([1, 2])
            direction = 1
            for t in range(self.T):
                pos += velocity * direction
                if pos + bar_h >= self.H or pos <= 0:
                    direction *= -1  # bounce
                seq[t, 0, pos:pos+bar_h, :] = 1.0

        elif cls == 1:
            # Vertikalna traka s periodičnim “bljeskanjem”
            bar_w = random.randint(2, 4)
            pos = random.randint(0, self.W - bar_w - 1)
            velocity = random.choice([1, 2])
            for t in range(self.T):
                pos = (pos + velocity) % (self.W - bar_w)
                if t % random.choice([3, 4, 5]) != 0:  # povremeno “nestane”
                    seq[t, 0, :, pos:pos+bar_w] = 1.0

        elif cls == 2:
            # Dijagonalna točka koja mijenja smjer nakon nekoliko frameova
            x = random.randint(0, self.W-1)
            y = random.randint(0, self.H-1)
            vx, vy = random.choice([-1, 1]), random.choice([-1, 1])
            for t in range(self.T):
                if t % random.randint(4, 7) == 0:  # promijeni smjer
                    vx, vy = -vx, -vy
                x = (x + vx) % self.W
                y = (y + vy) % self.H
                seq[t, 0, y, x] = 1.0

        else:
            # “Bouncing” kvadrat koji se odbija od rubova i mijenja veličinu
            size = random.randint(3, 6)
            x, y = random.randint(0, self.W-size-1), random.randint(0, self.H-size-1)
            vx, vy = random.choice([-1, 1]), random.choice([-1, 1])
            for t in range(self.T):
                if x + size >= self.W or x <= 0:
                    vx *= -1
                if y + size >= self.H or y <= 0:
                    vy *= -1
                x += vx
                y += vy

                if t % random.randint(3, 5) == 0:
                    size = min(max(2, size + random.choice([-1, 1])), 6)

                seq[t, 0, y:y+size, x:x+size] = 1.0

        # Bernoulli noise simulira spike jitter (realnije ponašanje senzora)
        spikes = torch.bernoulli(seq * random.uniform(0.8, 1.0))
        label = torch.tensor(cls, dtype=torch.long)
        return spikes, label

# ---------- SPIKING CNN ----------
class SpikingCNN(nn.Module):
    def __init__(self, num_classes=4):
        super().__init__()
        self.conv1 = nn.Conv2d(1, 16, kernel_size=3, padding=1)
        self.pool = nn.MaxPool2d(2)
        self.conv2 = nn.Conv2d(16, 32, kernel_size=3, padding=1)
        self.fc1 = nn.Linear(32 * (img_size//4) * (img_size//4), 128)
        self.fc2 = nn.Linear(128, num_classes)

        self.beta = 0.95
        spike_grad = surrogate.fast_sigmoid()
        self.mem_layer1 = snn.Leaky(beta=self.beta, spike_grad=spike_grad)
        self.mem_layer2 = snn.Leaky(beta=self.beta, spike_grad=spike_grad)
        self.mem_fc = snn.Leaky(beta=self.beta, spike_grad=spike_grad)

    def forward(self, input_seq):
        T, batch = input_seq.shape[0], input_seq.shape[1]
        mem1 = torch.zeros((batch, 16, img_size//2, img_size//2), device=input_seq.device)
        mem2 = torch.zeros((batch, 32, img_size//4, img_size//4), device=input_seq.device)
        memfc = torch.zeros((batch, 128), device=input_seq.device)
        sum_output = torch.zeros(batch, num_classes, device=input_seq.device)

        for t in range(T):
            x_t = input_seq[t]
            x = self.conv1(x_t)
            s1, mem1 = self.mem_layer1(x, mem1)
            x = self.pool(s1)
            x = self.conv2(x)
            s2, mem2 = self.mem_layer2(x, mem2)
            x = self.pool(s2)

            x = x.view(batch, -1)
            x = self.fc1(x)
            sfc, memfc = self.mem_fc(x, memfc)
            out = self.fc2(sfc)
            sum_output += out

        logits = sum_output / T
        return logits

# ---------- LOAD MODEL ----------
model = SpikingCNN(num_classes=num_classes).to(device)
model.load_state_dict(torch.load("spiking_cnn_synthetic.pth", map_location=device))
model.eval()
print("[MODEL] Loaded successfully")

# ---------- GENERATE TEST DATA ----------
dataset = ComplexSyntheticEventDataset(length=5, T=T, img_size=img_size) #add or remove Complex from dataset name
print(f"[DATASET] Generated {len(dataset)} test samples")

# ---------- PREDICTIONS + VISUALIZATION ----------
for i in range(len(dataset)):
    spikes, label = dataset[i]
    spikes_batch = spikes.unsqueeze(1).to(device)  # (T,1,1,H,W)

    with torch.no_grad():
        logits = model(spikes_batch)
        pred_class = logits.argmax(dim=1).item()

    print(f"Primjer {i}: True label = {label.item()}, Predicted = {pred_class}")

    # Vizualizacija spike sekvenci kroz vrijeme
    fig, axes = plt.subplots(2, T//2, figsize=(15,4))
    fig.suptitle(f"Sample {i}, True={label.item()}, Pred={pred_class}")
    for t in range(T):
        ax = axes[t//(T//2), t%(T//2)]
        ax.imshow(spikes[t,0].cpu(), cmap="gray")
        ax.axis("off")
        ax.set_title(f"T={t}")
    plt.show()
