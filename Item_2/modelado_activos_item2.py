import yfinance as yf
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

#estilo para los gráficos
plt.style.use('ggplot')

#A)
#descarga de datos ---

#definir fechas
fecha_fin=datetime.now()
fecha_inicio=fecha_fin-timedelta(days=365)
simbolo="FSLR" #First Solar, Inc.
#descargar datos
print(f"Descargando datos para {simbolo}...")
datos=yf.download(simbolo, start=fecha_inicio, end=fecha_fin, progress=False)

#seleccionamos solo el precio de cierre ajustado
serie_precios=datos['Close']

#grafico
plt.figure(figsize=(10, 5))
plt.plot(serie_precios, color='darkgreen', linewidth=1.5)
plt.title(f"Precio de Cierre Diario - {simbolo} (Último Año)")
plt.xlabel("Fecha")
plt.ylabel("Precio de Cierre (USD)")
plt.grid(True)
plt.show()

#----------------------------------------------------
#b)ajuste del Modelo GBM ---
#----------------------------------------------------

#calculo de retornos logaritmicos: ln(Pt / P_{t-1})
retornos_log=np.log(serie_precios/serie_precios.shift(1)).dropna()

#dias de trading (252 dias habiles aprox en un año)
dias_trading=252

#estimacion de parametros diarios
#convertimos explicitamente a float para solucionar el TypeError/FutureWarning
mu_diario=float(retornos_log.mean())
sigma_diario=float(retornos_log.std())

#anualizacion
mu_anual=mu_diario*dias_trading
sigma_anual=sigma_diario*np.sqrt(dias_trading)

#guardamos los parametros
drift_GBM=float(mu_anual)
volatilidad_GBM=float(sigma_anual)

print("-" * 30)
print("--- Parámetros Estimados ---")
print(f"Retorno Log diario promedio: {mu_diario:.6f}")
print(f"Volatilidad diaria:          {sigma_diario:.6f}")
print("-" * 30)
print(f"Drift Anual (mu):            {drift_GBM:.4f}")
print(f"Volatilidad Anual (sigma):   {volatilidad_GBM:.4f}")
print("-" * 30)

# ----------------------------------------------------
# tiempo de Primera Travesia ---
# ----------------------------------------------------

# configuracion de parametros
G0 = float(serie_precios.iloc[-1])  #ultimo precio real, convertido a float
barrera = G0 * 1.20                 #Meta: 20% más
mu = drift_GBM
sigma = volatilidad_GBM

n_simulaciones=5000        #cantidad de "futuros" a simular
pasos_por_anio=252         #pasos diarios
tiempo_max_anios=5         #si no llega en 5 años, lo descartamos
total_pasos=int(tiempo_max_anios * pasos_por_anio)
dt=1/pasos_por_anio      #delta t

#2.simulacion vectorizada (forumla logaritimica)
#generamos todos los numeros aleatorios de una vez (estos son los ruidos basicamente)
dW=np.random.normal(0, np.sqrt(dt), size=(total_pasos, n_simulaciones))
#inicializamos matriz de precios
trayectorias_log=np.zeros((total_pasos + 1, n_simulaciones))
trayectorias_log[0, :]=np.log(G0)
#aca estan las diferentes realizaciones matriz (nxm) n: cada realizacion, m: ruido de cada dia

#drift por paso (Correccion de Ito estándar para simulacion)
nu_dt=(mu-0.5*sigma**2)*dt
#digusion (ruido)
sigma_dW=sigma*dW

#acumulamos los cambios del precio. La suma es ahora entre un escalar (nu_dt) y una matriz.
cambios = nu_dt + sigma_dW
trayectorias_log[1:, :] = np.log(G0) + np.cumsum(cambios, axis=0)

#convertimos de nuevo a precios normales (deshacemos el log)
trayectorias = np.exp(trayectorias_log)

#3.encontrar el tiempo de primer cruce
#creamos una mascara donde el precio supera la barrera
supera_barrera = trayectorias >= barrera

#buscamos el indice del primer True en cada columna (simulacion)
indices_cruce = np.argmax(supera_barrera, axis=0)

#filtramos: si el índice es 0 (y el precio inicial no era mayor a la barrera), 
#significa que nunca cruzo en el tiempo simulado.
tiempos_exito = []

for i, idx in enumerate(indices_cruce):
    #si idx es 0, verificamos si realmente superó al inicio (raro) o si nunca superó
    if idx > 0 or supera_barrera[0, i]:
        tiempo_anio = idx * dt
        tiempos_exito.append(tiempo_anio)

#convertimos a numpy array para estadistica
tiempos_exito = np.array(tiempos_exito)

#4.resultados
probabilidad_exito = len(tiempos_exito) / n_simulaciones
tiempo_medio_estimado = np.mean(tiempos_exito) if len(tiempos_exito) > 0 else 0

print(f"\n--- Resultados Simulación (Barrera {barrera:.2f} USD) ---")
print(f"Precio Inicial: {G0:.2f} USD")
print(f"Probabilidad de llegar a la meta en {tiempo_max_anios} años: {probabilidad_exito*100:.2f}%")
print(f"Tiempo medio esperado (casos exitosos): {tiempo_medio_estimado:.4f} años")

#5.histograma
plt.figure(figsize=(10, 6))
plt.hist(tiempos_exito, bins=40, color='darkseagreen', edgecolor='white', alpha=0.8)
plt.axvline(tiempo_medio_estimado, color='red', linestyle='--', linewidth=2, label=f'Media: {tiempo_medio_estimado:.2f} años')
plt.title(f"Distribución del Tiempo para ganar 20% (FSLR) - {n_simulaciones} Sim.")
plt.xlabel("Tiempo (Años)")
plt.ylabel("Frecuencia")
plt.legend()
plt.show()
