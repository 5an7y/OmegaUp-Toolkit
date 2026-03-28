# CLAUDE.md — AI Knowledge Guide

This file is automatically read by Claude Code at the start of each conversation. It contains everything needed to use this toolkit effectively: conventions, workflows, design decisions, and examples. **Keep it alive:** update it whenever you learn something new relevant to creating or improving problems.

---

## Project Overview

**OmegaUp-Toolkit** is a set of tools for creating competitive programming problems compatible with the [OmegaUp](https://omegaup.com) judge platform. It provides:

- Python scripts to scaffold new problems, generate test cases, and test solutions
- C++ libraries for writing case generators (`Libs/`)
- Problem templates (`Examples/`)

This toolkit is platform-agnostic — use it for any contest, training program, or problem set that targets OmegaUp.

---

## Repository Structure

```
OmegaUp-Toolkit/
├── CreateProblem.py       # Creates a new problem from the template
├── GenerateCases.py       # Compiles and runs the case generator
├── TestCases.py           # Compiles and tests solutions against cases
├── Libs/                  # C++ libraries for case generators
│   ├── Generator.hpp      # File I/O for case generator
│   ├── Random.hpp         # Random generation utilities
│   ├── Background.hpp     # Segment tree (internal dependency)
│   └── Constants.hpp      # Constants
└── Examples/
    ├── Template/          # Base template for new problems
    ├── InteractiveTemplate/  # Template for interactive problems
    └── SimpleSum/         # Worked example
```

---

## Problem Structure

Each problem is a folder with this structure:

```
MyProblem/
├── case_generator.cpp     # Generates test cases
├── cases.arg              # Arguments for each case (one per line)
├── cases/                 # Generated .in and .out files
│   ├── c1.in
│   ├── c1.out
│   └── ...
├── solution/
│   └── solution.cpp       # Reference solution (can have multiple .cpp files)
├── statements/
│   └── es.markdown        # Problem statement in OmegaUp's markdown format
├── testplan               # (optional) Groups and weights for scoring
└── validator.cpp          # (optional) Custom output validator
```

---

## Statement Format: `statements/es.markdown`

OmegaUp uses a special Markdown format with predefined sections. Math formulas go between `$...$` (LaTeX inline).

```markdown
# Historia

Optional narrative context (can be omitted).

# Problema

Concise, precise problem description.

# Entrada

Input description.

# Salida

Exact description of what the program must print.

# Ejemplos

||input
2
1 3
||output
4
||description
Optional description of this example.
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

**Important rules:**
- `||input`, `||output`, `||description`, `||end` are OmegaUp special markers.
- `||description` is optional per example.
- Always end the examples section with `||end`.
- Math formulas use LaTeX syntax: `$O(N \log N)$`, `$10^9$`, etc.

---

## `cases.arg` Format

Each line defines one test case. The first token is the **case name**, the rest are **arguments** the generator can read.

```
c1 100
c2 1000
c3 100000
```

The generator receives the case name as `argv[1]` (used by `Generator::init_generator`) and additional arguments in `Generator::arguments`. Case names become the `.in` / `.out` file names.

**Group convention:** If using `testplan`, cases are grouped by the prefix before the first dot:
```
group1.c1 100
group1.c2 500
group2.c1 1000
```
This creates two groups (`group1`, `group2`). Within a group, **all cases must be AC** to earn the group's points.

---

## `testplan` Format

Defines the weight of each case for scoring. If absent, all cases are worth equal points.

```
c1 10
c2 10
c3 20
group1.c1 15
group1.c2 15
group2.c1 30
```

Generate a skeleton with:
```bash
python CreateProblem.py path/to/MyProblem --testplan
```
(Assigns weight 0 to all cases; adjust manually.)

---

## `Generator.hpp` Library

Provides three streams for use in `case_generator.cpp`:

| Stream | Usage |
|--------|-------|
| `Generator::case_in` | Writes the case input (`.in` file) |
| `Generator::case_out` | Writes the expected output (`.out` file) |
| `Generator::arguments` | Reads arguments from `cases.arg` |

**Always call first:** `Generator::init_generator(argc, argv);`

**Complete example:**
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

    // If output is simple, compute it here:
    // Generator::case_out << answer;
    // Otherwise, use --use_solution in GenerateCases.py

    return 0;
}
```

---

## `Random.hpp` Library

All functions are in the `Random` namespace:

```cpp
// Single random number in [a, b] (inclusive)
Random::rnd(a, b)

// Vector of sz random numbers in [a, b]
Random::rnd(a, b, sz)

// Vector of sz UNIQUE random numbers in [a, b]
Random::rnd_unique(a, b, sz)

// Ordered pair (a1 <= a2) with values in [a, b]
Random::rnd_pair(a, b)

// Vector of ordered pairs
Random::rnd_pair(a, b, sz)

// Vector of sz numbers that sum exactly to `sum`
Random::rnd_nums_that_sum(sum, sz)
Random::rnd_nums_that_sum(sum, sz, allow_zero=true)

// Random tree of N nodes, returns edge list
Random::rnd_tree(N)

// Random forest of N nodes and `trees` trees
Random::rnd_forest(N, trees)
```

**Types:** All functions are templates, work with `int`, `long long`, etc.

---

## Python Scripts

### `CreateProblem.py` — Create a new problem

```bash
python CreateProblem.py path/to/MyProblem
python CreateProblem.py path/to/MyProblem --validator   # include validator.cpp
python CreateProblem.py path/to/MyProblem --testplan    # generate testplan from cases.arg
```

Copies the `Examples/Template/` structure to the specified directory.

### `GenerateCases.py` — Generate test cases

```bash
python GenerateCases.py path/to/MyProblem
python GenerateCases.py path/to/MyProblem --use_solution   # generate .out from solution.cpp
python GenerateCases.py path/to/MyProblem --stack 33554432  # larger stack (32MB)
```

- Compiles `case_generator.cpp` with `g++ -std=c++20 -I ./Libs`
- Reads `cases.arg` and runs the generator for each case
- With `--use_solution`: compiles and runs `solution/solution.cpp` on each `.in` to generate `.out`
- **Note:** Default stack is 16MB (`16777216`). For deep recursion use `--stack 33554432`

### `TestCases.py` — Test solutions

```bash
python TestCases.py path/to/MyProblem
python TestCases.py path/to/MyProblem --time_limit 2000         # 2-second limit
python TestCases.py path/to/MyProblem --solutions sol1.cpp      # test only sol1.cpp
python TestCases.py path/to/MyProblem --cases c1 c2 c5          # test only these cases
python TestCases.py path/to/MyProblem --validator               # use validator.cpp
```

Verdicts:
| Verdict | Meaning |
|---------|---------|
| AC | Accepted |
| WA | Wrong Answer |
| TLE | Time Limit Exceeded |
| RTE | Runtime Error |
| PA | Partially Accepted (validator only) |

---

## Workflow for Creating a New Problem

1. **Create the structure:**
   ```bash
   python CreateProblem.py path/to/MyProblem
   ```

2. **Write the statement** in `statements/es.markdown`.

3. **Design test cases** in `cases.arg`: names and parameters.

4. **Implement the generator** in `case_generator.cpp` using `Generator.hpp` and `Random.hpp`.

5. **Implement the reference solution** in `solution/solution.cpp`.

6. **Generate cases:**
   ```bash
   python GenerateCases.py path/to/MyProblem --use_solution
   ```

7. **Verify the solution:**
   ```bash
   python TestCases.py path/to/MyProblem
   ```

8. **(Optional) Create testplan** for group-based scoring:
   ```bash
   python CreateProblem.py path/to/MyProblem --testplan
   # Edit testplan to assign weights
   ```

---

## Local Configuration

Create a `local_config.json` at the toolkit root to override the compiler:

```json
{
    "cpp_compiler": "/path/to/g++",
    "cpp_flags": "-std=c++20 -O2"
}
```

This file is gitignored.

---

## Keeping This File Updated

Update this file when:
- A new pattern for designing cases is discovered
- A new convention is established
- A new tool or library is added
- A common mistake and its fix are identified
