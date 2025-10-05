
---

```markdown
# 🧮 Zadatak (primjer)

Imamo grayscale sliku dimenzija 4×4:

```

I =
[[10, 10, 10, 10],
[10, 20, 20, 10],
[10, 20, 20, 10],
[10, 10, 10, 10]]

```

Primijeni Laplaceov filter s kernelom (4-neighbour Laplacian):

```

K =
[[ 0,  1,  0],
[ 1, -4,  1],
[ 0,  1,  0]]

```

Izračunaj rezultat konvolucije (**valid mode** — samo pozicije gdje kernel u potpunosti stane) i interpretiraj rezultat.  
Također, pokažimo kako bi isti Laplacian koristio za *sharpening*.

---

## 🧠 Korak-po-korak (ručni izračun)

Za 3×3 kernel i 4×4 sliku, izlaz u **valid modu** ima dimenzije:

```

(4 - 3 + 1) x (4 - 3 + 1) = 2 x 2

```

Centri kernel-prolaza su na pozicijama slike (1,1), (1,2), (2,1), (2,2) (0-based indexing).

---

### 1️⃣ Pozicija centra (1,1)

Okolica:

```

10  10  10
10  20  20
10  20  20

```

Primjena kernela:

```

(1*10) + (1*10) + (-4*20) + (1*20) + (1*20)
= 10 + 10 - 80 + 20 + 20 = -20

```

➡️ **Izlaz = -20**

---

### 2️⃣ Pozicija centra (1,2)

Okolica:

```

10  10  10
20  20  10
20  20  10

```

Zbroj: `10 + 20 - 80 + 10 + 20 = -20`  
➡️ **Izlaz = -20**

---

### 3️⃣ Pozicija centra (2,1)

Okolica:

```

10  20  20
10  20  20
10  10  10

```

Zbroj: `20 + 10 - 80 + 20 + 10 = -20`  
➡️ **Izlaz = -20**

---

### 4️⃣ Pozicija centra (2,2)

Okolica:

```

20  20  10
20  20  10
10  10  10

```

Zbroj: `20 + 20 - 80 + 10 + 10 = -20`  
➡️ **Izlaz = -20**

---

### ✅ Rezultat (valid izlaz 2×2):

```

L =
[[-20, -20],
[-20, -20]]

```

**Interpretacija:**  
Laplacian daje negativne vrijednosti u centru 2×2 bloka zato što je centar (20) svjetliji od svojih susjeda (10).  
Negativna vrijednost znači **konkavna promjena intenziteta** — vrh svjetline.  
Za detekciju rubova često uzimamo apsolutnu vrijednost ili thresholdiranje:

```

|L|    ili    L > threshold

```

---

## 💡 Kako koristiti rezultat (edge detection i sharpening)

**Edge detection:**
```

edge = (|L| > τ)

```

**Sharpening:**
Dodamo negirani Laplacian na original:

```

I_sharp = I - α * L

```

Ako uzmemo centar originala 20 i Laplacian -20, uz α=1:
```

I_sharp_center = 20 - (-20) = 40

````
Dakle centar postaje svjetliji → povećava kontrast i oštrinu.

---

## 🧩 Python primjer (NumPy + SciPy)

```python
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

I = np.array([
 [10,10,10,10],
 [10,20,20,10],
 [10,20,20,10],
 [10,10,10,10]
], dtype=float)

K = np.array([[0,1,0],
              [1,-4,1],
              [0,1,0]], dtype=float)

# valid konvolucija
L_valid = convolve2d(I, K, mode='valid')
print("Laplacian (valid):\n", L_valid)

# sharpening
L_same = convolve2d(I, K, mode='same', boundary='fill', fillvalue=0)
I_sharp = I - L_same
I_sharp = np.clip(I_sharp, 0, 255)

print("Laplacian (same):\n", L_same)
print("Sharpened image:\n", I_sharp)

# prikaz
fig, axs = plt.subplots(1,3, figsize=(9,3))
axs[0].imshow(I, cmap='gray'); axs[0].set_title('Original'); axs[0].axis('off')
axs[1].imshow(L_same, cmap='bwr'); axs[1].set_title('Laplacian (same)'); axs[1].axis('off')
axs[2].imshow(I_sharp, cmap='gray'); axs[2].set_title('Sharpened'); axs[2].axis('off')
plt.show()
````

---

## 📘 Sažetak

* **Laplacian** mjeri *drugu derivaciju* intenziteta — detektira mjesta naglih promjena (rubove, vrhove, udubine).
* Klasični kernel:

  ```
  [ 0,  1,  0 ]
  [ 1, -4,  1 ]
  [ 0,  1,  0 ]
  ```

  ili varijanta s -8 u centru (8-neighbour).
* Rezultati mogu biti pozitivni ili negativni → koristi se apsolutna vrijednost ili threshold.
* Za *sharpening* kombiniramo original i negirani Laplacian:

  ```
  I_sharp = I - α * L
  ```

---



Zaključak:
Ahaaa, znači taj laplacian doslovno uzme grupu drukčijih piskela (s drukčijim intenzitetom) i detektira rub oko njih?

Točno tako! 🔥
Genijalno si to skužio — Laplacian **doslovno “vidi rubove”** jer mjeri **drugu derivaciju intenziteta** slike.

Evo kako to intuitivno funkcionira:

* Ako je područje slike **ravno** (svi pikseli sličnog intenziteta), onda su promjene male → **Laplacian ≈ 0**.
* Ako se **naglo promijeni svjetlina** (npr. s 10 na 20 ili s bijelog na crno), Laplacian “poludi” i da **velike pozitivne ili negativne vrijednosti**.
* Dakle, on **otkriva mjesta gdje se intenzitet naglo mijenja**, što su upravo **rubovi, konture, prelazi između objekata**.

Primjer:

```text
[10, 10, 10]
[10, 50, 10]
[10, 10, 10]
```

Tu središnji piksel (50) ima puno veću vrijednost od okoline.
Laplacian vidi to kao “puf, ovdje se nešto drastično promijenilo!” i u rezultatu dobiješ jak rub.

💡 Zato se često koristi za:

* **Edge detection** (rubove objekata),
* **Image sharpening** (naglašavanje detalja),
* I kao pre-processing korak u **feature ekstrakciji** za CV modele.

Hoćeš da ti pokažem istu stvar, ali na **pravoj slici (npr. pejzaž, portret ili face)** pa da vidiš koliko moćno izgleda kad se Laplacian primijeni “u stvarnosti”?
