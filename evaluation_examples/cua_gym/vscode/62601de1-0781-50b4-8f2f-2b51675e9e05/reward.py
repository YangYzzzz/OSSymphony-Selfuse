"""
Reward Script: Create launch.json for Node.js debugging with outputCapture
Task ID: vscode_td_091
Domain: vs_code
Scoring:
  Component 1 (0.20): launch.json exists, valid JSON with configurations array
  Component 2 (0.25): type == "node" and request == "launch"
  Component 3 (0.25): program == "${workspaceFolder}/src/app.js"
  Component 4 (0.20): outputCapture == "std"
  Component 5 (0.10): console is "integratedTerminal" or "internalConsole"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_091'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'logging-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip block comments
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

    # Precondition: must be valid JSON with configurations array
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

    # Use the first configuration (or find a Node.js one)
    config = None
    for c in configs:
        if isinstance(c, dict) and c.get('type', '').lower() == 'node':
            config = c
            break
    if config is None:
        # Fall back to first config
        config = configs[0] if isinstance(configs[0], dict) else None

    if config is None:
        print("CRITICAL: No valid configuration object found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1 (0.20): launch.json has valid structure with configurations
    # This component checks that launch.json was CREATED (it doesn't exist in initial_env)
    # The file existence + valid structure together represent the task-introduced change
    try:
        if 'version' in data and len(configs) > 0:
            print(f"PASS: Component 1 - launch.json has valid structure with {len(configs)} configuration(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - launch.json missing version or empty configurations")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2 (0.25): type == "node" and request == "launch"
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'node' and cfg_request == 'launch':
            print(f"PASS: Component 2 - type='node', request='launch' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - expected type='node' request='launch', found type='{cfg_type}' request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3 (0.25): program == "${workspaceFolder}/src/app.js"
    try:
        program = config.get('program', '')
        if program == '${workspaceFolder}/src/app.js':
            print(f"PASS: Component 3 - program='${{workspaceFolder}}/src/app.js' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - expected program='${{workspaceFolder}}/src/app.js', found '{program}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4 (0.20): outputCapture == "std"
    try:
        output_capture = config.get('outputCapture', '')
        if output_capture == 'std':
            print(f"PASS: Component 4 - outputCapture='std' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - expected outputCapture='std', found '{output_capture}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5 (0.10): console is "integratedTerminal" or "internalConsole"
    try:
        console_val = config.get('console', '')
        if console_val in ('integratedTerminal', 'internalConsole'):
            print(f"PASS: Component 5 - console='{console_val}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - expected console='integratedTerminal' or 'internalConsole', found '{console_val}'")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
