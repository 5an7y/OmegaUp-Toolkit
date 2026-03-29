import argparse
import os
import pathlib
import platform
import subprocess
import json
from tqdm import tqdm

# Initialize parser
parser = argparse.ArgumentParser(description = "Program to generate the cases of a problem")

# Adding optional argument
parser.add_argument('path', type=pathlib.Path, help = "Directory where the problem is")
parser.add_argument('--use_solution', action='store_true', help = "Use this flag when creating your own case checker")
parser.add_argument('--stack', type=int, default=16777216, help = "Size of the stack for the solution and generator (Windows only)")

# Read arguments from command line
args = parser.parse_args()

# Read local configuration if it exists
config_path = pathlib.Path(__file__).parent / "local_config.json"
if config_path.exists():
    with open(config_path, "r") as f:
        config = json.load(f)
    cpp_compiler = config.get("cpp_compiler", "g++")
    cpp_flags = config.get("cpp_flags", "-std=c++20")
else:
    cpp_compiler = "g++"
    cpp_flags = "-std=c++20"

libs_path = pathlib.Path(__file__).parent / "Libs"
compile_flags = cpp_flags.split()
stack_flag = [f"-Wl,--stack,{args.stack}"] if platform.system() == "Windows" else []

path = args.path
gen_path = path / "case_generator.cpp"
exe_path = path / "case_generator.exe"
args_path = path / "cases.arg"
solution_path = path / "solution" / "solution.cpp"
sol_exe_path  = path / "solution" / "solution.exe"

# Check that required files exist
if not os.path.isfile(gen_path):
    print(f"Error: generator not found: {gen_path}")
    exit(1)

if not os.path.isfile(args_path):
    print(f"Error: cases.arg not found: {args_path}")
    exit(1)

if args.use_solution:
    if not os.path.isfile(solution_path):
        print(f"Error: solution not found: {solution_path}")
        exit(1)
    print(f"Compiling {solution_path}...")
    subprocess.run(
        [cpp_compiler, str(solution_path), "-I", str(libs_path)] + compile_flags + ["-o", str(sol_exe_path)] + stack_flag,
        check=True
    )

# Compile the case generator
print(f"Compiling {gen_path}...")
subprocess.run(
    [cpp_compiler, str(gen_path), "-I", str(libs_path)] + compile_flags + ["-o", str(exe_path)] + stack_flag,
    check=True
)

errors = []

# Generate cases
with open(args_path, "r") as f:
    lines = [line for line in f if line.strip()]

with tqdm(total=len(lines)) as pbar:
    for case_args in lines:
        case_parts = case_args.split()
        case_name = case_parts[0]
        pbar.set_postfix(case=case_name)

        case_file_path = str(path / "cases" / case_name)
        cmd = [str(exe_path), case_file_path] + case_parts[1:]

        try:
            subprocess.run(cmd, check=True)
        except subprocess.CalledProcessError as e:
            errors.append((case_name, e))
        else:
            if args.use_solution:
                with open(f"{path}/cases/{case_name}.in", 'r') as input_file, \
                     open(f"{path}/cases/{case_name}.out", 'w') as output_file:
                    subprocess.run([str(sol_exe_path)], stdin=input_file, stdout=output_file, check=True)

        pbar.update(1)

os.remove(exe_path)
if args.use_solution:
    os.remove(sol_exe_path)

# Show final errors
if errors:
    print(f"\nErrors generating {len(errors)} case(s):")
    for name, err in errors:
        print(f"  - {name}: {err}")
