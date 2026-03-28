# Problema

Muchos conocen el clásico juego de "Pato, Pato, Ganso", pero pocos conocen el grandioso "Pato, Ganso, Tolok" (derechos reservados de la OMI Yucatán). Este es un juego donde $N$ personas, numeradas del $1$ al $N$, están sentadas en círculo.

Comenzamos con la primera persona; a esta se le toca la cabeza diciendo **Pato**. Luego, a la segunda persona se le toca la cabeza diciendo **Ganso**, lo que provoca que esa persona quede eliminada y salga del círculo. Posteriormente, se repiten los mismos pasos con las personas siguientes en el círculo. El proceso se repite un total de $K$ veces. Sin embargo, en la última iteración del juego, en lugar de decirle **Ganso** a la última persona, se le dice **Tolok**, lo que significa que deberá enfrentarse en un duelo con quien estaba tocando las cabezas para ver quién gana.

Como buen programador, la condición física y el desperdicio de tiempo no son lo tuyo. Por lo tanto, deseas saber lo antes posible quién será la persona elegida como **Tolok**.

# Entrada

Se te dará un número $N$ que indica la cantidad de personas en el círculo y un entero $K$, correspondiente al número de iteraciones del juego.

# Salida

Deberás imprimir la persona que será elegida como **Tolok**.

# Ejemplos

||input
10 3
||output
6
||description
1 es pato, 2 es ganso, 3 es pato, 4 es ganso, 5 es pato y 6 es Tolok.

Nota cómo el ciclo se repite 3 veces, donde el último es el Tolok.
||input
10 7
||output
7
||description
1 es pato, 2 es ganso, 3 es pato, 4 es ganso, 5 es pato, 6 es ganso, 7 es pato, 8 es ganso, 9 es pato, 10 es ganso.

Después de las primeras 5 iteraciones, nuestro círculo de personas se ve así: $[1, 3, 5, 7, 9]$. Ahora 1 es pato, 3 es ganso, 5 es pato y 7 es Tolok.
||end

# Límites

- $1 \leq N \leq 10^{18}$.
- $1 \leq K \leq N$.
- Todas las subtareas están agrupadas.

**Subtarea 1 [15 puntos]**

- $N$ es par.
- $1 \leq K \leq N/2$.

**Subtarea 2 [25 puntos]**

- $N$ es una potencia de 2.

**Subtarea 3 [25 puntos]**

- $1 \leq N \leq 10^5$.

**Subtarea 4 [35 puntos]**

- Sin restricciones adicionales.