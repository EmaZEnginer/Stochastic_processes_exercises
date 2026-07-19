import numpy as np
import pymc as pm
import pytensor.tensor as pt
import matplotlib.pyplot as plt

# -------------------------------------------------------------------
# 1.CONFIGURACIoN INICIAL
# -------------------------------------------------------------------

#semilla con cedula
np.random.seed(8090) 

#datos sinteticos del ej
X = np.linspace(0, 1, 50)[:, None]  #variable explicativa (50 puntos)
true_f = np.sin(12 * X) + 0.66 * np.cos(25 * X) # funcion real usada por PyMC
Y = true_f + 0.1 * np.random.randn(50, 1) # datos con ruido gaussiano

# -------------------------------------------------------------------
# 2.DEFINICIoN DEL MODELO BAYESIANO CON PROCESO GAUSSIANO
# -------------------------------------------------------------------

with pm.Model() as modelo:

    # Hiperparametos del GP
    ℓ = pm.HalfNormal("ℓ", sigma=1.0) # Longitud de escala
    η = pm.HalfNormal("η", sigma=1.0) # Amplitud

    # KERNEL EXPONENCIAL
    cov = η**2 * pm.gp.cov.Exponential(input_dim=1, ls=ℓ)
    
    # Definir el Proceso Gaussiano (Linea reincorporada)
    gp = pm.gp.Marginal(cov_func=cov)

    # Ruido blanco (sigma del ruido)
    sigma = pm.HalfNormal("sigma", sigma=0.1)

    # Likelihood
    y_obs = gp.marginal_likelihood("y_obs", X=X, y=Y.flatten(), sigma=sigma)

    # Ajuste (inferencia)
    # OPTIMIZACIÓN: Reemplazamos pm.sample por pm.find_MAP
    print("Buscando el mejor ajuste (MAP)...")
    # Usamos L-BFGS-B para un mejor rendimiento sin g++
    mp = pm.find_MAP(method='L-BFGS-B') 


# -------------------------------------------------------------------
# 3. PREDICCIoN DEL GP (POSTERIOR PREDICTIVO)
# -------------------------------------------------------------------

# Malla fina para la prediccion
X_nuevo = np.linspace(0, 1, 200)[:, None]

with modelo:
    # Usamos los parámetros encontrados en el MAP (mp) para la predicción
    media_post, cov_post = gp.predict(X_nuevo, point=mp, diag=False, pred_noise=False)

# Desviación estándar para banda de incertidumbre
std_post = np.sqrt(np.diag(cov_post))

# -------------------------------------------------------------------
# 4. GRAFICA 1: DATOS, MEDIA POSTERIOR Y BANDA DE INCERTIDUMBRE
# -------------------------------------------------------------------

plt.figure(figsize=(10, 6))
plt.plot(X, Y, "ok", ms=4, label="Datos observados")
plt.plot(X_nuevo, media_post, "b", lw=2, label="Media posterior")
plt.fill_between(
    X_nuevo.flatten(),
    media_post - 2 * std_post,
    media_post + 2 * std_post,
    color="skyblue",
    alpha=0.4,
    label="95% región probable"
)
plt.title("Gráfica 1: Regresión con Proceso Gaussiano (Kernel Exponencial)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()

# -------------------------------------------------------------------
# 5. GRAFICA 2: CURVAS MUESTRALES DEL GP
# -------------------------------------------------------------------

# Muestreamos funciones posibles del GP
num_muestras = 20
# Usamos la matriz de covarianza posterior (cov_post) y la media (media_post)
# del ajuste MAP para simular caminos (Sample Paths)
muestras = np.random.multivariate_normal(
    mean=media_post, 
    cov=cov_post, 
    size=num_muestras
)


plt.figure(figsize=(10, 6))
for i in range(num_muestras):
    plt.plot(X_nuevo, muestras[i, :], lw=1, alpha=0.6)

plt.plot(X, Y, "ok", ms=4, label="Datos observados") 
plt.title("Gráfica 2: Curvas posibles según el GP (Sample Paths)")
plt.xlabel("x")
plt.ylabel("f(x)")
plt.legend()
plt.grid(True)
plt.show()
