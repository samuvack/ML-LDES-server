from river import drift
import numpy as np
import matplotlib.pyplot as plt
from matplotlib import gridspec
import random

# Generate data for 3 distributions
random_state = np.random.RandomState(seed=42)
dist_a = random_state.normal(0.8, 0.05, 1000)
dist_b = random_state.normal(0.4, 0.02, 1000)
dist_c = random_state.normal(0.6, 0.1, 1000)

# Concatenate data to simulate a data stream with 2 drifts
stream = np.concatenate((dist_a, dist_b, dist_c))

# Auxiliary function to plot the data


def plot_data(dist_a, dist_b, dist_c, drifts=None):
    fig = plt.figure(figsize=(7, 3), tight_layout=True)
    gs = gridspec.GridSpec(1, 2, width_ratios=[3, 1])
    ax1, ax2 = plt.subplot(gs[0]), plt.subplot(gs[1])
    ax1.grid()
    ax1.plot(stream, label='Stream')
    ax2.grid(axis='y')
    ax2.hist(dist_a, label=r'$dist_a$')
    ax2.hist(dist_b, label=r'$dist_b$')
    ax2.hist(dist_c, label=r'$dist_c$')
    if drifts is not None:
        for drift_detected in drifts:
            ax1.axvline(drift_detected, color='red')
    plt.show()


plot_data(dist_a, dist_b, dist_c)


rng = random.Random(12345)
adwin = drift.ADWIN()

 # Simulate a data stream composed by two data distributions
data_stream = rng.choices([0, 1], k=1000) + rng.choices(range(4, 8), k=1000)

 # Update drift detector and verify if change is detected
for i, val in enumerate(data_stream):
        _ = adwin.update(val)
        if adwin.drift_detected:
            print(f"Change detected at index {i}, input value: {val}")

adwin = drift.ADWIN()
drifts = []

for i, val in enumerate(stream):
    adwin.update(val)   # Data is processed one sample at a time
    if adwin.drift_detected:
        # The drift detector indicates after each sample if there is a drift in the data
        print(f'Change detected at index {i}')
        drifts.append(i)

plot_data(dist_a, dist_b, dist_c, drifts)
