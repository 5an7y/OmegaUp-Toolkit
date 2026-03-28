# Problema

Se te dará una permutación de $N$ elementos. Una permutación consiste en un arreglo de los elementos del $1$ al $N$ ordenados de manera aleatoria.

La permutación se puede ordenar usando la siguiente operación: Puedes intercambiar los elementos en la posición $i$ y $j$ siempre y cuanto $i - j = k$. Para cierto valor $k$.

Tu tarea es encontrar cual es el maximo valor que puede tomar $K$ de tal forma que el arreglo se pueda ordenar.

# Entrada

Un entero $N$ indicando el tamaño de la permutacion. Seguido los $N$ numeros $a_i$ que representan la permutacion.

# Salida

Deberas imprimir el maximo valor que $K$ puede alcanzar para ordenar la permutacion.

# Ejemplos

||input
4
4 2 3 1
||output
3
||description
Si elijo 3 puedo cambiar los elementos en la posicion 4 y 1, ya que $4 - 1 = 3$ y de esta forma el arreglo queda ordenado.
||input
5
5 4 3 2 1
||output
2
||end

# Limites

- $1 \leq N \leq 100$