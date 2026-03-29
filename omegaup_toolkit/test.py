import argparse
import json
import os
import pathlib
import shutil
import subprocess
import time

_TOOLKIT_DIR = pathlib.Path(__file__).parent.parent

FAIL_COLOR = '\033[91m'
OK_COLOR   = '\033[92m'
WARNING    = '\033[93m'
END_COLOR  = '\033[0m'
CHECK      = '\u2713'
CROSS      = '\u2717'


def _load_config():
    config_path = _TOOLKIT_DIR / "local_config.json"
    if config_path.exists():
        with open(config_path) as f:
            config = json.load(f)
        return config.get("cpp_compiler", "g++"), config.get("cpp_flags", "-std=c++20")
    return "g++", "-std=c++20"


def _solution_ok(cases_path, case_name, path, validator, validator_exe):
    case_out_path = cases_path / f"{case_name}.out"
    user_sol_path = cases_path / f"{case_name}_sol.out"

    if validator:
        shutil.copyfile(cases_path / f"{case_name}.in", "data.in")
        shutil.copyfile(case_out_path, "data.out")
        with open(user_sol_path) as f, open(path / "rank.txt", "w") as f_out:
            subprocess.run([str(validator_exe)], stdin=f, stdout=f_out, timeout=20, check=True)
        with open(path / "rank.txt") as f:
            return float(next(f).split()[0])
    else:
        def tokens(p):
            result = []
            with open(p) as f:
                for line in f:
                    t = line.split()
                    if t:
                        result += t
            return result
        return 1.0 if tokens(case_out_path) == tokens(user_sol_path) else 0.0


def _run_case(case, exe_p, cases_path, path, cases_weights, time_limit, validator, validator_exe):
    tab = "\t"
    print(f"{tab}{case}: Running...", end='\r')
    verdict    = ""
    case_score = 0.0
    case_total = cases_weights[case]

    start       = time.time()
    input_file  = open(cases_path / f"{case}.in")
    output_file = open(cases_path / f"{case}_sol.out", 'w')

    try:
        subprocess.run([str(exe_p)], stdin=input_file, stdout=output_file, timeout=time_limit, check=True)
    except subprocess.TimeoutExpired:
        verdict = "TLE"
        print(f"{tab}{FAIL_COLOR}{case}: {CROSS} [TLE, scr = 0/{case_total:.2f}]{END_COLOR}")
    except subprocess.CalledProcessError:
        verdict = "RTE"
        print(f"{tab}{FAIL_COLOR}{case}: {CROSS} [RTE, scr = 0/{case_total:.2f}]{END_COLOR}")
    else:
        elapsed_ms = int((time.time() - start) * 1000)
        ranking    = _solution_ok(cases_path, case, path, validator, validator_exe)
        if ranking == 1.0:
            verdict    = "AC"
            case_score = case_total
            print(f"{tab}{OK_COLOR}{case}: {CHECK} [AC, ms = {elapsed_ms}, scr = {case_score:.2f}]{END_COLOR}")
        elif ranking > 0:
            verdict    = "PA"
            case_score = ranking * case_total
            print(f"{tab}{WARNING}{case}: {CROSS} [PA, ms = {elapsed_ms}, scr = {case_score:.2f}/{case_total:.2f}]{END_COLOR}")
        else:
            verdict = "WA"
            print(f"{tab}{FAIL_COLOR}{case}: {CROSS} [WA, ms = {elapsed_ms}, scr = 0/{case_total:.2f}]{END_COLOR}")

    input_file.close()
    output_file.close()
    os.remove(cases_path / f"{case}_sol.out")
    return verdict, case_score


def _test_solution(solution, groups, solutions_path, cases_path, path,
                   cases_weights, total_weight, time_limit,
                   validator, validator_exe, cpp_compiler, compile_flags):
    print(f"Testing {solution}:")
    sol_p = solutions_path / solution
    exe_p = solutions_path / (solution[:-4] + ".exe")

    try:
        subprocess.run(
            [cpp_compiler, str(sol_p)] + compile_flags + ["-o", str(exe_p)],
            check=True
        )
    except subprocess.CalledProcessError:
        print(f"\t{FAIL_COLOR}COMPILATION ERROR{END_COLOR}")
        return 0

    mapeo = {"AC": 0, "PA": 0, "TLE": 0, "RTE": 0, "WA": 0}
    score            = 0.0
    total_case_score = 0

    for group_name, group in groups.items():
        group_score  = 0.0
        group_all_ac = True
        is_group     = len(group) > 1
        group_total  = 0

        for case in group:
            verdict, case_score = _run_case(
                case, exe_p, cases_path, path, cases_weights, time_limit, validator, validator_exe
            )
            group_score      += case_score
            group_total      += cases_weights[case]
            total_case_score += cases_weights[case]
            mapeo[verdict]   += 1
            if is_group and verdict != "AC":
                group_all_ac = False

        if group_all_ac:
            score += group_score

        if is_group:
            if group_all_ac:
                print(f"\t{OK_COLOR}{group_name}: {CHECK} [AC, score = {group_score:.2f}]{END_COLOR}")
            else:
                print(f"\t{FAIL_COLOR}{group_name}: {CROSS} [WA, score = 0/{group_total:.2f}]{END_COLOR}")

    os.remove(exe_p)
    final_score = (score / total_weight) * 100
    print(f"AC = {mapeo['AC']}, WA = {mapeo['WA']}, PA = {mapeo['PA']}, TLE = {mapeo['TLE']}, RTE = {mapeo['RTE']}, Score = {final_score:.2f}%")
    print("--------------------------------------------------------------------------------------")
    return final_score


def run(argv=None):
    parser = argparse.ArgumentParser(description="Test solutions against generated cases")
    parser.add_argument('path', type=pathlib.Path, help='Directory where the problem is')
    parser.add_argument('--time_limit', type=int, default=5000, help='Time limit in ms (default: 5000)')
    parser.add_argument('--solutions', type=str, nargs='*', default=[], help='Solutions to test (default: all)')
    parser.add_argument('--cases', type=str, nargs='*', default=[], help='Cases to test (default: all)')
    parser.add_argument('--validator', action='store_true', help='Use validator.cpp for output checking')
    args = parser.parse_args(argv)

    cpp_compiler, cpp_flags = _load_config()
    compile_flags  = cpp_flags.split()

    path           = args.path
    solutions_path = path / "solution"
    cases_path     = path / "cases"
    time_limit     = args.time_limit / 1000
    validator      = args.validator
    validator_path = path / "validator.cpp"
    validator_exe  = path / "validator.exe"

    # Collect cases
    all_cases = list(dict.fromkeys(
        os.path.splitext(c)[0] for c in os.listdir(cases_path)
    ))
    cases = list(dict.fromkeys(args.cases if args.cases else all_cases))

    cases_weights = {}
    for case in cases:
        if not os.path.isfile(cases_path / f"{case}.in"):
            print(f"Missing case file: {case}.in")
            raise SystemExit(1)
        if not os.path.isfile(cases_path / f"{case}.out"):
            print(f"Missing case file: {case}.out")
            raise SystemExit(1)
        cases_weights[case] = 1

    if validator:
        if not os.path.isfile(validator_path):
            print("Missing validator.cpp")
            raise SystemExit(1)
        print("Compiling validator...")
        subprocess.run(
            [cpp_compiler, str(validator_path)] + compile_flags + ["-o", str(validator_exe)],
            check=True
        )

    # Load testplan
    testplan_path = path / "testplan"
    total_weight  = len(cases)
    if os.path.isfile(testplan_path):
        print("Testplan detected. Checking testplan...")
        total_weight = 0
        with open(testplan_path) as f:
            for line in f:
                parts       = line.split()
                case_name   = parts[0]
                case_weight = int(parts[1])
                if case_name not in all_cases:
                    print(f"Error: case '{case_name}' in testplan but not found in cases/")
                    raise SystemExit(1)
                cases_weights[case_name] = case_weight
                total_weight += case_weight
        if total_weight == 0:
            print("Error: total weight in testplan is 0.")
            raise SystemExit(1)
        print("Testplan OK.")

    # Extract groups
    groups = {}
    for case in cases:
        groups.setdefault(case.split(".")[0], []).append(case)

    # Run solutions
    print()
    sol_map = {}
    try:
        for solution in sorted(os.listdir(solutions_path)):
            if not solution.endswith('.cpp'):
                continue
            if args.solutions and solution not in args.solutions:
                continue
            score = _test_solution(
                solution, groups, solutions_path, cases_path, path,
                cases_weights, total_weight, time_limit,
                validator, validator_exe, cpp_compiler, compile_flags
            )
            sol_map[solution] = f"{score:.2f}"
    finally:
        if validator:
            for f in [validator_exe, path / "rank.txt"]:
                if os.path.isfile(f):
                    os.remove(f)
            for f in ["data.in", "data.out"]:
                if os.path.isfile(f):
                    os.remove(f)

    print("Summary:")
    for key, value in sol_map.items():
        print(f"\t{key} = {value}%")
