import numpy as np
import matplotlib.pyplot as plt

# -----------------------------
# 1. Parametri simulacije
# -----------------------------
T_ms = 200              # trajanje simulacije u milisekundama
dt_ms = 1               # timestep
num_timesteps = int(T_ms/dt_ms)

r_max = 100             # maksimalna firing rate za bijeli piksel (Hz)
v_thr = 1.0             # threshold membrane voltage za IF neuron
v_reset = 0.0           # reset voltage nakon spikea
w_pixel = 0.01           # težina svakog spikea (koliko membrane voltage raste po spikeu)

# -----------------------------
# 2. MNIST "dummy" slika
# -----------------------------
# Za primjer, koristimo random 28x28 sliku vrijednosti [0,1]
H, W = 28, 28
image = np.random.rand(H, W)  # simulira normaliziranu MNIST sliku

# -----------------------------
# 3. Generiranje spike-trainova po pikselu
# -----------------------------
# Poissonov proces diskretiziran: Bernoulli trial za svaki timestep
# p = r * dt
p = image * r_max * (dt_ms / 1000.0)  # shape (28,28)
spike_trains = np.random.rand(num_timesteps, H, W) < p[None, :, :]
spike_trains = spike_trains.astype(np.uint8)  # 0 ili 1

# -----------------------------
# 4. Integrate-and-Fire neuron
# -----------------------------
v_mem = np.zeros(num_timesteps)  # membrane voltage kroz vrijeme
spikes = np.zeros(num_timesteps) # spike output neurona

for t in range(num_timesteps):
    # Ukupni input u ovom timestepu = suma svih aktivnih piksela * weight
    input_current = np.sum(spike_trains[t]) * w_pixel
    
    # Integracija membrane
    if t == 0:
        v_mem[t] = input_current
    else:
        v_mem[t] = v_mem[t-1] + input_current
    
    # Provjera da li neuron puca
    if v_mem[t] >= v_thr:
        spikes[t] = 1        # spike
        v_mem[t] = v_reset   # reset membrane voltage

# -----------------------------
# 5. Vizualizacija rezultata
# -----------------------------
plt.figure(figsize=(12,4))
plt.subplot(2,1,1)
plt.plot(v_mem, label='Membrane voltage')
plt.axhline(v_thr, color='r', linestyle='--', label='Threshold')
plt.ylabel('Voltage')
plt.legend()

plt.subplot(2,1,2)
plt.plot(spikes, drawstyle='steps-post', label='Neuron spikes')
plt.xlabel('Timestep (ms)')
plt.ylabel('Spike')
plt.legend()
plt.show()
