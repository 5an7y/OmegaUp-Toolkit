# Problema

Ximena y Abril decidieron hacer compras juntas. Tienen una lista de $N$ objetos que pueden elegir en la tienda. Sin embargo, cada una debe hacer su propia lista de deseos por separado.  
Ximena marcará cuáles objetos le gustaría tener, y Abril hará lo mismo por su cuenta.

Al final, la tienda les entregará todos los objetos que alguna de ellas haya elegido, **siempre y cuando no haya sido marcado por ambas**.  
Tu tarea es determinar cuántos objetos les dará la tienda.

## Entrada

- Un entero $N$, la cantidad de objetos disponibles.
- Dos listas de longitud $N$:  
  - La primera contiene los valores $a_1, a_2, \dots, a_N$ que indican si Ximena eligió cada objeto.  
  - La segunda contiene los valores $b_1, b_2, \dots, b_N$ que indican si Abril eligió cada objeto.

Cada valor es:
- `1` si eligieron el objeto,
- `0` si no lo eligieron.

## Salida

- Un entero: la cantidad de objetos que la tienda entregará.

## Ejemplos

||input
5  
1 0 0 1 0  
0 1 0 1 1  
||output
3  
||description
El primer, segundo y último objeto fueron elegidos solo por una de ellas.
||input
7  
1 1 1 1 1 1 1  
1 1 1 1 1 1 1  
||output
0  
||end

## Límites

- $1 \leq N \leq 100$
- $0 \leq a_i, b_i \leq 1$
