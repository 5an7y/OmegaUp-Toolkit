# OmegaUp-Toolkit

A toolkit for creating competitive programming problems for the [OmegaUp](https://omegaup.com) judge platform.

## Requirements

- Python 3.0+
- g++ with C++20 support

Works on Windows, macOS, and Linux.

```shell
python --version   # or: py --version (Windows)
g++ --version
```

## Quick Start

```bash
# Create a new problem
python CreateProblem.py path/to/MyProblem

# Generate test cases
python GenerateCases.py path/to/MyProblem --use_solution

# Test solutions
python TestCases.py path/to/MyProblem
```

## Structure

```
OmegaUp-Toolkit/
├── CreateProblem.py    # Scaffold a new problem from template
├── GenerateCases.py    # Compile and run the case generator
├── TestCases.py        # Test solutions against cases
├── Libs/               # C++ libraries for case generators
└── Examples/           # Templates and worked examples
```

## Local Configuration

Create `local_config.json` to override the compiler:

```json
{
    "cpp_compiler": "/path/to/g++",
    "cpp_flags": "-std=c++20 -O2"
}
```

See `CLAUDE.md` for full documentation.
