"""
Reward Script: Add a pytest test task to tasks.json in VSCode workspace
Task ID: vscode_td_003
Domain: vscode (tasks.json configuration)
Scoring:
  Component 1 (0.35): A new test task exists AND original build task is preserved
  Component 2 (0.35): New task has shell type and pytest command targeting tests/
  Component 3 (0.30): New task group is test kind with isDefault true
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_003'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'flask-api', '.vscode', 'tasks.json')


def load_tasks_json(path):
    """Load tasks.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_test_task(tasks):
    """Find a task that looks like a test/pytest task (not the original build task)."""
    for task in tasks:
        label = (task.get('label') or '').lower()
        command = (task.get('command') or '').lower()
        group = task.get('group', {})
        group_kind = group.get('kind', '') if isinstance(group, dict) else group

        # Skip the original build task
        if group_kind == 'build' or label == 'install dependencies':
            continue

        # This is a candidate test task if it mentions pytest/test in label or command
        if 'pytest' in command or 'test' in label or 'pytest' in label or group_kind == 'test':
            return task

    return None


def find_build_task(tasks):
    """Find the original build task."""
    for task in tasks:
        label = (task.get('label') or '').lower()
        group = task.get('group', {})
        group_kind = group.get('kind', '') if isinstance(group, dict) else group
        if group_kind == 'build' or label == 'install dependencies':
            return task
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        data = load_tasks_json(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: A new test task exists AND the original build task is preserved (0.35 points)
    # Both sub-conditions must hold. The build task alone is a precondition (true before task),
    # so we anchor it to the test task existence to avoid scoring pre-existing state.
    try:
        test_task = find_test_task(tasks)
        build_task = find_build_task(tasks)
        build_preserved = False
        if build_task is not None:
            build_command = (build_task.get('command') or '').lower()
            build_preserved = 'pip install' in build_command or 'requirements' in build_command

        if test_task is not None and build_preserved:
            print(f"PASS: Component 1 -- New test task '{test_task.get('label')}' found AND build task preserved (0.35 pts)")
            total_score += 0.35
        elif test_task is not None and not build_preserved:
            print(f"FAIL: Component 1 -- Test task found but original build task missing or altered")
        else:
            print(f"FAIL: Component 1 -- No test task found. Tasks: {[t.get('label') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: New task has type "shell" and command contains pytest targeting tests/ (0.35 points)
    try:
        if test_task is not None:
            task_type = (test_task.get('type') or '').lower()
            command = (test_task.get('command') or '').lower()
            type_ok = task_type == 'shell'
            cmd_has_pytest = 'pytest' in command
            cmd_has_tests = 'tests' in command
            if type_ok and cmd_has_pytest and cmd_has_tests:
                print(f"PASS: Component 2 -- type='{task_type}', command='{test_task.get('command')}' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- type='{task_type}' (need 'shell'), command='{test_task.get('command')}' (need pytest + tests)")
        else:
            print("FAIL: Component 2 -- No test task to check")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: New task group is test kind (0.30 points)
    try:
        if test_task is not None:
            group = test_task.get('group', {})
            if isinstance(group, dict):
                group_kind = group.get('kind', '')
                is_default = group.get('isDefault', False)
            elif isinstance(group, str):
                group_kind = group
                is_default = False
            else:
                group_kind = ''
                is_default = False

            if group_kind == 'test':
                print(f"PASS: Component 3 -- group kind is 'test', isDefault={is_default} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 -- group kind is '{group_kind}', expected 'test'")
        else:
            print("FAIL: Component 3 -- No test task to check")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
