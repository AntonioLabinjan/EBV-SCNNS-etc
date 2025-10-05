import cv2
import numpy as np
import matplotlib.pyplot as plt
from scipy.signal import convolve2d

# === 1. Učitaj sliku (promijeni put do svoje slike!) ===
path = "/content/WIN_20251005_22_37_32_Pro.jpg"
img = cv2.imread(path, cv2.IMREAD_GRAYSCALE)  # grayscale verzija

if img is None:
    raise FileNotFoundError(f"Nisam našao sliku na putu: {path}")

# === 2. Definiraj Laplacian kernel ===
K = np.array([[0, 1, 0],
              [1, -4, 1],
              [0, 1, 0]], dtype=float)

# === 3. Primijeni konvoluciju ===
L_same = convolve2d(img, K, mode='same', boundary='symm')

# === 4. Napravi sharpenanu verziju slike ===
img_sharp = img - L_same
img_sharp = np.clip(img_sharp, 0, 255).astype(np.uint8)

# === 5. Prikaži rezultate ===
fig, axs = plt.subplots(1, 3, figsize=(12, 4))

axs[0].imshow(img, cmap='gray')
axs[0].set_title('Original')
axs[0].axis('off')

axs[1].imshow(L_same, cmap='bwr')
axs[1].set_title('Laplacian (rubovi)')
axs[1].axis('off')

axs[2].imshow(img_sharp, cmap='gray')
axs[2].set_title('Sharpened')
axs[2].axis('off')

plt.tight_layout()
plt.show()
