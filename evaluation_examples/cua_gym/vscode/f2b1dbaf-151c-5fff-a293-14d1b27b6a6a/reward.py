"""
Reward Script: Create Python debug configuration in launch.json
Task ID: vscode_py_007
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists and is valid JSON with configurations array
  Component 2 (0.25): A configuration has type "debugpy" or "python" with request "launch"
  Component 3 (0.25): The configuration has program "${file}"
  Component 4 (0.30): The args field contains exactly ["--verbose", "--output", "results.csv"]
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_007'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip block comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_matching_config(configurations):
    """Find the first configuration that looks like a Python debug config."""
    for config in configurations:
        cfg_type = config.get('type', '').lower()
        if cfg_type in ('debugpy', 'python'):
            return config
    # Fallback: return first config if only one exists
    if len(configurations) == 1:
        return configurations[0]
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON with configurations array (0.20 points)
    try:
        if not os.path.exists(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 -- launch.json not found at {LAUNCH_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        data = load_jsonc(LAUNCH_JSON_PATH)
        configurations = data.get('configurations', [])
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 -- launch.json exists with {len(configurations)} configuration(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 -- launch.json has no configurations array or it is empty")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- Cannot load launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant Python debug configuration
    config = find_matching_config(configurations)
    if config is None:
        print("FAIL: No Python debug configuration found in launch.json")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Configuration has type "debugpy" or "python" with request "launch" (0.25 points)
    try:
        cfg_type = str(config.get('type', '')).lower()
        cfg_request = str(config.get('request', '')).lower()
        type_ok = cfg_type in ('debugpy', 'python')
        request_ok = cfg_request == 'launch'

        if type_ok and request_ok:
            print(f"PASS: Component 2 -- type='{config.get('type')}', request='{config.get('request')}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- type='{config.get('type')}' (expected debugpy/python), request='{config.get('request')}' (expected launch)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Configuration has program "${file}" (0.25 points)
    try:
        program = config.get('program', '')
        if program == '${file}':
            print(f"PASS: Component 3 -- program='{program}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- program='{program}', expected '${{file}}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: args field contains exactly ["--verbose", "--output", "results.csv"] (0.30 points)
    try:
        args = config.get('args', None)
        expected_args = ["--verbose", "--output", "results.csv"]
        if isinstance(args, list) and args == expected_args:
            print(f"PASS: Component 4 -- args={args} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 -- args={args}, expected {expected_args}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
