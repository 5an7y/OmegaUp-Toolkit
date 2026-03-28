# Problema

En un reino muy, muy lejano, existe una princesa llamada Sofía Quintal. Ella es muy exigente con su vestimenta, especialmente con sus zapatos. Tenía su propio zapatero, y nadie que no fuera él podía diseñar sus zapatos.

No obstante, había un gran problema: el zapatero se había retirado de la ciudad y ahora vivía algo lejos del reino. Además, Sofía no podía recordar cuál es su talla exacta de zapatos, lo único que recordaba era que es menor o igual a $N$. Como buena princesa, ella no puede salir del reino. Sin embargo, cada día Sofía manda a un caballero en búsqueda de un par de zapatillas de talla $x$. El caballero procede a salir **en la mañana de ese día**, sin embargo, no vuelve hasta la **noche del día siguiente**.

Cada vez que llega un caballero, Sofía sabe si necesita una talla menor, mayor o si es la que estaba buscando. Lo malo es que Sofía necesita las zapatillas para la noche del día $T$, para su gran evento. Ayúdala determinando la mejor estrategia que pueda seguir mandando a los caballeros.

*Solo se puede mandar un caballero por día ya que solo hay $2$ en el reino y no podemos arriesgar perder a ambos en el mismo viaje*.

# Implementación

Debes enviar un archivo que implemente la función `EncontrarZapatillas(int N)`. Esta función podrá llamar a la función `MandarCabellero(int x)` un máximo de $T$ veces.

## Función del evaluador `MandarCabellero()`

* C/C++: `char MandarCabellero(int x);`

### Descripción

El evaluador proporcionará esta función, la cual te permite mandar a un caballero en búsqueda de una zapatilla con talla $x$. La función devolverá un valor dependiendo de lo que sucedió con **la zapatilla que llegó esa noche** (ver la sección de parámetros).

### Parámetros

* `x`: La talla que se irá a buscar.
* Retorna: un carácter que representa lo que sucedió con la zapatilla que llegó el día que mandaste a ese caballero. `x`: indica que es el primer caballero que mandas, entonces no ha llegado nadie. `+`: indica que la zapatilla que llegó es más grande de lo esperado. `-`: indica que la zapatilla que llegó es más pequeña de lo esperado. `S`: indica que la zapatilla que llegó es la correcta.

## Función que debes implementar: `EncontrarZapatillas()`

* C/C++: `void EncontrarZapatillas(int N);`

### Descripción

La función deberá mandar a los caballeros hasta encontrar la zapatilla correcta.

### Parámetros

* `N`: Un entero que indica la talla máxima que Sofía podría calzar.
* Retorna: Nada, **la función debe terminar apenas llegue la zapatilla correcta**.

# Prueba

El archivo consta de tres enteros: $N$, $T$, $x$. Esto indica la talla máxima, el día que Sofía necesita las zapatillas y la talla real de Sofía.

# Ejemplo

||input
EncontrarZapatillas(3)
||output
||description
Se llama a la función que deberá resolver el problema.
||input
MandarCabellero(3)
||output
x
||description
Como es el primer caballero mandado, la función devuelve una `x`, indicando que no ha llegado ninguna zapatilla ese día.
||input
MandarCabellero(2)
||output
-
||description
Se manda un caballero en búsqueda de la zapatilla de talla 2, pero el de talla 3 llegó y, al parecer, quedó más grande de lo esperado.
||input
MandarCabellero(1)
||output
S
||description
Llegó el caballero con la zapatilla 2 y esa era la correcta, entonces el programa termina.
||end

# Límites

- $1 \leq N \leq 10^9$
- Siempre existe una forma de obtener la zapatilla en la noche $T$.
- Si haces una llamada inválida ($x \leq 0$ o $x > N$), obtendrás 0 puntos en esa subtarea automáticamente.
- Todas las subtareas están agrupadas.

**Subtarea 1 [6 puntos]**

- $N = 5$
- $T = 6$

**Subtarea 2 [6 puntos]**

- $N = 7$
- $T = 5$

**Subtarea 3 [12 puntos]**

- $N = 100$
- $T = 30$

**Subtarea 4 [18 puntos]**

- $N = 50$
- $T = 9$

**Subtarea 5 [6 puntos]**

- $N = 350$
- $T = 13$

**Subtarea 6 [9 puntos]**

- $N = 2500$
- $T = 17$

**Subtarea 7 [17 puntos]**

- $N = 3 \times 10^5$
- $T = 27$

**Subtarea 8 [26 puntos]**

- $N = 10^9$
- Para esta subtarea se pueden obtener puntos parciales. Sea $Q$ la cantidad de noches que te tardes en encontrar la zapatilla correcta; entonces,
    - Si $Q > 100$, obtendrás $0$ puntos.
    - Si $44 < Q \leq 100$, podrás obtener $\lceil\frac{2250000}{Q^3}\rceil$ puntos de los $26$.
    - Si $Q \leq 44$, obtendrás los $26$ puntos de la subtarea.


# Experimentación

{{libinteractive:download}}