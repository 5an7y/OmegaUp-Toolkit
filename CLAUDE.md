# CLAUDE.md — Guía de conocimiento para la IA

Este archivo es leído automáticamente por Claude Code al inicio de cada conversación. Contiene todo el conocimiento acumulado sobre este proyecto: convenciones, flujos de trabajo, decisiones de diseño, y ejemplos. **Debe mantenerse vivo:** cada vez que aprendamos algo nuevo relevante sobre cómo crear o mejorar problemas, agrégalo aquí.

---

## Contexto del proyecto

Este repositorio es una herramienta para crear problemas de programación competitiva para la **Olimpiada Mexicana de Informática en Yucatán (OMI Yucatán)**. Los problemas se suben a la plataforma [OmegaUp](https://omegaup.com), que tiene un formato específico. Las clases de la olimpiada usan estos problemas para entrenar a los estudiantes.

---

## Estructura del repositorio

```
CPProblemGenerator/
├── CreateProblem.py       # Crea la estructura de un nuevo problema desde el template
├── GenerateCases.py       # Compila y ejecuta el generador de casos
├── TestCases.py           # Compila y prueba soluciones contra los casos generados
├── Libs/                  # Librerías C++ para generadores
│   ├── Generator.hpp      # Maneja entrada/salida de archivos de casos
│   ├── Random.hpp         # Utilidades de generación aleatoria
│   ├── Background.hpp     # Segment tree interno (usado por Random.hpp)
│   └── Constants.hpp      # Constantes
├── Examples/
│   ├── Template/          # Template base para nuevos problemas
│   └── InteractiveTemplate/  # Template para problemas interactivos
├── Problems/              # Todos los problemas, organizados por fases y temas
│   ├── 01_IntroduccionProgramacion/
│   │   ├── 01_Condicionales/
│   │   ├── 02_Ciclos/
│   │   ├── 03_Arreglos/
│   │   └── 04_Strings/
│   ├── 02_PrimerosPasosAlgoritmia/
│   │   ├── 01_Matematicas/
│   │   ├── 02_Greedy/
│   │   └── 03_TecnicasBasicas/    # Binary search, two pointers, sliding window, cubeta
│   ├── 03_AlgoritmosEstructurasDatos/
│   │   ├── 01_EstructurasDatos/   # Stack, queue, deque, monotone stack (manual)
│   │   ├── 02_TeoriaNumeros/
│   │   ├── 03_ObjetosLibreria/    # STL: map, set, priority_queue, etc.
│   │   ├── 04_TecnicasBasicasII/  # Prefix arrays, update points, sweep line
│   │   └── 05_Ordenamientos/
│   ├── 04_ProgramacionCompetitiva/
│   │   ├── 01_Backtracking/
│   │   ├── 02_Interactivos/
│   │   ├── 03_Grafos/             # BFS, DFS
│   │   └── 04_DP/
│   ├── 05_TemasEspecializados/
│   │   ├── 01_Combinatoria/
│   │   ├── 02_AlgoritmosGrafos/   # Dijkstra, etc.
│   │   ├── 03_SegmentTree/
│   │   ├── 04_AlgoritmosArboles/
│   │   └── 05_DivideYVenceras/
│   └── _Recursos/                 # Editoriales, PDFs, imágenes de concursos
```

---

## Estructura de un problema

Cada problema es una carpeta con esta estructura:

```
MiProblema/
├── case_generator.cpp     # Genera los casos de prueba
├── cases.arg              # Argumentos para cada caso (uno por línea)
├── cases/                 # Archivos .in y .out generados
│   ├── c1.in
│   ├── c1.out
│   └── ...
├── solution/
│   └── solution.cpp       # Solución de referencia (puede haber múltiples .cpp)
├── statements/
│   └── es.markdown        # Enunciado del problema en español (formato OmegaUp)
├── testplan               # (opcional) Define grupos y pesos de casos
└── validator.cpp          # (opcional) Validador personalizado de salida
```

---

## Formato del enunciado: `statements/es.markdown`

OmegaUp usa un formato Markdown especial con secciones predefinidas. Las fórmulas matemáticas van entre `$...$` (LaTeX inline).

```markdown
# Historia

Contexto narrativo opcional que ambienta el problema (puede omitirse).

# Problema

Descripción concisa y precisa del problema a resolver.

# Entrada

Descripción de la entrada. Ejemplo:
Se te dará un entero $N$ en la primera línea, seguido de $N$ enteros.

# Salida

Descripción exacta de qué debe imprimir el programa.

# Ejemplos

||input
2
1 3
||output
4
||description
Descripción opcional del caso de ejemplo.
||input
3
1 2 3
||output
6
||end

# Limites

- $1 \leq N \leq 10^5$

**Para un 20% de los casos**

- $1 \leq N \leq 100$
```

**Reglas importantes del formato:**
- `||input`, `||output`, `||description` y `||end` son marcadores especiales de OmegaUp.
- `||description` es opcional por ejemplo.
- Siempre terminar la sección de ejemplos con `||end`.
- Las fórmulas matemáticas usan sintaxis LaTeX: `$O(N \log N)$`, `$10^9$`, etc.
- La sección `# Historia` es opcional pero recomendada para dar contexto a los estudiantes.

---

## Formato de `cases.arg`

Cada línea define un caso de prueba. El primer token es el **nombre del caso** y el resto son **argumentos** que el generador puede leer.

```
c1 100
c2 1000
c3 100000
```

El generador recibe el nombre del caso como `argv[1]` (usado por `Generator::init_generator`) y los argumentos adicionales quedan disponibles en `Generator::arguments`. Los nombres de los casos determinan los nombres de los archivos `.in` y `.out`.

**Convención de nombres con grupos:** Si usas `testplan`, los casos se agrupan por el prefijo antes del punto:
```
grupo1.c1 100
grupo1.c2 500
grupo2.c1 1000
```
Esto crea dos grupos (`grupo1`, `grupo2`). Dentro de un grupo, **todos los casos deben ser AC** para obtener puntos del grupo.

---

## Formato de `testplan`

Define el peso de cada caso para el puntaje. Si no existe, todos los casos valen igual.

```
c1 10
c2 10
c3 20
grupo1.c1 15
grupo1.c2 15
grupo2.c1 30
```

Se genera automáticamente con:
```bash
py CreateProblem.py Problems/MiTema/MiProblema --testplan
```
(Asigna peso 0 a todos; hay que ajustar manualmente los pesos.)

---

## Librería `Generator.hpp`

Provee tres streams para el `case_generator.cpp`:

| Stream | Uso |
|--------|-----|
| `Generator::case_in` | Escribe la entrada del caso (archivo `.in`) |
| `Generator::case_out` | Escribe la salida esperada del caso (archivo `.out`) |
| `Generator::arguments` | Lee los argumentos del `cases.arg` |

**Siempre llamar primero:** `Generator::init_generator(argc, argv);`

**Ejemplo completo:**
```cpp
#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);

    int N;
    Generator::arguments >> N;

    auto vec = Random::rnd(1, 1000, N);

    Generator::case_in << N << '\n';
    for (int i = 0; i < N; i++)
        Generator::case_in << vec[i] << " \n"[i == N-1];

    // Si el output es simple, puedes calcularlo aquí también:
    // Generator::case_out << answer;
    // De lo contrario, usa --use_solution en GenerateCases.py

    return 0;
}
```

---

## Librería `Random.hpp`

Funciones disponibles (todas en el namespace `Random`):

```cpp
// Número aleatorio en [a, b] (inclusive)
Random::rnd(a, b)

// Vector de sz números aleatorios en [a, b]
Random::rnd(a, b, sz)

// Vector de sz números ÚNICOS en [a, b]
Random::rnd_unique(a, b, sz)

// Par ordenado (a1 <= a2) con valores en [a, b]
Random::rnd_pair(a, b)

// Vector de pares ordenados
Random::rnd_pair(a, b, sz)

// Vector de sz números que suman exactamente `sum`
Random::rnd_nums_that_sum(sum, sz)
Random::rnd_nums_that_sum(sum, sz, allow_zero=true)

// Árbol aleatorio de N nodos, retorna lista de aristas
Random::rnd_tree(N)

// Bosque aleatorio de N nodos y `trees` árboles
Random::rnd_forest(N, trees)
```

**Tipos:** Las funciones son templates, funcionan con `int`, `long long`, etc.

---

## Scripts de Python

### `CreateProblem.py` — Crear un problema nuevo

```bash
py CreateProblem.py Problems/MiTema/MiProblema
py CreateProblem.py Problems/MiTema/MiProblema --validator   # incluye validator.cpp
py CreateProblem.py Problems/MiTema/MiProblema --testplan    # genera testplan desde cases.arg
```

Copia la estructura de `Examples/Template/` al directorio indicado.

### `GenerateCases.py` — Generar los casos

```bash
py GenerateCases.py Problems/MiTema/MiProblema
py GenerateCases.py Problems/MiTema/MiProblema --use_solution   # usa solution.cpp para generar .out
py GenerateCases.py Problems/MiTema/MiProblema --stack 33554432  # stack más grande (32MB)
```

- Compila `case_generator.cpp` con `g++ -std=c++20 -I ./Libs`
- Lee `cases.arg` y ejecuta el generador para cada caso
- Con `--use_solution`: compila `solution/solution.cpp` y la ejecuta sobre cada `.in` para generar los `.out`
- **Nota:** El stack por defecto es 16MB (`16777216`). Para recursiones profundas usar `--stack 33554432`

### `TestCases.py` — Probar soluciones

```bash
py TestCases.py Problems/MiTema/MiProblema
py TestCases.py Problems/MiTema/MiProblema --time_limit 2000         # límite de 2 segundos
py TestCases.py Problems/MiTema/MiProblema --solutions sol1.cpp      # solo prueba sol1.cpp
py TestCases.py Problems/MiTema/MiProblema --cases c1 c2 c5          # solo prueba esos casos
py TestCases.py Problems/MiTema/MiProblema --validator               # usa validator.cpp
```

Veredictos posibles:
| Veredicto | Significado |
|-----------|-------------|
| AC | Aceptado |
| WA | Respuesta incorrecta |
| TLE | Tiempo límite excedido |
| RTE | Error en ejecución |
| PA | Aceptado parcialmente (solo con validador) |

---

## Flujo de trabajo para crear un problema nuevo

1. **Crear la estructura:**
   ```bash
   py CreateProblem.py Problems/MiTema/NombreProblema
   ```

2. **Escribir el enunciado** en `statements/es.markdown` siguiendo el formato OmegaUp.

3. **Diseñar los casos** en `cases.arg`: nombres y parámetros de cada caso.

4. **Implementar el generador** en `case_generator.cpp` usando `Generator.hpp` y `Random.hpp`.

5. **Implementar la solución** en `solution/solution.cpp`.

6. **Generar los casos:**
   ```bash
   py GenerateCases.py Problems/MiTema/NombreProblema --use_solution
   ```

7. **Verificar la solución:**
   ```bash
   py TestCases.py Problems/MiTema/NombreProblema
   ```

8. **(Opcional) Crear testplan** para puntaje por grupos:
   ```bash
   py CreateProblem.py Problems/MiTema/NombreProblema --testplan
   # Luego editar manualmente testplan para asignar pesos
   ```

---

## Convenciones del proyecto

- Los problemas se nombran en `CamelCase` descriptivo, en español.
- Los casos simples se nombran `c1, c2, ...`; los casos con grupos usan `grupo.caso` o `subgrupo.caso`.
- Los argumentos en `cases.arg` normalmente incluyen el tamaño del input (N) u otros parámetros de dificultad.
- Los valores de borde siempre deben incluirse como casos: mínimo, máximo, casos especiales.
- La solución de referencia va siempre en `solution/solution.cpp`. Se pueden incluir soluciones alternativas (bruteforce, etc.) con otros nombres para comparar.
- Los recursos de concursos (editoriales, PDFs, imágenes) van en `Problems/_Recursos/`.

### Clasificación de problemas por tema

Los problemas se clasifican por el **tema máximo** requerido para obtener el 100% de los puntos. La clasificación depende de los **límites reales del problema**, no solo del nombre del algoritmo:

- **Regla clave:** si la solución de fuerza bruta (O(N²), O(N·Q), etc.) entra dentro del tiempo límite dado los constraints del problema, el problema se clasifica en la categoría más básica que permita esa solución.
  - Ejemplo: `ActualizacionRangos` con N,Q ≤ 100 → O(N·Q) = 10,000 ops → cabe en 1 seg → **Arreglos**, no TecnicasBasicasII.
  - Ejemplo: `InterseccionArreglos` con N,Q ≤ 100 → brute force cabe → **Arreglos**.
  - Si los mismos problemas tuvieran N,Q ≤ 10⁵, entonces sí irían en TecnicasBasicasII.
- Un problema puede requerir múltiples temas; siempre se clasifica por el más avanzado necesario para el 100%.
- La referencia de fases/temas está en Notion: "Temas OMI Yucatan".

---

## Diseño pedagógico de problemas

Los problemas están pensados para estudiantes de preparatoria/secundaria que aprenden programación competitiva. Algunas guías:

- **Historia:** Dar contexto local o divertido (referencias a Yucatán, nombres conocidos) hace los problemas más accesibles.
- **Subtareas:** Diseñar casos que permitan soluciones parciales (fuerza bruta para 20%, solución completa para 100%) ayuda a estudiantes de todos los niveles.
- **Claridad:** El enunciado debe ser preciso y sin ambigüedades. Los ejemplos deben cubrir casos representativos.
- **Casos borde:** Siempre incluir N=1, valores mínimos, valores máximos, y casos donde la respuesta es 0 o negativa si aplica.

---

## Cómo mantener este archivo

**Este archivo debe crecer con el tiempo.** Cada vez que:
- Aprendamos un nuevo patrón para diseñar casos
- Descubramos una convención nueva
- Creemos una herramienta nueva
- Encontremos un error común y su solución
- Decidamos algo sobre el diseño pedagógico

...debe agregarse aquí en la sección correspondiente. Si no existe sección adecuada, créala.

El objetivo es que cualquier persona (o IA) que clone este repo y abra Claude Code tenga todo el contexto necesario para crear problemas de calidad sin necesidad de explicaciones adicionales.
