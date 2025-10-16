# train_snn_event_debug.py
# Minimal, clean example: Spiking CNN (snnTorch) trained on synthetic event-like data.
# Dodani printovi za praćenje napretka (bez promjena konfiguracije)
# želimo ča manji loss i ča veći accuracy




'''Jako dobar izGPTjani explanation
Sjajno — idemo! Donosim detaljno, znanstveno i praktično objašnjenje koda kroz nekoliko jasno strukturiranih paragrafa. Bit ću precizan oko matematičke i implementacijske strane (objašnjenja membrane, surrogate gradijenta, oblik podataka, itd.), ali i praktičan s preporukama za poboljšanja i testove koje možeš brzo isprobati. Idemo nabrijano!

### 1. Opći pregled arhitekture i svrha skripte

Ovaj skript je minimalni, jasno strukturirani primjer treniranja spiking konvolucijske neuronske mreže (SNN) koristeći knjižnicu snnTorch na sintetičkim "event-like" podacima. Glavni ciljevi su: (1) demonstrirati kako prosljeđivati binarne spike sekvence kroz vremenski petlju, (2) pokazati uporabu Leaky spiking neurona s surrogate gradijentom za treniranje backpropagationom i (3) pružiti reproducibilan tijek treniranja i evaluacije (loss, accuracy). Model integrira vremenske informacije akumuliranjem izlaza kroz sve timestepe i na kraju računa prosječne logit-e, što je jednostavna ali učinkovita strategija za agregaciju informacija u SNN-u.

### 2. Strukturiranje i značenje sintetčkih podataka

Dataset klase `SyntheticEventDataset` (i kompleksnija varijanta `ComplexSyntheticEventDataset`) generira sekvence dimenzija `(T, 1, H, W)` gdje je T broj vremenskih koraka, H i W su prostorne dimenzije (32×32). Svaki primjer simulira jednostavne event-like fenomene: horizontalnu/vertikalnu traku, dijagonalnu točku ili odbijajući kvadrat. Sekvence su binarne nakon primjene Bernoulli uzorka — to modelira spike izdavanja događaja (1 = spike, 0 = nijema aktivnost). Time se dobiva dataset koji je vremenski bogat (temporalna dinamika nosi ključnu informaciju), što je idealno za SNN koji koristi dinamiku membrane neurona za kodiranje tih informacija.

### 3. Predprocesiranje i dimenzionalnosti pri batchiranju

U trening petlji primijetit ćeš permutaciju dimenzija ako su spike sekvence učitane u obliku `(batch, T, 1, H, W)` — kod je pripremljen da prihvati ulaz u obliku `(T, batch, 1, H, W)` (vrijeme prvo) prije prosljeđivanja u model. Ova konvencija olakšava iteriranje po vremenu i istovremeno izbjegava nepotrebno kopiranje podatkovnih blokova. Također, u `forward` metodi model inicijalizira memorijske tenzore (`mem1`, `mem2`, `memfc`) dimenzija koje odgovaraju izlazima konvolucijskih slojeva i punih veza, što osigurava kontinuitet stanja membrane između koraka.

### 4. Spiking mehanika: Leaky model i surrogate gradijent

Model koristi `snn.Leaky` neurone sa parametriziranim `beta` (=0.95) koji definira faktor zaborava membrane (ekvivalent diskretnog eksponencijalnog zaborava). Na sloju se dobiva par `(spike, mem)` pri svakom koraku — spike je diskretna izlazna aktivacija (0/1), mem je novo stanje membrane. Za treniranje problema s nediferencijabilnim spike funkcijama koristi se surrogate gradijent (ovdje `surrogate.fast_sigmoid()`), koji daje glatku aproksimaciju derivacije spike funkcije tijekom backpropagationa. Ovo omogućava uvođenje standardnih optimizatora (Adam) te računanje gradijenata unatoč diskretnim aktivacijama.

### 5. Prosljeđivanje kroz mrežu i agregacija odgovora

Unutar vremenske petlje svaki frame prolazi kroz conv→spike→pool→conv→spike→pool→reshape→fc→spike→fc; izlazi iz svakog timestep-a (logit-i) se akumuliraju u `sum_output` i na kraju dijele s T kako bi se dobio prosječan logit. Ovaj pristup implicitno modelira temporalnu integraciju: neuron skuplja dokaze kroz vrijeme i konačna klasa se odlučuje na temelju kumulativne aktivnosti. Takav način agregacije je jednostavan i stabilan, ali postoji mogućnost poboljšanja (npr. ponderirana suma, attention po vremenu, ili korištenje readout-sloja koji uzima konačne membrane umjesto spikes).

### 6. Trening i metrika: cross-entropy, loss i accuracy

Koristi se `CrossEntropyLoss` koji očekuje realne logit-e (ne softmaxirane) i pravi label-e kao integer klasne indekse. Tijekom treninga skripta čuva kumulativni loss pomnožen s veličinom batcha kako bi vratio točan prosjek po epochu. Accuracy se računa standardno preko argmax predikcije. Ispisi (`print`) po 20 batch-eva daju uvid u konvergenciju — korisno prilikom debugiranja. Za stabilniji trening preporučam pratiti i konfuzijske matrice, per-class recall/precision te learning-rate schedulere (npr. ReduceLROnPlateau) jer SNN-ovi često zahtijevaju finiju regulaciju LR-a.

### 7. Implementacijske opaske i moguća poboljšanja koda

U tvom kodu postoje duplikati (dvije definicije `SyntheticEventDataset`, dvije instalacije paketa itd.) — vrijedi očistiti skriptu u finalnoj verziji i ostaviti samo jednu, jasno imenovanu varijantu (npr. `ComplexSyntheticEventDataset` za evaluacije robusnosti). Također, inicijalizacija mem tenzora unutar `forward` pretpostavlja da je batch dimenzija statična za cijeli poziv — to je ok za standardni DataLoader, ali pazi na `drop_last` i varijabilne batch-eve u eval modu. Još jedno praktično poboljšanje: spremanje i logiranje metrika (npr. TensorBoard ili CSV) kako bi mogao raditi analizu u postprocesu.

### 8. Eksperimentalne varijable i hiperpodešavanje

Ključne varijable koje imaš za eksperimentiranje su: `T` (broj timesteps), `beta` (leak), surrogate funkcija (različiti surrogate-i imaju različitu stabilnost), arhitektura konvolucija (filteri, stride, dodatni slojevi), te način readout-a (sum/last/attention). Također, možeš testirati različite razine spike-noise (Bernoulli p), augmentacije sekvenci (promjene brzine, pad), te batch-normalization između konvolucija i spiking slojeva (pažljivo — BN s diskretnim spikes treba pravilno pozicionirati). Za metrika-fluktuacije u SNN često pomaže povećanje broja epoha i manji learning rate.

### 9. Fizička interpretacija i potencijalna primjena

Ovakav model je dobar primjer kako SNN može iskoristiti rijetku, vremenski strukturiranu aktivnost (event kamere, neuromorphic senzori). Prednost SNN-a je energetska učinkovitost i prirodna kompatibilnost s event-driven inputom: u hardverskim implementacijama (neuromorphic čipovi) ovakav model može dati značajnu uštedu energije u odnosu na klasične frame-based CNN-e. U istraživačkim scenarijima možeš koristiti sintetički dataset kao prvi korak, a zatim preći na stvarne DVS (event camera) zapise.

### 10. Zaključak i konkretni prijedlozi za iduće korake

Kratko: kod je vrlo dobar kao edukativni i eksperimentalni primjer SNN-a na temporanim, binarnim podacima. Preporučam sljedeće konkretne korake: (1) očisti duplikate u skripti i standardiziraj dataset API; (2) dodaj metrike po klasi i logging (TensorBoard/CSV); (3) pokušaj različite readout strategije (npr. koristiti konačna stanja membrane umjesto sumiranja spikes); (4) isprobaj različite surrogate funkcije i smanji početni learning rate uz scheduler; (5) testiraj model na stvarnim DVS datasetima (npr. N-MNIST, DVS Gesture) kako bi procijenio prenosivost naučenih reprezentacija.


'''
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
