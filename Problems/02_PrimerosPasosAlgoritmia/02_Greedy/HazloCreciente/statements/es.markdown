# Problema

Se te da un arreglo de $N$ elementos. A cada elemento le puedes aplicar la operación: "cambia el elemento $a_i$ por $a_i/2$ redondeado hacia abajo".

Determina el numero minimo de veces que debes aplicar la operaciones para hacer el arreglo creciente. Es decir, $a_1 < a_2 < ... < a_N$.

# Entrada

Se te dara un numero $N$ indicando la cantidad de elementos en el arreglo. En la siguiente linea se te daran los $N$ elementos.

# Salida

Deberas imprimir la cantidad minima de veces que tienes que aplicar la operacion para que el arreglo sea creciente. En caso de que no se pueda imprime -1.

# Ejemplos

||input
3
3 6 5
||output
2
||description
El arreglo nos puede quedar como $[1, 3, 5]$, despues de aplicar la operacion al primer y el segundo elemento.
||input
3
2 2 2
||output
-1
||input
5
8 26 5 21 10
||output
11
||end

# Limites

- $1 \leq N \leq 30$
- $1 \leq a_i \leq 10^9$