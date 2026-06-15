"""
Reward Script: VSCode tasks.json with flake8 multi-line problem matcher
Task ID: vscode_td_030
Domain: vs-code (libreoffice_calc domain label but actually VSCode task)
Scoring:
  Component 1: tasks.json exists with task running flake8 (0.2)
  Component 2: problemMatcher owner is "flake8" (0.15)
  Component 3: problemMatcher severity is "warning" (0.15)
  Component 4: Pattern regexp captures flake8 output format (0.3)
  Component 5: Pattern field mappings file=1,line=2,column=3,code=4,message=5 (0.2)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_030'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'python-linter-demo', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, stripping JSONC comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_flake8_task(data):
    """Find a task whose command contains 'flake8'."""
    tasks = data.get('tasks', [])
    for task in tasks:
        cmd = task.get('command', '')
        if 'flake8' in cmd:
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: tasks.json must be valid JSON
    try:
        data = load_tasks_json(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: A task exists that runs flake8 (0.2 points)
    try:
        flake8_task = find_flake8_task(data)
        if flake8_task is not None:
            cmd = flake8_task.get('command', '')
            print(f"PASS: Component 1 -- Found flake8 task with command: '{cmd}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- No task with 'flake8' in command found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if flake8_task is None:
        # Cannot check further components without the task
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Extract problemMatcher (could be dict or list)
    pm = flake8_task.get('problemMatcher', None)
    if isinstance(pm, list) and len(pm) > 0:
        pm = pm[0]

    # Component 2: problemMatcher owner is "flake8" (0.15 points)
    try:
        if isinstance(pm, dict):
            owner = pm.get('owner', '')
            if owner == 'flake8':
                print(f"PASS: Component 2 -- problemMatcher owner is 'flake8' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- Expected owner 'flake8', found '{owner}'")
        else:
            print(f"FAIL: Component 2 -- problemMatcher is not a dict/object, got: {type(pm)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: problemMatcher severity is "warning" (0.15 points)
    try:
        if isinstance(pm, dict):
            severity = pm.get('severity', '')
            if isinstance(severity, str) and severity.lower() == 'warning':
                print(f"PASS: Component 3 -- problemMatcher severity is 'warning' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- Expected severity 'warning', found '{severity}'")
        else:
            print(f"FAIL: Component 3 -- problemMatcher not a dict")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Extract pattern object
    pattern = None
    if isinstance(pm, dict):
        pattern = pm.get('pattern', None)
        # pattern could be a list of patterns for multi-line; take first if so
        if isinstance(pattern, list) and len(pattern) > 0:
            pattern = pattern[0]

    # Component 4: Pattern regexp captures flake8 output format (0.3 points)
    # The regexp should match lines like: filename:line:column: code message
    # It must have 5 capture groups corresponding to file, line, column, code, message
    try:
        comp4_msg = "No pattern object in problemMatcher"
        comp4_earned = 0.0
        if isinstance(pattern, dict):
            regexp_str = pattern.get('regexp', '')
            if not regexp_str:
                comp4_msg = "No regexp in pattern"
            else:
                try:
                    compiled = re.compile(regexp_str)
                    num_groups = compiled.groups
                    test_line = "main.py:10:5: E302 expected 2 blank lines, got 1"
                    match = compiled.match(test_line)
                    if num_groups < 5:
                        comp4_msg = f"Regexp has {num_groups} groups, need >= 5"
                    elif not match:
                        comp4_msg = f"Regexp doesn't match sample flake8 line: '{test_line}'"
                    else:
                        groups = match.groups()
                        file_g, line_g, col_g, code_g, msg_g = groups[0], groups[1], groups[2], groups[3], groups[4]
                        if file_g and line_g.isdigit() and col_g.isdigit() and code_g and msg_g:
                            comp4_earned = 0.3
                            comp4_msg = (f"Regexp has {num_groups} groups, matches sample: "
                                         f"file='{file_g}', line={line_g}, col={col_g}, "
                                         f"code='{code_g}', msg='{msg_g}'")
                        else:
                            comp4_msg = f"Regexp matches but groups don't capture expected values: {groups}"
                except re.error as e:
                    comp4_msg = f"Invalid regexp: {e}"
        if comp4_earned > 0:
            print(f"PASS: Component 4 -- {comp4_msg} (0.3 pts)")
            total_score += comp4_earned
        else:
            print(f"FAIL: Component 4 -- {comp4_msg}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Pattern field mappings (file=1, line=2, column=3, code=4, message=5) (0.2 points)
    try:
        if isinstance(pattern, dict):
            expected_mappings = {
                'file': 1,
                'line': 2,
                'column': 3,
                'code': 4,
                'message': 5
            }
            actual_mappings = {}
            for field, expected_group in expected_mappings.items():
                actual_group = pattern.get(field, None)
                actual_mappings[field] = actual_group

            if actual_mappings == expected_mappings:
                print(f"PASS: Component 5 -- Field mappings correct: {actual_mappings} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 -- Field mappings mismatch. "
                      f"Expected: {expected_mappings}, Got: {actual_mappings}")
        else:
            print(f"FAIL: Component 5 -- No pattern object to check field mappings")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
