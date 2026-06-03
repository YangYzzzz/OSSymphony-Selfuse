"""
Reward Script: VSCode tasks.json watch task configuration
Task ID: vscode_wf_030
Domain: vscode
Scoring:
  Component 1 (0.20) — tasks.json exists and is valid JSON with correct version
  Component 2 (0.20) — watch task has type "npm" and script "watch"
  Component 3 (0.20) — isBackground is true
  Component 4 (0.20) — problemMatcher is "$tsc-watch"
  Component 5 (0.20) — group is default build task
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_030'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_watch_task(tasks_data):
    """Find a task with label 'watch' in the tasks array."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        if isinstance(task, dict) and task.get('label', '').lower() == 'watch':
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists, is valid JSON, has version "2.0.0" (0.20 points)
    # This check FAILS on initial_env (no .vscode dir) and PASSES on golden_env
    tasks_data = None
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 — tasks.json not found at {TASKS_JSON_PATH}")
        else:
            tasks_data = load_jsonc(TASKS_JSON_PATH)
            version = tasks_data.get('version', '')
            if version == '2.0.0':
                print(f"PASS: Component 1 — tasks.json exists with version 2.0.0 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — version is '{version}', expected '2.0.0'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if tasks_data is None:
        # Cannot proceed without valid tasks.json
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find the watch task
    watch_task = find_watch_task(tasks_data)

    # Component 2: watch task has type "npm" and script "watch" (0.20 points)
    try:
        if watch_task is None:
            print("FAIL: Component 2 — no task with label 'watch' found")
        else:
            task_type = watch_task.get('type', '')
            task_script = watch_task.get('script', '')
            if task_type == 'npm' and task_script == 'watch':
                print(f"PASS: Component 2 — watch task has type='npm', script='watch' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — type='{task_type}' (expected 'npm'), script='{task_script}' (expected 'watch')")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if watch_task is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: isBackground is true (0.20 points)
    try:
        is_bg = watch_task.get('isBackground')
        if is_bg is True:
            print(f"PASS: Component 3 — isBackground is true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — isBackground is {is_bg}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: problemMatcher is "$tsc-watch" (0.20 points)
    try:
        matcher = watch_task.get('problemMatcher')
        # problemMatcher can be a string or a list containing the string
        if matcher == '$tsc-watch':
            print(f"PASS: Component 4 — problemMatcher is '$tsc-watch' (0.20 pts)")
            total_score += 0.20
        elif isinstance(matcher, list) and '$tsc-watch' in matcher:
            print(f"PASS: Component 4 — problemMatcher list contains '$tsc-watch' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — problemMatcher is {matcher}, expected '$tsc-watch'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: group is set to default build task (0.20 points)
    try:
        group = watch_task.get('group')
        if isinstance(group, dict):
            kind = group.get('kind', '')
            is_default = group.get('isDefault')
            if kind == 'build' and is_default is True:
                print(f"PASS: Component 5 — group is default build task (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — group kind='{kind}' (expected 'build'), isDefault={is_default} (expected true)")
        elif group == 'build':
            # Partial: group is "build" but not set as default
            print(f"FAIL: Component 5 — group is 'build' string, expected dict with kind='build' and isDefault=true")
        else:
            print(f"FAIL: Component 5 — group is {group}, expected dict with kind='build' and isDefault=true")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
