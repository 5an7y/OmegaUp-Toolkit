import sys

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

    cmd  = sys.argv[1]
    argv = sys.argv[2:]

    if cmd == "login":
        from omegaup_toolkit.login import run_login
        run_login()

    elif cmd == "logout":
        from omegaup_toolkit.login import run_logout
        run_logout()

    elif cmd == "create":
        from omegaup_toolkit.create import run
        run(argv)

    elif cmd == "generate-cases":
        from omegaup_toolkit.generate import run
        run(argv)

    elif cmd == "test":
        from omegaup_toolkit.test import run
        run(argv)

    else:
        print(f"Unknown command: '{cmd}'")
        print("Available commands: login, logout, create, generate-cases, test")
        sys.exit(1)
