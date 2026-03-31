# Official OmegaUp tags — source of truth for the interactive tag selectors in `omegaup create`.
# Keep in sync with tags-reference.md.

# ── problemTag* ──────────────────────────────────────────────────────────────
# List of (tag_name, description) tuples — only problemTag*, no problemTopic*.

PROBLEM_TAGS = [
    ("problemTagArithmetic",               "Arithmetic"),
    ("problemTagArrays",                   "Arrays"),
    ("problemTagBacktracking",             "Backtracking"),
    ("problemTagBigNumbers",               "Big Numbers"),
    ("problemTagBinarySearch",             "Binary Search"),
    ("problemTagBinarySearchTree",         "Binary Search Tree"),
    ("problemTagBipartiteMatching",        "Bipartite Matching"),
    ("problemTagBitManipulation",          "Bit Manipulation"),
    ("problemTagBooleanAlgebra",           "Boolean Algebra"),
    ("problemTagBreadthFirstSearch",       "Breadth-First Search (BFS)"),
    ("problemTagBruteForce",               "Brute Force"),
    ("problemTagCharsAndStrings",          "Characters and Strings"),
    ("problemTagChineseRemainderTheorem",  "Chinese Remainder Theorem"),
    ("problemTagCombinations",             "Combinations"),
    ("problemTagConditionals",             "Conditionals"),
    ("problemTagConvexHull",               "Convex Hull"),
    ("problemTagCountingProblems",         "Counting Problems"),
    ("problemTagDepthFirstSearch",         "Depth-First Search (DFS)"),
    ("problemTagDiophantineEquations",     "Diophantine Equations"),
    ("problemTagDirectedGraphs",           "Directed Graphs"),
    ("problemTagDisjointSets",             "Disjoint Sets (Union-Find)"),
    ("problemTagDivideAndConquer",         "Divide and Conquer"),
    ("problemTagDivisibilityRules",        "Divisibility Rules"),
    ("problemTagDynamicProgramming",       "Dynamic Programming"),
    ("problemTagExponentialSearch",        "Exponential Search"),
    ("problemTagExponentiationBySquaring", "Exponentiation by Squaring"),
    ("problemTagFenwickTrees",             "Fenwick Trees (BIT)"),
    ("problemTagFormattedInputAndOutput",  "Formatted Input and Output"),
    ("problemTagFunctions",                "Functions"),
    ("problemTagGCDAndLCM",                "GCD and LCM"),
    ("problemTagGameTheory",               "Game Theory"),
    ("problemTagGraphConnectivity",        "Graph Connectivity"),
    ("problemTagGraphRepresentation",      "Graph Representation"),
    ("problemTagGreedyAlgorithms",         "Greedy Algorithms"),
    ("problemTagHashing",                  "Hashing"),
    ("problemTagHeaps",                    "Heaps / Priority Queues"),
    ("problemTagImplementation",           "Implementation"),
    ("problemTagIncrementalSearch",        "Incremental Search"),
    ("problemTagInputAndOutput",           "Input and Output"),
    ("problemTagLinearSearch",             "Linear Search"),
    ("problemTagLinkedLists",              "Linked Lists"),
    ("problemTagLoops",                    "Loops"),
    ("problemTagMatrices",                 "Matrices"),
    ("problemTagMaxFlow",                  "Max Flow"),
    ("problemTagMeetInTheMiddle",          "Meet in the Middle"),
    ("problemTagMemorization",             "Memorization"),
    ("problemTagMinimumSpanningTrees",     "Minimum Spanning Trees"),
    ("problemTagModularArithmetic",        "Modular Arithmetic"),
    ("problemTagMonotoneStack",            "Monotone Stack"),
    ("problemTagNumberTheory",             "Number Theory"),
    ("problemTagNumericalSeries",          "Numerical Series"),
    ("problemTagPartialSums",              "Partial Sums (Prefix Sums)"),
    ("problemTagPermutations",             "Permutations"),
    ("problemTagPrimalityTest",            "Primality Test"),
    ("problemTagPrimeFactorization",       "Prime Factorization"),
    ("problemTagPrimeGeneration",          "Prime Generation (Sieve)"),
    ("problemTagQueues",                   "Queues"),
    ("problemTagRecursion",                "Recursion"),
    ("problemTagSQRTDecomposition",        "SQRT Decomposition"),
    ("problemTagShortestPaths",            "Shortest Paths"),
    ("problemTagSimulation",               "Simulation"),
    ("problemTagSlidingWindow",            "Sliding Window"),
    ("problemTagSorting",                  "Sorting"),
    ("problemTagStacks",                   "Stacks"),
    ("problemTagStringMatching",           "String Matching"),
    ("problemTagSubArraySearch",           "Subarray Search"),
    ("problemTagTrees",                    "Trees"),
    ("problemTagTwoPointersTechnique",     "Two Pointers Technique"),
    ("problemTagUnformattedInputAndOutput","Unformatted Input and Output"),
]

# ── problemLevel* ─────────────────────────────────────────────────────────────

LEVEL_TAGS = [
    ("problemLevelBasicIntroductionToProgramming",          "Introduction to Programming"),
    ("problemLevelBasicKarel",                              "Basic Karel"),
    ("problemLevelIntermediateAnalysisAndDesignOfAlgorithms","Analysis and Design of Algorithms"),
    ("problemLevelIntermediateDataStructuresAndAlgorithms", "Data Structures and Algorithms"),
    ("problemLevelIntermediateMathsInProgramming",          "Maths in Programming"),
    ("problemLevelAdvancedCompetitiveProgramming",          "Advanced Competitive Programming"),
    ("problemLevelAdvancedSpecializedTopics",               "Advanced Specialized Topics"),
]

# ── Derived structures ────────────────────────────────────────────────────────

# problemTag autocomplete: "Description  [tagName]"
_TAG_LABEL_TO_NAME = {}
TAG_CHOICES = []
for _name, _desc in PROBLEM_TAGS:
    _label = f"{_desc}  [{_name}]"
    TAG_CHOICES.append(_label)
    _TAG_LABEL_TO_NAME[_label] = _name

# problemLevel select: questionary.Choice objects
import questionary as _q
LEVEL_CHOICES = [
    _q.Choice(title=desc, value=name)
    for name, desc in LEVEL_TAGS
]
DEFAULT_LEVEL = "problemLevelBasicIntroductionToProgramming"

DEFAULT_TAG = "problemTagBruteForce"


def label_to_tag(label: str) -> str:
    """Convert a display label back to its OmegaUp problemTag name."""
    return _TAG_LABEL_TO_NAME[label]
