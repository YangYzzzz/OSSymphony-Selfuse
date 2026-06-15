"""
Reward Script: Verify Python FastAPI project VSCode tooling setup
Task ID: vscode_wf_048
Domain: vscode
Scoring:
  Component 1 (0.35): launch.json - debug config for FastAPI via uvicorn with --reload
  Component 2 (0.35): tasks.json - serve, test, lint tasks
  Component 3 (0.30): settings.json - Python linting, formatting, test discovery
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'project')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
TASK_ID = 'vscode_wf_048'


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def is_subset(expected, actual):
    """Check if expected is a subset of actual (recursive dict/list check)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        if not isinstance(actual, list):
            return False
        # For lists, check same length and element-wise subset
        if len(expected) != len(actual):
            return False
        return all(is_subset(e, a) for e, a in zip(expected, actual))
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: .vscode directory must exist
    if not os.path.isdir(VSCODE_DIR):
        print(f"CRITICAL: .vscode directory not found at {VSCODE_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # =========================================================================
    # Component 1: launch.json debug configuration (0.35 points)
    # Task requires: debug via module 'uvicorn' with args ['app.main:app', '--reload']
    # =========================================================================
    try:
        launch_path = os.path.join(VSCODE_DIR, 'launch.json')
        if not os.path.exists(launch_path):
            print("FAIL: Component 1 -- launch.json not found")
        else:
            launch_data = load_jsonc(launch_path)
            configs = launch_data.get('configurations', [])

            if not configs:
                print("FAIL: Component 1 -- no configurations in launch.json")
            else:
                # Find a configuration that uses module 'uvicorn'
                found_config = 0  # 0=not found, 1=found
                for cfg in configs:
                    module_val = cfg.get('module', '')
                    args_val = cfg.get('args', [])

                    has_uvicorn_module = (module_val == 'uvicorn')
                    has_app_main_arg = ('app.main:app' in args_val)
                    has_reload_arg = ('--reload' in args_val)

                    if has_uvicorn_module and has_app_main_arg and has_reload_arg:
                        print(f"PASS: Component 1 -- launch.json has uvicorn debug config with --reload (0.35 pts)")
                        total_score += 0.35
                        found_config = 1  # marker: full match found
                        break

                if found_config != 1:
                    # Check partial credit
                    partial = 0.0
                    for cfg in configs:
                        module_val = cfg.get('module', '')
                        args_val = cfg.get('args', [])
                        if module_val == 'uvicorn':
                            partial = 0.15
                            if 'app.main:app' in args_val:
                                partial = 0.25
                    if partial > 0:
                        print(f"PARTIAL: Component 1 -- launch.json has uvicorn module but missing args ({partial} pts)")
                        total_score += partial
                    else:
                        print(f"FAIL: Component 1 -- no uvicorn debug config found in launch.json")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================================
    # Component 2: tasks.json with serve, test, lint tasks (0.35 points)
    # Task requires three tasks: 'serve', 'test', 'lint'
    # =========================================================================
    try:
        tasks_path = os.path.join(VSCODE_DIR, 'tasks.json')
        if not os.path.exists(tasks_path):
            print("FAIL: Component 2 -- tasks.json not found")
        else:
            tasks_data = load_jsonc(tasks_path)
            task_list = tasks_data.get('tasks', [])
            task_labels = [t.get('label', '').lower() for t in task_list]

            required_tasks = ['serve', 'test', 'lint']
            found_tasks = []
            for rt in required_tasks:
                if rt in task_labels:
                    found_tasks.append(rt)

            if len(found_tasks) == 3:
                print(f"PASS: Component 2 -- tasks.json has all 3 tasks: {found_tasks} (0.35 pts)")
                total_score += 0.35
            elif len(found_tasks) > 0:
                partial = round(0.35 * len(found_tasks) / 3, 2)
                print(f"PARTIAL: Component 2 -- tasks.json has {len(found_tasks)}/3 tasks: {found_tasks} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 2 -- tasks.json has none of the required tasks. Found: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================================
    # Component 3: settings.json with Python development config (0.30 points)
    # Task requires: Python linting, formatting, and test discovery
    # =========================================================================
    try:
        settings_path = os.path.join(VSCODE_DIR, 'settings.json')
        if not os.path.exists(settings_path):
            print("FAIL: Component 3 -- settings.json not found")
        else:
            settings_data = load_jsonc(settings_path)
            sub_score = 0.0

            # Sub-check 3a: pytest enabled for test discovery (0.10 pts)
            if settings_data.get('python.testing.pytestEnabled') is True:
                print("PASS: Component 3a -- pytestEnabled is true (0.10 pts)")
                sub_score += 0.10
            else:
                print(f"FAIL: Component 3a -- python.testing.pytestEnabled not true, found: {settings_data.get('python.testing.pytestEnabled')}")

            # Sub-check 3b: formatOnSave or Python formatting config (0.10 pts)
            has_format_on_save = settings_data.get('editor.formatOnSave') is True
            python_section = settings_data.get('[python]', {})
            has_python_format = python_section.get('editor.formatOnSave') is True if isinstance(python_section, dict) else False
            if has_format_on_save or has_python_format:
                print("PASS: Component 3b -- formatOnSave enabled (0.10 pts)")
                sub_score += 0.10
            else:
                print("FAIL: Component 3b -- no formatOnSave setting found")

            # Sub-check 3c: Python linting enabled (0.10 pts)
            has_linting = settings_data.get('python.linting.enabled') is True
            has_type_checking = settings_data.get('python.analysis.typeCheckingMode') is not None
            if has_linting or has_type_checking:
                print("PASS: Component 3c -- Python linting/analysis configured (0.10 pts)")
                sub_score += 0.10
            else:
                print("FAIL: Component 3c -- no Python linting configuration found")

            if sub_score > 0:
                print(f"Component 3 total: {sub_score} pts")
            total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
