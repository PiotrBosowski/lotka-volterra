import streamlit as st
import pandas as pd

from evaluation import average_populations, estimate_period, max_population, stabilization_time
from models import models, solve_ode
from plotting import plot_series_and_phase



st.set_page_config(page_title="Symulator modelu Lotki-Volterry", layout="wide")
st.title("Model Lotki-Volterry 🐇🦊")


model_choice = st.sidebar.selectbox("Model:", models.keys())

# Shared sliders (used in all models)
st.sidebar.markdown("**Parametry modelu**")
r = st.sidebar.slider("Zdolność (r)ozrodcza ofiar", 0.1, 1.0, 0.6, step=0.01)
a = st.sidebar.slider("Współczynnik drapieżnicwa (a)", 0.01, 1.0, 0.4, step=0.01)
b = st.sidebar.slider("Współczynnik rozrodczości drapieżników (b)", 0.01, 1.0, 0.1, step=0.01)
m = st.sidebar.slider("Ś(m)iertelność drapieżników", 0.1, 1.0, 0.4, step=0.01)

# Model-specific sliders
model_params = {'r': r, 'a': a, 'b': b, 'm': m}

if model_choice == "Ograniczona pojemność":
    st.sidebar.header("Parametry modyfikacji")
    k = st.sidebar.slider("Pojemność środowiska (k)", 1, 500, 100, 1)
    model_params["k"] = k

elif model_choice == "Kryjówki":
    st.sidebar.header("Marametry modyfikacji")
    s = st.sidebar.slider("Liczba kryjówek (s)", 0, 25, 3, step=1)
    model_params["s"] = s

st.sidebar.markdown("**Początkowe liczebności**")
V0 = st.sidebar.slider("Liczebność ofiar (V₀)", 1, 50, 10, step=1)
P0 = st.sidebar.slider("Liczebność drapieżników (P₀)", 1, 50, 5, step=1)

with st.sidebar.expander("Ustawienia symulacji"):
    T = st.slider("Czas trwania (T)", 10, 1000, 50, step=1)
    resolution = st.slider("Rozdzielczość (pkt / jedn. czas.)", 1, 100, 5, step=1)
    solver_choice = st.selectbox('Algorytm rozwiązywania ODE', ['DOP853', 'RK45', 'RK23'])

model = models[model_choice](**model_params)


if __name__ == '__main__':
    t, V, P = solve_ode(model=model, initial_state=(V0, P0), solver=solver_choice, time_limit=T, resolution=resolution)

    plot_series_and_phase(t, V, P, model.stability_points())
    period = estimate_period(t, V)
    avg_V = average_populations(t, V)
    avg_P = average_populations(t, P)
    max_V = max_population(t, V)
    max_P = max_population(t, P)
    stab_time = stabilization_time(t, V, P, epsilon=0.1)

    if period is not None:
        st.markdown(f"**Czas odradzania się populacji: {period:.2f}**")

    if avg_V and avg_P and max_V and max_P:
        num_cycles = min(len(avg_V), len(avg_P), len(max_V), len(max_P))
        df_stats = pd.DataFrame({
            "🔁 Cykl": list(range(1, num_cycles + 1)),
            "🐇 Średnia populacja ofiar": avg_V[:num_cycles],
            "🦊 Średnia populacja drapieżników": avg_P[:num_cycles],
            "🐇 Maks. populacja ofiar": max_V[:num_cycles],
            "🦊 Maks. populacja drapieżników": max_P[:num_cycles],
        })

        st.markdown("### Statystyki populacji dla kolejnych cykli")
        st.dataframe(df_stats, use_container_width=True, hide_index=True)

    if stab_time is not None:
        st.markdown(f"**🪢 Stabilizacja układu następuje po: {stab_time:.2f} jednostkach czasu**")
    else:
        st.markdown("**🪢 Układ nie osiągnął stabilizacji w czasie symulacji**")