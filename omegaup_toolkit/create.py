import argparse
import os
import pathlib
import shutil

_TEMPLATE_DIR = pathlib.Path(__file__).parent.parent / "template"


def run(argv=None):
    parser = argparse.ArgumentParser(description="Scaffold a new problem from the template")
    parser.add_argument('path', type=pathlib.Path, help='Directory where the problem will be created')
    parser.add_argument('--validator', action='store_true', help='Include a validator.cpp template')
    parser.add_argument('--testplan', action='store_true', help='Create/update testplan from cases.arg')
    parser.add_argument('-y', '--yes', action='store_true', help='Automatically confirm new directory creation')
    args = parser.parse_args(argv)

    path = args.path

    if args.testplan:
        args_path = path / "cases.arg"
        testplan_path = path / "testplan"
        with open(args_path, "r") as f, open(testplan_path, "w") as out:
            for line in f:
                if line.strip():
                    out.write(line.split()[0] + " 0\n")
        return

    if os.path.isdir(path):
        print(f"Error: directory already exists: {path}")
        raise SystemExit(1)

    p = pathlib.PurePath()
    for x in path.parts[:-1]:
        p = p / x
        if not os.path.isdir(p):
            if args.yes:
                continue
            val = input(f"You are creating a new directory '{p}', are you sure? (Y/N) ")
            if val not in ["Y", "N"]:
                print("Invalid option. Please enter Y or N.")
                raise SystemExit(1)
            if val == "N":
                raise SystemExit(0)

    shutil.copytree(_TEMPLATE_DIR, path)
    if not args.validator:
        os.remove(path / 'validator.cpp')

    print(f"Problem {path} created successfully!")
