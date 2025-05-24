import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Lotka-Volterra Simulator", layout="wide")
st.title("Lotka-Volterra model 🐇🦊")



st.sidebar.header("Model Parameters")
r = st.sidebar.slider("r - Prey's (r)eproduction rate", 0.1, 2.0, 1.1, 0.1)
a = st.sidebar.slider("a - Predation Rate", 0.01, 1.0, 0.4, 0.01)
b = st.sidebar.slider("b - Predation-reproducing Rate", 0.01, 1.0, 0.1, 0.01)
m = st.sidebar.slider("m - Predator's (m)ortality", 0.1, 2.0, 0.4, 0.1)

st.sidebar.header("Initial Populations")
V0 = st.sidebar.slider("Initial Prey (V₀)", 1, 50, 10, 1)
P0 = st.sidebar.slider("Initial Predator (V₀)", 1, 50, 5, 1)

st.sidebar.header("Simulation Settings")
T = st.sidebar.slider("Simulation Duration (T)", 10, 200, 50, 10)

def lotka_volterra(_, current_point):
    V, P = current_point
    dVdt = r * V - a * V * P
    dPdt = - m * P + b * V * P 
    return [dVdt, dPdt]


def solve_ode(model, time_limit):
    t_span = (0, time_limit)
    t_eval = np.linspace(t_span[0], t_span[1], 10000)
    sol = solve_ivp(fun=model, t_span=t_span, y0=[V0, P0], t_eval=t_eval)
    t, prey, predator = sol.t, sol.y[0], sol.y[1]
    return t, prey, predator


t, V, P = solve_ode(model=lotka_volterra, time_limit=T)

def plot_series_and_phase(t, V, P):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.plot(t, V, label="Prey")
    ax1.plot(t, P, label="Predator")
    ax1.set_title("Population vs Time")
    ax1.set_xlabel("Time")
    ax1.set_ylabel("Population")
    ax1.legend()

    ax2.plot(V, P)
    ax2.set_title("Phase Space (Prey vs Predator)")
    ax2.set_xlabel("Prey Population")
    ax2.set_ylabel("Predator Population")

    st.pyplot(fig)


plot_series_and_phase(t, V, P)
