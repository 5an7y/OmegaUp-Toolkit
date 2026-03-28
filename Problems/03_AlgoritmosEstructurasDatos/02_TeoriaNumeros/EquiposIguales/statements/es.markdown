# Problema

Hoy es el dia que los mundos se cruzan, decidiste juntar a tus dos grupos de amigos para tu cumpleanos. El primer grupo cuenta con una cantidad $N$ de personas, mientras que el segundo grupo cuenta con $M$ personas. 

Te gustaria hacer una dinamica donde estos puedan participar y conocerse. No obstante, la dinamica que tienes pensada se basa en formar equipo de cierta cantidad de personas (tu eliges la cantidad). Tu sabes, que en principio nadie del primero grupo va a querer hacer equipo con alguien del segundo y vicerversa, entonces, quieres elegir un tamano de grupo de tal forma que cada quien este con alguien de su mismo grupo.

Tu tarea en este problema sera determinar de cuantas formas puedes elegir el tamano de los equipos.

# Entrada

Se te daran los numeros $N$ y $M$ mencionados anteriormente.

No lo sabias? Eres famoso, entonces estos numeros son **muy** grandes. Por lo tanto, no se te daran de forma normal como enteros.

En la primera linea se te dara un entero $A$ representando la cantidad de factores primos del numero $N$. Luego, se te procedera a darte los $A$ factores primos del numero.

En la segunda linea se te dara un entero $B$ representando la cantidad de factores primos del numero $M$. Luego, se te procedera a darte los $B$ factores primos del numero.

# Salida

Deberas imprimir la cantidad de tamanos distintos de los que puedes elegir los equipos. Como la respuesta puede ser muy grande, imprimela modulo $10^9 + 7$.

# Ejemplos

||input
3
2 2 2
3
2 2 3
||output
3
||description
El primer grupo consta de $2^3 = 8$ personas. Mientras que el segundo consta de $2^2 \times 3 = 12$ personas. Puedes hacer equipos de tamano $[1, 2, 4]$ sin problema, ya que en cualquier caso cada uno de los grupos puede formar equipos de esos tamanos entre si.

Por otro lado, aunque teoricamente son $20$ en total y puedes hacer equipos de $5$, esto implicaria que habria por lo menos un equipo donde hayan personas de un grupo mezcladas con las del otro.
||input
1
13
1
7
||output
1
||end

# Limites

- $1 \leq A, B \leq 10^5$.
- $1 \leq a_i, b_i \leq 10^6$.

**Subtarea 1 [6 puntos]**

- $A = B = 1$.

**Subtarea 2 [6 puntos]**

- $A = 1$.

**Subtarea 3 [11 puntos]**

- $1 \leq N = a_1 \times ... \times a_{A} \leq 10^8$.
- $1 \leq M = b_1 \times ... \times b_{B} \leq 10^8$.

**Subtarea 4 [12 puntos]**

- Los tamanos de los grupos que pueden ser formados se encuentran en el rango $[1, 10^3]$.

**Subtarea 5 [15 puntos]**

- $N = M$.

**Subtarea 6 [15 puntos]**

- Los tamanos de los grupos que pueden ser formados se encuentran en el rango $[1, 10^{8}]$.

**Subtarea 7 [10 puntos]**

- Los tamanos de los grupos que pueden ser formados se encuentran en el rango $[1, 10^{16}]$.

**Subtarea 8 [10 puntos]**

- $a_i < a_{i+1}$.
- $b_i < b_{i+1}$.

**Subtarea 9 [15 puntos]**

- Sin restricciones adicionales