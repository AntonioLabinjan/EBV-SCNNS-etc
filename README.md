TODO: hitit se na detaljnije proučavanje onih STDP i Brainchip papera; kod pustit ća jeno malo...koncept san skužija, performanse ću ben peglat

Istražit STDP
https://www.sciencedirect.com/science/article/abs/pii/S0893608017302903
- GRADIENT BOOSTING MIGHT HELP IN FUTURE
- Sanity check: ako accuracy raste iz epohe u epohu, ali validation accuracy pada, vrlo vjerojatno se radi o overfittingu.
- Solution: early stopping
- sanity check by Gepetto
✅ ±3–5% oscilacija → normalno, očekivano
⚠️ nagli pad >10% → znak overfittinga ili prevelikog learning ratea
🚀 stabilan rast + male oscilacije → idealno
Zanimljivost -> nekad izgleda kao da performanse imaju checkpointe...raste, raste, raste, dojde do local maximuma, onda pleše oko njega (malo raste, malo pada) i onda nakon malo plesanja ipak nastavi dalje rast

Ovo mi je toliko bitno da ću hitit u readme😂
- https://doc.brainchipinc.com/user_guide/cnn2snn.html
- https://tech-writing-graphics.com/wp-content/uploads/2019/06/Akida-CNN2SNN-toolKit-v.1.1.pdf
- https://brainchip-inc.github.io/akida_examples_2.3.0-doc-1/examples/cnn2snn/plot_1_advanced_cnn2snn.html
Jebe me setupiranje cnn2snn alata...malo detaljnije kopat po temu :D

https://doc.brainchipinc.com/user_guide/user_guide.html
https://doc.brainchipinc.com/user_guide/cnn2snn.html


# CNN2SNN Toolkit - Step by Step Setup Guide

## 📋 Preduvjeti

Prije nego počneš, provjeri da imaš:
- Python 3.8 ili noviji
- pip package manager
- Virtualno okruženje (preporučeno)

---

## 🚀 Korak 1: Priprema okruženja

### 1.1 Kreiraj virtualno okruženje (preporučeno)

```bash
# Kreiraj novo virtualno okruženje
python -m venv akida_env

# Aktiviraj ga
# Na Linuxu/macOS:
source akida_env/bin/activate

# Na Windowsu:
akida_env\Scripts\activate
```

### 1.2 Upgrade pip

```bash
pip install --upgrade pip
```

---

## 📦 Korak 2: Instalacija paketa

### 2.1 Instaliraj osnovne Akida pakete

```bash
# Akida runtime
pip install akida

# Pretrained modeli
pip install akida-models

# CNN2SNN toolkit
pip install cnn2snn
```

### 2.2 Instaliraj QuantizeML (opcionalno, ali preporučeno)

```bash
pip install quantizeml
```

### 2.3 Provjeri instalaciju

```bash
python -c "import cnn2snn; print(cnn2snn.__version__)"
python -c "import akida; print(akida.__version__)"
```

---

## 🎯 Korak 3: Prvi primjer - Python API

### 3.1 Kreiraj test skriptu

Napravi novu datoteku `test_cnn2snn.py`:

```python
from akida_models import ds_cnn_kws_pretrained
from cnn2snn import convert

print("Učitavanje pretrained modela...")
quantized_model = ds_cnn_kws_pretrained()

print("Konverzija u Akida format...")
model_akida = convert(quantized_model)

print("Spremanje modela...")
model_akida.save("my_first_model.fbz")

print("✅ Gotovo! Model spremljen kao 'my_first_model.fbz'")

# Provjeri model
print(f"\nBroj layer-a: {len(model_akida.layers)}")
print(f"Input shape: {model_akida.input_shape}")
```

### 3.2 Pokreni skriptu

```bash
python test_cnn2snn.py
```

---

## 💻 Korak 4: Command-line način

### 4.1 Preuzmi pretrained model

```bash
# Kreiraj direktorij za modele
mkdir models
cd models

# Preuzmi kvantiziran model
wget https://data.brainchip.com/models/AkidaV2/ds_cnn/ds_cnn_kws_i8_w8_a8.h5
```

### 4.2 Konvertiraj model

```bash
# Jednostavna konverzija
cnn2snn convert -m ds_cnn_kws_i8_w8_a8.h5

# Rezultat: ds_cnn_kws_i8_w8_a8.fbz
```

### 4.3 Provjeri konvertirani model

```bash
# Prikaži informacije o modelu
cnn2snn show -m ds_cnn_kws_i8_w8_a8.fbz
```

---

## 🔧 Korak 5: Rad s vlastitim modelima

### 5.1 Provjeri kompatibilnost

```python
from cnn2snn import check_model_compatibility
from tensorflow import keras

# Učitaj svoj Keras model
model = keras.models.load_model('moj_model.h5')

# Provjeri može li se konvertirati
check_model_compatibility(model)
```

### 5.2 Konvertiraj vlastiti model

```python
from cnn2snn import convert

# Konvertiraj
model_akida = convert(model)

# Spremi
model_akida.save("moj_model.fbz")
```

---

## ⚙️ Korak 6: Napredne opcije

### 6.1 Konverzija za Akida 1.0

```python
from cnn2snn import convert, set_akida_version, AkidaVersion

with set_akida_version(AkidaVersion.v1):
    model_akida = convert(quantized_model)
    model_akida.save("model_v1.fbz")
```

Ili putem environment variable:

```bash
CNN2SNN_TARGET_AKIDA_VERSION=v1 cnn2snn convert -m model.h5
```

### 6.2 Custom input scaling

```python
# Za slike normalizirane između -1 i 1
model_akida = convert(
    model_keras, 
    input_scaling=(128, 128)
)
```

### 6.3 Dodatne opcije konverzije

```bash
# Verbose output
cnn2snn convert -m model.h5 -v

# Specificiran output direktorij
cnn2snn convert -m model.h5 -o ./output/

# Custom ime output datoteke
cnn2snn convert -m model.h5 -o custom_name.fbz
```

---

## 🧪 Korak 7: Test konvertiranog modela

### 7.1 Učitaj i testiraj model

```python
from akida import Model
import numpy as np

# Učitaj konvertirani model
model = Model("my_first_model.fbz")

# Kreiraj dummy input (primjer za 32x32 RGB sliku)
dummy_input = np.random.randint(0, 256, (1, 32, 32, 3), dtype=np.uint8)

# Izvrši inference
predictions = model.predict(dummy_input)

print(f"Predictions shape: {predictions.shape}")
print(f"Top prediction: {np.argmax(predictions)}")
```

---

## 🔍 Korak 8: Troubleshooting

### Problem: Model nije kompatibilan

**Rješenje:** Provjeri da je model kvantiziran:

```python
from quantizeml.models import quantize

# Kvantizacija modela
model_quantized = quantize(
    model,
    weight_quantization=4,
    activation_quantization=4,
    input_weight_quantization=8
)
```

### Problem: Import greška

**Rješenje:** Reinstaliraj pakete:

```bash
pip uninstall cnn2snn akida akida-models -y
pip install cnn2snn akida akida-models
```

### Problem: Verzija konflikti

**Rješenje:** Provjeri kompatibilne verzije:

```bash
pip list | grep -E "cnn2snn|akida|quantizeml"
```

---

## 📚 Kompletan workflow primjer

```bash
# 1. Setup
python -m venv akida_env
source akida_env/bin/activate
pip install akida akida-models cnn2snn quantizeml

# 2. Kreiraj model (ili koristi pretrained)
python -c "from akida_models import ds_cnn_kws_pretrained; m = ds_cnn_kws_pretrained(); m.save('model.h5')"

# 3. Konvertiraj u Akida format
cnn2snn convert -m model.h5 -v

# 4. Provjeri rezultat
python -c "from akida import Model; m = Model('model.fbz'); print(m.summary())"
```

---

## ✅ Gotovo!

Sada imaš potpuno postavljen CNN2SNN toolkit. Sljedeći koraci:

1. Eksperimentiraj s različitim pretrained modelima iz `akida-models`
2. Konvertiraj vlastite Keras modele
3. Optimiziraj modele za različite Akida verzije
4. Testiraj performanse na Akida hardveru

## 🔗 Korisni resursi

- **Dokumentacija:** https://docs.brainchip.com
- **Primjeri:** https://github.com/Brainchip-Inc/akida-examples
- **Model zoo:** https://docs.brainchip.com/api_reference/akida_models_apis.html
