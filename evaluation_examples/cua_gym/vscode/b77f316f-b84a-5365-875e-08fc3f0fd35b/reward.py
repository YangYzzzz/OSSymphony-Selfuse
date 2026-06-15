"""
Reward Script: Set up a Python launch configuration for Flask debugging
Task ID: vscode_lp_026
Domain: vs_code
Scoring:
  Component 1 (0.2): launch.json exists and is valid JSON with configurations array
  Component 2 (0.2): Configuration uses module "flask"
  Component 3 (0.2): Configuration has args ["run", "--port", "5000"]
  Component 4 (0.2): Configuration has env with FLASK_APP=app.py
  Component 5 (0.2): Configuration has request "launch" and a Python debugger type
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_026'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'workspace', '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_flask_config(configurations):
    """Find a Flask-related configuration from the configurations list."""
    for config in configurations:
        if not isinstance(config, dict):
            continue
        # Match by module=flask or name containing flask (case-insensitive)
        module_val = config.get('module', '')
        if isinstance(module_val, str) and module_val.lower() == 'flask':
            return config
    # Fallback: check name
    for config in configurations:
        if not isinstance(config, dict):
            continue
        name_val = config.get('name', '')
        if isinstance(name_val, str) and 'flask' in name_val.lower():
            return config
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON with configurations array (0.2 pts)
    try:
        if not os.path.isfile(LAUNCH_JSON_PATH):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        data = load_jsonc(LAUNCH_JSON_PATH)
        configurations = data.get('configurations', None)
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 — launch.json exists with {len(configurations)} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — launch.json missing or empty 'configurations' array")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot parse launch.json: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find the Flask configuration
    flask_config = find_flask_config(configurations)
    if flask_config is None:
        print(f"FAIL: No Flask configuration found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Configuration uses module "flask" (0.2 pts)
    try:
        module_val = flask_config.get('module', None)
        if isinstance(module_val, str) and module_val.lower() == 'flask':
            print(f"PASS: Component 2 — module is '{module_val}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Expected module 'flask', found: {module_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Configuration has args ["run", "--port", "5000"] (0.2 pts)
    try:
        args_val = flask_config.get('args', None)
        if isinstance(args_val, list):
            # Normalize: convert all elements to strings for comparison
            args_str = [str(a) for a in args_val]
            expected_args = ["run", "--port", "5000"]
            if args_str == expected_args:
                print(f"PASS: Component 3 — args are {args_str} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected args {expected_args}, found: {args_str}")
        else:
            print(f"FAIL: Component 3 — 'args' not found or not a list, found: {args_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Configuration has env with FLASK_APP=app.py (0.2 pts)
    try:
        env_val = flask_config.get('env', None)
        if isinstance(env_val, dict):
            flask_app = env_val.get('FLASK_APP', None)
            if flask_app == 'app.py':
                print(f"PASS: Component 4 — env.FLASK_APP is 'app.py' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Expected env.FLASK_APP='app.py', found: {flask_app}")
        else:
            print(f"FAIL: Component 4 — 'env' not found or not a dict, found: {env_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Configuration has request "launch" and a Python debugger type (0.2 pts)
    try:
        request_val = flask_config.get('request', None)
        type_val = flask_config.get('type', None)
        # Valid Python debugger types: "python", "debugpy", "pythondebug"
        valid_types = {'python', 'debugpy', 'pythondebug'}
        request_ok = isinstance(request_val, str) and request_val.lower() == 'launch'
        type_ok = isinstance(type_val, str) and type_val.lower() in valid_types
        if request_ok and type_ok:
            print(f"PASS: Component 5 — request='{request_val}', type='{type_val}' (0.2 pts)")
            total_score += 0.2
        else:
            details = []
            if not request_ok:
                details.append(f"request='{request_val}' (expected 'launch')")
            if not type_ok:
                details.append(f"type='{type_val}' (expected one of {valid_types})")
            print(f"FAIL: Component 5 — {', '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
