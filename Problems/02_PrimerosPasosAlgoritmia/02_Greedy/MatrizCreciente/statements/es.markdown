# Problema

Tienes una matriz de $N \times N$ que es **estrictamente creciente**, es decir, los números aumentan tanto a lo largo de las filas como a lo largo de las columnas.  
Sin embargo, algunas posiciones están vacías y se representan con un **0**.

Los espacios vacíos se pueden llenar con números positivos (mayores que 0), de tal forma que la matriz siga siendo estrictamente creciente en filas y columnas.  
Debes determinar si es posible completar la matriz de esta manera.

## Entrada

- Un entero $N$ indicando el tamaño de la matriz.
- A continuación, se dan $N$ líneas con $N$ enteros cada una, representando la matriz.  
  Un número positivo indica un valor fijo, mientras que un `0` indica una celda vacía que puedes rellenar.

## Salida

- Imprime `"SI"` si es posible completar la matriz respetando el orden creciente.
- Imprime `"NO"` en caso contrario.

## Ejemplos

||input
3  
1 2 3  
4 0 6  
7 8 9  
||output
SI  
||description
Podemos colocar un 5 en la posición vacía, y la matriz sigue siendo creciente.  
||input
4  
1 2 3 4  
2 4 0 5  
3 0 0 6  
4 5 6 7  
||output
NO  
||description
No hay ningún número que podamos colocar debajo del 4 de la segunda columna que mantenga el orden creciente.  
||end


## Límites

- $3 \leq N \leq 100$
- $0 \leq a_{i, j} \leq 10^5$
