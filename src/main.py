import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.integrate import solve_ivp

st.set_page_config(page_title="Lotka-Volterra Simulator", layout="wide")
st.title("🐇🦊 Lotka-Volterra Predator-Prey Model")

# Sidebar - Parameters
st.sidebar.header("Model Parameters")
alpha = st.sidebar.slider("α (Prey Growth Rate)", 0.1, 2.0, 1.1, 0.1)
beta = st.sidebar.slider("β (Predation Rate)", 0.01, 1.0, 0.4, 0.01)
delta = st.sidebar.slider("δ (Predator Reproduction Rate)", 0.01, 1.0, 0.1, 0.01)
gamma = st.sidebar.slider("γ (Predator Death Rate)", 0.1, 2.0, 0.4, 0.1)

st.sidebar.header("Initial Populations")
x0 = st.sidebar.slider("Initial Prey (x₀)", 1, 50, 10, 1)
y0 = st.sidebar.slider("Initial Predator (y₀)", 1, 50, 5, 1)

st.sidebar.header("Simulation Settings")
T = st.sidebar.slider("Simulation Duration (T)", 10, 200, 50, 10)

# Define model
def lotka_volterra(t, z):
    x, y = z
    dxdt = alpha * x - beta * x * y
    dydt = delta * x * y - gamma * y
    return [dxdt, dydt]

# Solve ODE
t_span = (0, T)
t_eval = np.linspace(t_span[0], t_span[1], 1000)
sol = solve_ivp(lotka_volterra, t_span, [x0, y0], t_eval=t_eval)

# Plotting
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Population vs Time
ax1.plot(sol.t, sol.y[0], label="Prey")
ax1.plot(sol.t, sol.y[1], label="Predator")
ax1.set_title("Population vs Time")
ax1.set_xlabel("Time")
ax1.set_ylabel("Population")
ax1.legend()

# Phase Space
ax2.plot(sol.y[0], sol.y[1])
ax2.set_title("Phase Space (Prey vs Predator)")
ax2.set_xlabel("Prey Population")
ax2.set_ylabel("Predator Population")

st.pyplot(fig)

