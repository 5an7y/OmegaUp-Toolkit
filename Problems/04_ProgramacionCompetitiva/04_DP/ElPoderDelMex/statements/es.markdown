# Problema

La funcion $mex$ de un arreglo es el entero (no negativo) mas pequeño que no aparece en el arreglo. Por ejemplo $mex([1, 0, 1, 2, 3, 6, 8, 3]) = 4$ porque $4$ es el elemento mas chico que no aparece. $mex([1, 2, 3, 4, 5]) = 0$.

Tienes un arreglo de tamaño $N$. Tú puedes realizar la siguiente operacion: Elige dos enteros $1 \leq l \leq r \leq N$, todos los elementos del **subarreglo** $[a_l, ..., a_r]$ se vuelven $mex([a_l, ..., a_r])$.

Digamos que tengo el arreglo $[0, 3, 5, 1, 0, 6]$. Puedo elegir los elementos entre la segunda y penultima posicion (es decir, $[3, 5, 1, 0]$) y transformarlos en su $mex$. Por lo que, el arreglo me quedaria como $[0,2, 2, 2, 2, 6]$.

La pregunta es, cuantas veces debes aplicar este proceso para convertir todo el arreglo en $0$.

# Entrada

Se te dara un numero $N$ indicando la cantidad de elementos. En la siguiente linea $N$ enteros $a_i$ que son los elementos del arreglo.

# Salida

Deberas imprimir la cantidad de veces de aplicar la operacion mencionada para volver todos los elementos del arreglo $0$.

# Ejemplos

||input
5
0 1 2 3 4
||output
1
||description
Aplicas la operacion a partir del segundo elemento
||input
4
1 2 1 2
||output
1
||end

# Limites

- $1 \leq N \leq 100$
- $0 \leq a_i \leq 100$