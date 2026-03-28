# Problema

![](puntos.png)

Sobre una recta unidimensional pones un punto $A$ con coordenada $x = n$. Te gustaria encontrar un punto $B$ entre el origen ($O$) y $A$ de tal forma que si $\overline{OB}$ es la distancia del origen hasta $B$ y $\overlines{BA}$ la distancia de $B$ hasta el punto $A$; entonces 

$$
|\overline{OB} - \overlines{BA}| = k
$$

para cierto $k$. A veces este punto $B$ puede NO existir, entonces puedes recorrer $A$ una unidad hacia adelante o atras para que exista. La pregunta que estamos intentando responder es cuantas unidades debes mover el punto $A$ para que punto $B$ descrito anteriormente exista.

# Entrada

Los enteros $n$ y $k$.

# Salida

Un entero describiendo la cantidad de unidades que debes mover $A$ para que el punto $B$ exista.

# Ejemplos

||input
4 0
||output
0
||description
Esta es la imagen de ejemplo. Si ponemos $B = 2$, entonces $\overlines{OB} = 2$ y $\overline{BA} = 2$. Por lo tanto, $|\overline{OB} - \overline{BA}| = |2 - 2| = 0$.
||input
0 10
||output
10
||end

# Limites

- $1 \leq n, k \leq 10^9$