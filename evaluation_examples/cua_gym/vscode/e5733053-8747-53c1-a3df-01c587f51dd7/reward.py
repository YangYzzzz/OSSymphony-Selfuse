"""
Reward Script: Add pre-commit hook tasks to tasks.json with dependency chaining
Task ID: vscode_td_033
Domain: vscode
Scoring:
  Component 1 (0.15): tasks.json has 3 or more tasks
  Component 2 (0.25): "Format (black)" task exists with black command
  Component 3 (0.30): "Sort Imports (isort)" task exists with isort command and dependsOn ["Format (black)"]
  Component 4 (0.30): "Type Check (mypy)" task exists with mypy command and dependsOn ["Sort Imports (isort)"]
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_033'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'typed-python', '.vscode', 'tasks.json')


def normalize(s):
    """Normalize a string for flexible comparison."""
    return re.sub(r'\s+', ' ', s.strip().lower())


def find_task_by_label(tasks, label):
    """Find a task by label (case-insensitive, whitespace-normalized)."""
    target = normalize(label)
    for task in tasks:
        if normalize(task.get('label', '')) == target:
            return task
    return None


def command_contains(task, tool_name):
    """Check if a task's command references the given tool."""
    cmd = task.get('command', '')
    return tool_name.lower() in cmd.lower()


def has_depends_on(task, expected_deps):
    """Check if task has the expected dependsOn labels (case-insensitive)."""
    deps = task.get('dependsOn', [])
    if isinstance(deps, str):
        deps = [deps]
    normalized_deps = [normalize(d) for d in deps]
    normalized_expected = [normalize(e) for e in expected_deps]
    return set(normalized_expected).issubset(set(normalized_deps))


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist and be valid JSON
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        data = json.loads(content_clean)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: tasks.json has at least 3 tasks (0.15 points)
    # Initial env has 0 tasks, so this differentiates.
    try:
        if len(tasks) >= 3:
            print(f"PASS: Component 1 -- tasks.json has {len(tasks)} tasks (>= 3) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected >= 3 tasks, found {len(tasks)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: "Format (black)" task exists with black command (0.25 points)
    try:
        black_task = find_task_by_label(tasks, "Format (black)")
        if black_task and command_contains(black_task, 'black'):
            print(f"PASS: Component 2 -- 'Format (black)' task found with black command (0.25 pts)")
            total_score += 0.25
        elif black_task:
            print(f"FAIL: Component 2 -- 'Format (black)' task found but command does not reference black: {black_task.get('command', '')}")
        else:
            print(f"FAIL: Component 2 -- 'Format (black)' task not found. Available labels: {[t.get('label', '') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: "Sort Imports (isort)" task with isort command and dependsOn ["Format (black)"] (0.30 points)
    try:
        isort_task = find_task_by_label(tasks, "Sort Imports (isort)")
        if isort_task and command_contains(isort_task, 'isort') and has_depends_on(isort_task, ["Format (black)"]):
            print(f"PASS: Component 3 -- 'Sort Imports (isort)' task found with isort command and correct dependsOn (0.30 pts)")
            total_score += 0.30
        elif isort_task and command_contains(isort_task, 'isort'):
            deps = isort_task.get('dependsOn', [])
            print(f"FAIL: Component 3 -- 'Sort Imports (isort)' task found with isort command but dependsOn is {deps}, expected ['Format (black)']")
        elif isort_task:
            print(f"FAIL: Component 3 -- 'Sort Imports (isort)' task found but command does not reference isort: {isort_task.get('command', '')}")
        else:
            print(f"FAIL: Component 3 -- 'Sort Imports (isort)' task not found. Available labels: {[t.get('label', '') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: "Type Check (mypy)" task with mypy command and dependsOn ["Sort Imports (isort)"] (0.30 points)
    try:
        mypy_task = find_task_by_label(tasks, "Type Check (mypy)")
        if mypy_task and command_contains(mypy_task, 'mypy') and has_depends_on(mypy_task, ["Sort Imports (isort)"]):
            print(f"PASS: Component 4 -- 'Type Check (mypy)' task found with mypy command and correct dependsOn (0.30 pts)")
            total_score += 0.30
        elif mypy_task and command_contains(mypy_task, 'mypy'):
            deps = mypy_task.get('dependsOn', [])
            print(f"FAIL: Component 4 -- 'Type Check (mypy)' task found with mypy command but dependsOn is {deps}, expected ['Sort Imports (isort)']")
        elif mypy_task:
            print(f"FAIL: Component 4 -- 'Type Check (mypy)' task found but command does not reference mypy: {mypy_task.get('command', '')}")
        else:
            print(f"FAIL: Component 4 -- 'Type Check (mypy)' task not found. Available labels: {[t.get('label', '') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
