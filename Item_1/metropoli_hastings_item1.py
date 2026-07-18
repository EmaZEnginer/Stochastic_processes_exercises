import numpy as np
import matplotlib.pyplot as plt

#funcion de densidad (es decir, mi pi(x)) entre el rango estipulado
def f(x):
    if 0<x<5:
        return np.exp(-(x - 1.5)**2 / 2) + np.exp(-(x - 4)**2 / 4)
    else:
        return 0

#definimos unos parametros iniciales
N=1000000
X=np.zeros(N)   #cadena de markov de los N pasos (ojo, no es matriz de transcion)
X[0]=2.5        #valor inicial o semilla
sigma=1         #desviacion de mi kernel propuesto

#algoritmo metropoli-hastings
for i in range(1,N):
  x_propuesta=np.random.normal(X[i-1],sigma)  #mi x' propuesta usando mi kernel g
  
  #calculo de funcion de aceptacion
  a=min(1,f(x_propuesta)/f(X[i-1]))           #es f(x)/f(x') porque es simetrico,

  #decision: se acepta o rechaza en un "u" aleatorio en base a la funcion de aceptacion
  if np.random.rand() < a:
    X[i]=x_propuesta
  else:
    X[i]=X[i-1]

#burn in: eliminacion delas 1000 primeras muestras
burn_in=10000
muestra_final=X[burn_in:]

#graficamos histograma
plt.hist(muestra_final, bins=500, density=True, alpha=0.6, color='steelblue')
plt.title("Histograma de muestras Metropolis-Hastings")
plt.xlabel("x")
plt.ylabel("Densidad estimada")
plt.show()

#finalmente calculamos media y varianza con nuestros valores esperados
media=np.mean(muestra_final)
varianza=np.var(muestra_final)

def med(x):
  return x

def var(x):
  return x**2

suma_media=0
suma_varianza=0

for i in muestra_final:
  suma_media=suma_media+med(i)

for i in muestra_final:
  suma_varianza=suma_varianza+var(i)

media1=(1/len(muestra_final))*suma_media
varianza1=((1/len(muestra_final))*suma_varianza) - media1**2

print(f"Media aproximada: {media:.4f}")
print(f"Varianza aproximada: {varianza:.4f}")
print(f"Media aproximada1: {media1:.4f}")
print(f"Varianza aproximada1: {varianza1:.4f}")
