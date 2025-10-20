import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

np.random.seed(42)

# --- osnovni parametri ---
N = 80
T = 800
dt = 1.0
steps = int(T / dt)

tau_m = 20.0
V_rest = -65.0
V_reset = -65.0
V_th = -52.0
R = 1.0
refractory_period = 4

# --- sinaptičke veze ---
p_conn = 0.25
W_scale = 8.0
W = (np.random.rand(N, N) < p_conn).astype(float) * np.random.normal(1.0, 0.5, (N, N))
W *= W_scale
np.fill_diagonal(W, 0)

# --- vanjski input ---
rate_ext = 120.0
p_ext = rate_ext * dt / 1000.0
I_ext_amp = 40.0

# --- stanje ---
V = np.ones(N) * V_rest
last_spike_time = np.ones(N) * (-1e9)
spike_record = []

delay_steps = 2
spike_buffer = [np.zeros(N) for _ in range(delay_steps)]

V[:5] = V_th + 10

for tstep in range(steps):
    t = tstep * dt
    ext_spikes = (np.random.rand(N) < p_ext).astype(float)
    I_ext = I_ext_amp * (ext_spikes + 0.2 * np.sin(t / 30))
    delayed_spikes = spike_buffer[tstep % delay_steps]
    syn_input = W.T.dot(delayed_spikes)
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
        spike_buffer[tstep % delay_steps] = np.zeros(N)
        spike_buffer[tstep % delay_steps][spiked] = 1.0
    else:
        spike_buffer[tstep % delay_steps] = np.zeros(N)

# --- pozicije neurona ---
theta = np.linspace(0, 2 * np.pi, N, endpoint=False)
x = np.cos(theta) + 0.1 * np.random.randn(N)
y = np.sin(theta) + 0.1 * np.random.randn(N)

# --- priprema figure ---
fig, ax = plt.subplots(figsize=(8, 8))
ax.axis('off')
ax.set_title(
    "🧠 BrainChip Neural Storm — neuronska mreža sa sinapsama\n"
    "(točke = neuroni, linije = sinapse, boje = spike događaji)",
    fontsize=11, fontweight='bold'
)

# --- prikaz sinapsi ---
lines = []
for i in range(N):
    for j in range(N):
        if W[i, j] != 0:
            line, = ax.plot([x[i], x[j]], [y[i], y[j]], color='gray', alpha=0.05, lw=0.5, zorder=1)
            lines.append((i, j, line))

# --- scatter za neurone ---
scat = ax.scatter(x, y, s=80, c='royalblue', edgecolors='black', linewidths=0.5, zorder=2)

spike_dict = {}
for n, t in spike_record:
    spike_dict.setdefault(int(t), []).append(int(n))

def update(frame):
    colors = np.array(['royalblue'] * N, dtype=object)
    sizes = np.full(N, 80)

    # neuroni koji pucaju
    active_neurons = spike_dict.get(frame, [])
    if active_neurons:
        for idx in active_neurons:
            colors[idx] = np.random.choice(['gold', 'lime', 'deeppink', 'cyan'])
            sizes[idx] = 250

        # aktiviraj sinapse za spikeane neurone
        for i, j, line in lines:
            if i in active_neurons:
                line.set_alpha(0.6)
                line.set_color('orange')
            else:
                # sinapse polako "blijede"
                alpha = max(0.05, line.get_alpha() * 0.85)
                line.set_alpha(alpha)
                line.set_color('gray')
    else:
        # sinapse blijede kroz vrijeme
        for _, _, line in lines:
            alpha = max(0.05, line.get_alpha() * 0.9)
            line.set_alpha(alpha)
            line.set_color('gray')

    pulse = 1 + 0.2 * np.sin(frame / 10)
    scat.set_sizes(sizes * pulse)
    scat.set_color(colors)
    ax.set_title(
        f"🧠 BrainChip Neural Storm — t = {frame} ms\n"
        "(neuroni i njihove sinapse dinamički pale impulse kao u neuromorfnom čipu)",
        fontsize=11
    )
    return scat,

ani = animation.FuncAnimation(fig, update, frames=range(0, steps, 2), interval=40, blit=True)
plt.show()
