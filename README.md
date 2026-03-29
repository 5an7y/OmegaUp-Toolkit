# OmegaUp Toolkit

A toolkit for creating and testing competitive programming problems for the [OmegaUp](https://omegaup.com) judge platform.

## Requirements

- Python 3.6+
- g++ with C++20 support

```shell
python3 --version
g++ --version
```

Works on Windows, macOS, and Linux.

---

## Installation

Clone the repository and install it as a local package:

```bash
git clone https://github.com/5an7y/OmegaUp-Toolkit.git
cd OmegaUp-Toolkit
pip install -e .
```

This makes the `omegaup` command available system-wide. You only need to do this once.

---

## Quick Start

```bash
# 1. Scaffold a new problem
omegaup create path/to/MyProblem

# 2. Implement case_generator.cpp and solution/solution.cpp

# 3. Generate test cases (using the solution to produce .out files)
omegaup generate-cases path/to/MyProblem --use_solution

# 4. Test all solutions
omegaup test path/to/MyProblem
```

See `Examples/SimpleSum/` for a complete working example.

---

## Using with AI

You can use any AI assistant (Claude, ChatGPT, etc.) to create problems with this toolkit. Give it this prompt:

```
Read the CLAUDE.md file in the OmegaUp-Toolkit repository to understand
how the toolkit works. Then create a problem about: [DESCRIBE YOUR PROBLEM HERE]
```

If the AI doesn't have access to the repo, point it to the README instead:

```
Read the README at github.com/5an7y/OmegaUp-Toolkit and then create a
problem about: [DESCRIBE YOUR PROBLEM HERE]
```

The AI will generate the statement, `case_generator.cpp`, `solution.cpp`, and `cases.arg` ready to use.

---

## Problem Structure

```
MyProblem/
├── case_generator.cpp      # generates test cases
├── cases.arg               # arguments for each case (one per line)
├── cases/                  # generated .in and .out files
├── solution/
│   ├── solution.cpp        # reference (correct) solution
│   └── brute.cpp           # optional: other solutions to compare
├── statements/
│   └── es.markdown         # problem statement (OmegaUp format)
└── testplan                # optional: case weights for scoring
```

---

## omegaup create

Scaffolds a new problem from the template.

```bash
omegaup create <path> [flags]
```

**Examples:**

```bash
# Create a problem (prompts before creating new parent directories)
omegaup create Phase1/Arrays/MaxSubarray

# Skip confirmation prompts
omegaup create Phase1/Arrays/MaxSubarray --yes

# Include a custom validator
omegaup create Phase1/Arrays/MaxSubarray --validator

# Regenerate testplan from cases.arg
omegaup create Phase1/Arrays/MaxSubarray --testplan
```

| Flag | Description |
|------|-------------|
| `--yes` / `-y` | Automatically confirm new parent directory creation |
| `--validator` | Include a `validator.cpp` template |
| `--testplan` | Create/update `testplan` based on `cases.arg` |

---

## cases.arg

Each line defines one test case. The first token is the case name; remaining tokens are arguments passed to your generator.

```
small_1 1 100
small_2 1 100
large_1 1 1000000000
edge_1  0 0
edge_2  1000000000 1000000000
```

Cases are grouped by the prefix before the first `.` for scoring purposes (see [testplan](#testplan)).

---

## case_generator.cpp

```cpp
#include <iostream>
#include "Generator.hpp"
#include "Random.hpp"

int main(int argc, char *argv[]) {
    Generator::init_generator(argc, argv); // always first

    // Read your custom arguments from cases.arg
    int N, maxVal;
    Generator::arguments >> N >> maxVal;

    // Write the input file
    Generator::case_in << N << "\n";
    for (int i = 0; i < N; i++)
        Generator::case_in << Random::rnd(1, maxVal) << " \n"[i == N-1];

    // (Optional) Write the expected output directly
    // Generator::case_out << answer;

    return 0;
}
```

`Generator::case_in` and `Generator::case_out` are `std::ofstream` objects — write to them exactly as you'd write to `std::cout`.

---

## Random.hpp Reference

All functions live in the `Random::` namespace.

### Numbers

```cpp
int x    = Random::rnd(1, 100);           // single integer in [a, b]
auto v   = Random::rnd(1, 100, N);        // vector of N integers in [a, b]
auto u   = Random::rnd_unique(1, 100, N); // N unique integers in [a, b]
auto p   = Random::rnd_pair(1, 100);      // pair (a, b) with a <= b
auto pv  = Random::rnd_pair(1, 100, N);   // vector of N such pairs
auto ns  = Random::rnd_nums_that_sum(100, 5);  // 5 positives summing to 100
```

### Strings and permutations

```cpp
auto s   = Random::rnd_string(10);           // 10 random lowercase letters
auto s2  = Random::rnd_string(5, "abc");     // custom charset
auto pm  = Random::rnd_permutation(5);       // permutation of [0, 5)
auto pm2 = Random::rnd_permutation(5, 1);    // permutation of [1, 6)
```

Available charsets in `Constants::`:
- `Constants::lowercaseEnglishAlphabet` — `"abc...z"`
- `Constants::uppercaseEnglishAlphabet` — `"ABC...Z"`
- `Constants::specialCharacters`
- `Constants::spaces`

### Graphs

```cpp
auto edges  = Random::rnd_tree(N);       // random tree: N-1 edges
auto forest = Random::rnd_forest(N, K);  // random forest: N nodes, K trees (N >= K)
```

---

## omegaup generate-cases

Compiles `case_generator.cpp` and runs it for every case in `cases.arg`.

```bash
omegaup generate-cases <path> [flags]
```

```bash
# Generate .in files only
omegaup generate-cases path/to/MyProblem

# Generate .in and .out files by running the solution
omegaup generate-cases path/to/MyProblem --use_solution
```

| Flag | Description |
|------|-------------|
| `--use_solution` | Run `solution/solution.cpp` on each `.in` to produce `.out` files |
| `--stack N` | Stack size in bytes — Windows only (default: 16 MB) |

---

## omegaup test

Compiles and runs all `.cpp` files in `solution/` against the generated cases.

```bash
omegaup test <path> [flags]
```

```bash
omegaup test path/to/MyProblem
omegaup test path/to/MyProblem --time_limit 2000
omegaup test path/to/MyProblem --solutions solution.cpp brute.cpp
omegaup test path/to/MyProblem --cases small_1 small_2 edge_1
omegaup test path/to/MyProblem --validator
```

| Flag | Description |
|------|-------------|
| `--time_limit N` | Time limit in ms (default: 5000) |
| `--solutions` | Specific `.cpp` files to test (default: all) |
| `--cases` | Specific cases to test (default: all) |
| `--validator` | Use `validator.cpp` for custom output checking |

**Verdicts:** `AC` · `WA` · `TLE` · `RTE` · `PA` (partial, validator only)

---

## testplan

Optional file for grouping cases and assigning point weights. If absent, each case is worth 1 point.

```
small_1 0
small_2 0
small_3 0
large_1 50
large_2 50
```

Cases sharing the same prefix (e.g. `large_1`, `large_2`) form a group. A group only scores if **all** its cases pass. Weight `0` means the case is tested but worth no points.

---

## validator.cpp

For problems where the output isn't unique, write a custom validator. It receives the contestant's output via stdin and writes a score between `0.0` and `1.0` to stdout.

Enable it with `--validator` in `omegaup create` and `omegaup test`.

---

## Local Configuration

Create `local_config.json` in the toolkit root to override compiler settings:

```json
{
    "cpp_compiler": "/usr/local/bin/g++-14",
    "cpp_flags": "-std=c++20 -O2"
}
```

---

## Calling scripts directly

If you prefer not to install the package, the scripts also work directly — they resolve all paths relative to themselves:

```bash
python3 /path/to/OmegaUp-Toolkit/CreateProblem.py MyProblem
python3 /path/to/OmegaUp-Toolkit/GenerateCases.py MyProblem --use_solution
python3 /path/to/OmegaUp-Toolkit/TestCases.py MyProblem
```
