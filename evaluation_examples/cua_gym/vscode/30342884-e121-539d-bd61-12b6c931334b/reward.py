"""
Reward Script: Create launch.json for Flask debugging in VSCode
Task ID: vscode_dbg_031
Domain: vs_code
Scoring:
  Component 1 (0.2): .vscode/launch.json file exists in ~/projects/flask-app/
  Component 2 (0.3): config has type='debugpy' and request='launch'
  Component 3 (0.3): config has module='flask' and args containing 'run' and '--no-debugger'
  Component 4 (0.2): config env has FLASK_APP='app.py'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_031'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'projects', 'flask-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file that may contain // comments (JSONC format)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task(launch_json_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/launch.json file exists (0.2 points)
    # This FAILS on initial_env (no .vscode dir) and PASSES on golden_env
    try:
        if os.path.isfile(launch_json_path):
            print(f"PASS: Component 1 — launch.json exists at {launch_json_path} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — launch.json not found at {launch_json_path}")
            # Without the file, remaining components cannot pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load launch.json (gate check)
    try:
        data = load_jsonc(launch_json_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    configurations = data.get('configurations', [])
    if not configurations or not isinstance(configurations, list):
        print(f"FAIL: launch.json has no 'configurations' array")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first configuration for verification
    config = configurations[0]

    # Component 2: type='debugpy' and request='launch' (0.3 points)
    # Both must be present and correct — ensures this is a proper Python debugger config
    try:
        cfg_type = config.get('type', '')
        cfg_request = config.get('request', '')
        if cfg_type == 'debugpy' and cfg_request == 'launch':
            print(f"PASS: Component 2 — type='{cfg_type}', request='{cfg_request}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected type='debugpy', request='launch'; "
                  f"found type='{cfg_type}', request='{cfg_request}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: module='flask' and args contains 'run' and '--no-debugger' (0.3 points)
    # The module-based launch is the correct way to run Flask in debugpy
    try:
        cfg_module = config.get('module', '')
        cfg_args = config.get('args', [])
        module_ok = (cfg_module == 'flask')
        args_ok = isinstance(cfg_args, list) and ('run' in cfg_args) and ('--no-debugger' in cfg_args)
        if module_ok and args_ok:
            print(f"PASS: Component 3 — module='{cfg_module}', args={cfg_args} (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — expected module='flask' with args ['run', '--no-debugger']; "
                  f"found module='{cfg_module}', args={cfg_args}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: env.FLASK_APP == 'app.py' (0.2 points)
    # Environment variable must point to the Flask entry point
    try:
        cfg_env = config.get('env', {})
        flask_app_value = cfg_env.get('FLASK_APP', '') if isinstance(cfg_env, dict) else ''
        if flask_app_value == 'app.py':
            print(f"PASS: Component 4 — env.FLASK_APP='{flask_app_value}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected env.FLASK_APP='app.py'; "
                  f"found FLASK_APP='{flask_app_value}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task(LAUNCH_JSON_PATH)
