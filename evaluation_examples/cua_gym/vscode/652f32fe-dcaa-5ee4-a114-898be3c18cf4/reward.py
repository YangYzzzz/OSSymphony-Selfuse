"""
Reward Script: Create launch.json with Python debug configuration (justMyCode: false)
Task ID: vscode_td_061
Domain: vscode
Scoring:
  - Component 1: launch.json exists and is valid JSON with configurations array (0.15)
  - Component 2: type is "debugpy" (0.15)
  - Component 3: request is "launch" (0.1)
  - Component 4: program is "${workspaceFolder}/src/main.py" (0.2)
  - Component 5: justMyCode is false (0.25)
  - Component 6: console is "integratedTerminal" (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_061'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'library-debug', '.vscode', 'launch.json')


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

    # Precondition: launch.json must be valid JSON(C) with configurations
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    configs = data.get('configurations', [])
    if not isinstance(configs, list) or len(configs) == 0:
        print("CRITICAL: No configurations array or it is empty")
        print("REWARD: 0.0")
        return 0.0

    # Find the Python debug configuration (search all configs)
    python_config = None
    for cfg in configs:
        if isinstance(cfg, dict) and cfg.get('type') in ('debugpy', 'python'):
            python_config = cfg
            break

    if python_config is None:
        # Fall back to first config if no Python-typed config found
        python_config = configs[0] if isinstance(configs[0], dict) else None

    if python_config is None:
        print("CRITICAL: No valid configuration object found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json has valid structure with version and configurations (0.15 points)
    # This component checks that launch.json was CREATED (it doesn't exist in initial_env)
    try:
        has_version = 'version' in data
        has_configs = len(configs) > 0
        if has_version and has_configs:
            print(f"PASS: Component 1 - launch.json has version '{data.get('version')}' and {len(configs)} configuration(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - version present: {has_version}, configs count: {len(configs)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: type is "debugpy" (0.15 points)
    try:
        cfg_type = python_config.get('type', '')
        if cfg_type == 'debugpy':
            print(f"PASS: Component 2 - type is 'debugpy' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 - expected type 'debugpy', found '{cfg_type}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: request is "launch" (0.1 points)
    try:
        cfg_request = python_config.get('request', '')
        if cfg_request == 'launch':
            print(f"PASS: Component 3 - request is 'launch' (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 - expected request 'launch', found '{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: program is "${workspaceFolder}/src/main.py" (0.2 points)
    try:
        cfg_program = python_config.get('program', '')
        expected_program = '${workspaceFolder}/src/main.py'
        if cfg_program == expected_program:
            print(f"PASS: Component 4 - program is '{cfg_program}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - expected program '{expected_program}', found '{cfg_program}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: justMyCode is false (0.25 points) - KEY requirement
    try:
        if 'justMyCode' in python_config:
            jmc_value = python_config['justMyCode']
            if jmc_value is False:
                print(f"PASS: Component 5 - justMyCode is false (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 5 - justMyCode is {jmc_value}, expected false")
        else:
            print(f"FAIL: Component 5 - justMyCode key not found in configuration")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: console is "integratedTerminal" (0.15 points)
    try:
        cfg_console = python_config.get('console', '')
        if cfg_console == 'integratedTerminal':
            print(f"PASS: Component 6 - console is 'integratedTerminal' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 6 - expected console 'integratedTerminal', found '{cfg_console}'")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
