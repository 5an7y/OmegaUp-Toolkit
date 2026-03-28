# Problema

Un día, Santiago estaba monitoreando un examen de la OMI Yucatán. Sin embargo, como es una persona muy ocupada, no tiene tiempo para estar revisando el ranking constantemente. Por eso, uno de sus mejores programadores, Juan Andrés Ávila, diseñó un sistema de *Highlights*.

Este sistema es capaz de resaltar los momentos más importantes de un concurso. ¿Cómo lo hace? Bastante sencillo. Se tienen un total de $N$ envíos a lo largo del concurso, y el envío más destacado en un rango $[L, R]$ es aquel con el mayor puntaje. Entonces, el sistema debe ser capaz de recibir cualquier intervalo y devolver el puntaje máximo para obtener el *highlight* de ese periodo.

Además, en los concursos, muchas veces existen reevaluaciones, por lo que algunos puntajes pueden verse afectados. Por lo tanto, el sistema también debe ser capaz de soportar estos cambios.

Tu tarea es diseñar el sistema que sea capaz de:

- Obtener el puntaje máximo en un intervalo dado.
- Cambiar el puntaje de un envío específico.

# Entrada

Se te dará un número $N$ que indica la cantidad de envíos totales en el concurso.

Luego, se te proporcionarán los $N$ puntajes $a_i$ de cada envío.

Seguido de esto, se te dará un número entero $Q$ que indica la cantidad de operaciones que debes procesar.

En las siguientes $Q$ líneas se te darán operaciones representadas por 3 enteros:

- Si $q_i = 1$, deberás imprimir el puntaje más alto en el rango $[l_i, r_i]$.
- Si $q_i = 2$, deberás cambiar el puntaje de $a_{p_i}$ a $j_i$.

# Salida

Deberás imprimir las respuestas a las operaciones del tipo 1.

# Ejemplos

||input
5  
8 4 1 3 2  
3  
1 2 4  
2 3 10  
1 2 4  
||output
4  
10  
||description
Primero, nos preguntan el puntaje máximo en el rango de 2 a 4, y resulta que es $4$, ya que los elementos son $[4, 1, 3]$.

Luego, se actualiza el tercer envío a un puntaje de 10. Entonces, cuando nos vuelven a hacer la pregunta, el mayor puntaje es 10, ya que los elementos ahora son $[4, 10, 3]$.
||end

# Límites

- $1 \leq N, Q \leq 3 \times 10^5$.
- $1 \leq a_i, j_i \leq 10^5$.
- $1 \leq l_i \leq r_i \leq N$.
- $1 \leq p_i \leq N$.
- Todas las subtareas estan agrupadas

**Subtarea 1 [15 puntos]**

- $1 \leq N, Q \leq 100$.

**Subtarea 2 [15 puntos]**

- $q_i = 1$ y $a_i = 1$.

**Subtarea 3 [20 puntos]**

- $q_i = 1$.

**Subtarea 4 [20 puntos]**

- $1 \leq N \leq 10^5$.
- $1 \leq Q \leq 5 \times 10^4$.

**Subtarea 5 [30 puntos]**

- Sin restricciones adicionales.