import argparse
import os
import pathlib
import re
import shutil

import questionary
import yaml

from omegaup_toolkit._tags import TAG_CHOICES, DEFAULT_TAG_LABEL, label_to_tag

_TEMPLATE_DIR = pathlib.Path(__file__).parent.parent / "template"

_LANGUAGES = [
    questionary.Choice("C++17", value="cpp17", checked=True),
    questionary.Choice("C++20", value="cpp20", checked=True),
    questionary.Choice("Java", value="java", checked=False),
    questionary.Choice("Python 3", value="py3", checked=False),
    questionary.Choice("C", value="c", checked=False),
    questionary.Choice("C#", value="cs", checked=False),
    questionary.Choice("Kotlin", value="kt", checked=False),
    questionary.Choice("Ruby", value="rb", checked=False),
    questionary.Choice("Lua", value="lua", checked=False),
    questionary.Choice("Pascal", value="pas", checked=False),
]


def _folder_to_alias(name: str) -> str:
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1-\2', name)
    s = re.sub(r'[\s_]+', '-', s)
    return s.lower()


def _folder_to_title(name: str) -> str:
    s = re.sub(r'([a-z0-9])([A-Z])', r'\1 \2', name)
    s = re.sub(r'[_-]+', ' ', s)
    return s.strip()


def _ask(yes: bool, prompt_fn):
    """Run prompt_fn() unless --yes, in which case return its default."""
    if yes:
        return prompt_fn().skip_if(True, default=None).ask()
    return prompt_fn().ask()


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
            ok = questionary.confirm(f"Create new directory '{p}'?", default=True).ask()
            if not ok:
                raise SystemExit(0)

    shutil.copytree(_TEMPLATE_DIR, path)
    if not args.validator:
        os.remove(path / 'validator.cpp')

    folder_name = path.name
    default_alias = _folder_to_alias(folder_name)
    default_title = _folder_to_title(folder_name)
    default_validator = 'custom' if args.validator else 'token'

    print(f"\nConfigurando problem.yaml para: {path}\n")

    if args.yes:
        alias      = default_alias
        title      = default_title
        time_limit = 1000
        memory_mb  = 256
        visibility = 'private'
        prob_type  = 'normal'
        validator  = default_validator
        languages  = ['cpp17', 'cpp20']
    else:
        alias = questionary.text(
            "Alias:", default=default_alias
        ).ask()

        title = questionary.text(
            "Título:", default=default_title
        ).ask()

        time_limit = int(questionary.text(
            "Time limit (ms):", default="1000",
            validate=lambda v: v.isdigit() or "Debe ser un número entero"
        ).ask())

        memory_mb = int(questionary.text(
            "Memory limit (MB):", default="256",
            validate=lambda v: v.isdigit() or "Debe ser un número entero"
        ).ask())

        visibility = questionary.select(
            "Visibilidad:",
            choices=["private", "public"],
            default="private"
        ).ask()

        prob_type = questionary.select(
            "Tipo de problema:",
            choices=[
                questionary.Choice("Normal (con envíos de código)", value="normal"),
                questionary.Choice("Lectura (sin envíos)", value="lectura"),
            ],
            default="normal"
        ).ask()

        validator = questionary.select(
            "Validador:",
            choices=[
                questionary.Choice("token          — compara token por token (default)", value="token"),
                questionary.Choice("token-caseless — igual pero ignora mayúsculas", value="token-caseless"),
                questionary.Choice("literal        — comparación byte a byte exacta", value="literal"),
                questionary.Choice("custom         — usa validator.cpp del problema", value="custom"),
            ],
            default=default_validator
        ).ask()

        if prob_type == 'normal':
            languages = questionary.checkbox(
                "Lenguajes permitidos (espacio para marcar, enter para confirmar):",
                choices=_LANGUAGES
            ).ask() or ['cpp17', 'cpp20']
        else:
            languages = []

        tag_label = questionary.autocomplete(
            "Tag pública (escribe para buscar):",
            choices=TAG_CHOICES,
            default=DEFAULT_TAG_LABEL,
            validate=lambda v: v in TAG_CHOICES or "Selecciona una opción de la lista",
        ).ask()
        selected_tag = label_to_tag(tag_label) if tag_label else "problemTagBruteForce"

    if args.yes:
        selected_tag = "problemTagBruteForce"

    tags = [{'name': selected_tag, 'public': True}]

    metadata = {
        'alias': alias,
        'title': title,
        'source': '',
        'time_limit': time_limit,
        'memory_limit': memory_mb,
        'visibility': visibility,
        'type': prob_type,
        'validator': validator,
        'languages': ','.join(languages) if languages else '',
        'tags': tags,
    }

    with open(path / 'problem.yaml', 'w') as f:
        yaml.dump(metadata, f, allow_unicode=True, default_flow_style=False, sort_keys=False)

    print(f"\n✓ Problema creado en {path}")
