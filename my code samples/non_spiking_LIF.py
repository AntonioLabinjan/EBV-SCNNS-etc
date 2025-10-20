# Simulacija jednostavnog Leaky Integrate-and-Fire (LIF) spiking neuronskog mrežnog modela
# koja ilustrira ideju kako rade neuromorfni "brainchipovi" — događajni (spiking) prijenos,
# lokalne sinapse i vremenska dinamika.
# Kod je minimalističan, jasno strukturiran i odmah se može pokrenuti.

import numpy as np
import matplotlib.pyplot as plt

# --- parametri simulacije ---
np.random.seed(42)
N = 50                # broj neurona u mreži
T = 500               # ukupno vrijeme (ms)
dt = 1.0              # korak integracije (ms)
steps = int(T / dt)

tau_m = 20.0          # membrane time constant (ms)
V_rest = -65.0        # resting potential (mV)
V_reset = -65.0       # reset potential nakon spikea (mV)
V_th = -50.0          # prag za spike (mV)
R = 1.0               # otpor (arbitrarna jedinica)
refractory_period = 5 # ms

# --- mreža i ulaz ---
p_conn = 0.1                      # gustoća konekcija
W_scale = 0.5                     # skaliranje sinaptičkih težina
W = (np.random.rand(N, N) < p_conn).astype(float) * np.random.normal(0.6, 0.2, (N, N))
W *= W_scale
np.fill_diagonal(W, 0)            # bez samospojeva

# Poisson eksterni ulaz (događajni input — slično neuromorfnom ulazu)
rate_ext = 5.0  # prosječno 5 spikeova/s -> u ms: 5Hz ~ 0.005 per ms
p_ext = rate_ext * dt / 1000.0    # prilagodba na ms
I_ext_amp = 15.0                  # jakost eksternog impulsa (povremeni poticaj)

# --- varijable stanja ---
V = np.ones(N) * V_rest
last_spike_time = np.ones(N) * (-1e9)
spike_record = []  # lista (neuron_index, time)
V_trace = np.zeros((N, steps))

# --- simulacija ---
for tstep in range(steps):
    t = tstep * dt

    # eksterni Poisson spikeovi
    ext_spikes = (np.random.rand(N) < p_ext).astype(float)
    I_ext = ext_spikes * I_ext_amp

    # sinaptičke transmisije (Dale-like instant kicks kad su bili spikeovi u prethodnom kroku)
    # jednostavno modeliramo da spike odmah daje presinaptički impulse u sljedećem koraku
    syn_input = np.zeros(N)
    if tstep > 0:
        # pronadi koje su neurone pucale u prethodnom koraku
        prev_spiked = np.zeros(N)
        for (n_idx, ts) in spike_record:
            if ts == (t - dt):
                prev_spiked[int(n_idx)] = 1.0
        syn_input = W.T.dot(prev_spiked) * 5.0  # skok proporcionalan težinama

    # LIF dinamika (Euler eksplicitni)
    dV = ( (V_rest - V) + R * (I_ext + syn_input) ) * (dt / tau_m)
    # refraktorno: ako neuron je unutar refractory_period od zadnjeg spikea - držimo ga na V_reset
    is_refractory = (t - last_spike_time) < refractory_period

    V = V + dV
    V[is_refractory] = V_reset

    # spike detekcija
    spiked = np.where(V >= V_th)[0]
    if spiked.size > 0:
        for n in spiked:
            spike_record.append((n, t))
            last_spike_time[n] = t
            V[n] = V_reset  # reset nakon spikea

    V_trace[:, tstep] = V

# --- priprema podataka za iscrtavanje ---
spike_record = np.array(spike_record) if len(spike_record) > 0 else np.empty((0,2))
# Raster plot (svaki spike kao točka: vrijeme vs neuron index)
plt.figure(figsize=(10, 5))
if spike_record.size > 0:
    plt.scatter(spike_record[:,1], spike_record[:,0], s=6)
plt.xlabel('Time (ms)')
plt.ylabel('Neuron index')
plt.title('Spike raster plot (LIF network)')
plt.xlim(0, T)
plt.ylim(-1, N)
plt.show()

# Membrane potential trace za prvih 5 neurona (pojedinačni graf - pravilo: 1 plot po chartu)
for i in range(min(5, N)):
    plt.figure(figsize=(10, 3))
    plt.plot(np.arange(0, T, dt), V_trace[i, :])
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    plt.title(f'V(t) - neuron {i}')
    plt.ylim(V_rest - 5, V_th + 10)
    plt.xlim(0, T)
    plt.show()

# Kratki sažetak rezultata kao print (broj spikeova po neuronu)
spike_counts = np.zeros(N, dtype=int)
if spike_record.size > 0:
    for n_idx, _ in spike_record:
        spike_counts[int(n_idx)] += 1
print("Spike count per neuron (first 10):", spike_counts[:10].tolist())
print("Total spikes:", spike_counts.sum())

# Spremi rezultate u datoteku (opcionalno)
import json, os
out = {
    "params": {"N": N, "T": T, "dt": dt, "tau_m": tau_m, "V_th": V_th},
    "spike_counts": spike_counts.tolist(),
    "total_spikes": int(spike_counts.sum())
}
os.makedirs('/mnt/data', exist_ok=True)
with open('/mnt/data/lif_simulation_summary.json', 'w') as f:
    json.dump(out, f)
print("[Saved] /mnt/data/lif_simulation_summary.json")
