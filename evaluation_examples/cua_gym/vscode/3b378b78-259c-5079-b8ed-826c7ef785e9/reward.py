"""
Reward Script: Create a VSCode task "Format Code" that runs "black ."
Task ID: vscode_td_010
Domain: vscode
Scoring:
  Component 1 (0.2): tasks.json exists and is valid JSON with tasks array
  Component 2 (0.3): Task with label "Format Code" exists
  Component 3 (0.2): The task type is "shell"
  Component 4 (0.3): The task command is "black ."
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_010'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'data-pipeline', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, handling JSONC (comments) if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def find_task_by_label(tasks_data, label):
    """Find a task entry by its label (case-insensitive)."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        if isinstance(task, dict) and task.get('label', '').strip().lower() == label.lower():
            return task
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with tasks array (0.2 points)
    try:
        if not os.path.isfile(file_path):
            print(f"FAIL: Component 1 — tasks.json does not exist at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_tasks_json(file_path)

        if isinstance(tasks_data, dict) and 'tasks' in tasks_data and isinstance(tasks_data['tasks'], list):
            print(f"PASS: Component 1 — tasks.json is valid JSON with tasks array (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — tasks.json missing 'tasks' array. Keys found: {list(tasks_data.keys()) if isinstance(tasks_data, dict) else type(tasks_data)}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: A task with label "Format Code" exists (0.3 points)
    try:
        target_task = find_task_by_label(tasks_data, "Format Code")
        if target_task is not None:
            print(f"PASS: Component 2 — Task with label 'Format Code' found (0.3 pts)")
            total_score += 0.3
        else:
            labels = [t.get('label', '<no label>') for t in tasks_data.get('tasks', []) if isinstance(t, dict)]
            print(f"FAIL: Component 2 — No task with label 'Format Code'. Found labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The task type is "shell" (0.2 points)
    try:
        if target_task is not None:
            task_type = target_task.get('type', '').strip().lower()
            if task_type == 'shell':
                print(f"PASS: Component 3 — Task type is 'shell' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Expected type 'shell', found: '{target_task.get('type')}'")
        else:
            print(f"FAIL: Component 3 — Cannot check type; 'Format Code' task not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: The task command is "black ." (0.3 points)
    try:
        if target_task is not None:
            command = target_task.get('command', '').strip()
            # Accept "black ." or variations like "black ./"
            if command == 'black .' or command == 'black ./':
                print(f"PASS: Component 4 — Task command is '{command}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 — Expected command 'black .', found: '{command}'")
        else:
            print(f"FAIL: Component 4 — Cannot check command; 'Format Code' task not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

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
