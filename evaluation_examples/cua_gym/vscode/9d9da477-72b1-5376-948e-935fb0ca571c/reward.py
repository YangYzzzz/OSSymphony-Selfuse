"""
Reward Script: Create VSCode launch.json with Debug CLI configuration and input variables
Task ID: vscode_gf2_039
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists with valid JSON structure and configurations array
  Component 2 (0.20): Configuration named "Debug CLI" with type=python, request=launch
  Component 3 (0.15): Program set to "${workspaceFolder}/cli.py"
  Component 4 (0.25): Args array matches expected values including ${input:inputFile}
  Component 5 (0.25): inputs array with inputFile promptString definition
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_039'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'cli-tool', '.vscode', 'launch.json')

EXPECTED_ARGS = ["--input", "${input:inputFile}", "--output", "output.json", "--verbose"]


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load the file
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid JSON structure with configurations array (0.15 points)
    try:
        configs = data.get("configurations")
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 — launch.json has valid configurations array with {len(configs)} entries (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — 'configurations' missing or empty, found: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the "Debug CLI" configuration
    debug_cli_config = None
    if isinstance(data.get("configurations"), list):
        for cfg in data["configurations"]:
            if isinstance(cfg, dict) and cfg.get("name") == "Debug CLI":
                debug_cli_config = cfg
                break

    # Component 2: Configuration named "Debug CLI" with type=python, request=launch (0.20 points)
    try:
        if debug_cli_config is None:
            print("FAIL: Component 2 — No configuration named 'Debug CLI' found")
        else:
            cfg_type = debug_cli_config.get("type", "")
            cfg_request = debug_cli_config.get("request", "")
            if cfg_type == "python" and cfg_request == "launch":
                print(f"PASS: Component 2 — 'Debug CLI' config has type='python', request='launch' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — type='{cfg_type}' (expected 'python'), request='{cfg_request}' (expected 'launch')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Program set to "${workspaceFolder}/cli.py" (0.15 points)
    try:
        if debug_cli_config is None:
            print("FAIL: Component 3 — No 'Debug CLI' configuration found")
        else:
            program = debug_cli_config.get("program", "")
            if program == "${workspaceFolder}/cli.py":
                print(f"PASS: Component 3 — program is '${{workspaceFolder}}/cli.py' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — program='{program}', expected '${{workspaceFolder}}/cli.py'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Args array matches expected values (0.25 points)
    try:
        if debug_cli_config is None:
            print("FAIL: Component 4 — No 'Debug CLI' configuration found")
        else:
            actual_args = debug_cli_config.get("args", [])
            if actual_args == EXPECTED_ARGS:
                print(f"PASS: Component 4 — args array matches exactly (0.25 pts)")
                total_score += 0.25
            else:
                # Check partial credit: at least has --input and ${input:inputFile}
                has_input_flag = "--input" in actual_args
                has_input_var = "${input:inputFile}" in actual_args
                has_output = "--output" in actual_args and "output.json" in actual_args
                has_verbose = "--verbose" in actual_args
                partial = sum([has_input_flag, has_input_var, has_output, has_verbose])
                if partial >= 3:
                    print(f"PARTIAL: Component 4 — args partially match ({partial}/4 key elements), but not exact match (0.15 pts)")
                    print(f"  Expected: {EXPECTED_ARGS}")
                    print(f"  Actual:   {actual_args}")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — args mismatch")
                    print(f"  Expected: {EXPECTED_ARGS}")
                    print(f"  Actual:   {actual_args}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: inputs array with inputFile promptString definition (0.25 points)
    try:
        inputs = data.get("inputs", [])
        if not isinstance(inputs, list) or len(inputs) == 0:
            print(f"FAIL: Component 5 — 'inputs' array missing or empty")
        else:
            # Find the inputFile input variable
            input_file_def = None
            for inp in inputs:
                if isinstance(inp, dict) and inp.get("id") == "inputFile":
                    input_file_def = inp
                    break

            if input_file_def is None:
                print("FAIL: Component 5 — No input variable with id='inputFile' found")
            else:
                inp_type = input_file_def.get("type", "")
                inp_desc = input_file_def.get("description", "")
                type_ok = inp_type == "promptString"
                desc_ok = inp_desc == "Path to input file"

                if type_ok and desc_ok:
                    print(f"PASS: Component 5 — inputFile input: type='promptString', description='Path to input file' (0.25 pts)")
                    total_score += 0.25
                elif type_ok or desc_ok:
                    print(f"PARTIAL: Component 5 — type='{inp_type}' ({'OK' if type_ok else 'WRONG'}), description='{inp_desc}' ({'OK' if desc_ok else 'WRONG'}) (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 5 — type='{inp_type}' (expected 'promptString'), description='{inp_desc}' (expected 'Path to input file')")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
