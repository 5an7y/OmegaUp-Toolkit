# Official OmegaUp problemTag* and problemTopic* tags with human-readable descriptions.
# Source of truth for the interactive tag selector in `omegaup create`.
# Keep in sync with tags-reference.md.

# List of (tag_name, description) tuples.
TAGS = [
    # ── problemTag ──────────────────────────────────────────────────────────
    ("problemTagArithmetic",               "Aritmética básica"),
    ("problemTagArrays",                   "Arreglos"),
    ("problemTagBacktracking",             "Backtracking"),
    ("problemTagBigNumbers",               "Números grandes"),
    ("problemTagBinarySearch",             "Búsqueda binaria"),
    ("problemTagBinarySearchTree",         "Árbol de búsqueda binaria"),
    ("problemTagBipartiteMatching",        "Matching bipartito"),
    ("problemTagBitManipulation",          "Manipulación de bits"),
    ("problemTagBooleanAlgebra",           "Álgebra booleana"),
    ("problemTagBreadthFirstSearch",       "BFS (búsqueda en anchura)"),
    ("problemTagBruteForce",               "Fuerza bruta"),
    ("problemTagCharsAndStrings",          "Caracteres y cadenas"),
    ("problemTagChineseRemainderTheorem",  "Teorema chino del resto"),
    ("problemTagCombinations",             "Combinaciones"),
    ("problemTagConditionals",             "Condicionales"),
    ("problemTagConvexHull",               "Cápsula convexa"),
    ("problemTagCountingProblems",         "Problemas de conteo"),
    ("problemTagDepthFirstSearch",         "DFS (búsqueda en profundidad)"),
    ("problemTagDiophantineEquations",     "Ecuaciones diofánticas"),
    ("problemTagDirectedGraphs",           "Grafos dirigidos"),
    ("problemTagDisjointSets",             "Conjuntos disjuntos (Union-Find)"),
    ("problemTagDivideAndConquer",         "Divide y vencerás"),
    ("problemTagDivisibilityRules",        "Reglas de divisibilidad"),
    ("problemTagDynamicProgramming",       "Programación dinámica"),
    ("problemTagExponentialSearch",        "Búsqueda exponencial"),
    ("problemTagExponentiationBySquaring", "Exponenciación rápida"),
    ("problemTagFenwickTrees",             "Árbol de Fenwick (BIT)"),
    ("problemTagFormattedInputAndOutput",  "Entrada/salida con formato"),
    ("problemTagFunctions",                "Funciones"),
    ("problemTagGCDAndLCM",                "MCD y MCM"),
    ("problemTagGameTheory",               "Teoría de juegos"),
    ("problemTagGraphConnectivity",        "Conectividad en grafos"),
    ("problemTagGraphRepresentation",      "Representación de grafos"),
    ("problemTagGreedyAlgorithms",         "Algoritmos greedy"),
    ("problemTagHashing",                  "Hashing"),
    ("problemTagHeaps",                    "Heaps / colas de prioridad"),
    ("problemTagImplementation",           "Implementación"),
    ("problemTagIncrementalSearch",        "Búsqueda incremental"),
    ("problemTagInputAndOutput",           "Entrada y salida"),
    ("problemTagLinearSearch",             "Búsqueda lineal"),
    ("problemTagLinkedLists",              "Listas enlazadas"),
    ("problemTagLoops",                    "Ciclos"),
    ("problemTagMatrices",                 "Matrices"),
    ("problemTagMaxFlow",                  "Flujo máximo"),
    ("problemTagMeetInTheMiddle",          "Meet in the middle"),
    ("problemTagMemorization",             "Memorización"),
    ("problemTagMinimumSpanningTrees",     "Árbol de expansión mínima"),
    ("problemTagModularArithmetic",        "Aritmética modular"),
    ("problemTagMonotoneStack",            "Pila monótona"),
    ("problemTagNumberTheory",             "Teoría de números"),
    ("problemTagNumericalSeries",          "Series numéricas"),
    ("problemTagPartialSums",              "Sumas de prefijo"),
    ("problemTagPermutations",             "Permutaciones"),
    ("problemTagPrimalityTest",            "Prueba de primalidad"),
    ("problemTagPrimeFactorization",       "Factorización de primos"),
    ("problemTagPrimeGeneration",          "Generación de primos (criba)"),
    ("problemTagQueues",                   "Colas"),
    ("problemTagRecursion",                "Recursión"),
    ("problemTagSQRTDecomposition",        "Descomposición en raíz cuadrada"),
    ("problemTagShortestPaths",            "Caminos más cortos"),
    ("problemTagSimulation",               "Simulación"),
    ("problemTagSlidingWindow",            "Ventana deslizante"),
    ("problemTagSorting",                  "Ordenamiento"),
    ("problemTagStacks",                   "Pilas"),
    ("problemTagStringMatching",           "Búsqueda de patrones en cadenas"),
    ("problemTagSubArraySearch",           "Búsqueda de subarreglos"),
    ("problemTagTrees",                    "Árboles"),
    ("problemTagTwoPointersTechnique",     "Técnica de dos punteros"),
    ("problemTagUnformattedInputAndOutput","Entrada/salida sin formato"),
    # ── problemTopic ─────────────────────────────────────────────────────────
    ("problemTopicArrays",                 "Arreglos [topic]"),
    ("problemTopicBacktracking",           "Backtracking [topic]"),
    ("problemTopicBinarySearch",           "Búsqueda binaria [topic]"),
    ("problemTopicBreadthDepthFirstSearch","BFS / DFS [topic]"),
    ("problemTopicBruteForce",             "Fuerza bruta [topic]"),
    ("problemTopicCombinatorics",          "Combinatoria [topic]"),
    ("problemTopicDataStructures",         "Estructuras de datos [topic]"),
    ("problemTopicDisjointSets",           "Conjuntos disjuntos [topic]"),
    ("problemTopicDivideAndConquer",       "Divide y vencerás [topic]"),
    ("problemTopicDynamicProgramming",     "Programación dinámica [topic]"),
    ("problemTopicGameTheory",             "Teoría de juegos [topic]"),
    ("problemTopicGeometry",               "Geometría [topic]"),
    ("problemTopicGraphTheory",            "Teoría de grafos [topic]"),
    ("problemTopicGreedy",                 "Greedy [topic]"),
    ("problemTopicHashing",                "Hashing [topic]"),
    ("problemTopicIfElseSwitch",           "Condicionales [topic]"),
    ("problemTopicImplementation",         "Implementación [topic]"),
    ("problemTopicInputOutput",            "Entrada y salida [topic]"),
    ("problemTopicLoops",                  "Ciclos [topic]"),
    ("problemTopicMath",                   "Matemáticas [topic]"),
    ("problemTopicMatrices",               "Matrices [topic]"),
    ("problemTopicMaxFlow",                "Flujo máximo [topic]"),
    ("problemTopicNumberTheory",           "Teoría de números [topic]"),
    ("problemTopicShortestPath",           "Caminos más cortos [topic]"),
    ("problemTopicSimulation",             "Simulación [topic]"),
    ("problemTopicSorting",                "Ordenamiento [topic]"),
    ("problemTopicStackQueue",             "Pilas y colas [topic]"),
    ("problemTopicStrings",                "Cadenas [topic]"),
    ("problemTopicTrees",                  "Árboles [topic]"),
    ("problemTopicTwoPointers",            "Dos punteros [topic]"),
]

# Map display label → tag name (used after autocomplete selection)
_LABEL_TO_TAG = {}

# Autocomplete choices: "Descripción  [tagName]"
TAG_CHOICES = []

for _tag, _desc in TAGS:
    _label = f"{_desc}  [{_tag}]"
    TAG_CHOICES.append(_label)
    _LABEL_TO_TAG[_label] = _tag

DEFAULT_TAG_LABEL = next(
    label for label, tag in _LABEL_TO_TAG.items() if tag == "problemTagBruteForce"
)


def label_to_tag(label: str) -> str:
    """Convert a display label back to its OmegaUp tag name."""
    return _LABEL_TO_TAG[label]
