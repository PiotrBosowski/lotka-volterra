import numpy as np
from scipy.signal import find_peaks


def estimate_period(t, signal):
    peaks, _ = find_peaks(signal)
    if len(peaks) > 1:
        peak_times = t[peaks]
        periods = np.diff(peak_times)
        average_period = np.mean(periods)
        return average_period
    return None


def average_populations(t, signal):
    peaks, _ = find_peaks(signal)
    if len(peaks) < 2:
        return None

    cycle_avgs = []
    for i in range(len(peaks) - 1):
        t_start, t_end = t[peaks[i]], t[peaks[i + 1]]
        mask = (t >= t_start) & (t <= t_end)
        cycle_avgs.append(np.mean(signal[mask]))

    return cycle_avgs


def max_population(t, signal):
    peaks, _ = find_peaks(signal)
    if len(peaks) < 2:
        return None

    max_values = []
    for i in range(len(peaks) - 1):
        t_start, t_end = t[peaks[i]], t[peaks[i + 1]]
        mask = (t >= t_start) & (t <= t_end)
        max_values.append(np.max(signal[mask]))

    return max_values


def stabilization_time(t, V, P, epsilon=0.01):
    peaks, _ = find_peaks(V)
    if len(peaks) < 3:
        return None  # Not enough cycles to compare

    for i in range(1, len(peaks) - 1):
        # Time window: current cycle vs previous
        mask_prev = (t >= t[peaks[i - 1]]) & (t <= t[peaks[i]])
        mask_curr = (t >= t[peaks[i]]) & (t <= t[peaks[i + 1]])

        V_prev, V_curr = V[mask_prev], V[mask_curr]
        P_prev, P_curr = P[mask_prev], P[mask_curr]

        # Resample to common length for comparison
        min_len = min(len(V_prev), len(V_curr))
        V_prev, V_curr = V_prev[:min_len], V_curr[:min_len]
        P_prev, P_curr = P_prev[:min_len], P_curr[:min_len]

        delta_V = np.max(np.abs(V_curr - V_prev))
        delta_P = np.max(np.abs(P_curr - P_prev))

        if delta_V < epsilon and delta_P < epsilon:
            return t[peaks[i]]  # Stabilization starts here

    return None
