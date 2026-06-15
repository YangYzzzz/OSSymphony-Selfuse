"""
Reward Script: Create launch.json for debugging Python Jupyter notebook
Task ID: vscode_td_087
Domain: vscode
Scoring:
  - Component 1 (0.15): launch.json exists with valid JSON and configurations array
  - Component 2 (0.25): Configuration has type "debugpy" and request "launch"
  - Component 3 (0.25): purpose contains "debug-in-terminal"
  - Component 4 (0.20): justMyCode is false
  - Component 5 (0.15): console is "integratedTerminal"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_087'

LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'data-science', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_debug_config(configurations):
    """Find a Python/debugpy debug configuration in the configurations list."""
    for config in configurations:
        if isinstance(config, dict):
            cfg_type = config.get('type', '')
            # Accept debugpy or python type
            if cfg_type in ('debugpy', 'python'):
                return config
    return None


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

    # Component 1: launch.json is valid JSON(C) with configurations array (0.15 points)
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
        configs = data.get('configurations', None)
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 — launch.json is valid with {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — 'configurations' missing or empty. Found: {type(configs)}")
            # Cannot proceed without configurations
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the debug configuration
    config = find_debug_config(configs)
    if config is None:
        # Try first config as fallback
        config = configs[0] if configs else {}
        print(f"INFO: No debugpy/python config found, using first configuration")

    # Component 2: type is "debugpy" and request is "launch" (0.25 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        type_ok = cfg_type == 'debugpy'
        request_ok = cfg_request == 'launch'
        if type_ok and request_ok:
            print(f"PASS: Component 2 — type='{cfg_type}', request='{cfg_request}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected type='debugpy' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: purpose contains "debug-in-terminal" (0.25 points)
    try:
        purpose = config.get('purpose', [])
        if isinstance(purpose, list) and 'debug-in-terminal' in purpose:
            print(f"PASS: Component 3 — purpose includes 'debug-in-terminal' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected purpose=['debug-in-terminal'], found: {purpose}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: justMyCode is false (0.20 points)
    try:
        just_my_code = config.get('justMyCode', None)
        if just_my_code is False:
            print(f"PASS: Component 4 — justMyCode is false (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Expected justMyCode=false, found: {just_my_code}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: console is "integratedTerminal" (0.15 points)
    try:
        console = config.get('console', '')
        if console == 'integratedTerminal':
            print(f"PASS: Component 5 — console='integratedTerminal' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Expected console='integratedTerminal', found: '{console}'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
