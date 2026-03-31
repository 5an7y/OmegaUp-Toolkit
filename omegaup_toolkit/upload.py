import argparse
import io
import json
import pathlib
import sys
import zipfile

import yaml


_REQUIRED_FIELDS = ['alias', 'title', 'time_limit', 'memory_limit', 'visibility',
                    'type', 'validator', 'languages', 'tags']

_VALID_TYPES = ('normal', 'lectura')
_VALID_VALIDATORS = ('token', 'token-caseless', 'literal', 'custom')


def _load_metadata(problem_path: pathlib.Path) -> dict:
    yaml_path = problem_path / 'problem.yaml'
    if not yaml_path.exists():
        print(
            f"Error: problem.yaml not found in {problem_path}\n"
            "Run 'omegaup create <path>' to generate it."
        )
        sys.exit(1)

    with open(yaml_path) as f:
        data = yaml.safe_load(f)

    if not isinstance(data, dict):
        print("Error: problem.yaml is malformed (expected key-value pairs).")
        sys.exit(1)

    prob_type_early = data.get('type', '')
    for field in _REQUIRED_FIELDS:
        # languages is not required for lectura problems
        if field == 'languages' and prob_type_early == 'lectura':
            continue
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            # tags can be an empty list — handle separately below
            if field != 'tags':
                print(f"Error: '{field}' is missing or empty in problem.yaml")
                sys.exit(1)

    # Validate type
    prob_type = data.get('type', '')
    if prob_type not in _VALID_TYPES:
        print(f"Error: 'type' must be one of {_VALID_TYPES}, got '{prob_type}'")
        sys.exit(1)

    # Validate validator
    validator = data.get('validator', '')
    if validator not in _VALID_VALIDATORS:
        print(f"Error: 'validator' must be one of {_VALID_VALIDATORS}, got '{validator}'")
        sys.exit(1)

    # Validate tags: must be a list with at least one public tag
    tags = data.get('tags') or []
    if not isinstance(tags, list) or len(tags) == 0:
        print("Error: 'tags' must be a non-empty list in problem.yaml")
        print("  Example:\n    tags:\n      - name: dp\n        public: true")
        sys.exit(1)

    public_tags = [t for t in tags if isinstance(t, dict) and t.get('public')]
    if not public_tags:
        print("Error: at least one tag must have 'public: true' in problem.yaml")
        sys.exit(1)

    return data


def _validate_folder(problem_path: pathlib.Path, prob_type: str):
    statement = problem_path / 'statements' / 'es.markdown'
    if not statement.exists():
        print(f"Error: statements/es.markdown not found in {problem_path}")
        sys.exit(1)

    if prob_type == 'lectura':
        return  # no cases required for reading problems

    cases_dir = problem_path / 'cases'
    if not cases_dir.exists():
        print(f"Error: cases/ directory not found in {problem_path}")
        sys.exit(1)

    in_files = set(p.stem for p in cases_dir.glob('*.in'))
    out_files = set(p.stem for p in cases_dir.glob('*.out'))
    if not (in_files & out_files):
        print("Error: No matching .in/.out test cases found in cases/")
        sys.exit(1)

    if not (problem_path / 'testplan').exists():
        print("Warning: testplan not found (all cases will have equal weight)")


def _build_zip(problem_path: pathlib.Path) -> io.BytesIO:
    buf = io.BytesIO()
    cases_dir = problem_path / 'cases'

    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        zf.write(problem_path / 'statements' / 'es.markdown', 'statements/es.markdown')

        if cases_dir.exists():
            for f in sorted(cases_dir.iterdir()):
                if f.is_file() and f.suffix in ('.in', '.out'):
                    zf.write(f, f'cases/{f.name}')

        testplan = problem_path / 'testplan'
        if testplan.exists():
            zf.write(testplan, 'testplan')

        validator = problem_path / 'validator.cpp'
        if validator.exists():
            zf.write(validator, 'validator.cpp')

    buf.seek(0)
    return buf


def _max_output_size(problem_path: pathlib.Path) -> int:
    """Return max .out file size in bytes, or 0 if none found."""
    cases_dir = problem_path / 'cases'
    sizes = [f.stat().st_size for f in cases_dir.glob('*.out') if f.is_file()] if cases_dir.exists() else []
    return max(sizes) if sizes else 0


def _check_exists(client, alias: str) -> bool:
    try:
        client.problem.details(problem_alias=alias)
        return True
    except Exception as e:
        msg = str(e).lower()
        if 'not found' in msg or '404' in msg or 'doesnotexist' in msg:
            return False
        raise


def run(argv=None):
    parser = argparse.ArgumentParser(description="Upload a problem to OmegaUp")
    parser.add_argument('path', type=pathlib.Path, help='Problem directory containing problem.yaml')
    parser.add_argument(
        '--message', default='Update via omegaup-toolkit',
        help='Commit message for OmegaUp version history'
    )
    parser.add_argument('-y', '--yes', action='store_true', help='Skip confirmation prompt')
    parser.add_argument('--dry-run', action='store_true', help='Build ZIP and print contents without uploading')
    args = parser.parse_args(argv)

    problem_path = args.path.resolve()
    if not problem_path.is_dir():
        print(f"Error: path does not exist or is not a directory: {problem_path}")
        sys.exit(1)

    meta = _load_metadata(problem_path)
    _validate_folder(problem_path, meta.get('type', 'normal'))
    zip_buf = _build_zip(problem_path)

    alias         = meta['alias']
    title         = meta['title']
    source        = meta.get('source') or ''
    time_limit    = int(meta['time_limit'])
    memory_limit  = int(meta['memory_limit'])
    visibility    = meta['visibility']
    prob_type     = meta['type']
    validator     = meta['validator']
    tags          = meta['tags']

    # type → languages: 'lectura' means no submissions (empty languages string)
    languages = '' if prob_type == 'lectura' else meta['languages']

    # Auto-calculate output_limit: max .out size + 1000 bytes padding
    output_limit = _max_output_size(problem_path) + 1000

    # Build selected_tags JSON string for the API
    selected_tags = json.dumps([
        {'tagname': t['name'], 'public': bool(t.get('public', False))}
        for t in tags
    ])

    if args.dry_run:
        print("Dry run — ZIP contents:")
        zip_buf.seek(0)
        with zipfile.ZipFile(zip_buf) as zf:
            for name in zf.namelist():
                info = zf.getinfo(name)
                print(f"  {name}  ({info.file_size} bytes)")
        print(f"\nMetadata:")
        print(f"  Alias:          {alias}")
        print(f"  Título:         {title}")
        print(f"  Time limit:     {time_limit} ms")
        print(f"  Memory:         {memory_limit} MB")
        print(f"  Visibilidad:    {visibility}")
        print(f"  Tipo:           {prob_type}")
        print(f"  Validador:      {validator}")
        print(f"  Languages:      {languages!r}")
        print(f"  Output limit:   {output_limit} bytes (auto)")
        print(f"  Tags:           {selected_tags}")
        print("\n(dry-run) No se hizo ninguna llamada a la API.")
        return

    from omegaup_toolkit.auth import get_client
    client = get_client()

    exists = _check_exists(client, alias)
    action = "ACTUALIZAR" if exists else "CREAR"

    zip_buf.seek(0)
    with zipfile.ZipFile(zip_buf) as zf:
        file_list = ', '.join(zf.namelist())
    zip_buf.seek(0)

    print(f"\nProblema a subir:")
    print(f"  Alias:          {alias}")
    print(f"  Título:         {title}")
    print(f"  Time limit:     {time_limit} ms")
    print(f"  Memory:         {memory_limit} MB")
    print(f"  Visibilidad:    {visibility}")
    print(f"  Tipo:           {prob_type}")
    print(f"  Validador:      {validator}")
    print(f"  Output limit:   {output_limit} bytes (auto)")
    print(f"  Tags:           {', '.join(t['name'] for t in tags)}")
    print(f"  Acción:         {action}")
    print(f"  Archivos:       {file_list}")

    if not args.yes:
        answer = input("\n¿Continuar? [s/N]: ").strip().lower()
        if answer not in ('s', 'si', 'sí', 'y', 'yes'):
            print("Cancelado.")
            sys.exit(0)

    try:
        common = dict(
            problem_alias=alias,
            title=title,
            source=source,
            time_limit=time_limit,
            memory_limit=memory_limit,
            output_limit=output_limit,
            visibility=visibility,
            validator=validator,
            languages=languages,
            selected_tags=selected_tags,
            files_={'contents': zip_buf},
        )
        if not exists:
            client.problem.create(**common)
            print(f"\n✓ Creado: https://omegaup.com/arena/problem/{alias}/")
        else:
            client.problem.update(message=args.message, redirect=False, **common)
            print(f"\n✓ Actualizado: https://omegaup.com/arena/problem/{alias}/")
    except Exception as e:
        print(f"\nError al subir el problema: {e}")
        sys.exit(1)
