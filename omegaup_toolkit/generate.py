import argparse
import json
import os
import pathlib
import platform
import subprocess

from tqdm import tqdm

_TOOLKIT_DIR = pathlib.Path(__file__).parent.parent


def _load_config():
    config_path = _TOOLKIT_DIR / "local_config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        return config.get("cpp_compiler", "g++"), config.get("cpp_flags", "-std=c++20")
    return "g++", "-std=c++20"


def run(argv=None):
    parser = argparse.ArgumentParser(description="Compile and run the case generator")
    parser.add_argument('path', type=pathlib.Path, help='Directory where the problem is')
    parser.add_argument('--use_solution', action='store_true', help='Run solution to produce .out files')
    parser.add_argument('--stack', type=int, default=16777216, help='Stack size in bytes (Windows only)')
    args = parser.parse_args(argv)

    cpp_compiler, cpp_flags = _load_config()
    libs_path     = _TOOLKIT_DIR / "Libs"
    compile_flags = cpp_flags.split()
    stack_flag    = [f"-Wl,--stack,{args.stack}"] if platform.system() == "Windows" else []

    path          = args.path
    gen_path      = path / "case_generator.cpp"
    exe_path      = path / "case_generator.exe"
    args_path     = path / "cases.arg"
    solution_path = path / "solution" / "solution.cpp"
    sol_exe_path  = path / "solution" / "solution.exe"

    if not os.path.isfile(gen_path):
        print(f"Error: generator not found: {gen_path}")
        raise SystemExit(1)
    if not os.path.isfile(args_path):
        print(f"Error: cases.arg not found: {args_path}")
        raise SystemExit(1)

    if args.use_solution:
        if not os.path.isfile(solution_path):
            print(f"Error: solution not found: {solution_path}")
            raise SystemExit(1)
        print(f"Compiling {solution_path}...")
        subprocess.run(
            [cpp_compiler, str(solution_path), "-I", str(libs_path)] + compile_flags + ["-o", str(sol_exe_path)] + stack_flag,
            check=True
        )

    print(f"Compiling {gen_path}...")
    subprocess.run(
        [cpp_compiler, str(gen_path), "-I", str(libs_path)] + compile_flags + ["-o", str(exe_path)] + stack_flag,
        check=True
    )

    errors = []
    with open(args_path) as f:
        lines = [line for line in f if line.strip()]

    with tqdm(total=len(lines)) as pbar:
        for case_args in lines:
            case_parts = case_args.split()
            case_name  = case_parts[0]
            pbar.set_postfix(case=case_name)

            cmd = [str(exe_path), str(path / "cases" / case_name)] + case_parts[1:]
            try:
                subprocess.run(cmd, check=True)
            except subprocess.CalledProcessError as e:
                errors.append((case_name, e))
            else:
                if args.use_solution:
                    with open(path / "cases" / f"{case_name}.in") as inp, \
                         open(path / "cases" / f"{case_name}.out", 'w') as out:
                        subprocess.run([str(sol_exe_path)], stdin=inp, stdout=out, check=True)
            pbar.update(1)

    os.remove(exe_path)
    if args.use_solution:
        os.remove(sol_exe_path)

    if errors:
        print(f"\nErrors generating {len(errors)} case(s):")
        for name, err in errors:
            print(f"  - {name}: {err}")
        raise SystemExit(1)
