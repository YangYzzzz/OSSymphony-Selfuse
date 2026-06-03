"""
Reward Script: Create Django debug configuration in launch.json
Task ID: vscode_py_016
Domain: vscode
Scoring:
  Component 1 (0.20): launch.json exists with valid JSON containing a configurations array
  Component 2 (0.20): Configuration type is "debugpy" with request "launch"
  Component 3 (0.20): program field references manage.py via ${workspaceFolder}/manage.py
  Component 4 (0.20): args include "runserver" and "8080"
  Component 5 (0.20): Django-specific: django=true AND env contains DEBUG=True
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_016'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
LAUNCH_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'launch.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_django_config(configurations):
    """Find a Django debug configuration among all configurations."""
    for config in configurations:
        if not isinstance(config, dict):
            continue
        # Look for configs that mention django or debugpy or runserver
        config_type = str(config.get('type', '')).lower()
        config_args = config.get('args', [])
        has_django_flag = config.get('django', False)
        args_str = ' '.join(str(a) for a in config_args) if isinstance(config_args, list) else str(config_args)

        if 'debugpy' in config_type or 'python' in config_type or has_django_flag or 'runserver' in args_str:
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

    # Precondition: launch.json must exist
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: launch.json exists with valid JSON and configurations array (0.20 points)
    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
        configurations = data.get('configurations', [])
        if isinstance(configurations, list) and len(configurations) > 0:
            print(f"PASS: Component 1 - launch.json is valid JSON with {len(configurations)} configuration(s) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - configurations array is empty or missing")
    except Exception as e:
        print(f"ERROR: Component 1 - Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Django configuration
    config = find_django_config(configurations)
    if config is None:
        print("FAIL: No Django-related debug configuration found")
        print(f"REWARD: {total_score}")
        return total_score

    print(f"  Using config: {config.get('name', '<unnamed>')}")

    # Component 2: Configuration type is "debugpy" with request "launch" (0.20 points)
    try:
        config_type = str(config.get('type', '')).lower()
        config_request = str(config.get('request', '')).lower()
        if 'debugpy' in config_type and config_request == 'launch':
            print(f"PASS: Component 2 - type='{config.get('type')}', request='{config.get('request')}' (0.20 pts)")
            total_score += 0.20
        elif 'python' in config_type and config_request == 'launch':
            # Accept 'python' type as partial (older VSCode uses 'python' instead of 'debugpy')
            print(f"PARTIAL: Component 2 - type='{config.get('type')}' (acceptable), request='{config.get('request')}' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 - expected type='debugpy', request='launch', found type='{config.get('type')}', request='{config.get('request')}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: program field references manage.py (0.20 points)
    try:
        program = str(config.get('program', ''))
        # Accept various forms: ${workspaceFolder}/manage.py, manage.py, ./manage.py
        if 'manage.py' in program:
            if '${workspaceFolder}' in program or '${workspaceRoot}' in program:
                print(f"PASS: Component 3 - program='{program}' (0.20 pts)")
                total_score += 0.20
            else:
                # manage.py referenced but without workspace variable
                print(f"PARTIAL: Component 3 - program='{program}' references manage.py but not via ${{workspaceFolder}} (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 3 - expected program referencing manage.py, found: '{program}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: args include "runserver" and "8080" (0.20 points)
    try:
        args = config.get('args', [])
        if not isinstance(args, list):
            args = [str(args)]
        args_lower = [str(a).lower() for a in args]
        args_str = ' '.join(str(a) for a in args)

        has_runserver = 'runserver' in args_lower
        has_port = '8080' in args_str

        if has_runserver and has_port:
            print(f"PASS: Component 4 - args contain 'runserver' and '8080': {args} (0.20 pts)")
            total_score += 0.20
        elif has_runserver or has_port:
            found = []
            if has_runserver:
                found.append('runserver')
            if has_port:
                found.append('8080')
            print(f"PARTIAL: Component 4 - args contain {found} but missing others: {args} (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 - expected args with 'runserver' and '8080', found: {args}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Django-specific settings: django=true AND DEBUG=True in env (0.20 points)
    try:
        django_flag = config.get('django', False)
        env_dict = config.get('env', {})
        if not isinstance(env_dict, dict):
            env_dict = {}

        # Check DEBUG in env
        debug_in_env = False
        for key, val in env_dict.items():
            if key.upper() == 'DEBUG' and str(val).lower() == 'true':
                debug_in_env = True
                break

        # Also check if DEBUG might be in djangoEnv or other fields
        django_env = config.get('djangoEnv', {})
        if isinstance(django_env, dict):
            for key, val in django_env.items():
                if key.upper() == 'DEBUG' and str(val).lower() == 'true':
                    debug_in_env = True
                    break

        if django_flag and debug_in_env:
            print(f"PASS: Component 5 - django={django_flag}, DEBUG=True in env (0.20 pts)")
            total_score += 0.20
        elif django_flag:
            print(f"PARTIAL: Component 5 - django={django_flag} but DEBUG not found in env (0.10 pts)")
            total_score += 0.10
        elif debug_in_env:
            print(f"PARTIAL: Component 5 - DEBUG=True in env but django flag not set (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 - django={django_flag}, DEBUG not found in env")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
