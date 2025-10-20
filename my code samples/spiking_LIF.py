import numpy as np
import matplotlib.pyplot as plt

np.random.seed(42)

N = 50
T = 500
dt = 1.0
steps = int(T / dt)

tau_m = 20.0
V_rest = -65.0
V_reset = -65.0
V_th = -50.0
R = 1.0
refractory_period = 5

p_conn = 0.1
W_scale = 1.0
W = (np.random.rand(N, N) < p_conn).astype(float) * np.random.normal(1.0, 0.3, (N, N))
W *= W_scale
np.fill_diagonal(W, 0)

# Povećavamo eksterni spike rate i amplitude
rate_ext = 30.0  # Hz
p_ext = rate_ext * dt / 1000.0
I_ext_amp = 25.0

V = np.ones(N) * V_rest
last_spike_time = np.ones(N) * (-1e9)
spike_record = []
V_trace = np.zeros((N, steps))

# Početni "kick" prvom neuronu
V[0] = V_th + 5  

for tstep in range(steps):
    t = tstep * dt

    ext_spikes = (np.random.rand(N) < p_ext).astype(float)
    I_ext = ext_spikes * I_ext_amp

    syn_input = np.zeros(N)
    if tstep > 0:
        prev_spiked = np.zeros(N)
        for (n_idx, ts) in spike_record:
            if ts == (t - dt):
                prev_spiked[int(n_idx)] = 1.0
        syn_input = W.T.dot(prev_spiked) * 10.0

    dV = ((V_rest - V) + R * (I_ext + syn_input)) * (dt / tau_m)
    is_refractory = (t - last_spike_time) < refractory_period
    V = V + dV
    V[is_refractory] = V_reset

    spiked = np.where(V >= V_th)[0]
    if spiked.size > 0:
        for n in spiked:
            spike_record.append((n, t))
            last_spike_time[n] = t
            V[n] = V_reset

    V_trace[:, tstep] = V

spike_record = np.array(spike_record) if len(spike_record) > 0 else np.empty((0,2))

plt.figure(figsize=(10, 5))
if spike_record.size > 0:
    plt.scatter(spike_record[:,1], spike_record[:,0], s=6)
plt.xlabel('Time (ms)')
plt.ylabel('Neuron index')
plt.title('Spike raster plot (LIF network)')
plt.xlim(0, T)
plt.ylim(-1, N)
plt.show()

for i in range(min(5, N)):
    plt.figure(figsize=(10, 3))
    plt.plot(np.arange(0, T, dt), V_trace[i, :])
    plt.xlabel('Time (ms)')
    plt.ylabel('Membrane potential (mV)')
    plt.title(f'V(t) - neuron {i}')
    plt.ylim(V_rest - 5, V_th + 10)
    plt.xlim(0, T)
    plt.show()

spike_counts = np.zeros(N, dtype=int)
if spike_record.size > 0:
    for n_idx, _ in spike_record:
        spike_counts[int(n_idx)] += 1

print("Spike count per neuron (first 10):", spike_counts[:10].tolist())
print("Total spikes:", spike_counts.sum())
