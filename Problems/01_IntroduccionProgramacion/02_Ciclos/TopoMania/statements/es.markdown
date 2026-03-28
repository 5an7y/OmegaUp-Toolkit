# Problema

TopoMania es un juego mecanico donde tienes una fila de $N$ hoyos donde puede salir un topo. Cada segundo, los topos aparecen en un lugar distinto y te da tiempo de pegarles con un martillo para ganar puntos.

Has descubierto como el sistema de topos funciona y estas dispuesto a ganar la mayor cantidad de puntos posibles. Inicialmente se tiene un arreglo $S$ de $N$ elementos $[a_1, a_2, ..., a_N]$ donde cada elemento es cero o uno. Un $0$ indica que no hay un topo y un $1$ indica que si hay.

El juego consta de $N$ segundos, en el segundo $i$ la configuracion que se despliega es $S$ con el elemento $i$ invertido. Es decir, si $a_i$ era un $0$ pasa a ser un $1$ o viceversa.

La pregunta que debes responder es cual es la cantidad maxima de topos a los que les puedes pegar.

# Entrada

Se te dara un numero $N$ que es la cantidad de hoyos. Seguido el arreglo $S$ con elementos $a_i$ del arreglo.

# Salida

Deberas imprimir un entero representando la cantidad maxima de topos que les puedes pegar.

# Ejemplos

||input
3
1 0 1
||output
5
||description
En el primer tiempo la configuracion es $[0, 0, 1]$ que corresponde al arreglo original con el primer elemento invertido. Esto significa que habra un solo topo y puedes conseguir un punto. Luego, $[1, 1, 1]$ en el segundo tiempo pudiendo ganar 3 puntos. Finalmente $[1, 0, 0]$ pudiendo ganar $1$ punto. Dando un total de $1+3+1= 5$ puntos.
||input
4
1 1 1 1
||output
12
||end

# Limites

- $1 \leq N \leq 100$