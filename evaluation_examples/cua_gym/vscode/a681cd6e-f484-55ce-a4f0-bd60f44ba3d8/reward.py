"""
Reward Script: Fix VSCode task dependency configuration
Task ID: vscode_fix_047
Domain: vscode
Scoring:
  - Component 1 (0.30): problemMatcher has a background section
  - Component 2 (0.30): background has begPattern with non-empty regexp
  - Component 3 (0.25): background has endPattern with non-empty regexp
  - Component 4 (0.15): background.activeOnStart is true
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_047'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, stripping JSONC comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def get_build_task(tasks_data):
    """Find the 'build' task from the tasks array."""
    for task in tasks_data.get('tasks', []):
        if task.get('label') == 'build':
            return task
    return None


def verify_task(file_path):
    """
    Verify that the build task has a proper problemMatcher with background
    section containing begPattern and endPattern, so VSCode knows when
    the background task finishes and dependent tasks can start.

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        tasks_data = load_tasks_json(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load tasks.json at {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: build task must exist
    build_task = get_build_task(tasks_data)
    if build_task is None:
        print("CRITICAL: No 'build' task found in tasks.json")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: problemMatcher must exist on build task
    pm = build_task.get('problemMatcher')
    if not isinstance(pm, dict):
        print(f"CRITICAL: build task problemMatcher is not a dict: {type(pm)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: problemMatcher has a 'background' section (0.30 points)
    # This is the key fix — without background, VSCode cannot detect when
    # a background task finishes, so dependent tasks never start.
    try:
        background = pm.get('background')
        if isinstance(background, dict) and len(background) > 0:
            print(f"PASS: Component 1 — problemMatcher has 'background' section (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — problemMatcher missing 'background' section (found: {background})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: background has begPattern with a non-empty regexp (0.30 points)
    # begPattern tells VSCode when the background task starts a new cycle.
    try:
        background = pm.get('background', {})
        beg_pattern = background.get('begPattern') if isinstance(background, dict) else None
        if isinstance(beg_pattern, dict):
            beg_regexp = beg_pattern.get('regexp', '')
            if isinstance(beg_regexp, str) and len(beg_regexp.strip()) > 0:
                print(f"PASS: Component 2 — begPattern has regexp: '{beg_regexp}' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 2 — begPattern regexp is empty or missing: '{beg_regexp}'")
        elif isinstance(beg_pattern, str) and len(beg_pattern.strip()) > 0:
            # Some configs use shorthand string form
            print(f"PASS: Component 2 — begPattern is string regexp: '{beg_pattern}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — begPattern missing or invalid: {beg_pattern}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: background has endPattern with a non-empty regexp (0.25 points)
    # endPattern tells VSCode when the background task finishes — this is
    # the critical piece that allows dependent tasks to start.
    try:
        background = pm.get('background', {})
        end_pattern = background.get('endPattern') if isinstance(background, dict) else None
        if isinstance(end_pattern, dict):
            end_regexp = end_pattern.get('regexp', '')
            if isinstance(end_regexp, str) and len(end_regexp.strip()) > 0:
                print(f"PASS: Component 3 — endPattern has regexp: '{end_regexp}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — endPattern regexp is empty or missing: '{end_regexp}'")
        elif isinstance(end_pattern, str) and len(end_pattern.strip()) > 0:
            # Some configs use shorthand string form
            print(f"PASS: Component 3 — endPattern is string regexp: '{end_pattern}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — endPattern missing or invalid: {end_pattern}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: background.activeOnStart is true (0.15 points)
    # activeOnStart indicates the task is already running when it starts,
    # which is typical for watch/build tasks.
    try:
        background = pm.get('background', {})
        active_on_start = background.get('activeOnStart') if isinstance(background, dict) else None
        if active_on_start is True:
            print(f"PASS: Component 4 — activeOnStart is true (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — activeOnStart is not true (found: {active_on_start})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
