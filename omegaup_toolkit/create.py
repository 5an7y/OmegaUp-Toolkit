import argparse
import os
import pathlib
import re
import shutil

import yaml

_TEMPLATE_DIR = pathlib.Path(__file__).parent.parent / "template"


def _folder_to_alias(name: str) -> str:
    """Convert a folder name to a kebab-case alias. E.g. 'MiProblema' → 'mi-problema'."""
    # Insert hyphen before uppercase letters that follow lowercase letters or digits
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    # Replace spaces and underscores with hyphens
    s = re.sub(r'[\s_]+', '-', s)
    return s.lower()


def _folder_to_title(name: str) -> str:
    """Convert a folder name to a human-readable title. E.g. 'MiProblema' → 'Mi Problema'."""
    # Insert space before uppercase letters that follow lowercase letters or digits
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    # Replace underscores and hyphens with spaces
    s = re.sub(r'[_-]+', ' ', s)
    return s.strip()


def _prompt(label: str, default: str, yes: bool) -> str:
    """Prompt the user for a value, showing the default. Returns default if --yes."""
    if yes:
        return default
    val = input(f"  {label:<18} [{default}]: ").strip()
    return val if val else default


def run(argv=None):
    parser = argparse.ArgumentParser(description="Scaffold a new problem from the template")
    parser.add_argument('path', type=pathlib.Path, help='Directory where the problem will be created')
    parser.add_argument('--validator', action='store_true', help='Include a validator.cpp template')
    parser.add_argument('--testplan', action='store_true', help='Create/update testplan from cases.arg')
    parser.add_argument('-y', '--yes', action='store_true', help='Accept all defaults without prompting')
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

    # Interactive problem.yaml setup
    folder_name = path.name
    default_alias = _folder_to_alias(folder_name)
    default_title = _folder_to_title(folder_name)

    print(f"\nConfigurando problem.yaml para: {path}")
    alias       = _prompt("Alias",       default_alias,  args.yes)
    title       = _prompt("Título",      default_title,  args.yes)
    time_limit  = _prompt("Time limit ms", "1000",       args.yes)
    memory_mb   = _prompt("Memory MB",   "256",          args.yes)
    visibility  = _prompt("Visibilidad", "private",      args.yes)
    languages   = _prompt("Languages",   "cpp17,cpp20",  args.yes)

    metadata = {
        'alias': alias,
        'title': title,
        'source': '',
        'time_limit': int(time_limit),
        'memory_limit': int(memory_mb),
        'visibility': visibility,
        'languages': languages,
    }

    with open(path / 'problem.yaml', 'w') as f:
        yaml.dump(metadata, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\n✓ Problema creado en {path}")
