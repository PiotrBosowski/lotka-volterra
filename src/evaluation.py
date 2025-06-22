import numpy as np
from scipy.signal import find_peaks


def estimate_period(t, signal):
    """
    Based on 5 consecutive cycles
    """
    peaks, _ = find_peaks(signal)
    if len(peaks) > 6:
        peak_times = t[peaks]
        periods = np.diff(peak_times)
        average_period = np.mean(periods[1:6])
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


def stabilization_cycles(t, V, epsilon=0.01):  # epsilon = relative threshold
    V_max_values = max_population(t, V)

    if V_max_values is None:
        return None

    for i in range(1, len(V_max_values)):
        delta_V = abs(V_max_values[i] - V_max_values[i - 1])

        V_ref = abs(V_max_values[i - 1]) if V_max_values[i - 1] != 0 else 1e-8

        if (delta_V / V_ref < epsilon):
            return i  # Stabilization occurred after `i` full cycles

    return None  # Did not stabilize within available cycles

