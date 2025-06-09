import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp
from scipy.signal import find_peaks


from models import models


st.set_page_config(page_title="Lotka-Volterra Simulator", layout="wide")
st.title("Lotka-Volterra model 🐇🦊")



model_choice = st.sidebar.selectbox("Choose a model:", models.keys())

# Shared sliders (used in all models)
st.sidebar.markdown("**Common parameters**")
r = st.sidebar.slider("r - Prey's (r)eproduction rate", 0.1, 1.0, 0.6, step=0.01)
a = st.sidebar.slider("a - Predation rate", 0.01, 1.0, 0.4, step=0.01)
b = st.sidebar.slider("b - Predation-reproducing rate", 0.01, 1.0, 0.1, step=0.01)
m = st.sidebar.slider("m - Predator (m)ortality", 0.1, 1.0, 0.4, step=0.01)

# Model-specific sliders
model_params = {'r': r, 'a': a, 'b': b, 'm': m}

if model_choice == "Limited environment":
    st.sidebar.header("Additional parameters")
    k = st.sidebar.slider("k - Environment capacity", 1, 500, 100, 1)
    model_params["k"] = k

elif model_choice == "Prey shelters":
    st.sidebar.header("Additional parameters")
    s = st.sidebar.slider("s - Number of shelters", 0, 25, 3, step=1)
    model_params["s"] = s

st.sidebar.markdown("**Initial populations**")
V0 = st.sidebar.slider("Initial Prey (V₀)", 1, 50, 10, step=1)
P0 = st.sidebar.slider("Initial Predator (P₀)", 1, 50, 5, step=1)

with st.sidebar.expander("Simulation settings"):
    T = st.slider("Simulation Duration (T)", 10, 1000, 50, step=1)
    resolution = st.slider("Time resolution (points per unit)", 1, 100, 5, step=1)
    solver_choice = st.selectbox('Choose a solver:', ['DOP853', 'RK45', 'RK23'])

model = models[model_choice](**model_params)


def solve_ode(model, time_limit, solver, resolution=10):
    t_span = (0, time_limit)
    t_eval = np.linspace(t_span[0], t_span[1], time_limit * resolution)
    sol = solve_ivp(fun=model, t_span=t_span, y0=[V0, P0], method=solver, t_eval=t_eval)
    t, prey, predator = sol.t, sol.y[0], sol.y[1]
    return t, prey, predator



def plot_series_and_phase(t, V, P, stability_points=None):
    """
    Parameters
    ----------
    t : 1-d array-like
        Time vector.
    V : 1-d array-like
        Prey population over time.
    P : 1-d array-like
        Predator population over time.
    stability_points : iterable of (float, float, str), optional
        Each tuple is (V, P, label).  Example:
            stability_points=[(12.5, 7.9, "co-existence")]
    """
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # ── time-series panel ──────────────────────────────────────────────
    ax1.plot(t, V, label="Prey")
    ax1.plot(t, P, label="Predator")
    ax1.set_title("Population vs Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population")
    ax1.legend()

    # ── phase-space panel ─────────────────────────────────────────────
    ax2.plot(V, P, label="Trajectory")

    # add stability points, if any
    if stability_points is not None:
        for v, p, lbl in stability_points:
            # dashed guides in phase space
            ax2.axvline(v, linestyle="--", color="gray", alpha=0.7)
            ax2.axhline(p, linestyle="--", color="gray", alpha=0.7)

            # equilibrium point
            ax2.scatter(v, p, color="red", zorder=5)
            ax2.text(v, p, f"  {v:.3f}, {p:.3f}", color="red",
                     va="bottom", ha="left")

    ax2.set_title("Phase Space (Prey vs Predator)")
    ax2.set_xlabel("Prey Population")
    ax2.set_ylabel("Predator Population")
    ax2.legend()

    st.pyplot(fig)


def estimate_period(t, signal):
    peaks, _ = find_peaks(signal)
    if len(peaks) > 1:
        peak_times = t[peaks]
        periods = np.diff(peak_times)
        average_period = np.mean(periods)
        return average_period
    return None


def average_populations(t, signal):
    peaks, _ = find_peaks(V)  # Use prey peaks to define cycles
    if len(peaks) < 2:
        return None

    cycle_avgs = []
    for i in range(len(peaks) - 1):
        t_start = t[peaks[i]]
        t_end = t[peaks[i + 1]]
        mask = (t >= t_start) & (t <= t_end)
        cycle_avgs.append(np.mean(signal[mask]))

    return [float(a) for a in cycle_avgs]


def max_population(t, signal):
    """
    Calculates the average of maximum population values within each prey-defined cycle.

    Parameters:
        t : 1D array-like
            Time array.
        signal : 1D array-like
            Population signal (V or P).

    Returns:
        avg_max_value : float or None
            Average maximum population across all full cycles, or None if not enough peaks.
    """
    peaks, _ = find_peaks(V)  # Use prey peaks to define cycle boundaries
    if len(peaks) < 2:
        return None

    max_values = []
    for i in range(len(peaks) - 1):
        t_start = t[peaks[i]]
        t_end = t[peaks[i + 1]]
        mask = (t >= t_start) & (t <= t_end)
        max_values.append(np.max(signal[mask]))

    return [float(a) for a in max_values]



if __name__ == '__main__':
    t, V, P = solve_ode(model=model, solver=solver_choice, time_limit=T, resolution=resolution)

    plot_series_and_phase(t, V, P, model.stability_points())
    period = estimate_period(t, V)
    avg_V = average_populations(t, V)
    avg_P = average_populations(t, P)
    max_V = max_population(t, V)
    max_P = max_population(t, P)

    if period is not None:
        st.markdown(f"**Periodicity: {period:.2f} time units**")
    if avg_V:
        st.markdown(f"**🐇 Prey average populations across cycles (peak to peak): {avg_V}**")
    if avg_P:
        st.markdown(f"**🦊 Predator average populations across cycles (peak to peak): {avg_P}**")
    if max_V:
        st.markdown(f"**🐇 Prey maximum populations across cycles (peak to peak): {max_V}**")
    if max_P:
        st.markdown(f"**🦊 Predator maximum populations across cycles (peak to peak): {max_P}**")