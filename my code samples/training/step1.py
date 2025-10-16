# KOD
# Revidirani minimalni SNN: trening + evaluacija (robustan)
import torch
import torch.nn as nn
import snntorch as snn
from snntorch import surrogate
from torch.utils.data import DataLoader, TensorDataset

# ---------- Podaci ----------
def generate_synthetic_data(n_samples=200, img_size=16):
    X = torch.zeros((n_samples, 1, img_size, img_size))
    y = torch.zeros(n_samples, dtype=torch.long)
    for i in range(n_samples):
        if torch.rand(1).item() > 0.5:
            y[i] = 1
            X[i, 0, 4:12, 4:12] = 1.0  # kvadrat
        else:
            y[i] = 0
            rr, cc = torch.meshgrid(torch.arange(img_size), torch.arange(img_size), indexing='ij')
            mask = (rr - 8)**2 + (cc - 8)**2 < 16
            X[i, 0][mask] = 1.0  # krug
    return X, y

X, y = generate_synthetic_data(400)
train_X, test_X = X[:300], X[300:]
train_y, test_y = y[:300], y[300:]

train_dl = DataLoader(TensorDataset(train_X, train_y), batch_size=16, shuffle=True)
test_dl = DataLoader(TensorDataset(test_X, test_y), batch_size=16)

# ---------- Model (time loop unutar forward) ----------
class SpikingCNN(nn.Module):
    def __init__(self, num_steps=10):
        super().__init__()
        self.num_steps = num_steps
        self.conv1 = nn.Conv2d(1, 8, 3, padding=1)                 # -> (B,8,16,16)
        self.lif1 = snn.Leaky(beta=0.9, spike_grad=surrogate.fast_sigmoid())
        self.fc1 = nn.Linear(8 * 16 * 16, 2)                       # -> (B,2)
        self.lif2 = snn.Leaky(beta=0.9, spike_grad=surrogate.fast_sigmoid())

    def forward(self, x):
        batch = x.size(0)
        device = x.device

        # eksplicitna inicijalizacija membrane (stabilno)
        mem1 = torch.zeros((batch, 8, 16, 16), device=device)   # za conv1 izlaz
        mem2 = torch.zeros((batch, 2), device=device)           # za fc izlaz (readout)

        sum_out = torch.zeros((batch, 2), device=device)

        for _ in range(self.num_steps):
            cur1 = self.conv1(x)               # feed-forward konv
            spk1, mem1 = self.lif1(cur1, mem1) # spiking iz conv
            flat = spk1.view(batch, -1)
            cur2 = self.fc1(flat)
            spk2, mem2 = self.lif2(cur2, mem2)
            sum_out += spk2

        # vratimo kumulativne logite (ili prosjek -> ali prosjek samo skala)
        return sum_out

# ---------- Setup ----------
device = 'cuda' if torch.cuda.is_available() else 'cpu'
num_steps = 10
net = SpikingCNN(num_steps=num_steps).to(device)
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()

# ---------- Trening ----------
n_epochs = 5
for epoch in range(n_epochs):
    net.train()
    epoch_loss = 0.0
    for data, targets in train_dl:
        data, targets = data.to(device), targets.to(device)

        optimizer.zero_grad()
        outputs = net(data)                # forward (sadrži time-loop)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()

        epoch_loss += loss.item() * data.size(0)

    epoch_loss /= len(train_dl.dataset)
    print(f"Epoch {epoch+1}/{n_epochs} - Loss: {epoch_loss:.4f}")

# ---------- Evaluacija ----------
net.eval()
correct = 0
total = 0
with torch.no_grad():
    for data, targets in test_dl:
        data, targets = data.to(device), targets.to(device)
        outputs = net(data)
        preds = outputs.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)

print(f"Test accuracy: {100.0 * correct / total:.2f}%")

'''
---

# Minimalni Spiking CNN - Dokumentacija

## 1️⃣ Biblioteke

* `torch` → glavni PyTorch framework za tensore i autograd.
* `torch.nn` → definicija neuronskih mreža (layers, loss, itd.).
* `snntorch` → biblioteka za Spiking Neural Networks (SNN).
* `snntorch.surrogate` → surrogate gradijenti za spike funkcije.
* `DataLoader` i `TensorDataset` → batchiranje i iteracija nad datasetom.

---

## 2️⃣ Sintetički podaci

```python
X, y = generate_synthetic_data(400)
train_X, test_X = X[:300], X[300:]
train_y, test_y = y[:300], y[300:]
train_dl = DataLoader(TensorDataset(train_X, train_y), batch_size=16, shuffle=True)
test_dl = DataLoader(TensorDataset(test_X, test_y), batch_size=16)
```

* Kreiramo 400 slika dimenzija 16x16.
* Pola su kvadrati, pola krugovi.
* 300 za trening, 100 za test.
* Batch size = 16.

---

## 3️⃣ Spiking CNN Model

```python
class SpikingCNN(nn.Module):
    def __init__(self, num_steps=10):
        super().__init__()
        self.num_steps = num_steps
        self.conv1 = nn.Conv2d(1, 8, 3, padding=1)                 # (B,8,16,16)
        self.lif1 = snn.Leaky(beta=0.9, spike_grad=surrogate.fast_sigmoid())
        self.fc1 = nn.Linear(8 * 16 * 16, 2)                       # (B,2)
        self.lif2 = snn.Leaky(beta=0.9, spike_grad=surrogate.fast_sigmoid())
```

* `conv1` → konvolucijski sloj.
* `lif1` → Leaky Integrate-and-Fire neuron.
* `fc1` → linearni sloj za 2 klase.
* `lif2` → LIF neuron za izlaz.
* `num_steps` → broj vremenskih koraka za simulaciju.

### Forward funkcija

```python
mem1 = torch.zeros((batch, 8, 16, 16), device=device)
mem2 = torch.zeros((batch, 2), device=device)
sum_out = torch.zeros((batch, 2), device=device)
for _ in range(self.num_steps):
    cur1 = self.conv1(x)
    spk1, mem1 = self.lif1(cur1, mem1)
    flat = spk1.view(batch, -1)
    cur2 = self.fc1(flat)
    spk2, mem2 = self.lif2(cur2, mem2)
    sum_out += spk2
return sum_out
```

* `mem1/mem2` → membrane potentials.
* Petlja simulira spikeove kroz `num_steps` timesteps.
* `sum_out` → kumulativni spike logiti, koristi se za loss.

---

## 4️⃣ Setup treniranja

```python
device = 'cuda' if torch.cuda.is_available() else 'cpu'
net = SpikingCNN(num_steps=10).to(device)
optimizer = torch.optim.Adam(net.parameters(), lr=1e-3)
criterion = nn.CrossEntropyLoss()
```

* Koristimo GPU ako postoji.
* Adam optimizer.
* CrossEntropyLoss za klasifikaciju.

---

## 5️⃣ Trening

```python
for epoch in range(n_epochs):
    net.train()
    for data, targets in train_dl:
        data, targets = data.to(device), targets.to(device)
        optimizer.zero_grad()
        outputs = net(data)
        loss = criterion(outputs, targets)
        loss.backward()
        optimizer.step()
```

* Standardni loop po epozi i batchu.
* Forward simulira spikeove kroz timesteps.
* Backprop jednom po batchu.

---

## 6️⃣ Evaluacija

```python
net.eval()
correct = 0
total = 0
with torch.no_grad():
    for data, targets in test_dl:
        data, targets = data.to(device), targets.to(device)
        outputs = net(data)
        preds = outputs.argmax(dim=1)
        correct += (preds == targets).sum().item()
        total += targets.size(0)
accuracy = 100.0 * correct / total
```

* `net.eval()` → isključuje training-specific behavior.
* `torch.no_grad()` → deaktivira gradijente.
* Predikcija = argmax kumulativnih spike logita.
* Izračunavamo točnost na test setu.

---

## 🔑 Bitne napomene

1. Model je **Spiking CNN**: aktivacija neurona = spike, ne kontinuirana.
2. `mem1/mem2` → pohrana membrane potencijala (LIF).
3. Forward simulira `num_steps` timesteps.
4. Kumulativni spike output → proxy za rate-based output.
5. Trening: optimizer + loss + backward, **jedan backward po batchu**.
6. Evaluacija: standardna klasifikacija → argmax na kumulativne logite.
'''


'''
Epoch 1/5 - Loss: 0.6931
Epoch 2/5 - Loss: 0.2131
Epoch 3/5 - Loss: 0.0111
Epoch 4/5 - Loss: 0.0019
Epoch 5/5 - Loss: 0.0007
Test accuracy: 100.00%
'''
