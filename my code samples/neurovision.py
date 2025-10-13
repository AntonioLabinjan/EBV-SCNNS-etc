'''
---

### **1. Retina (gore lijevo)**

* Predstavlja **ulazni sloj vizualnog sustava**, baš kao mrežnica oka.
* Zadužena je za detekciju **svjetline, kontrasta i osnovnih kontura**.
* U kodu to postiže **Gaussian blur + histogram equalization**, čime se simulira adaptacija na svjetlo.
* Retina ne “razumije” što vidi, samo priprema signal za daljnju obradu — čisti i normalizira informacije.

---

### **2. LGN (Lateral Geniculate Nucleus) – gore sredina**

* Ovdje dolazi do **prostorno-frekvencijskog filtriranja** — pojačavanja rubova i prijelaza.
* LGN prenosi informacije iz retine prema vizualnom korteksu i “naglašava” promjene u slici.
* Koristi se **Laplacian filter** koji ističe visoke frekvencije (nagla promjena svjetline).
* U biološkom smislu, LGN je “pojačivač kontrasta” koji priprema podatke za neuronske detektore rubova.

---

### **3. V1 (Orientation Map) – gore desno**

* Simulira **neurone orijentacijske selektivnosti** u primarnom vizualnom korteksu (V1).
* Svaki neuron u V1 “specijaliziran” je za određeni smjer ruba (horizontalni, dijagonalni, vertikalni...).
* Boje na mapi predstavljaju **različite orijentacije rubova** koje mozak detektira u slici.
* Ovo je prvi sloj u mozgu koji “razumije geometriju” slike — gdje su linije, oblici i smjerovi.

---

### **4. V1 (Magnitude Map) – dolje lijevo**

* Prikazuje **snagu** (magnitudu) odgovora iz V1 — koliko je neki rub jak.
* Što je područje svjetlije, to je veći kontrast i jači vizualni signal.
* To je kao “neuronalna aktivnost” – mjesta gdje je mozak najviše “uzbuđen” zbog vizualne promjene.
* U kombinaciji s orijentacijskom mapom, ovo daje potpunu sliku što mozak vidi i koliko jako reagira.

---

### **5. V2/V4 (Saliency Map) – dolje sredina**

* Ovaj sloj detektira **pokret i pažnju** — što se u sceni mijenja i na što bi mozak “gledao”.
* Računa se pomoću **razlike između trenutnog i prethodnog framea**.
* Pokretni dijelovi scene postaju jarko obojeni (crveno, žuto), dok statični dijelovi blijede.
* Ova mapa simulira **mehanizam pažnje** – fokus mozga na dinamične i bitne dijelove okoline.

---

### **6. Input (dolje desno)**

* To je **izvorni video signal** s tvoje kamere — ono što “oko vidi”.
* Služi kao usporedba između sirovog vizualnog inputa i procesiranih slojeva.
* Pokazuje koliko mozak zapravo “transformira” ulazni signal u korisne informacije.
* Na temelju njega možeš vizualno uočiti kako svaka faza obrade dodaje svoj “nivo razumijevanja”.

'''

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
if not cap.isOpened():
    raise SystemExit("Camera not accessible")

def normalize(img):
    img = cv2.normalize(img, None, 0, 255, cv2.NORM_MINMAX)
    return np.uint8(img)

scale = 0.5  # faktor za smanjenje svih prikaza

while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.resize(frame, None, fx=scale, fy=scale)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # -------- LAYER 1: RETINA (brightness & contrast)
    retina = cv2.GaussianBlur(gray, (5, 5), 0)
    retina = cv2.equalizeHist(retina)

    # -------- LAYER 2: LGN (spatial frequency & edge enhancement)
    high_freq = cv2.Laplacian(retina, cv2.CV_64F)
    high_freq = normalize(np.abs(high_freq))

    # -------- LAYER 3: V1 (orientation selective neurons)
    sobelx = cv2.Sobel(retina, cv2.CV_64F, 1, 0, ksize=3)
    sobely = cv2.Sobel(retina, cv2.CV_64F, 0, 1, ksize=3)
    magnitude = np.sqrt(sobelx**2 + sobely**2)
    angle = np.arctan2(sobely, sobelx)
    magnitude = normalize(magnitude)
    orientation = cv2.applyColorMap(normalize((angle + np.pi) * 255 / (2 * np.pi)), cv2.COLORMAP_HSV)

    # -------- LAYER 4: V2/V4 (motion saliency)
    if 'prev_gray' in locals():
        diff = cv2.absdiff(retina, prev_gray)
        motion = cv2.threshold(diff, 30, 255, cv2.THRESH_BINARY)[1]
        motion = cv2.medianBlur(motion, 5)
        saliency = cv2.applyColorMap(motion, cv2.COLORMAP_JET)
    else:
        saliency = np.zeros_like(frame)

    prev_gray = retina.copy()

    # -------- Visualization
    retina_col = cv2.cvtColor(retina, cv2.COLOR_GRAY2BGR)
    high_col = cv2.applyColorMap(high_freq, cv2.COLORMAP_MAGMA)
    mag_col = cv2.applyColorMap(magnitude, cv2.COLORMAP_TURBO)

    # Stack panels (2x3 grid)
    top_row = np.hstack((retina_col, high_col, orientation))
    bottom_row = np.hstack((mag_col, saliency, frame))
    combined = np.vstack((top_row, bottom_row))

    cv2.putText(combined, 
                'RETINA | LGN | V1 (orientation) | V1 (magnitude) | V2/V4 (saliency) | Input',
                (10, 25), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 1)
    
    cv2.imshow("Compact Brain Visual Processing Simulator", combined)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
