"""
Reward Script: Create tasks.json with custom problem matcher for Python tracebacks
Task ID: vscode_td_025
Domain: vscode
Scoring:
  - Component 1 (0.15): tasks.json exists and is valid JSON with version 2.0.0
  - Component 2 (0.20): A task entry runs pytest
  - Component 3 (0.25): problemMatcher has owner=python and fileLocation absolute/relative
  - Component 4 (0.25): Pattern regexp matches Python traceback format with file=1, line=2
  - Component 5 (0.15): Severity is error
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_025'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'ml-pipeline', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(stripped)


def find_pytest_task(tasks_data):
    """Find the first task that runs pytest. Returns the task dict or None."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        cmd = task.get('command', '')
        args = task.get('args', [])
        # Check if command is pytest or if pytest appears in command string
        if 'pytest' in str(cmd).lower():
            return task
        # Also check args
        if isinstance(args, list) and any('pytest' in str(a).lower() for a in args):
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================
    # Component 1: tasks.json exists and is valid JSON (0.15)
    # =========================================================
    try:
        if not os.path.isfile(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 — tasks.json not found at {TASKS_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_jsonc(TASKS_JSON_PATH)

        if not isinstance(tasks_data, dict):
            print(f"FAIL: Component 1 — tasks.json root is not an object")
            print("REWARD: 0.0")
            return 0.0

        version = tasks_data.get('version', '')
        if version == '2.0.0':
            print(f"PASS: Component 1 — tasks.json exists, valid JSON, version={version} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version is '{version}', expected '2.0.0'")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 — Could not parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # =========================================================
    # Component 2: A task runs pytest (0.20)
    # =========================================================
    try:
        pytest_task = find_pytest_task(tasks_data)
        if pytest_task is not None:
            print(f"PASS: Component 2 — Found pytest task: label='{pytest_task.get('label', '?')}' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No task with pytest command found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # If no pytest task found, remaining components depend on it
    if pytest_task is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # =========================================================
    # Component 3: problemMatcher has owner=python, fileLocation (0.25)
    # =========================================================
    try:
        pm = pytest_task.get('problemMatcher', {})
        # problemMatcher can be a string, list, or dict
        if isinstance(pm, str):
            print(f"FAIL: Component 3 — problemMatcher is a built-in string reference '{pm}', not custom")
        elif isinstance(pm, list):
            # Use first custom matcher in list
            pm = pm[0] if pm else {}

        if isinstance(pm, dict):
            owner = pm.get('owner', '')
            file_location = pm.get('fileLocation', '')

            owner_ok = owner.lower() == 'python'
            fl_ok = isinstance(file_location, str) and file_location.lower() in ('absolute', 'relative')

            if owner_ok and fl_ok:
                print(f"PASS: Component 3 — problemMatcher owner='{owner}', fileLocation='{file_location}' (0.25 pts)")
                total_score += 0.25
            else:
                if not owner_ok:
                    print(f"FAIL: Component 3 — owner is '{owner}', expected 'python'")
                if not fl_ok:
                    print(f"FAIL: Component 3 — fileLocation is '{file_location}', expected 'absolute' or 'relative'")
        else:
            print(f"FAIL: Component 3 — problemMatcher is unexpected type: {type(pm)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================
    # Component 4: Pattern has correct regexp and file/line groups (0.25)
    # =========================================================
    try:
        pm = pytest_task.get('problemMatcher', {})
        if isinstance(pm, list):
            pm = pm[0] if pm else {}

        pattern = pm.get('pattern', {})
        if isinstance(pattern, list):
            pattern = pattern[0] if pattern else {}

        regexp = pattern.get('regexp', '')
        file_group = pattern.get('file', None)
        line_group = pattern.get('line', None)

        # Check that regexp contains the Python traceback pattern
        # Expected: something like File "(.*)", line (\d+)
        # We check that the regex can match a Python traceback line
        traceback_match = None
        if regexp:
            try:
                test_line = '  File "/home/user/test.py", line 42, in test_func'
                traceback_match = re.search(regexp, test_line)
            except re.error:
                pass

        file_ok = file_group == 1
        line_ok = line_group == 2

        if traceback_match is not None and file_ok and line_ok:
            print(f"PASS: Component 4 — Pattern regexp matches traceback, file={file_group}, line={line_group} (0.25 pts)")
            total_score += 0.25
        else:
            if traceback_match is None:
                print(f"FAIL: Component 4 — regexp '{regexp}' does not match Python traceback format")
            if not file_ok:
                print(f"FAIL: Component 4 — file group is {file_group}, expected 1")
            if not line_ok:
                print(f"FAIL: Component 4 — line group is {line_group}, expected 2")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================
    # Component 5: Severity is error (0.15)
    # =========================================================
    try:
        pm = pytest_task.get('problemMatcher', {})
        if isinstance(pm, list):
            pm = pm[0] if pm else {}

        severity = pm.get('severity', '')
        if isinstance(severity, str) and severity.lower() == 'error':
            print(f"PASS: Component 5 — severity='{severity}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — severity is '{severity}', expected 'error'")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
