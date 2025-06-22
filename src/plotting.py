import streamlit as st
import matplotlib.pyplot as plt



def plot_series_and_phase(t, V, P, stability_points=None):
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # ── time-series panel ──────────────────────────────────────────────
    ax1.plot(t, V, label="Ofiary")
    ax1.plot(t, P, label="Drapieżnicy")
    ax1.set_title("Liczebność populacji w zależności od czasu")
    ax1.set_xlabel("Czas, a.u.")
    ax1.set_ylabel("Liczebność")
    ax1.legend()

    # ── phase-space panel ─────────────────────────────────────────────
    ax2.plot(V, P, label="Trajektoria")

    # add stability points, if any
    if stability_points is not None:
        for v, p, _ in stability_points:
            # dashed guides in phase space
            ax2.axvline(v, linestyle="--", color="gray", alpha=0.7)
            ax2.axhline(p, linestyle="--", color="gray", alpha=0.7)

            # equilibrium point
            ax2.scatter(v, p, color="red", zorder=5)
            ax2.text(v, p, f"  {v:.3f}, {p:.3f}", color="red",
                     va="bottom", ha="left")

    ax2.set_title("Wykres fazowy (ofiary vs drapieżnicy)")
    ax2.set_xlabel("Liczebność ofiar")
    ax2.set_ylabel("Liczebność drapieżników")
    ax2.legend()

    st.pyplot(fig)