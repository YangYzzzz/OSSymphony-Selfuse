"""
Reward Script: Fix Flask debug launch configuration in VSCode
Task ID: vscode_fix_052
Domain: vscode
Scoring:
  - Component 1 (0.4): FLASK_APP env var set to "app.py"
  - Component 2 (0.3): jinja set to true
  - Component 3 (0.3): justMyCode set to false
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_052'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'flask-app', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) but not inside strings
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_flask_config(data):
    """Find the Flask debug configuration in launch.json."""
    configurations = data.get('configurations', [])
    for config in configurations:
        # Match by name containing 'Flask' or module being 'flask'
        if config.get('module') == 'flask' or 'flask' in config.get('name', '').lower():
            return config
    return None


def verify_task(launch_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load launch.json
    try:
        data = load_jsonc(launch_path)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {launch_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Flask configuration
    flask_config = find_flask_config(data)
    if flask_config is None:
        print("CRITICAL: No Flask configuration found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found Flask config: '{flask_config.get('name', 'unnamed')}'")

    # Component 1: FLASK_APP env var set to "app.py" (0.4 points)
    # This is the primary fix - initial state is missing FLASK_APP entirely
    try:
        env_vars = flask_config.get('env', {})
        flask_app_val = env_vars.get('FLASK_APP')
        if flask_app_val is not None and str(flask_app_val).strip() == 'app.py':
            print(f"PASS: Component 1 - FLASK_APP is set to '{flask_app_val}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - Expected FLASK_APP='app.py', found: {flask_app_val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: jinja set to true (0.3 points)
    # Initial state has no jinja field; golden state adds jinja: true
    try:
        jinja_val = flask_config.get('jinja')
        if jinja_val is True:
            print(f"PASS: Component 2 - jinja is set to true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - Expected jinja=true, found: {jinja_val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: justMyCode set to false (0.3 points)
    # Initial state has justMyCode: true; golden state changes to false
    try:
        jmc_val = flask_config.get('justMyCode')
        if jmc_val is False:
            print(f"PASS: Component 3 - justMyCode is set to false (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - Expected justMyCode=false, found: {jmc_val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
