import numpy as np
import matplotlib.pyplot as plt

# Time axis
t = np.linspace(0, 7, 500)

# Parameters
P0 = 1          # Initial population
r = 0.8         # Growth rate
K = 10          # Carrying capacity for logistic growth

# Malthusian (Exponential) growth: P(t) = P0 * e^(r*t)
P_malthus = P0 * np.exp(r * t)

# Verhulstian (Logistic) growth: P(t) = K / (1 + ((K - P0) / P0) * e^(-r*t))
P_logistic = K / (1 + ((K - P0) / P0) * np.exp(-r * t))

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(t, P_malthus, label='Wzrost Malthusa (eksponencjalny)', linewidth=2)
plt.plot(t, P_logistic, label='Wzrost Verhulsta (logistyczny)', linewidth=2)
plt.axhline(K, color='gray', linestyle='--', label='Pojemność środowiska', linewidth=1.5)
plt.title('Wzrost Malthusa vs Verhulsta')
plt.xlabel('Czas')
plt.ylabel('Liczebność populacji, r.u.')
plt.legend()
plt.grid(True)
# plt.ylim(0, max(P_malthus.max(), P_logistic.max()) * 1.1)
plt.ylim((0, 40))
plt.show()
