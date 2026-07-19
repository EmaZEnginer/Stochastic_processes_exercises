## Punto 1:

#### Enunciado: Modelado de Riesgo Crediticio mediante Cadenas de Markov en Tiempo Continuo y Simulación de Absorción

A partir de una matriz de transición de probabilidad discreta anual $P \in \mathbb{R}^{9 \times 9}$, la cual describe el comportamiento de transición de las calificaciones de riesgo crediticio corporativo en un horizonte temporal de $t = 1$ año (desde la categoría óptima AAA hasta el estado de impago o default D y entidades no calificadas NR):

1. Aproximación del Generador Infinitesimal: Implemente la aproximación de la matriz generadora infinitesimal $Q$ mediante la serie de Taylor para el logaritmo matricial, considerando los primeros tres términos del desarrollo matemático ($\ln(P) \approx (P-I) - \frac{1}{2}(P-I)^2 + \frac{1}{3}(P-I)^3$).

2. Ajuste Técnico del Generador: Realice las correcciones numéricas necesarias sobre la diagonal de la matriz aproximada $\hat{Q}$ para garantizar las propiedades teóricas de una matriz de tasas continuas (donde la suma de cada fila debe ser estrictamente cero y los elementos fuera de la diagonal deben ser no negativos).

3. Simulación de Montecarlo (Cadena de Saltos Inmersa): Diseñe e implemente un algoritmo de simulación estocástica para estimar la trayectoria de una empresa que inicia con una calificación crediticia intermedia de alto nivel (AA) hasta alcanzar el estado absorbente de default (D). El algoritmo debe acumular los tiempos de permanencia modelados a través de variables aleatorias exponenciales parametrizadas por las tasas de salida de cada estado.

4. Análisis de Resultados: Ejecute $N = 5.000$ simulaciones utilizando el método de Montecarlo para aproximar el tiempo medio esperado de absorción (en años) y grafique la distribución empírica de los tiempos simulados mediante un histograma de frecuencias.

#### Sustentación:

- Recuperación del Generador Infinitesimal mediante Serie de Taylor:

En una cadena de Markov en tiempo continuo, la relación matemática entre la matriz de transición de probabilidad acumulada $P(t)$ en el instante $t$ y la matriz generadora infinitesimal $Q$ está gobernada por la ecuación diferencial de Kolmogorov, cuya solución formal es la exponencial matricial:

$$P(t) = e^{Qt}$$

Para un periodo anual regularizado ($t = 1$), la matriz observada se define como $P = e^Q$, lo que implica que el generador continuo equivale al logaritmo matricial de la estructura discreta, $Q = \ln(P)$. Utilizando la expansión en serie de Taylor alrededor de la matriz identidad $I$, y definiendo el cambio lineal $X = P - I$, se deduce la aproximación algorítmica:

$$\ln(I + X) = X - \frac{X^2}{2} + \frac{X^3}{3} - \dots$$

$$Q \approx (P - I) - \frac{1}{2}(P - I)^2 + \frac{1}{3}(P - I)^3$$

- Restricciones de Cierre y Corrección del Generador:

Debido al truncamiento de la serie de Taylor y a las fluctuaciones de redondeo numérico, la matriz aproximada requiere una reconfiguración sobre su diagonal principal. Teóricamente, en cualquier matriz generadora $Q$, los elementos fuera de la diagonal representan tasas de transición hacia otros estados y deben cumplir que $q_{ij} \ge 0$ para todo $i \neq j$. Dado que las probabilidades de la fila deben preservarse continuas, la tasa de salida instantánea de un estado $i$ (representada por $-q_{ii}$) debe equilibrar con exactitud la suma de las tasas de entrada a los demás estados de la fila:

$$\sum_{j=1}^{9} q_{ij} = 0 \implies q_{ii} = -\sum_{j \neq i} q_{ij}$$

El algoritmo garantiza esta condición aislando temporalmente los elementos externos, calculando su suma vectorial por filas y reasignando el inverso aditivo directamente sobre la diagonal principal.

- Formalización Dinámica de la Cadena de Saltos Inmersa:

El comportamiento de una cadena continua se descompone en dos procesos estocásticos complementarios: el tiempo que el sistema permanece en un estado y el salto discreto hacia el siguiente destino.

Tiempo de Permanencia: Al encontrarse en un estado actual $i$, el tiempo transcurrido $T_i$ hasta que ocurre una transición sigue una distribución exponencial cuya tasa de intensidad instantánea es $\lambda_i = -q_{ii}$. La variable aleatoria continua se simula mediante: 

$$T_i \sim \text{Exponencial}\left(\text{escala} = \frac{1}{-q_{ii}}\right)$$

Probabilidades de Transición de Salto: Dado que el sistema efectivamente abandona el estado $i$, la selección probabilística del nuevo estado destino $j$ (donde $j \neq i$) está gobernada por la cadena de Markov discreta inmersa, cuyas probabilidades relativas de salto se normalizan bajo la regla:

$$P(\text{Saltar de } i \to j) = \frac{q_{ij}}{-q_{ii}}$$

Este ciclo de simulación se repite iterativamente de manera dinámica, acumulando los tiempos de paso $t_{\text{total}} = \sum T_i$, hasta que la variable de estado intersecta el índice correspondiente al estado absorbente de default ($q_{DD} = 0$), provocando la terminación del bucle y registrando el tiempo total del caso exitoso.

A continuación se muestra la matriz infintesimal y los resulados obtenidos:

![Matriz infinitesimal](..\images\matrix_p1_item2.png)

![Resultados punto 1](..\images\results_p1_item2.png)

## Punto 2:

#### Enunciado: Modelado del Tiempo de Primera Travesía en Activos Financieros mediante el Movimiento Browniano Geométrico

Utilizando series temporales históricas de precios de cierre diarios obtenidas de Yahoo Finance para el activo First Solar, Inc. (FSLR), desarrolle e implemente el marco metodológico del Movimiento Browniano Geométrico (GBM) bajo las siguientes especificaciones:

1. Estimación de Parámetros: Calcule los retornos logarítmicos diarios de la serie y utilícelos para estimar mediante momentos muestrales los parámetros anualizados del modelo: el rendimiento esperado o tendencia (drift, $\mu$) y la volatilidad del activo ($\sigma$), asumiendo un año comercial estandarizado de $252$ días hábiles.

2. Validación Teórica del Modelo: Demuestre analíticamente mediante el Lema de Itô que la ecuación diferencial estocástica (SDE) del precio, definida como $dG_t = \mu G_t dt + \sigma G_t dW_t$, se satisface plenamente a partir de su solución explícita exponencial.

3. Simulación Estocástica Vectorizada: Diseñe un algoritmo en Python que simule de forma vectorizada $N = 5.000$ trayectorias aleatorias del precio del activo para un horizonte máximo de $T = 5$ años, discretizando la dinámica en incrementos diarios ($\Delta t = 1/252$).

4. Análisis de Barrera (First Passage Time): Establezca una barrera financiera equivalente a un incremento del $20\%$ sobre el último precio de cierre real observado ($1.20 \times G_0$). A partir de las trayectorias simuladas, calcule:
 - La probabilidad empírica de alcanzar dicha meta de rentabilidad dentro del periodo de 5 años.
 - El tiempo medio esperado (en años) que tardan los escenarios exitosos en cruzar por primera vez dicha barrera.
 - Represente los tiempos de llegada mediante un histograma de frecuencias con su respectiva media muestral.

#### Sustentación:

- Estimación Paramétrica y Anualización

  Dado que las series de precios no cumplen con el supuesto de estacionariedad, el análisis se traslada al espacio de los retornos logarítmicos diarios $r_t$, los cuales se definen a partir del diferencial logarítmico del precio de cierre de días consecutivos:

  $$r_t = \ln\left(\frac{G_t}{G_{t-1}}\right) = \ln(G_t) - \ln(G_{t-1})$$

  Asumiendo que los retornos diarios siguen una distribución normal independiente e idénticamente distribuida (i.i.d.), de modo que $r_t \sim \mathcal{N}(\mu_{\text{diario}}, \sigma^2_{\text{diario}})$, se calculan la media muestral ($\bar{r}$) y la desviación estándar muestral ($s_r$). Para proyectar estos valores a una escala anual (donde $A = 252$ días de operación), se aplican las propiedades de escala temporal de los procesos de difusión:

  $$\mu = \mu_{\text{anual}} = \bar{r} \times A$$

  $$\sigma = \sigma_{\text{anual}} = s_r \times \sqrt{A}$$

- Demostración de la Dinámica del GBM mediante el Lema de Itô

  La solución analítica de la ecuación diferencial estocástica que modela el precio del activo financiero es una función que depende explícitamente del tiempo $t$ y del proceso de Wiener estándar $X_t = W_t$, definida como:

  $$f(t, W_t) = G_t = G_0 \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t\right)$$

  De acuerdo con el Lema de Itô, el diferencial total estocástico de esta función $df(t,W_t)$ se rige por el desarrollo de Taylor expandido hasta el término de segundo orden para el ruido, debido a que $(dW_t)^2 = dt$:

  $$dG_t = \left( \frac{\partial f}{\partial t} + \frac{1}{2}\sigma^2 \frac{\partial^2 f}{\partial W_t^2} \right) dt + \frac{\partial f}{\partial W_t} dW_t$$

  Calculando las derivadas parciales de la función exponencial de forma independiente se obtiene:

  Derivada temporal parcial:

  $$\frac{\partial f}{\partial t} = \left(\mu - \frac{1}{2}\sigma^2\right) G_0 \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t\right) = \left(\mu - \frac{1}{2}\sigma^2\right)G_t$$

  Primera derivada espacial parcial:

  $$\frac{\partial f}{\partial W_t} = \sigma G_0 \exp\left(\left(\mu - \frac{1}{2}\sigma^2\right)t + \sigma W_t\right) = \sigma G_t$$

  Segunda derivada espacial parcial:

  $$\frac{\partial^2 f}{\partial W_t^2} = \frac{\partial}{\partial W_t}(\sigma G_t) = \sigma^2 G_t$$

  Sustituyendo estas derivadas parciales directamente en la ecuación del Lema de Itô, simplificamos algebraicamente los términos aritméticos dentro del diferencial de tiempo:

  $$dG_t = \left[ \left(\mu - \frac{1}{2}\sigma^2\right)G_t + \frac{1}{2}\sigma^2 (\sigma^2 G_t) \right] dt + (\sigma G_t) dW_t$$

  $$dG_t = \left[ \mu G_t - \frac{1}{2}\sigma^2 G_t + \frac{1}{2}\sigma^2 G_t \right] dt + \sigma G_t dW_t$$

  $$dG_t = \mu G_t dt + \sigma G_t dW_t$$

  Queda firmemente demostrado que la especificación exponencial propuesta satisface la ecuación diferencial del precio exponencial, donde la tasa de retorno instantánea se compone de un rendimiento esperado ponderado por $\mu dt$ más una difusión estocástica dada por $\sigma dW_t$.

- Discretización de Euler-Maruyama y Simulación Vectorizada
 
Para la simulación computacional, aplicamos una transformación logarítmica sobre el precio, $Y_t = \ln(G_t)$, convirtiendo el modelo no lineal en un sistema lineal aditivo. Aplicando el esquema numérico de Euler-Maruyama bajo incrementos discretos de tiempo $\Delta t = dt$, la actualización del estado logarítmico en el paso $k+1$ se formaliza como:

$$\ln(G_{k+1}) = \ln(G_k) + \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z_{k+1}$$

Donde $Z \sim \mathcal{N}(0, 1)$ representa una variable aleatoria normal estándar independiente generada de forma masiva en una matriz de dimensiones $({\text{pasos}} \times {\text{simulaciones}})$. Las trayectorias continuas acumuladas en el espacio logarítmico se calculan eficientemente mediante sumas parciales vectorizadas y se transforman de vuelta a la escala original de precios mediante la función exponencial:

$$G_k = \exp\left( \ln(G_0) + \sum_{i=1}^{k} \left[ \left(\mu - \frac{1}{2}\sigma^2\right)\Delta t + \sigma \sqrt{\Delta t} Z_i \right] \right)$$

Posteriormente, el algoritmo evalúa de manera matricial la condición lógica de frontera $G_k \ge B$, aislando el menor índice temporal $k$ para cada columna (simulación) que cumpla con el criterio de activación, determinando así el tiempo empírico de primera travesía $\tau = k \times \Delta t$.  

A continuación se muestran la gráfica de la serie obtenida, la volatilidad y los resultados obtenidos:

![Serie](..\images\serie_p2_item2.png)

![Volatilidad](..\images\voltatilidad_p2_item2.png)

## Punto 3:

#### Enunciado: Regresión Bayesiana No Paramétrica mediante Procesos Gaussianos (GP) en PyMC

A partir de un conjunto de observaciones bidimensionales conteniendo una variable predictora $X$ y una variable de respuesta continua $Y$, implemente un modelo de Regresión por Procesos Gaussianos para inferir la función subyacente de los datos y realizar predicciones estocásticas en zonas no observadas:

1. Especificación del Prior:
   Defina un proceso gaussiano latente estructurado a partir de una función de media nula ($\mu(x) = 0$) y una función de covarianza o kernel de Exponencial Cuadrática (también conocida como Función de Base Radial o RBF).

2. Definición de Hiperparámetros:
   Asigne distribuciones de probabilidad a priori para los hiperparámetros del kernel: una distribución Half-Normal para la escala de amplitud vertical ($\eta$) y una distribución Gamma para la escala de longitud horizontal (lengthscale, $\ell$). Modele el ruido de medición de la verosimilitud ($\sigma$) mediante una distribución Half-Normal.

3. Optimización Bayesiana (Estimación MAP):
   Dadas las restricciones de cómputo y con el fin de optimizar la eficiencia del modelo, implemente la estimación del Máximo a Posteriori (MAP) empleando la función pm.find_MAP de la librería PyMC configurada con el algoritmo de optimización cuasi-Newton L-BFGS-B.

4. Predicción e Inferencia Visual:
   Utilice la API condicional de PyMC (gp.conditional) para evaluar el proceso sobre un dominio denso de prueba ($X_* $). Grafique la media predictiva estimada junto con sus respectivos intervalos de credibilidad bayesiana al $95\%$ ($\pm 1.96\sigma_*$) superpuestos con los puntos de entrenamiento originales.

#### Sustentación:

- Formulación del Modelo de Regresión por Procesos Gaussianos
  Un Proceso Gaussiano (GP) es una colección infinita de variables aleatorias, tal que cualquier subconjunto finito de ellas sigue una distribución conjunta gaussiana. En un problema de regresión, asumimos que la relación entre la variable de entrada $x$ y la respuesta observada $y$ está sujeta a un ruido aditivo gaussiano blanco e independiente:

  $$y = f(x) + \epsilon, \quad \epsilon \sim \mathcal{N}(0, \sigma^2)$$

  Donde la función latente desconocida $f(x)$ se modela directamente en su espacio funcional mediante un GP priorizado:

  $$f(x) \sim \mathcal{GP}\left(m(x), k(x, x')\right)$$

  Configurando la función de media como nula ($m(x) = 0$), la estructura geométrica y de suavizado de las trayectorias queda determinada por la función de covarianza Exponencial Cuadrática (RBF), parametrizada por la amplitud $\eta$ y la escala de longitud $\ell$:

  $$k(x, x') = \eta^2 \exp\left( -\frac{(x - x')^2}{2\ell^2} \right)$$

  Aquí, $\ell$ controla la suavidad de la función (qué tan rápido cambia a lo largo del eje horizontal) y $\eta$ controla la variabilidad vertical.

- Distribución Predictiva Condicional (Kriging Bayesiano):

  Dado un conjunto de datos de entrenamiento $D = \{(x_i, y\_i)\}\_{i=1}^n$ y un nuevo conjunto de puntos de prueba $X_* $, la distribución conjunta entre las observaciones y las predicciones latentes $f_* = f(X_*)$ es una distribución normal multivariada:
  
  ![eq1](..\images\eq1.svg)
  
  Aplicando las reglas de condicionamiento gaussianas, se deduce que la distribución posterior predictiva de las variables latentes en los nuevos puntos también es una gaussiana, $f_* \mid X, \mathbf{y}, X_* \sim \mathcal{N}(\mu_*, \Sigma)$, donde los momentos estadísticos óptimos se calculan mediante las ecuaciones de proyección matricial:
  
  ![eq2](..\images\eq2.svg)
  
  ![eq3](..\images\eq3.svg)

- Estimación del Máximo a Posteriori (MAP) mediante L-BFGS-B:

  En lugar de simular la distribución posterior completa de los hiperparámetros $\boldsymbol{\theta} = \{\ell, \eta, \sigma\}$ usando algoritmos de muestreo basados en gradientes (como NUTS), el método MAP calcula el estimador puntual que maximiza la densidad de la probabilidad posterior. Por el Teorema de Bayes, esto equivale a maximizar la suma del logaritmo de la verosimilitud marginal y el logaritmo de las distribuciones a priori:

  ![eq4](..\images\eq4.svg)

  El algoritmo L-BFGS-B (Limited-memory Broyden–Fletcher–Goldfarb–Shanno con restricciones de caja) resuelve este problema de optimización numérica no lineal de gran escala. Utiliza aproximaciones compactas de la matriz inversa de Hessian para guiar la dirección del gradiente, asegurando que los hiperparámetros se mantengan estrictamente dentro de sus límites físicos (por ejemplo, restricciones de positividad $\ell, \eta, \sigma > 0$)

Finalmente se muestran las gráficas de algunas de las posibles trayectorias del proceso Gaussino junto con una banda de confianza del 95% para el proceso:

  ![Posibles curvas](..\images\posibles_curvas_gp.png)

  ![Bandas de confianza](..\images\bandas_de_confianza.png)
   
