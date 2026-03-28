# Problema

Obsesionados con optimizar su lenguaje, la civilización maya decidió crear nuevas versiones de su diccionario. Digamos que $s_1$ es una palabra original y, en la siguiente edición del diccionario maya, se creó $s_2$ como reemplazo de $s_1$. La palabra $s_2$ resulta de quitar una letra a $s_1$, escogiendo la versión con el menor valor lexicográfico.

Por ejemplo, si tenemos la palabra *maya*, al quitar una letra, obtenemos las siguientes opciones:

- aya
- mya
- maa
- may

Entre todas estas, *aya* es la que tiene el menor valor lexicográfico.

Después de $n$ iteraciones, donde $n$ es el tamaño de la palabra original, la palabra deja de existir. Los mayas decidieron crear la "historia" de una palabra como la concatenación de todos los cambios de una palabra, es decir,

$$
H(s) = s_1 + s_2 + s_3 + ... + s_n.
$$

Tu tarea consiste en determinar cuál es el $k$-ésimo carácter en la historia de una palabra.


*valor lexicografico:* La comparación lexicográfica es similar a cómo se ordenan las palabras en un diccionario. Se comparan los caracteres en las mismas posiciones de dos palabras. El primer carácter diferente entre ambas palabras determina cuál es menor. Por ejemplo, en el alfabeto inglés, "ana" es menor que "bat" porque la letra 'a' viene antes que la 'b'. Si dos palabras comienzan de la misma manera, se compara el siguiente carácter hasta encontrar una diferencia, o hasta que una palabra se termine.

# Entrada

En la primera línea, recibirás la cadena de caracteres $s$ que representa la palabra original, seguida de un entero $k$ que indica el carácter que se desea conocer.

# Salida

Debes imprimir el carácter en la posición $k$ en la historia de $s$.

# Ejemplos

||input
maya
7
||output
a
||description
La historia de *maya* es: mayaayaaaa. El séptimo carácter es `a`.
||input
x
1
||output
x
||end

# Límites

- $1 \leq |s| \leq 10^5$
- $1 \leq k \leq \frac{|s|(|s|+1)}{2}$.
- La cadena está formada por letras minúsculas del alfabeto inglés.

**Subtarea 1 [5 puntos]**

- $1 \leq k \leq |s|$.

**Subtarea 2 [7 puntos]**

- $1 \leq |s| \leq 50$.
- $1 \leq k \leq 2 * |s| - 1$.

**Subtarea 3 [9 puntos]**

- $1 \leq k \leq 2 * |s| - 1$.

**Subtarea 4 [10 puntos]**

- $1 \leq |s| \leq 10$.

**Subtarea 5 [13 puntos]**

- $1 \leq |s| \leq 1000$.

**Subtarea 6 [15 puntos]**

- $s$ está ordenado alfabéticamente.

**Subtarea 7 [16 puntos]**

- $s$ contiene únicamente los caracteres `a` o `b`.

**Subtarea 8 [25 puntos]**

- Sin restricciones adicionales.