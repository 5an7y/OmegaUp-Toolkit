# Historia

Había una vez un programador que estaba en búsqueda de un gran tesoro. Completó muchas aventuras, incluso llegó a ser el hombre más popular de la ciudad (ja, un programador siendo popular), cuando de repente se le apareció una puerta secreta que decía "Cueva del malvado robot OMI".

Sin dudarlo, el programador se adentró en la cueva. Vio que estaba todo vacío, parecía una mina abandonada. De repente todo empezó a temblar y el suelo de la mina comenzó a abrirse. ¡Parece que el programador se topó con una trampa! El suelo se abría y había lava allí, entonces nuestro aventurero comenzó a correr buscando la salida.

La puerta por donde entró parecía cerrada con una contraseña. Había un papel al lado con una combinación de dígitos. El programador intentó poner eso como la contraseña, pero no la aceptaba. Ya casi se iba a entregar a la muerte nuestro compañero cuando, un mono de juguete que estaba en la cueva comenzó a hablar y le dijo:

"Yo vi cómo el robot creó la contraseña. Verás, esa combinación que ves era la *antigua* contraseña. Obvio el robot no la iba a dejar allí nada más para escapar. Sin embargo, usó esa contraseña para crear la nueva. Lo que hizo fue reemplazar el primer número con su número favorito; después, el segundo dígito lo promedió con el primero y lo redondeó; para el tercero repitió el mismo proceso pero sacando el promedio con el segundo, y así sucesivamente.

Por ejemplo, si el código es `12345` y tu número favorito (del 0 al 9) es 6, entonces reemplazas el primer número por el 6 y te queda `62345`. Luego, para el segundo haces el promedio $(6 + 2) / 2 = 4$ y reemplazas el segundo número por el 4, quedando así `64345`. Después haces lo mismo con el tercero pero sacando el promedio con el segundo, es decir, $(4 + 3) / 2 = 3.5$. En este caso, él decidía si redondearlo hacia arriba o hacia abajo. Entonces podía ser $4$ o $3$".

El problema es que nadie sabía cuáles fueron los movimientos exactos que hizo el robot, ni su número favorito. Por lo cual, el programador se preguntó cuál era la cantidad de posibles contraseñas que se podían generar, para ver si valía la pena intentarlo o buscar otra forma de seguir.

# Problema

Dada la secuencia de números $K$, determina cuáles son todas las posibles contraseñas que se pueden generar. Como el número puede ser muy grande, la respuesta debe ser $mod 10^{16} - 7$.

# Entrada

El código inicial $A$, con dígitos entre 0 y 9.

# Salida

Un único entero que representa la cantidad de posibles códigos.

# Ejemplos

||input
12345
||output
48
||input
09
||output
15
||end

# Límites

Llamamos $S$ al tamaño de $A$.

- $1 \leq S \leq 10^4$
- Todas las subtareas se encuentran agrupadas

**Subtarea 1 [5 puntos]**

- $S = 1$

**Subtarea 2 [10 puntos]**

- $S = 2$

**Subtarea 3 [20 puntos]**

- Todos los dígitos de $A$ son `0`.

**Subtarea 4 [20 puntos]**

- $1 \leq S \leq 15$

**Subtarea 5 [20 puntos]**

- $0 \leq S \leq 30$

**Subtarea 6 [25 puntos]**

- Sin restricciones adicionales