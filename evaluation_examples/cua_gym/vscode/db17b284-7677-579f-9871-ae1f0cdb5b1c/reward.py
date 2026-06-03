"""
Reward Script: Configure Flask debug launch.json in VSCode
Task ID: vscode_stu_078
Domain: vscode
Scoring:
  Component 1: launch.json exists and is valid JSON with configurations array (0.2)
  Component 2: A configuration entry targets Flask (module or program) (0.2)
  Component 3: FLASK_APP env var set to "app.py" (0.2)
  Component 4: FLASK_DEBUG env var set to "1" (0.2)
  Component 5: Port 5000 configured in args (0.2)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_078'
PROJECT_DIR = os.path.join(WORKDIR, 'cs301', 'flask-app')
LAUNCH_JSON = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Component 1: launch.json exists and is valid JSON with configurations (0.2 pts) ----
    try:
        if not os.path.exists(LAUNCH_JSON):
            print(f"FAIL: Component 1 -- launch.json not found at {LAUNCH_JSON}")
            print("REWARD: 0.0")
            return 0.0

        data = load_jsonc(LAUNCH_JSON)
        configs = data.get('configurations', [])
        if isinstance(configs, list) and len(configs) > 0:
            print(f"PASS: Component 1 -- launch.json exists with {len(configs)} configuration(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- launch.json has no configurations array or it is empty")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Flask-related configuration entry
    flask_config = None
    for cfg in configs:
        # Look for flask in module, program, or name fields
        module = str(cfg.get('module', '')).lower()
        name = str(cfg.get('name', '')).lower()
        program = str(cfg.get('program', '')).lower()
        if 'flask' in module or 'flask' in name or 'flask' in program:
            flask_config = cfg
            break

    # ---- Component 2: Configuration targets Flask (0.2 pts) ----
    try:
        if flask_config is not None:
            print(f"PASS: Component 2 -- Found Flask configuration: '{flask_config.get('name', 'unnamed')}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- No configuration entry targets Flask (checked module/name/program)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # For remaining checks, use flask_config if found, else try first config
    cfg = flask_config if flask_config else (configs[0] if configs else {})
    env_vars = cfg.get('env', {})
    if not isinstance(env_vars, dict):
        env_vars = {}

    # ---- Component 3: FLASK_APP env var set to "app.py" (0.2 pts) ----
    try:
        flask_app = env_vars.get('FLASK_APP', None)
        if flask_app is not None and str(flask_app).strip() == 'app.py':
            print(f"PASS: Component 3 -- FLASK_APP = '{flask_app}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Expected FLASK_APP='app.py', found: {flask_app!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # ---- Component 4: FLASK_DEBUG env var set to "1" (0.2 pts) ----
    try:
        flask_debug = env_vars.get('FLASK_DEBUG', None)
        if flask_debug is not None and str(flask_debug).strip() == '1':
            print(f"PASS: Component 4 -- FLASK_DEBUG = '{flask_debug}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- Expected FLASK_DEBUG='1', found: {flask_debug!r}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # ---- Component 5: Port 5000 configured in args (0.2 pts) ----
    try:
        args = cfg.get('args', [])
        if not isinstance(args, list):
            args = []

        args_str_list = [str(a).strip() for a in args]
        args_joined = ' '.join(args_str_list)

        # Check: "5000" appears in args (e.g. --port 5000) OR port config key
        port_val = cfg.get('port', None)
        has_port_in_args = '5000' in args_str_list or ('--port' in args_joined and '5000' in args_joined)
        has_port_in_config = (port_val is not None and str(port_val).strip() == '5000')

        if has_port_in_args or has_port_in_config:
            print(f"PASS: Component 5 -- Port 5000 configured (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 -- Port 5000 not found in args={args} or port config")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
