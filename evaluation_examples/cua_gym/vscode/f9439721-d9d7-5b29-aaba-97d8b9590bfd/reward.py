"""
Reward Script: Add a watch task to tasks.json with npm run watch and isBackground: true
Task ID: vscode_td_006
Domain: vscode
Scoring:
  Component 1 (0.3): A new watch task exists in tasks.json (more than the original 1 task)
  Component 2 (0.3): The new task's command is "npm run watch"
  Component 3 (0.2): The new task has isBackground set to true
  Component 4 (0.2): Original Build task is preserved and new task has a label
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_006'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'webpack-app', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, handling JSONC (comments)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC compatibility
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def find_watch_task(tasks):
    """Find the watch task among the task list.
    Returns the task dict if found, None otherwise.
    Identifies the watch task by its command containing 'npm run watch'.
    """
    for task in tasks:
        cmd = task.get('command', '')
        if isinstance(cmd, str) and 'npm run watch' in cmd.lower():
            return task
    # Fallback: check label for 'watch' (case-insensitive) excluding the original Build
    for task in tasks:
        label = task.get('label', '')
        if isinstance(label, str) and 'watch' in label.lower():
            return task
    return None


def find_build_task(tasks):
    """Find the original Build task."""
    for task in tasks:
        label = task.get('label', '')
        cmd = task.get('command', '')
        if isinstance(label, str) and label.lower() == 'build':
            return task
        if isinstance(cmd, str) and 'npm run build' in cmd.lower():
            return task
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the tasks.json file
    try:
        data = load_tasks_json(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Find the watch task
    watch_task = find_watch_task(tasks)

    # Component 1: A new watch task exists (0.3 points)
    # Initial state has exactly 1 task (Build). Golden should have >= 2.
    try:
        if watch_task is not None:
            print(f"PASS: Component 1 - Watch task found in tasks list (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 - No watch task found. Tasks: {[t.get('label', 'unlabeled') for t in tasks]}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The watch task command is "npm run watch" (0.3 points)
    try:
        if watch_task is not None:
            cmd = watch_task.get('command', '')
            if isinstance(cmd, str) and 'npm run watch' in cmd:
                print(f"PASS: Component 2 - Command is '{cmd}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Expected command containing 'npm run watch', found: '{cmd}'")
        else:
            print(f"FAIL: Component 2 - No watch task to check command")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: isBackground is set to true (0.2 points)
    try:
        if watch_task is not None:
            is_bg = watch_task.get('isBackground', None)
            if is_bg is True:
                print(f"PASS: Component 3 - isBackground is true (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - Expected isBackground=true, found: {is_bg}")
        else:
            print(f"FAIL: Component 3 - No watch task to check isBackground")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Original Build task preserved AND watch task has a label (0.2 points)
    try:
        build_task = find_build_task(tasks)
        if build_task is not None and watch_task is not None:
            watch_label = watch_task.get('label', '')
            if isinstance(watch_label, str) and len(watch_label.strip()) > 0:
                print(f"PASS: Component 4 - Build task preserved, watch label='{watch_label}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 - Watch task has no label: '{watch_label}'")
        elif build_task is None:
            print(f"FAIL: Component 4 - Original Build task not found (may have been deleted)")
        else:
            print(f"FAIL: Component 4 - No watch task found")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
