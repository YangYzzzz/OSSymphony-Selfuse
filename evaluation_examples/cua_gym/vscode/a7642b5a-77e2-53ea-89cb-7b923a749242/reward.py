"""
Reward Script: Create launch.json with Python debug configuration passing CLI args
Task ID: vscode_td_051
Domain: vscode
Scoring:
  Component 1 (0.15): launch.json exists and is valid JSON with configurations array
  Component 2 (0.20): type == "debugpy" and request == "launch"
  Component 3 (0.25): program == "${workspaceFolder}/src/cli.py"
  Component 4 (0.30): args array matches expected CLI arguments exactly
  Component 5 (0.10): configuration has a name string field
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_051'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'data-tool')
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')

EXPECTED_ARGS = ["--input", "data/input.csv", "--output", "results/output.json", "--verbose"]
EXPECTED_PROGRAM = "${workspaceFolder}/src/cli.py"


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
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

    # Component 1: launch.json exists and is valid JSON with configurations array (0.15 points)
    config = None
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 -- launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        data = load_jsonc(LAUNCH_JSON_PATH)
        configs = data.get("configurations", [])
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- launch.json is valid JSON with {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
            # Find the first Python/debugpy configuration
            for c in configs:
                if c.get("type") in ("debugpy", "python") or "cli" in c.get("name", "").lower() or "python" in c.get("name", "").lower():
                    config = c
                    break
            if config is None:
                config = configs[0]  # fallback to first config
        else:
            print(f"FAIL: Component 1 -- configurations is not a non-empty list: {type(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if config is None:
        print(f"FAIL: No configuration found to evaluate further")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type == "debugpy" and request == "launch" (0.20 points)
    try:
        cfg_type = config.get("type", "")
        cfg_request = config.get("request", "")
        if cfg_type == "debugpy" and cfg_request == "launch":
            print(f"PASS: Component 2 -- type='debugpy', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- expected type='debugpy' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: program == "${workspaceFolder}/src/cli.py" (0.25 points)
    try:
        cfg_program = config.get("program", "")
        if cfg_program == EXPECTED_PROGRAM:
            print(f"PASS: Component 3 -- program='{cfg_program}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- expected program='{EXPECTED_PROGRAM}', found '{cfg_program}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: args array matches expected CLI arguments (0.30 points)
    try:
        cfg_args = config.get("args", [])
        if isinstance(cfg_args, list) and cfg_args == EXPECTED_ARGS:
            print(f"PASS: Component 4 -- args match exactly (0.30 pts)")
            total_score += 0.30
        else:
            # Partial credit: check if at least some args are present
            if isinstance(cfg_args, list) and len(cfg_args) > 0:
                # Count how many expected args are present in order
                matches = sum(1 for a, b in zip(cfg_args, EXPECTED_ARGS) if a == b)
                if matches >= 3:
                    partial = 0.15
                    print(f"PARTIAL: Component 4 -- {matches}/{len(EXPECTED_ARGS)} args match in order, partial credit (0.15 pts)")
                    total_score += partial
                else:
                    print(f"FAIL: Component 4 -- args mismatch. Expected {EXPECTED_ARGS}, found {cfg_args}")
            else:
                print(f"FAIL: Component 4 -- args missing or not a list. Found: {cfg_args}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: configuration has a name string (0.10 points)
    try:
        cfg_name = config.get("name", None)
        if isinstance(cfg_name, str) and len(cfg_name.strip()) > 0:
            print(f"PASS: Component 5 -- configuration name='{cfg_name}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- configuration missing or empty name field")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
