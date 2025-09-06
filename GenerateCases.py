import argparse
import os
import pathlib
import subprocess
import json
from tqdm import tqdm

# Initialize parser
parser = argparse.ArgumentParser(description = "Program to generate the cases of a problem")
 
# Adding optional argument
parser.add_argument('path', type=pathlib.Path, help = "Directory where the problem is")
parser.add_argument('--use_solution', action='store_true', help = "Use this flag when creating your own case checker")

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
    raise FileNotFoundError(f"Local configuration file not found: {config_path}")

path = args.path
gen_path = path/"case_generator.cpp"
exe_path = path/"case_generator.exe"
args_path = path/"cases.arg"
solution_path = path/"solution/solution.cpp"
sol_exe_path  = path/"solution/solution.exe"

# Check that files exists in the folder
if not os.path.isfile(gen_path):
    print(f"Didn't found the generator {gen_path}")
    exit()

if not os.path.isfile(args_path):
    print(f"Didn't found the cases arguments {args_path}")
    exit()

if args.use_solution:
    if not os.path.isfile(solution_path):
        print(f"Didn't found the solution {solution_path}")
        exit()
    subprocess.run(f"{cpp_compiler} {solution_path} {cpp_flags} -o {sol_exe_path}", check=True)

# Compile generator.cpp and parse cases.arg
subprocess.run(f"{cpp_compiler} {gen_path} -I ./Libs {cpp_flags} -o {exe_path}", check=True)
num_lines = sum(1 for line in open(args_path))
f = open(args_path, "r")
errors = []

# Generate cases
with tqdm(total = num_lines) as pbar:
    for case_args in f:
        case_name = case_args.split()[0]
        pbar.set_postfix(case = case_name)

        try :
            subprocess.run(f"{exe_path} {path}/cases/{case_args}", check=True)
        except subprocess.CalledProcessError as e:
            errors.append((case_name, e))
        else:
            if args.use_solution:
                case_name = case_name.rstrip()
                input_file  = open(f"{path}/cases/{case_name}.in", 'r')
                output_file = open(f"{path}/cases/{case_name}.out", 'w')
                subprocess.run(f"{sol_exe_path}", stdin = input_file, stdout = output_file, check=True)
                input_file.close()
                output_file.close()

        pbar.update(1)

f.close()

# Show final errors
if len(errors) > 0:
    print("ERROR WHEN GENERATING SOME CASES:\n")
    print([case_name for case_name, msg in errors])
    print(f"\nError for {errors[0][0]}:\n")
    print(errors[0][1])

os.remove(exe_path)

if args.use_solution:
    os.remove(sol_exe_path)