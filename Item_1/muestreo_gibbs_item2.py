import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gamma, poisson

iter = 10000 # num de iteraciones
des = 1000 # num de iteraciones a descartar

#listas para guardar las muestras
x = np.zeros(iter)
n = np.zeros(iter, dtype=int)

#inicializamos n
n[0] = 1

#muestreo de Gibbs
for t in range(1,iter):
   #X | N ~ Gamma(n+1, 3)
   x[t] = gamma.rvs(a=n[t-1] + 1, scale=1/3)

    #N | X ~ Poisson(x)
    n[t] = poisson.rvs(mu=x[t])

# descartar las primeras iteraciones
x_muestras = x[des:]
n_muestras = n[des:]

print(x_muestras)
print(n_muestras)

#estimaciones
#(i) P(X^2 < N)

prob_est = np.mean(x_muestras**2 < n_muestras)

#(ii) E(XN)
E_est = np.mean(x_muestras * n_muestras)

print(f"Estimación P(X^2 < N): {prob_est:.4f}")
print(f"Estimación E(XN): {E_est:.4f}")

plt.figure(figsize=(6,5))
plt.scatter(x_muestras, n_muestras, s=5, alpha=0.4)
plt.title("Diagrama de dispersión entre X y N (Gibbs Sampling)")
plt.xlabel("X")
plt.ylabel("N")
plt.grid(True, linestyle='--', alpha=0.6)
plt.show()
