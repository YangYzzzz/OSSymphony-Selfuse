"""
Reward Script: Set up Storybook integration in VSCode
Task ID: vscode_web_078
Domain: vscode
Scoring:
  Component 1 (0.3): launch.json exists with a "Debug Storybook" configuration
  Component 2 (0.3): Launch config has type=chrome, url=localhost:6006, preLaunchTask
  Component 3 (0.2): tasks.json exists with a "Start Storybook" task
  Component 4 (0.2): Storybook task has npm type, correct script, and background matcher
"""

import os
import json
import re

WORKDIR = '/home/user'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
LAUNCH_JSON = os.path.join(VSCODE_DIR, 'launch.json')
TASKS_JSON = os.path.join(VSCODE_DIR, 'tasks.json')
TASK_ID = 'vscode_web_078'


def load_jsonc(file_path):
    """Load a JSON or JSONC file, stripping comments safely."""
    with open(file_path, 'r') as f:
        content = f.read()
    # First try standard JSON parse (works for most files)
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip single-line comments only outside of strings
    # Use a simple state machine approach
    result = []
    i = 0
    in_string = False
    while i < len(content):
        ch = content[i]
        if in_string:
            result.append(ch)
            if ch == '\\' and i + 1 < len(content):
                i += 1
                result.append(content[i])
            elif ch == '"':
                in_string = False
        else:
            if ch == '"':
                in_string = True
                result.append(ch)
            elif ch == '/' and i + 1 < len(content) and content[i + 1] == '/':
                # Skip to end of line
                while i < len(content) and content[i] != '\n':
                    i += 1
                continue
            else:
                result.append(ch)
        i += 1
    cleaned = ''.join(result)
    # Strip trailing commas before } or ]
    cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
    return json.loads(cleaned)


def verify_task():
    """
    Verify Storybook debug integration in VSCode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================================
    # Component 1: launch.json exists with a "Debug Storybook" configuration (0.3 pts)
    # =========================================================================
    debug_storybook_config = None
    try:
        if not os.path.exists(LAUNCH_JSON):
            print(f"FAIL: Component 1 — launch.json not found at {LAUNCH_JSON}")
        else:
            launch_data = load_jsonc(LAUNCH_JSON)
            configs = launch_data.get('configurations', [])
            # Find a configuration whose name contains "Debug Storybook" (case-insensitive)
            for cfg in configs:
                name = cfg.get('name', '')
                if 'debug' in name.lower() and 'storybook' in name.lower():
                    debug_storybook_config = cfg
                    break
            if debug_storybook_config:
                print(f"PASS: Component 1 — Found 'Debug Storybook' launch configuration (name: {debug_storybook_config['name']}) (0.3 pts)")
                total_score += 0.3
            else:
                config_names = [c.get('name', '?') for c in configs]
                print(f"FAIL: Component 1 — No 'Debug Storybook' configuration found. Available: {config_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================================
    # Component 2: Launch config has type=chrome, url=localhost:6006, preLaunchTask (0.3 pts)
    # =========================================================================
    try:
        if debug_storybook_config is None:
            print("FAIL: Component 2 — No debug config to check (depends on Component 1)")
        else:
            sub_score = 0.0
            # Check type is "chrome" (for Chrome debugger)
            cfg_type = debug_storybook_config.get('type', '')
            if cfg_type.lower() == 'chrome':
                sub_score += 0.1
                print(f"  PASS: Component 2a — type is 'chrome'")
            else:
                print(f"  FAIL: Component 2a — expected type 'chrome', found '{cfg_type}'")

            # Check url contains localhost:6006
            cfg_url = debug_storybook_config.get('url', '')
            if 'localhost:6006' in cfg_url or '127.0.0.1:6006' in cfg_url:
                sub_score += 0.1
                print(f"  PASS: Component 2b — url targets port 6006 ({cfg_url})")
            else:
                print(f"  FAIL: Component 2b — expected url with localhost:6006, found '{cfg_url}'")

            # Check preLaunchTask is set (to start the storybook server)
            pre_task = debug_storybook_config.get('preLaunchTask', '')
            if pre_task:
                sub_score += 0.1
                print(f"  PASS: Component 2c — preLaunchTask is set ('{pre_task}')")
            else:
                print(f"  FAIL: Component 2c — no preLaunchTask defined in launch config")

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 2 — Launch config properties verified ({sub_score} pts)")
            else:
                print(f"FAIL: Component 2 — No sub-checks passed")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================================
    # Component 3: tasks.json exists with a Storybook task (0.2 pts)
    # =========================================================================
    storybook_task = None
    try:
        if not os.path.exists(TASKS_JSON):
            print(f"FAIL: Component 3 — tasks.json not found at {TASKS_JSON}")
        else:
            tasks_data = load_jsonc(TASKS_JSON)
            tasks = tasks_data.get('tasks', [])
            # Find a task whose label matches the preLaunchTask, or contains 'storybook'
            pre_task_label = ''
            if debug_storybook_config:
                pre_task_label = debug_storybook_config.get('preLaunchTask', '').lower()
            for t in tasks:
                label = t.get('label', '').lower()
                if 'storybook' in label:
                    storybook_task = t
                    break
            if storybook_task is None and pre_task_label:
                # Try exact label match
                for t in tasks:
                    if t.get('label', '').lower() == pre_task_label:
                        storybook_task = t
                        break
            if storybook_task:
                print(f"PASS: Component 3 — Found Storybook task (label: '{storybook_task.get('label')}') (0.2 pts)")
                total_score += 0.2
            else:
                task_labels = [t.get('label', '?') for t in tasks]
                print(f"FAIL: Component 3 — No Storybook task found. Available: {task_labels}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================================
    # Component 4: Storybook task has npm type, correct script, background matcher (0.2 pts)
    # =========================================================================
    try:
        if storybook_task is None:
            print("FAIL: Component 4 — No storybook task to check (depends on Component 3)")
        else:
            sub_score = 0.0

            # Check task type is npm or shell (common patterns)
            task_type = storybook_task.get('type', '')
            # npm type with "storybook" script, or shell type with npx/npm command
            if task_type.lower() == 'npm':
                script = storybook_task.get('script', '')
                if 'storybook' in script.lower():
                    sub_score += 0.1
                    print(f"  PASS: Component 4a — npm task with script '{script}'")
                else:
                    print(f"  FAIL: Component 4a — npm task but script is '{script}', expected 'storybook'")
            elif task_type.lower() == 'shell':
                command = storybook_task.get('command', '')
                if 'storybook' in command.lower():
                    sub_score += 0.1
                    print(f"  PASS: Component 4a — shell task with storybook command")
                else:
                    print(f"  FAIL: Component 4a — shell task but command doesn't mention storybook: '{command}'")
            else:
                print(f"  FAIL: Component 4a — unexpected task type '{task_type}'")

            # Check isBackground is true (storybook is a long-running server)
            is_bg = storybook_task.get('isBackground', False)
            if is_bg:
                sub_score += 0.1
                print(f"  PASS: Component 4b — isBackground is true (long-running server)")
            else:
                # Also check problemMatcher for background pattern as alternative
                pm = storybook_task.get('problemMatcher', {})
                if isinstance(pm, dict) and pm.get('background'):
                    sub_score += 0.1
                    print(f"  PASS: Component 4b — background problemMatcher defined")
                else:
                    print(f"  FAIL: Component 4b — isBackground not set and no background problemMatcher")

            if sub_score > 0:
                total_score += sub_score
                print(f"PASS: Component 4 — Storybook task properties verified ({sub_score} pts)")
            else:
                print(f"FAIL: Component 4 — No sub-checks passed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point artifacts
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
