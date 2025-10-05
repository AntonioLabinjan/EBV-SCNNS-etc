---

# 🧮 Zadatak (primjer)

Imamo sliku (grayscale) dimenzija 4×4:

$$
I =
\begin{bmatrix}
10 & 10 & 10 & 10[4pt]
10 & 20 & 20 & 10[4pt]
10 & 20 & 20 & 10[4pt]
10 & 10 & 10 & 10
\end{bmatrix}
$$

Primijeni Laplaceov filter s kernelom (4-neighbour Laplacian):

$$
K =
\begin{bmatrix}
0 & 1 & 0[4pt]
1 & -4 & 1[4pt]
0 & 1 & 0
\end{bmatrix}
$$

Izračunaj rezultat konvolucije (**valid mode** — samo pozicije gdje kernel u potpunosti stane) i interpretiraj rezultat. Također, pokažimo kako bi isti Laplacian koristio za *sharpening*.

---

# 🧠 Korak-po-korak (ručni izračun)

Za 3×3 kernel i 4×4 sliku, valid (bez paddinga) izlazna mapa ima dimenzije
$$(4-3+1) \times (4-3+1) = 2 \times 2.$$

Centri kernel-prolaza su na pozicijama slike s indeksima (1,1), (1,2), (2,1), (2,2) (0-based indexing).

---

### 1️⃣ Pozicija centra (1,1)

Okolica (redovi 0..2, kolone 0..2):

$$
\begin{bmatrix}
10 & 10 & 10\
10 & 20 & 20\
10 & 20 & 20
\end{bmatrix}
$$

Primjena kernela:

* top middle: $1 \cdot 10 = 10$
* middle left: $1 \cdot 10 = 10$
* center: $-4 \cdot 20 = -80$
* middle right: $1 \cdot 20 = 20$
* bottom middle: $1 \cdot 20 = 20$

Zbroj: $10 + 10 - 80 + 20 + 20 = -20$
➡️ **Izlaz = -20**

---

### 2️⃣ Pozicija centra (1,2)

Okolica (redovi 0..2, kolone 1..3):

$$
\begin{bmatrix}
10 & 10 & 10\
20 & 20 & 10\
20 & 20 & 10
\end{bmatrix}
$$

Zbroj: $10 + 20 - 80 + 10 + 20 = -20$
➡️ **Izlaz = -20**

---

### 3️⃣ Pozicija centra (2,1)

Okolica (redovi 1..3, kolone 0..2):

$$
\begin{bmatrix}
10 & 20 & 20\
10 & 20 & 20\
10 & 10 & 10
\end{bmatrix}
$$

Zbroj: $20 + 10 - 80 + 20 + 10 = -20$
➡️ **Izlaz = -20**

---

### 4️⃣ Pozicija centra (2,2)

Okolica (redovi 1..3, kolone 1..3):

$$
\begin{bmatrix}
20 & 20 & 10\
20 & 20 & 10\
10 & 10 & 10
\end{bmatrix}
$$

Zbroj: $20 + 20 - 80 + 10 + 10 = -20$
➡️ **Izlaz = -20**

---

### ✅ Rezultat (valid izlaz 2×2):

$$
L =
\begin{bmatrix}
-20 & -20\
-20 & -20
\end{bmatrix}
$$

**Interpretacija:**
Laplacian daje negativne vrijednosti u centru 2×2 bloka zato što je centar (20) **svjetliji** od svojih susjeda (10).
Negativna vrijednost znači „konkavna” promjena intenziteta — vrh svjetline.
Često za detekciju rubova koristimo apsolutnu vrijednost ili thresholdiranje:
$$|L| \quad \text{ili} \quad L > \text{threshold}.$$

---

# 💡 Kako koristiti rezultat (edge detection i sharpening)

* **Edge detection:**
  $$\text{edge} = (|L| > \tau)$$

* **Sharpening:**
  Additivno kombiniramo original i (negirani) Laplacian:
  $$
  I_{\text{sharp}} = I_{\text{orig}} - \alpha \cdot \text{Laplacian}
  $$

Ako uzmemo centar originala $20$ i Laplacian $-20$, uz $\alpha = 1$:
$$
I_{\text{sharp, center}} = 20 - (-20) = 40
$$
Dakle centar postaje svjetliji → povećava kontrast i oštrinu (uz clip u [0,255]).

---

# 🧩 Python primjer (NumPy + SciPy)

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
```

---

# 📘 Sažetak

* **Laplacian** mjeri *drugu derivaciju* intenziteta — detektira mjesta naglih promjena (rubove, vrhove, udubine).
* Klasični kernel:
  $$
  \begin{bmatrix}
  0 & 1 & 0\
  1 & -4 & 1\
  0 & 1 & 0
  \end{bmatrix}
  $$
  ili varijanta s -8 u centru (8-neighbour).
* Rezultati mogu biti negativni ili pozitivni → koristi se apsolutna vrijednost ili threshold.
* Za *sharpening* kombiniramo original i (negirani) Laplacian.

---

