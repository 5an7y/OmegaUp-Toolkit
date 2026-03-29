# CLAUDE.md — AI Knowledge Guide

This file is automatically read by Claude Code at the start of each conversation. It contains everything needed to use this toolkit effectively: conventions, workflows, design decisions, and examples. **Keep it alive:** update it whenever you learn something new relevant to creating or improving problems.

---

## Project Overview

**OmegaUp-Toolkit** is a Python package and CLI for creating competitive programming problems for the [OmegaUp](https://omegaup.com) judge platform. It provides:

- A CLI (`omegaup`) to scaffold problems, generate test cases, test solutions, and publish to OmegaUp
- C++ libraries for writing case generators (`Libs/`)
- A base problem template (`template/`)

Install once with `pip install -e .` and the `omegaup` command is available system-wide.

---

## Repository Structure

```
OmegaUp-Toolkit/
├── omegaup_toolkit/       # Python package (all CLI logic lives here)
│   ├── cli.py             # Entry point — routes subcommands
│   ├── create.py          # omegaup create
│   ├── generate.py        # omegaup generate-cases
│   ├── test.py            # omegaup test
│   ├── login.py           # omegaup login / logout
│   └── auth.py            # Token storage and API client helpers
├── Libs/                  # C++ headers for case generators
│   ├── Generator.hpp      # File I/O (case_in, case_out, arguments)
│   ├── Random.hpp         # Random generation utilities
│   ├── Background.hpp     # Segment tree (internal dependency of Random.hpp)
│   └── Constants.hpp      # String charset constants
├── template/              # Base template copied by omegaup create
├── Examples/
│   ├── SimpleSum/         # Worked example problem
│   └── InteractiveTemplate/  # Reference for interactive problems
└── pyproject.toml         # Package definition (entry point: omegaup)
```

---

## CLI Commands

```bash
omegaup login                                        # Save OmegaUp API token
omegaup logout                                       # Remove saved credentials
omegaup create         <path> [--yes] [--validator] [--testplan]
omegaup generate-cases <path> [--use_solution] [--stack N]
omegaup test           <path> [--time_limit N] [--solutions ...] [--cases ...]
```

Credentials are saved to `~/.config/omegaup/credentials.json`.
`auth.get_client()` returns an authenticated `omegaup.api.Client` for use in future commands (e.g. `omegaup publish`).

---

## Problem Structure

```
MyProblem/
├── case_generator.cpp     # Generates test cases
├── cases.arg              # Arguments for each case (one per line)
├── cases/                 # Generated .in and .out files
├── solution/
│   └── solution.cpp       # Reference solution (can have multiple .cpp files)
├── statements/
│   └── es.markdown        # Problem statement in OmegaUp markdown format
├── testplan               # (optional) Groups and weights for scoring
└── validator.cpp          # (optional) Custom output validator
```

---

## Statement Format: `statements/es.markdown`

OmegaUp uses a special Markdown format. Math formulas go between `$...$` (LaTeX inline).

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

**Rules:** `||input`, `||output`, `||description`, `||end` are OmegaUp markers. Always end with `||end`. `||description` is optional per example.

---

## `cases.arg` Format

Each line: first token is the **case name**, the rest are **arguments** the generator reads.

```
small_1 1 100
small_2 1 100
large_1 1 1000000000
edge_1  0 0
```

**Group convention for testplan:** cases are grouped by prefix before the first dot:
```
group1.c1 100
group1.c2 500
group2.c1 1000
```

---

## `testplan` Format

```
small_1 0
small_2 0
large_1 50
large_2 50
```

Weight `0` = tested but no points. All cases in a group must be AC to earn the group's points. Generate a skeleton with `omegaup create <path> --testplan`.

---

## `Generator.hpp`

| Stream | Usage |
|--------|-------|
| `Generator::case_in` | Writes the `.in` file |
| `Generator::case_out` | Writes the `.out` file |
| `Generator::arguments` | Reads extra arguments from `cases.arg` |

Always call `Generator::init_generator(argc, argv)` first.

```cpp
#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv);

    int N, maxVal;
    Generator::arguments >> N >> maxVal;

    Generator::case_in << N << '\n';
    for (int i = 0; i < N; i++)
        Generator::case_in << Random::rnd(1, maxVal) << " \n"[i == N-1];

    // If output is simple enough, write it directly:
    // Generator::case_out << answer;
    // Otherwise use --use_solution in generate-cases

    return 0;
}
```

---

## `Random.hpp`

All functions in the `Random::` namespace. Uses a single global `mt19937` RNG.

```cpp
// Numbers
Random::rnd(a, b)                        // single integer in [a, b]
Random::rnd(a, b, sz)                    // vector of sz integers in [a, b]
Random::rnd_unique(a, b, sz)             // vector of sz UNIQUE integers in [a, b]
Random::rnd_pair(a, b)                   // ordered pair (a1 <= a2) in [a, b]
Random::rnd_pair(a, b, sz)               // vector of ordered pairs
Random::rnd_nums_that_sum(sum, sz)       // sz positive integers summing to sum
Random::rnd_nums_that_sum(sum, sz, true) // allow zeros

// Strings & permutations
Random::rnd_string(len)                  // random lowercase string of length len
Random::rnd_string(len, charset)         // custom charset (e.g. "abc" or Constants::uppercaseEnglishAlphabet)
Random::rnd_permutation(n)               // random permutation of [0, n)
Random::rnd_permutation(n, base)         // random permutation of [base, base+n)

// Graphs
Random::rnd_tree(N)                      // random tree: N-1 edges as pairs
Random::rnd_forest(N, trees)             // random forest: N nodes, trees trees (N >= trees)
```

Available charsets: `Constants::lowercaseEnglishAlphabet`, `Constants::uppercaseEnglishAlphabet`, `Constants::specialCharacters`, `Constants::spaces`.

---

## Workflow for Creating a New Problem

1. **Create the structure:**
   ```bash
   omegaup create path/to/MyProblem
   ```

2. **Write the statement** in `statements/es.markdown`.

3. **Design test cases** in `cases.arg`.

4. **Implement the generator** in `case_generator.cpp`.

5. **Implement the reference solution** in `solution/solution.cpp`.

6. **Generate cases:**
   ```bash
   omegaup generate-cases path/to/MyProblem --use_solution
   ```

7. **Verify:**
   ```bash
   omegaup test path/to/MyProblem
   ```

8. **(Optional) Create testplan:**
   ```bash
   omegaup create path/to/MyProblem --testplan
   # Edit testplan to assign weights
   ```

---

## Local Configuration

Create `local_config.json` at the toolkit root to override compiler settings (gitignored):

```json
{
    "cpp_compiler": "/path/to/g++",
    "cpp_flags": "-std=c++20 -O2"
}
```

---

## Keeping This File Updated

Update this file when:
- New CLI commands are added
- New `Random.hpp` functions are added
- A new convention or pattern is established
- A common mistake and its fix are identified
