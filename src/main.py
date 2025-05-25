import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

from models import LotkaVoltera, LotkaVolteraLimitedEnviron, LotkaVolteraPreyShelters

st.set_page_config(page_title="Lotka-Volterra Simulator", layout="wide")
st.title("Lotka-Volterra model 🐇🦊")


models = {
    "Base model": LotkaVoltera,
    "Limited environment": LotkaVolteraLimitedEnviron,
    "Prey shelters": LotkaVolteraPreyShelters,
}

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
    k = st.sidebar.slider("k - Environment capacity", 10, 500, 100, 10)
    model_params["k"] = k

elif model_choice == "Prey shelters":
    st.sidebar.header("Additional parameters")
    s = st.sidebar.slider("s - Number of shelters", 0, 25, 3, step=1)
    model_params["s"] = s

st.sidebar.markdown("**Initial populations**")
V0 = st.sidebar.slider("Initial Prey (V₀)", 1, 50, 10, step=1)
P0 = st.sidebar.slider("Initial Predator (P₀)", 1, 50, 5, step=1)

with st.sidebar.expander("Simulation settings"):
    T = st.slider("Simulation Duration (T)", 10, 200, 50, step=1)
    resolution = st.slider("Time resolution (points per unit)", 1, 100, 5, step=1)
    solver_choice = st.selectbox('Choose a solver:', ['DOP853', 'RK45', 'RK23'])

model = models[model_choice](**model_params)


def solve_ode(model, time_limit, solver, resolution=10):
    t_span = (0, time_limit)
    t_eval = np.linspace(t_span[0], t_span[1], time_limit * resolution)
    sol = solve_ivp(fun=model, t_span=t_span, y0=[V0, P0], method=solver, t_eval=t_eval)
    t, prey, predator = sol.t, sol.y[0], sol.y[1]
    return t, prey, predator


t, V, P = solve_ode(model=model, solver=solver_choice, time_limit=T, resolution=resolution)

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
            ax2.text(v, p, f"  {lbl}", color="red",
                     va="bottom", ha="left")

    ax2.set_title("Phase Space (Prey vs Predator)")
    ax2.set_xlabel("Prey Population")
    ax2.set_ylabel("Predator Population")
    ax2.legend()

    st.pyplot(fig)


plot_series_and_phase(t, V, P, model.stability_points())
