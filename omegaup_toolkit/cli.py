import sys
import subprocess
import pathlib

_TOOLKIT = pathlib.Path(__file__).parent.parent

_SCRIPT_COMMANDS = {
    "create":         _TOOLKIT / "CreateProblem.py",
    "generate-cases": _TOOLKIT / "GenerateCases.py",
    "test":           _TOOLKIT / "TestCases.py",
}

_HELP = """\
OmegaUp Toolkit — command-line interface

Usage:
  omegaup login                                        Authenticate with OmegaUp
  omegaup logout                                       Remove saved credentials
  omegaup create         <path> [--yes] [--validator] [--testplan]
  omegaup generate-cases <path> [--use_solution] [--stack N]
  omegaup test           <path> [--time_limit N] [--solutions ...] [--cases ...]

Commands:
  login           Save your OmegaUp API token
  logout          Remove saved credentials
  create          Scaffold a new problem from the template
  generate-cases  Compile and run the case generator
  test            Test solutions against generated cases

Run 'omegaup <command> --help' for details on each command.
"""

def main():
    if len(sys.argv) < 2 or sys.argv[1] in ("-h", "--help"):
        print(_HELP)
        sys.exit(0)

    cmd = sys.argv[1]

    if cmd == "login":
        from omegaup_toolkit.login import run_login
        run_login()
        return

    if cmd == "logout":
        from omegaup_toolkit.login import run_logout
        run_logout()
        return

    if cmd not in _SCRIPT_COMMANDS:
        print(f"Unknown command: '{cmd}'")
        print(f"Available commands: login, logout, {', '.join(_SCRIPT_COMMANDS)}")
        sys.exit(1)

    result = subprocess.run(
        [sys.executable, str(_SCRIPT_COMMANDS[cmd])] + sys.argv[2:]
    )
    sys.exit(result.returncode)
