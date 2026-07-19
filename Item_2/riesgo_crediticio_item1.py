import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

#semilla para reproducibilidad (para que nos den los mismos números al probar)
np.random.seed(42)

#a)residuo ---

cedula_1=1020398068
cedula_2=1034988474
cedula_3=1001418090
cedula_4=1000871745

suma_cedulas=cedula_1+cedula_2+cedula_3+cedula_4
residuo = suma_cedulas % 3
print(f"La suma es: {suma_cedulas}")
print(f"El residuo al dividir por 3 es: {residuo}")

#b)definicion de Matriz P

filas_cols = ["AAA", "AA", "A", "BBB", "BB", "B", "CCC", "D", "NR"]

# Datos copiados del R (en fila continua)
datos_matriz = [
    68.252, 13.577, 6.576, 0.939, 0.611, 0.103, 0.008, 0.253, 9.682,
    0.683, 64.800, 15.044, 3.513, 0.645, 0.198, 0.015, 0.520, 14.581,
    0.048, 1.183, 65.677, 10.093, 2.771, 0.709, 0.041, 1.718, 17.759,
    0.011, 0.558, 4.429, 66.024, 9.331, 1.977, 0.125, 2.232, 15.312,
    0.009, 0.181, 0.816, 4.638, 61.760, 8.825, 0.530, 4.046, 19.192,
    0.009, 0.030, 0.232, 0.963, 3.689, 59.774, 3.561, 10.091, 21.652,
    0.004, 0.011, 0.080, 1.008, 1.724, 4.764, 24.978, 56.869, 11.316,
    0, 0, 0, 0, 0, 0, 0, 100, 0,
    0.058, 0.022, 0.298, 0.637, 0.851, 0.918, 0.097, 3.040, 94.078
]

# Convertimos la lista en una matriz de 9x9 y dividimos por 100
matriz_P=np.array(datos_matriz).reshape(9, 9)/100

#usamos Pandas para visualizarla bonita con sus etiquetas (opcional pero recomendado)
df_P=pd.DataFrame(matriz_P, index=filas_cols, columns=filas_cols)
print("Matriz de Transición P (t=1):")
print(df_P)

# --- Parte c) Aproximacion de Q ---

#matriz identidad
I=np.eye(9)

#definimos X = P - I
X=matriz_P-I

#potencias de matrices (usamos el operador @ para multiplicación matricial)
#OJO: X**2 en python elevaria cada numero al cuadrado, X @ X multiplica las matrices.
X2=X @ X
X3=X2 @ X

#aproximación de Taylor (3 primeros terminos)
matriz_Q_aprox = X - (0.5 * X2) + ((1/3) * X3)

#ajuste del generador ---
#en una matriz Q, la suma de cada fila debe ser 0.
#las tasas de salida (diagonal) deben ser negativas y equilibrar a las de entrada.

#1.ponemos la diagonal en 0 temporalmente para sumar solo los elementos de fuera
np.fill_diagonal(matriz_Q_aprox, 0)

#2.calculamos la suma de cada fila (off-diagonal sum)
row_sums=matriz_Q_aprox.sum(axis=1)

#3.asignamos a la diagonal el negativo de esa suma
np.fill_diagonal(matriz_Q_aprox, -row_sums)

#visualizamos Q
df_Q=pd.DataFrame(matriz_Q_aprox, index=filas_cols, columns=filas_cols)
print("\nMatriz Generadora Q Aproximada:")
print(df_Q.round(4)) #redondeamos a 4 decimales

#d)simulacion ---

def simular_trayectoria(Q, estado_inicial_idx, estado_absorbente_idx):
    estado_actual=estado_inicial_idx
    tiempo_total=0
    
    #bucle para llegar hasya el absorbente
    while estado_actual != estado_absorbente_idx:
        #tasa de salida (lambda) es el valor absoluto de la diagonal: -q_ii
        tasa_salida=-Q[estado_actual, estado_actual]
        
        #seguridad: si la tasa es 0, es un estado absorbente y paramos
        if tasa_salida < 1e-8:
            break
            
        #generar tiempo de permanencia (distribución exponencial)
        #en numpy, scale = 1/lambda
        tiempo_paso=np.random.exponential(scale=1/tasa_salida)
        tiempo_total+=tiempo_paso     #aqui se acumula el tiempo
        
        #determinar siguiente estado (Cadena de saltos)
        #Probabilidades=q_ij/tasa_salida (para j != i)
        probs=Q[estado_actual, :].copy()
        
        #no podemos saltar al mismo estado en la cadena discreta inmersa
        probs[estado_actual]=0 
        
        #limpieza: la aproximacion de Taylor puede dejar numeros negativos muy pequeños (-1e-15)
        #los forzamos a 0 para no romper la función de probabilidad
        probs=np.maximum(probs, 0)
        
        #normalizamos para que sumen 1 exacto
        suma_probs = probs.sum()
        if suma_probs > 0:
            probs=probs/suma_probs
            #elegimos el siguiente estado basado en las probabilidades (con la funcion random.choice)
            estado_actual=np.random.choice(range(9), p=probs)
        else:
            break #no hay salida posible
            
    return tiempo_total

#parametros de la simulacion (para nuestra funcion)--- 
n_simulaciones=5000
idx_AA=filas_cols.index("AA") #buscamos el indice numerico de "AA"
idx_D=filas_cols.index("D")   #buscamos el índice numerico de "D"

#ejecutamos las simulaciones 5000 veces (lista por comprension")
tiempos_simulados=[simular_trayectoria(matriz_Q_aprox, idx_AA, idx_D) for _ in range(n_simulaciones)]

#calculamos el promedio
tiempo_medio=np.mean(tiempos_simulados)

print(f"\nTiempo medio estimado de absorción (AA -> D): {tiempo_medio:.4f} años")

plt.figure(figsize=(8, 5))
plt.hist(tiempos_simulados, bins=200, color='skyblue', edgecolor='white', alpha=0.9)
plt.axvline(tiempo_medio, color='red', linestyle='--', linewidth=1.5, label=f'Media: {tiempo_medio:.2f}')
plt.title('Distribución del Tiempo de Absorción (AA -> D)')
plt.xlabel('Tiempo (Años)')
plt.ylabel('Frecuencia')
plt.legend()
plt.grid(axis='y', alpha=0.5)
plt.show()

