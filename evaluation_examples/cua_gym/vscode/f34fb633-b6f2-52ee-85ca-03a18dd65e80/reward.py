"""
Reward Script: VSCode launch.json Flask debug configuration
Task ID: vscode_prod_042
Domain: vscode
Scoring:
  - Component 1: launch.json file exists with valid JSON (0.15)
  - Component 2: Configuration type is debugpy/python, request is launch (0.2)
  - Component 3: Program set to ${workspaceFolder}/app.py (0.2)
  - Component 4: FLASK_ENV=development in env section (0.2)
  - Component 5: Port 5000 configured in args or elsewhere (0.15)
  - Component 6: Configuration has a name (appears in dropdown) (0.1)
"""

import os
import json

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'flask-app')
LAUNCH_JSON = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: launch.json exists and is valid JSON (0.15 points)
    try:
        if not os.path.exists(LAUNCH_JSON):
            print(f"FAIL: Component 1 — .vscode/launch.json does not exist")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(LAUNCH_JSON, 'r') as f:
            content = f.read()

        # Handle JSONC (strip comments)
        import re
        clean_content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        clean_content = re.sub(r'/\*.*?\*/', '', clean_content, flags=re.DOTALL)

        launch_data = json.loads(clean_content)
        if isinstance(launch_data, dict):
            print(f"PASS: Component 1 — launch.json exists and is valid JSON (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — launch.json is not a JSON object")
    except (json.JSONDecodeError, Exception) as e:
        print(f"FAIL: Component 1 — launch.json exists but is not valid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Find configurations array
    configurations = launch_data.get('configurations', [])
    if not configurations:
        print(f"FAIL: No configurations found in launch.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Use the first configuration (or find a Flask-related one)
    config = None
    for c in configurations:
        name = str(c.get('name', '')).lower()
        if 'flask' in name or 'python' in name:
            config = c
            break
    if config is None:
        config = configurations[0]

    # Component 2: Type is debugpy or python, request is launch (0.2 points)
    try:
        config_type = str(config.get('type', '')).lower()
        config_request = str(config.get('request', '')).lower()

        type_ok = config_type in ('debugpy', 'python')
        request_ok = config_request == 'launch'

        if type_ok and request_ok:
            print(f"PASS: Component 2 — type='{config.get('type')}', request='{config.get('request')}' (0.2 pts)")
            total_score += 0.2
        elif type_ok:
            print(f"PARTIAL: Component 2 — type correct but request='{config.get('request')}' (expected 'launch') (0.1 pts)")
            total_score += 0.1
        elif request_ok:
            print(f"PARTIAL: Component 2 — request correct but type='{config.get('type')}' (expected 'debugpy' or 'python') (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 2 — type='{config.get('type')}' (expected debugpy/python), request='{config.get('request')}' (expected launch)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Program set to ${workspaceFolder}/app.py (0.2 points)
    try:
        program = config.get('program', '')
        program_str = str(program)

        # Accept various valid forms
        valid_programs = [
            '${workspaceFolder}/app.py',
            '${workspaceFolder}\\app.py',
        ]
        # Also accept if it ends with app.py and references workspaceFolder
        if program_str in valid_programs:
            print(f"PASS: Component 3 — program='{program_str}' (0.2 pts)")
            total_score += 0.2
        elif 'workspaceFolder' in program_str and 'app.py' in program_str:
            print(f"PASS: Component 3 — program='{program_str}' contains workspaceFolder and app.py (0.2 pts)")
            total_score += 0.2
        elif 'app.py' in program_str:
            print(f"PARTIAL: Component 3 — program='{program_str}' references app.py but not via workspaceFolder (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 3 — program='{program_str}' (expected '${{workspaceFolder}}/app.py')")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: FLASK_ENV=development in env section (0.2 points)
    try:
        env_section = config.get('env', {})
        flask_env = env_section.get('FLASK_ENV', None)

        if flask_env == 'development':
            print(f"PASS: Component 4 — env.FLASK_ENV='development' (0.2 pts)")
            total_score += 0.2
        elif flask_env is not None:
            print(f"PARTIAL: Component 4 — env.FLASK_ENV='{flask_env}' (expected 'development') (0.05 pts)")
            total_score += 0.05
        else:
            print(f"FAIL: Component 4 — FLASK_ENV not found in env section (env keys: {list(env_section.keys())})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Port 5000 configured (0.15 points)
    # Port can be in args, env, or other config fields
    try:
        config_str = json.dumps(config)

        if '5000' in config_str:
            print(f"PASS: Component 5 — Port 5000 configured (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — Port 5000 not found in configuration")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Configuration has a name (0.1 points)
    try:
        config_name = config.get('name', '')
        if config_name and len(str(config_name)) > 0:
            print(f"PASS: Component 6 — Configuration name: '{config_name}' (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 6 — Configuration has no name")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
