# train_snn_event_debug.py
# Minimal, clean example: Spiking CNN (snnTorch) trained on synthetic event-like data.
# Dodani printovi za praćenje napretka (bez promjena konfiguracije)
# želimo ča manji loss i ča veći accuracy

!pip install torch torchvision snntorch


import math
import torch
import torch.nn as nn
import torch.optim as optim
from torch.utils.data import Dataset, DataLoader
import snntorch as snn
from snntorch import surrogate
import random, time

# ---- Hyperparams ----
device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
T = 16
batch_size = 32
epochs = 20
lr = 1e-3
num_classes = 4
img_size = 32

print(f"[INFO] Device: {device}")
print(f"[INFO] Hyperparams -> T={T}, batch_size={batch_size}, epochs={epochs}, lr={lr}")
print("[INFO] Import & setup complete.\n")

# ---- Synthetic event-based dataset ----
class SyntheticEventDataset(Dataset):
    def __init__(self, length=2000, T=16, img_size=32):
        self.length = length
        self.T = T
        self.H = img_size
        self.W = img_size
        print(f"[DATASET] SyntheticEventDataset initialized with {length} samples ({T} timesteps).")

    def __len__(self):
        return self.length

    def __getitem__(self, idx):
        cls = random.randrange(num_classes)
        seq = torch.zeros(self.T, 1, self.H, self.W, dtype=torch.float32)

        if cls == 0:  # horizontal bar
            bar_h = 3
            start = random.randint(0, self.H - bar_h - 1)
            velocity = random.choice([1, 2])
            for t in range(self.T):
                pos = (start + t*velocity) % (self.H - bar_h)
                seq[t, 0, pos:pos+bar_h, :] = 1.0
        elif cls == 1:  # vertical bar
            bar_w = 3
            start = random.randint(0, self.W - bar_w - 1)
            velocity = random.choice([1, 2])
            for t in range(self.T):
                pos = (start + t*velocity) % (self.W - bar_w)
                seq[t, 0, :, pos:pos+bar_w] = 1.0
        elif cls == 2:  # diagonal
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

# ---- Spiking CNN ----
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

        print("[MODEL] SpikingCNN initialized.")

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

# ---- Train / Eval ----
def train_epoch(model, loader, criterion, optimizer, epoch):
    model.train()
    total_loss, correct, total = 0, 0, 0
    start_time = time.time()

    for batch_idx, (spikes, labels) in enumerate(loader):
        spikes, labels = spikes.to(device), labels.to(device)
        if spikes.dim() == 5 and spikes.shape[1] == T:
            spikes = spikes.permute(1, 0, 2, 3, 4).contiguous()

        optimizer.zero_grad()
        logits = model(spikes)
        loss = criterion(logits, labels)
        loss.backward()
        optimizer.step()

        total_loss += loss.item() * labels.size(0)
        preds = logits.argmax(dim=1)
        correct += (preds == labels).sum().item()
        total += labels.size(0)

        if (batch_idx + 1) % 20 == 0:
            print(f"  [Train] Epoch {epoch} | Batch {batch_idx+1}/{len(loader)} | Loss {loss.item():.4f}")

    duration = time.time() - start_time
    return total_loss / total, correct / total, duration

def eval_epoch(model, loader, criterion):
    model.eval()
    total_loss, correct, total = 0, 0, 0
    with torch.no_grad():
        for spikes, labels in loader:
            spikes, labels = spikes.to(device), labels.to(device)
            if spikes.dim() == 5 and spikes.shape[1] == T:
                spikes = spikes.permute(1, 0, 2, 3, 4).contiguous()
            logits = model(spikes)
            loss = criterion(logits, labels)
            total_loss += loss.item() * labels.size(0)
            preds = logits.argmax(dim=1)
            correct += (preds == labels).sum().item()
            total += labels.size(0)
    return total_loss / total, correct / total

# ---- Data setup ----
print("[INFO] Initializing datasets and loaders...")
train_ds = SyntheticEventDataset(length=3000, T=T, img_size=img_size)
val_ds = SyntheticEventDataset(length=600, T=T, img_size=img_size)
train_loader = DataLoader(train_ds, batch_size=batch_size, shuffle=True, drop_last=True)
val_loader = DataLoader(val_ds, batch_size=batch_size)
print("[INFO] Datasets ready.\n")

# ---- Model / Training ----
model = SpikingCNN(num_classes=num_classes).to(device)
criterion = nn.CrossEntropyLoss()
optimizer = optim.Adam(model.parameters(), lr=lr)

print("[TRAINING] Starting training...\n")

for epoch in range(1, epochs + 1):
    train_loss, train_acc, train_time = train_epoch(model, train_loader, criterion, optimizer, epoch)
    val_loss, val_acc = eval_epoch(model, val_loader, criterion)
    print(f"[EPOCH {epoch:02d}] Time {train_time:.1f}s | Train Loss {train_loss:.4f} Acc {train_acc*100:.2f}% | "
          f"Val Loss {val_loss:.4f} Acc {val_acc*100:.2f}%\n")

torch.save(model.state_dict(), "spiking_cnn_synthetic.pth")
print("[DONE] Training finished, model saved to spiking_cnn_synthetic.pth")
