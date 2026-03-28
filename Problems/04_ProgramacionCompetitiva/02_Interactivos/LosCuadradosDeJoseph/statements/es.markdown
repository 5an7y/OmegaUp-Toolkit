# Problema

Muchos conocen el gran teorema de Joseph-Louis Lagrange, pero pocos saben que, en realidad, la teoría se originó de un matemático poco conocido llamado Joseph Jael Tenorio, aunque la gente los confundió debido a que tenían el mismo nombre.

El teorema dicta que todo número entero no negativo se puede expresar como la suma de cuatro enteros no negativos elevados al cuadrado. Es decir,

$$
p = a^2 + b^2 + c^2 + d^2.
$$

El doctor profesor Santiago aún no cree del todo en esta teoría, por lo que te dio ciertos valores de $p$ y deberás determinar los cuatro enteros $0 \leq a, b, c, d \leq 10^9$ que satisfagan la condición del teorema. Se te asegura que $p \leq 10^{18}$.

# Evaluación

Este es un problema de solo salida. Deberás resolver los casos proporcionados a continuación.

{{output-only:download}}

Debes crear un archivo `zip` que contenga los archivos `.out` con las respuestas, y ese `zip` será el que deberás enviar. Para cada uno de los casos, se calculará $p' = a^2 + b^2 + c^2 + d^2$, y se te otorgarán puntos conforme al siguiente criterio:

- Si $|p' - p| \geq 10$, tu puntaje para ese caso será 0.
- Si $|p' - p| < 10$, tu puntaje para ese caso será $10 - |p' - p|$.

Si la respuesta no es válida, el puntaje será 0.

# Ejemplos

||input  
4  
||output  
1 1 1 1  
||end