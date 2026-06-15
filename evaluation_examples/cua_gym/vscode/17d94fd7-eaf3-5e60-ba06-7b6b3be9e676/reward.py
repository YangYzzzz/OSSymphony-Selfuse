"""
Reward Script: Create launch.json for debugging a Python package in editable mode
Task ID: vscode_td_089
Domain: vscode
Scoring:
  - Component 1 (0.15): launch.json exists, valid JSON, has configurations array with debugpy config
  - Component 2 (0.20): type == "debugpy" and request == "launch"
  - Component 3 (0.25): module == "mypackage" (not a file path)
  - Component 4 (0.20): args == ["--config", "config/dev.yaml"]
  - Component 5 (0.10): justMyCode == false
  - Component 6 (0.10): console == "integratedTerminal"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_089'

LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'mypackage', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (VSCode JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_debug_config(configurations):
    """Find the first configuration with type debugpy or python."""
    for config in configurations:
        if isinstance(config, dict) and config.get('type') in ('debugpy', 'python'):
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

    # Precondition: Must be valid JSON
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Must have configurations array
    configurations = data.get('configurations', [])
    if not isinstance(configurations, list) or len(configurations) == 0:
        print(f"CRITICAL: No configurations array found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant debug configuration
    config = find_debug_config(configurations)

    # Component 1: A debugpy configuration exists (0.15 points)
    try:
        if config is not None:
            print(f"PASS: Component 1 -- debugpy configuration found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- no debugpy/python configuration found in launch.json")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if config is None:
        # No debug config found; remaining checks cannot pass
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type == "debugpy" and request == "launch" (0.20 points)
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'debugpy' and cfg_request == 'launch':
            print(f"PASS: Component 2 -- type='debugpy', request='launch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 -- expected type='debugpy' and request='launch', "
                  f"found type='{cfg_type}' and request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: module == "mypackage" (0.25 points)
    try:
        cfg_module = config.get('module', '')
        if cfg_module == 'mypackage':
            print(f"PASS: Component 3 -- module='mypackage' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- expected module='mypackage', found module='{cfg_module}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: args == ["--config", "config/dev.yaml"] (0.20 points)
    try:
        cfg_args = config.get('args', [])
        expected_args = ["--config", "config/dev.yaml"]
        if cfg_args == expected_args:
            print(f"PASS: Component 4 -- args={cfg_args} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 -- expected args={expected_args}, found args={cfg_args}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: justMyCode == false (0.10 points)
    try:
        cfg_jmc = config.get('justMyCode')
        if cfg_jmc is False:
            print(f"PASS: Component 5 -- justMyCode=false (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 -- expected justMyCode=false, found justMyCode={cfg_jmc}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: console == "integratedTerminal" (0.10 points)
    try:
        cfg_console = config.get('console', '')
        if cfg_console == 'integratedTerminal':
            print(f"PASS: Component 6 -- console='integratedTerminal' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- expected console='integratedTerminal', found console='{cfg_console}'")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
