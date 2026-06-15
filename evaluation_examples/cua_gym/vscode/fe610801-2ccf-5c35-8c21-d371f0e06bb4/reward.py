"""
Reward Script: Configure Django project's launch.json for debugging
Task ID: vscode_py_063
Domain: vscode
Scoring:
  - Component 1: --noreload flag in args (0.3 pts)
  - Component 2: DJANGO_SETTINGS_MODULE env var set correctly (0.4 pts)
  - Component 3: django: true for template debugging (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_063'
LAUNCH_JSON_PATH = os.path.join(WORKDIR, 'myproject', '.vscode', 'launch.json')


def load_jsonc(path):
    """Load a JSON or JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_django_config(data):
    """Find the Django debug configuration in launch.json."""
    configurations = data.get('configurations', [])
    for config in configurations:
        # Look for a configuration that is Django-related
        name = (config.get('name') or '').lower()
        if 'django' in name:
            return config
    # Fallback: look for any config with django key or Django in program
    for config in configurations:
        if config.get('django') is True:
            return config
        program = config.get('program', '')
        if 'manage.py' in program:
            return config
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: launch.json must exist and be valid JSON
    if not os.path.exists(LAUNCH_JSON_PATH):
        print(f"CRITICAL: launch.json not found at {LAUNCH_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        data = load_jsonc(LAUNCH_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find Django configuration
    django_config = find_django_config(data)
    if django_config is None:
        print("CRITICAL: No Django debug configuration found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found Django config: {json.dumps(django_config, indent=2)}")

    # Component 1: --noreload flag in args (0.3 points)
    # Task requires args to include ["runserver", "--noreload"]
    # Initial state only has ["runserver"], so --noreload is the task-introduced change
    try:
        args = django_config.get('args', [])
        has_noreload = '--noreload' in args
        has_runserver = 'runserver' in args
        if has_noreload and has_runserver:
            print(f"PASS: Component 1 -- args contain 'runserver' and '--noreload': {args} (0.3 pts)")
            total_score += 0.3
        elif has_noreload:
            print(f"PARTIAL: Component 1 -- '--noreload' present but 'runserver' missing: {args} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- '--noreload' not found in args: {args}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: DJANGO_SETTINGS_MODULE env var (0.4 points)
    # Task requires env.DJANGO_SETTINGS_MODULE = "myproject.settings.development"
    # Initial state has no "env" key at all, so this is task-introduced
    try:
        env = django_config.get('env', {})
        settings_module = env.get('DJANGO_SETTINGS_MODULE', None)
        expected_module = 'myproject.settings.development'
        if settings_module == expected_module:
            print(f"PASS: Component 2 -- DJANGO_SETTINGS_MODULE = '{settings_module}' (0.4 pts)")
            total_score += 0.4
        elif settings_module is not None and 'development' in settings_module:
            print(f"PARTIAL: Component 2 -- DJANGO_SETTINGS_MODULE = '{settings_module}', expected '{expected_module}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- DJANGO_SETTINGS_MODULE = {settings_module!r}, expected '{expected_module}'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: django: true for template debugging (0.3 points)
    # Task requires "django": true for template debugging support
    # Initial state has "jinja": true but NOT "django": true, so this is task-introduced
    try:
        django_flag = django_config.get('django', None)
        if django_flag is True:
            print(f"PASS: Component 3 -- 'django': true is set (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 -- 'django' is {django_flag!r}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
