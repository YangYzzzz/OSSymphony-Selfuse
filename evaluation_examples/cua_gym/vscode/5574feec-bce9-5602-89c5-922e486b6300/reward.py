"""
Reward Script: Create VSCode tasks.json with 'Run Tests' task
Task ID: vscode_stu_058
Domain: vscode
Scoring:
  Component 1 (0.2): tasks.json exists and is valid JSON with version field
  Component 2 (0.2): A task with label 'Run Tests' exists
  Component 3 (0.2): The 'Run Tests' task type is 'shell'
  Component 4 (0.4): The 'Run Tests' task command is 'python3 -m pytest tests/'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_058'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'cs301', 'project', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task_by_label(tasks_data, label):
    """Find a task entry by its label (case-insensitive)."""
    tasks_list = tasks_data.get('tasks', [])
    for task in tasks_list:
        if isinstance(task, dict) and task.get('label', '').strip().lower() == label.lower():
            return task
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tasks.json is valid JSON with version field (0.2 points)
    tasks_data = None
    try:
        tasks_data = load_jsonc(file_path)
        if isinstance(tasks_data, dict) and 'version' in tasks_data:
            print(f"PASS: Component 1 -- tasks.json is valid JSON with version='{tasks_data['version']}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- tasks.json parsed but missing 'version' field")
    except Exception as e:
        print(f"ERROR: Component 1 -- Could not parse tasks.json: {e}")

    if tasks_data is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: A task with label 'Run Tests' exists (0.2 points)
    run_tests_task = None
    try:
        run_tests_task = find_task_by_label(tasks_data, 'Run Tests')
        if run_tests_task is not None:
            print(f"PASS: Component 2 -- Found task with label 'Run Tests' (0.2 pts)")
            total_score += 0.2
        else:
            labels = [t.get('label', '<no label>') for t in tasks_data.get('tasks', []) if isinstance(t, dict)]
            print(f"FAIL: Component 2 -- No task with label 'Run Tests'. Found labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if run_tests_task is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: The 'Run Tests' task type is 'shell' (0.2 points)
    try:
        task_type = run_tests_task.get('type', '').strip().lower()
        if task_type == 'shell':
            print(f"PASS: Component 3 -- Task type is 'shell' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Expected type 'shell', found: '{run_tests_task.get('type')}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: The 'Run Tests' task command is 'python3 -m pytest tests/' (0.4 points)
    try:
        command = run_tests_task.get('command', '').strip()
        expected_command = 'python3 -m pytest tests/'
        if command == expected_command:
            print(f"PASS: Component 4 -- Command matches exactly: '{command}' (0.4 pts)")
            total_score += 0.4
        elif command.lower() == expected_command.lower():
            # Close match (case difference) -- partial credit
            print(f"PARTIAL: Component 4 -- Command case mismatch: '{command}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- Expected command '{expected_command}', found: '{command}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
