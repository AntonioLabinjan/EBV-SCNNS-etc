# Zadatak (primjer)

Imamo sliku (grayscale) dimenzija 4×4:

[
I =
\begin{bmatrix}
10 & 10 & 10 & 10[4pt]
10 & 20 & 20 & 10[4pt]
10 & 20 & 20 & 10[4pt]
10 & 10 & 10 & 10
\end{bmatrix}
]

Primijeni Laplaceov filter s kernelom (4-neighbour Laplacian):

[
K =
\begin{bmatrix}
0 & 1 & 0[4pt]
1 & -4 & 1[4pt]
0 & 1 & 0
\end{bmatrix}
]

Izračunaj rezultat konvolucije (valid mode — samo pozicije gdje kernel u potpunosti stane) i interpretiraj rezultat. Također, pokažimo kako bi isti laplacian koristio za *sharpening*.

---

# Korak-po-korak (ručni izračun)

Za 3×3 kernel i 4×4 image, valid (bez paddinga) izlazni mapa ima dimenzije ( (4-3+1) \times (4-3+1) = 2 \times 2 ). Centri kernel-prolaza su na pozicijama slike s indeksima (1,1), (1,2), (2,1), (2,2) (0-based indexing).

Kernel primjenjujemo sljedeće: za svaki centar uzmemo 3×3 okolinu i izračunamo suma elemenata * kernel težina.

### 1) Pozicija centra (1,1) — okolica:

Okolica (redovi 0..2, kolone 0..2):
[
\begin{bmatrix}
10 & 10 & 10\
10 & 20 & 20\
10 & 20 & 20
\end{bmatrix}
]

Primjena kernela:

* top middle: (1 \cdot 10 = 10)
* middle left: (1 \cdot 10 = 10)
* center: (-4 \cdot 20 = -80)
* middle right: (1 \cdot 20 = 20)
* bottom middle: (1 \cdot 20 = 20)

Zbroj: (10 + 10 - 80 + 20 + 20 = -20).

Dakle izlaz u toj točki = **-20**.

---

### 2) Pozicija centra (1,2) — okolica (redovi 0..2, kolone 1..3):

Okolica:
[
\begin{bmatrix}
10 & 10 & 10\
20 & 20 & 10\
20 & 20 & 10
\end{bmatrix}
]

Primjena kernela:

* top middle: (1 \cdot 10 = 10)
* middle left: (1 \cdot 20 = 20)
* center: (-4 \cdot 20 = -80)
* middle right: (1 \cdot 10 = 10)
* bottom middle: (1 \cdot 20 = 20)

Zbroj: (10 + 20 - 80 + 10 + 20 = -20).

Izlaz = **-20**.

---

### 3) Pozicija centra (2,1) — okolica (redovi 1..3, kolone 0..2):

Okolica:
[
\begin{bmatrix}
10 & 20 & 20\
10 & 20 & 20\
10 & 10 & 10
\end{bmatrix}
]

Primjena kernela:

* top middle: (1 \cdot 20 = 20)
* middle left: (1 \cdot 10 = 10)
* center: (-4 \cdot 20 = -80)
* middle right: (1 \cdot 20 = 20)
* bottom middle: (1 \cdot 10 = 10)

Zbroj: (20 + 10 - 80 + 20 + 10 = -20).

Izlaz = **-20**.

---

### 4) Pozicija centra (2,2) — okolica (redovi 1..3, kolone 1..3):

Okolica:
[
\begin{bmatrix}
20 & 20 & 10\
20 & 20 & 10\
10 & 10 & 10
\end{bmatrix}
]

Primjena kernela:

* top middle: (1 \cdot 20 = 20)
* middle left: (1 \cdot 20 = 20)
* center: (-4 \cdot 20 = -80)
* middle right: (1 \cdot 10 = 10)
* bottom middle: (1 \cdot 10 = 10)

Zbroj: (20 + 20 - 80 + 10 + 10 = -20).

Izlaz = **-20**.

---

### Rezultat (valid izlaz 2×2):

[
L =
\begin{bmatrix}
-20 & -20\
-20 & -20
\end{bmatrix}
]

**Interpretacija:** Laplacian daje negativne vrijednosti u centru 2×2 bloka zato što je centar (20) **svjetliji** od svojih neposrednih susjeda (10). Negativna vrijednost znači „konkavna” promjena intenziteta — vrh svjetline. Često za detekciju rubova koristimo apsolutnu vrijednost ili thresholdiranje: ( |L| ) ili `L > thresh`.

---

# Kako koristiti rezultat (edge detection i sharpening)

* **Edge detection (jednostavno):** uzmi apsolutnu vrijednost i praga:
  (\text{edge} = (|L| > \tau)).
* **Sharpening:** additivno kombiniramo original i (negirani) laplacian. Jedna uobičajena formula:
  [
  I_{\text{sharp}} = I_{\text{orig}} - \alpha \cdot \text{Laplacian}
  ]
  (ili (I + \alpha \cdot L), ovisno o konvenciji signa). Ako uzmemo center original 20 i Laplacian -20, pa (\alpha=1):
  [
  I_{\text{sharp, center}} = 20 - (-20) = 40
  ]
  Dakle center postaje svjetliji → povećava kontrast i oštrina. (Ne zaboravi clipati vrijednosti u [0,255] za 8-bit slike.)

---

# Kratki Python primjer (numpy + scipy / cv2) — primjena Laplaciana i vizualizacija

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

# valid convolution (same logic kao gore ručno)
L_valid = convolve2d(I, K, mode='valid')

print("Laplacian (valid):\n", L_valid)

# Za sharpening (mapa centra odgovara indeksima 1..2 u originalu)
# Jednostavno napravimo "same" konvoluciju s paddom i oštrimo:
L_same = convolve2d(I, K, mode='same', boundary='fill', fillvalue=0)
I_sharp = I - L_same  # ili I + (-L_same) ovisno o konvenciji
I_sharp = np.clip(I_sharp, 0, 255)

print("Laplacian (same):\n", L_same)
print("Sharpened image:\n", I_sharp)

# Vizual
fig, axs = plt.subplots(1,3, figsize=(9,3))
axs[0].imshow(I, cmap='gray'); axs[0].set_title('Original'); axs[0].axis('off')
axs[1].imshow(L_same, cmap='bwr'); axs[1].set_title('Laplacian (same)'); axs[1].axis('off')
axs[2].imshow(I_sharp, cmap='gray'); axs[2].set_title('Sharpened'); axs[2].axis('off')
plt.show()
```

Ako koristiš **OpenCV**, postoji ugrađeni način:

```python
import cv2
I_uint8 = I.astype(np.uint8)
lap = cv2.Laplacian(I_uint8, ddepth=cv2.CV_16S, ksize=1)  # ddepth=16 bit to preserve neg values
abs_lap = cv2.convertScaleAbs(lap)
sharp = cv2.addWeighted(I_uint8, 1.0, abs_lap, -1.0, 0)  # primjeri kombinacija
```

---

# Kratki sažetak / takeaway

* **Laplacian** mjeri *drugu derivaciju* intenziteta — dobro detektira mjesta gdje intenzitet brzo mijenja smjer (vrhovi/udubine), dakle rubove.
* Diskretni Laplacian kernel najčešće je ([[0,1,0],[1,-4,1],[0,1,0]]) ili 8-susjedna varijanta s -8 u centru.
* Rezultati mogu biti negativni ili pozitivni; često se koristi apsolutna vrijednost, zero-crossing ili threshold za ekstrakciju rubova.
* Za *sharpening* koristimo kombinaciju originala i (negativnog) laplaciana.

