import argparse
import io
import json
import pathlib
import sys
import zipfile

import yaml


_REQUIRED_FIELDS = ['alias', 'title', 'time_limit', 'memory_limit', 'visibility',
                    'type', 'validator', 'level', 'tags']

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
        # languages only required for normal problems
        if field == 'languages' and prob_type_early == 'lectura':
            continue
        if field not in data or data[field] is None or str(data[field]).strip() == '':
            # tags handled separately below
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
        print("  Example:\n    tags:\n      - name: problemTagBruteForce\n        public: true")
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
        # Empaqueta todo el contenido de statements/ (es.markdown + imagenes
        # u otros recursos que el enunciado pueda referenciar).
        statements_dir = problem_path / 'statements'
        for f in sorted(statements_dir.iterdir()):
            if f.is_file():
                zf.write(f, f'statements/{f.name}')

        if cases_dir.exists():
            for f in sorted(cases_dir.iterdir()):
                if f.is_file() and f.suffix in ('.in', '.out'):
                    zf.write(f, f'cases/{f.name}')
        else:
            # OmegaUp requires at least one case even for lectura problems.
            # Include a minimal dummy case: read one integer, output it.
            zf.writestr('cases/dummy.in', '0\n')
            zf.writestr('cases/dummy.out', '0\n')

        testplan = problem_path / 'testplan'
        if testplan.exists():
            zf.write(testplan, 'testplan')

        validator = problem_path / 'validator.cpp'
        if validator.exists():
            zf.write(validator, 'validator.cpp')

    buf.seek(0)
    return buf


def _max_output_size(problem_path: pathlib.Path) -> int:
    cases_dir = problem_path / 'cases'
    sizes = [f.stat().st_size for f in cases_dir.glob('*.out') if f.is_file()] if cases_dir.exists() else []
    return max(sizes) if sizes else 0


def _check_exists(client, alias: str) -> bool:
    try:
        client.problem.details(problem_alias=alias)
        return True
    except AttributeError:
        # SDK parsing bug: API response has dict fields returned as []
        # Can't determine existence reliably — assume not exists and let
        # the create/update logic below handle the alias-exists fallback.
        return False
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

    alias        = meta['alias']
    title        = meta['title']
    source       = meta.get('source') or ''
    time_limit   = int(meta['time_limit'])
    memory_limit = int(meta['memory_limit'])
    visibility   = meta['visibility']
    prob_type    = meta['type']
    validator    = meta['validator']
    level        = meta['level']
    tags         = meta['tags']

    languages = '' if prob_type == 'lectura' else meta['languages']
    # API expects memory_limit in KiB
    memory_limit_kb = memory_limit * 1024
    # overall_wall_time_limit must always be sent explicitly (OmegaUp bug:
    # PHP checks memoryLimit but writes overallWallTimeLimit, producing "ms" if omitted)
    overall_wall_time_limit = int(meta.get('overall_wall_time_limit') or 60000)
    output_limit = max(_max_output_size(problem_path) + 1000, 10240)

    tag_list = [{'tagname': t['name'], 'public': bool(t.get('public', False))} for t in tags]
    if prob_type == 'lectura':
        tag_list.append({'tagname': 'problemRestrictedTagNoSubmissions', 'public': False})
    selected_tags = json.dumps(tag_list)

    if args.dry_run:
        print("Dry run — ZIP contents:")
        zip_buf.seek(0)
        with zipfile.ZipFile(zip_buf) as zf:
            for name in zf.namelist():
                info = zf.getinfo(name)
                print(f"  {name}  ({info.file_size} bytes)")
        print(f"\nMetadata:")
        print(f"  Alias:          {alias}")
        print(f"  Title:          {title}")
        print(f"  Time limit:     {time_limit} ms")
        print(f"  Memory:         {memory_limit} MB ({memory_limit_kb} KiB sent to API)")
        print(f"  Wall time:      {overall_wall_time_limit} ms")
        print(f"  Visibility:     {visibility}")
        print(f"  Type:           {prob_type}")
        print(f"  Validator:      {validator}")
        print(f"  Level:          {level}")
        print(f"  Languages:      {languages!r}")
        print(f"  Output limit:   {output_limit} bytes (auto)")
        print(f"  Tags:           {selected_tags}")
        print("\n(dry-run) No API call was made.")
        return

    from omegaup_toolkit.auth import get_client
    client = get_client()

    exists = _check_exists(client, alias)
    action = "UPDATE" if exists else "CREATE"

    zip_buf.seek(0)
    with zipfile.ZipFile(zip_buf) as zf:
        file_list = ', '.join(zf.namelist())
    zip_buf.seek(0)

    print(f"\nProblem to upload:")
    print(f"  Alias:          {alias}")
    print(f"  Title:          {title}")
    print(f"  Time limit:     {time_limit} ms")
    print(f"  Memory:         {memory_limit} MB")
    print(f"  Visibility:     {visibility}")
    print(f"  Type:           {prob_type}")
    print(f"  Validator:      {validator}")
    print(f"  Level:          {level}")
    print(f"  Output limit:   {output_limit} bytes (auto)")
    print(f"  Tags:           {', '.join(t['name'] for t in tags)}")
    print(f"  Action:         {action}")
    print(f"  Files:          {file_list}")

    if not args.yes:
        answer = input("\nContinue? [y/N]: ").strip().lower()
        if answer not in ('y', 'yes'):
            print("Cancelled.")
            sys.exit(0)

    try:
        common = dict(
            problem_alias=alias,
            title=title,
            source=source,
            time_limit=time_limit,
            memory_limit=memory_limit_kb,
            output_limit=output_limit,
            overall_wall_time_limit=overall_wall_time_limit,
            visibility=visibility,
            validator=validator,
            languages=languages,
            problem_level=level,
            selected_tags=selected_tags,
            files_={'problem_contents': zip_buf},
        )
        if not exists:
            try:
                client.problem.create(**common)
                print(f"\n✓ Created: https://omegaup.com/arena/problem/{alias}/")
            except Exception as create_err:
                # If creation fails because alias already exists, fall back to update
                err_msg = str(create_err).lower()
                if 'alias' in err_msg or 'exist' in err_msg or 'duplicate' in err_msg or 'taken' in err_msg:
                    zip_buf.seek(0)
                    client.problem.update(message=args.message, redirect=False, **common)
                    print(f"\n✓ Updated (alias existed): https://omegaup.com/arena/problem/{alias}/")
                else:
                    raise
        else:
            client.problem.update(message=args.message, redirect=False, **common)
            print(f"\n✓ Updated: https://omegaup.com/arena/problem/{alias}/")
    except Exception as e:
        print(f"\nError uploading problem: {e}")
        sys.exit(1)
