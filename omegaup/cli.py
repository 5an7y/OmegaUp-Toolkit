import sys
import subprocess
import pathlib

_TOOLKIT = pathlib.Path(__file__).parent.parent

_COMMANDS = {
    "create":   _TOOLKIT / "CreateProblem.py",
    "generate": _TOOLKIT / "GenerateCases.py",
    "test":     _TOOLKIT / "TestCases.py",
}

_HELP = """\
OmegaUp Toolkit — command-line interface

Usage:
  omegaup create   <path> [--yes] [--validator] [--testplan]
  omegaup generate <path> [--use_solution] [--stack N]
  omegaup test     <path> [--time_limit N] [--solutions ...] [--cases ...]

Commands:
  create    Scaffold a new problem from the template
  generate  Compile and run the case generator
  test      Test solutions against generated cases

Run 'omegaup <command> --help' for details on each command.
"""

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(_HELP)
        sys.exit(0)

    cmd = sys.argv[1]
    if cmd not in _COMMANDS:
        print(f"Unknown command: '{cmd}'")
        print(f"Available commands: {', '.join(_COMMANDS)}")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(_COMMANDS[cmd])] + sys.argv[2:]
    )
    sys.exit(result.returncode)
