# Descripción

Se acerca el fin de año, y con ello el Hackathon Internacional de Pair Programming, en la cuál parejas de programadores se reunen para desarrollar un proyecto que tenga un impacto social positivo en su comunidad. Aarón el resposable de organizar los equipos que irán a competir este año representando a tu universidad. 

Para garantizar el mejor desempeño, dos personas pueden formar una pareja unicamente si conocen la misma cantidad de tecnologias. Hay programadores de nuevo ingreso que dominan cero tecnologías. Estos _pueden_ ser emparejados con cualquier programador que domine al menos una tecnología, porque el más experimentado se hará responsable de enseñarle lo que sabe a su compañero con el fin de garantizar que trabajarán al mismo ritmo durante la competencia. **No** se puede emparejar a un programador con sigo mismo.

Para averiguar cuantas tecnologías domina cada uno, cada programador deberá contestar una encuesta en la que seleccionará las tecnologías que domina. Inicialmente, debemos asumir que todos dominan cero tecnologías.

Recibirás $N$ respuestas de la forma $X$, $Y$, donde $Y$ es la cantidad de tecnologías que el programador $X$ seleccionó en la encuesta. Conforme vayas recibiendo las respuestas, debes imprimir cuantas parejas distintas puedes mandar al Hackathon para que representen a la escuela, de acuerdo con la información que tienes hasta ese momento.

# Entrada

- La primera contiene $N$, que representa la cantidad de estudiantes.
- Las siguientes $N$ lineas contienen 2 enteros: $X$ y $Y$, que representan el número del programador y la cantidad de tecnologías que domina.

# Salida

Por cada caso de prueba, imprime $N$ enteros en una sola linea, separados por un espacio, que indiquen la máxima cantidad de equipos que podrías mandar al hackathon, si emparejaras de forma óptima a los programadores que conocen cero tecnologias con los que conocen al menos una, de acuerdo con la información que tienes hasta ese momento.

# Ejemplo

||input
4
3 2
1 1
4 1
2 4
||output
6 5 4 1
||description
Con la primera respuesta la cantidad de tecnologias que domina cada quien es $[0, 0, 2, 0]$. El tecero puede hacer pareja con cualquiera de los otros 3, ademas los $0$ pueden hacer pareja con cualquier otro igual, tenemos un total de $6$ parejas posibles.

Cuando nos dan la segunda respuesta tenemos $[1, 0, 2, 0]$. Solo puedes formar las parejas con $0$.

Cuando nos dan la tercera respuesta tenemos $[1, 0, 2, 1]$. Ahora podemos formar las parejas $(1_1, 1_4), (1_1, 0), (1_4, 0), (2, 0)$.

Cuando nos dan la cuarta respuesta tenemos $[1, 4, 2, 1]$. Ahora podemos formar solo la pareja $(1_1, 1_4)$.
||input
3
1 1
2 1
3 1
||output
3 3 3
||end

# Limites

* $1 \leq N \leq 2*10^5$
* $1 \leq X \leq N$
* $0 \leq Y \leq N$
* Todas las $N$ respuestas tienen valores distintos de $X$.

# Subtareas

* 25 puntos:
    - $1 \leq N \leq 100$
    - $1 \leq Y \leq 2$.
* 25 puntos:
    - $1 \leq N \leq 100$
* 25 puntos:
    - $1 \leq N \leq 5 \times 10^3$
* 25 puntos:
    - Sin restricciones adicionales.