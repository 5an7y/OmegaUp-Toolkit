import argparse
import io
import pathlib
import sys
import zipfile

import yaml


_REQUIRED_FIELDS = ['alias', 'title', 'time_limit', 'memory_limit', 'visibility', 'languages']


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

    for field in _REQUIRED_FIELDS:
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            print(f"Error: '{field}' is missing or empty in problem.yaml")
            sys.exit(1)

    return data


def _validate_folder(problem_path: pathlib.Path):
    statement = problem_path / 'statements' / 'es.markdown'
    if not statement.exists():
        print(f"Error: statements/es.markdown not found in {problem_path}")
        sys.exit(1)

    cases_dir = problem_path / 'cases'
    if not cases_dir.exists():
        print(f"Error: cases/ directory not found in {problem_path}")
        sys.exit(1)

    in_files = set(p.stem for p in cases_dir.glob('*.in'))
    out_files = set(p.stem for p in cases_dir.glob('*.out'))
    matched = in_files & out_files
    if not matched:
        print(f"Error: No matching .in/.out test cases found in cases/")
        sys.exit(1)

    # Warnings for optional files
    if not (problem_path / 'testplan').exists():
        print("Warning: testplan not found (all cases will have equal weight)")
    if not (problem_path / 'validator.cpp').exists():
        pass  # validator is optional, no warning needed


def _build_zip(problem_path: pathlib.Path) -> io.BytesIO:
    buf = io.BytesIO()
    cases_dir = problem_path / 'cases'

    with zipfile.ZipFile(buf, 'w', compression=zipfile.ZIP_DEFLATED) as zf:
        # Statement
        zf.write(problem_path / 'statements' / 'es.markdown', 'statements/es.markdown')

        # Test cases
        for f in sorted(cases_dir.iterdir()):
            if f.is_file() and f.suffix in ('.in', '.out'):
                zf.write(f, f'cases/{f.name}')

        # Optional files
        testplan = problem_path / 'testplan'
        if testplan.exists():
            zf.write(testplan, 'testplan')

        validator = problem_path / 'validator.cpp'
        if validator.exists():
            zf.write(validator, 'validator.cpp')

    buf.seek(0)
    return buf


def _check_exists(client, alias: str) -> bool:
    try:
        client.problem.details(problem_alias=alias)
        return True
    except Exception as e:
        msg = str(e).lower()
        if 'not found' in msg or '404' in msg or 'doesnotexist' in msg:
            return False
        # Re-raise unexpected errors
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
    _validate_folder(problem_path)
    zip_buf = _build_zip(problem_path)

    alias = meta['alias']
    title = meta['title']
    source = meta.get('source') or ''
    time_limit = int(meta['time_limit'])
    memory_limit = int(meta['memory_limit'])
    visibility = meta['visibility']
    languages = meta['languages']

    if args.dry_run:
        print("Dry run — ZIP contents:")
        zip_buf.seek(0)
        with zipfile.ZipFile(zip_buf) as zf:
            for name in zf.namelist():
                info = zf.getinfo(name)
                print(f"  {name}  ({info.file_size} bytes)")
        print(f"\nMetadata:")
        print(f"  Alias:       {alias}")
        print(f"  Título:      {title}")
        print(f"  Time limit:  {time_limit} ms")
        print(f"  Memory:      {memory_limit} MB")
        print(f"  Visibilidad: {visibility}")
        print(f"  Languages:   {languages}")
        print("\n(dry-run) No se hizo ninguna llamada a la API.")
        return

    from omegaup_toolkit.auth import get_client
    client = get_client()

    # Determine action
    exists = _check_exists(client, alias)
    action = "ACTUALIZAR" if exists else "CREAR"

    # Show confirmation
    zip_buf.seek(0)
    with zipfile.ZipFile(zip_buf) as zf:
        file_list = ', '.join(zf.namelist())
    zip_buf.seek(0)

    print(f"\nProblema a subir:")
    print(f"  Alias:       {alias}")
    print(f"  Título:      {title}")
    print(f"  Time limit:  {time_limit} ms")
    print(f"  Memory:      {memory_limit} MB")
    print(f"  Visibilidad: {visibility}")
    print(f"  Acción:      {action}")
    print(f"  Archivos:    {file_list}")

    if not args.yes:
        answer = input("\n¿Continuar? [s/N]: ").strip().lower()
        if answer not in ('s', 'si', 'sí', 'y', 'yes'):
            print("Cancelado.")
            sys.exit(0)

    try:
        if not exists:
            client.problem.create(
                problem_alias=alias,
                title=title,
                source=source,
                time_limit=time_limit,
                memory_limit=memory_limit,
                visibility=visibility,
                languages=languages,
                files_={'contents': zip_buf},
            )
            print(f"\n✓ Creado: https://omegaup.com/arena/problem/{alias}/")
        else:
            client.problem.update(
                problem_alias=alias,
                message=args.message,
                redirect=False,
                title=title,
                source=source,
                time_limit=time_limit,
                memory_limit=memory_limit,
                visibility=visibility,
                languages=languages,
                files_={'contents': zip_buf},
            )
            print(f"\n✓ Actualizado: https://omegaup.com/arena/problem/{alias}/")
    except Exception as e:
        print(f"\nError al subir el problema: {e}")
        sys.exit(1)
