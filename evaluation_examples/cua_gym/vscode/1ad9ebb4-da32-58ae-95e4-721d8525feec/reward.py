"""
Reward Script: Create .vscode/tasks.json with Docker Build and Docker Push tasks
Task ID: vscode_ops_035
Domain: vscode
Scoring:
  Component 1 - tasks.json exists and is valid JSON with version 2.0.0 (0.15 pts)
  Component 2 - Docker Build task with correct command (0.30 pts)
  Component 3 - Docker Push task with correct command (0.25 pts)
  Component 4 - Docker Push dependsOn Docker Build (0.30 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_035'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'myapp', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task_by_label(tasks_list, label):
    """Find a task dict by its label (case-insensitive match)."""
    for task in tasks_list:
        if isinstance(task, dict) and task.get('label', '').strip().lower() == label.lower():
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with version "2.0.0" (0.15 pts)
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 - {TASKS_JSON_PATH} does not exist")
            print("REWARD: 0.0")
            return 0.0
        data = load_jsonc(TASKS_JSON_PATH)
        if not isinstance(data, dict):
            print(f"FAIL: Component 1 - tasks.json root is not a JSON object")
            print("REWARD: 0.0")
            return 0.0
        if data.get('version') == '2.0.0':
            print(f"PASS: Component 1 - tasks.json exists with version 2.0.0 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - version is '{data.get('version')}', expected '2.0.0'")
    except (json.JSONDecodeError, Exception) as e:
        print(f"ERROR: Component 1 - Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks_list = data.get('tasks', [])
    if not isinstance(tasks_list, list):
        print(f"FAIL: 'tasks' field is not a list")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Docker Build task with correct shell command (0.30 pts)
    try:
        build_task = find_task_by_label(tasks_list, 'Docker Build')
        if build_task is None:
            print(f"FAIL: Component 2 - No task with label 'Docker Build' found")
        else:
            task_type = build_task.get('type', '').strip().lower()
            command = build_task.get('command', '').strip()
            type_ok = task_type == 'shell'
            cmd_ok = command == 'docker build -t myapp:latest .'
            if type_ok and cmd_ok:
                print(f"PASS: Component 2 - Docker Build task: type=shell, command correct (0.30 pts)")
                total_score += 0.30
            else:
                if not type_ok:
                    print(f"FAIL: Component 2 - Docker Build type is '{task_type}', expected 'shell'")
                if not cmd_ok:
                    print(f"FAIL: Component 2 - Docker Build command is '{command}', expected 'docker build -t myapp:latest .'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Docker Push task with correct shell command (0.25 pts)
    try:
        push_task = find_task_by_label(tasks_list, 'Docker Push')
        if push_task is None:
            print(f"FAIL: Component 3 - No task with label 'Docker Push' found")
        else:
            task_type = push_task.get('type', '').strip().lower()
            command = push_task.get('command', '').strip()
            type_ok = task_type == 'shell'
            cmd_ok = command == 'docker push myapp:latest'
            if type_ok and cmd_ok:
                print(f"PASS: Component 3 - Docker Push task: type=shell, command correct (0.25 pts)")
                total_score += 0.25
            else:
                if not type_ok:
                    print(f"FAIL: Component 3 - Docker Push type is '{task_type}', expected 'shell'")
                if not cmd_ok:
                    print(f"FAIL: Component 3 - Docker Push command is '{command}', expected 'docker push myapp:latest'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Docker Push dependsOn Docker Build (0.30 pts)
    try:
        push_task = find_task_by_label(tasks_list, 'Docker Push')
        if push_task is None:
            print(f"FAIL: Component 4 - No Docker Push task to check dependsOn")
        else:
            depends_on = push_task.get('dependsOn', [])
            if isinstance(depends_on, str):
                depends_on = [depends_on]
            # Check if 'Docker Build' is in dependsOn (case-insensitive)
            depends_labels = [d.strip().lower() if isinstance(d, str) else '' for d in depends_on]
            if 'docker build' in depends_labels:
                print(f"PASS: Component 4 - Docker Push dependsOn includes 'Docker Build' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 4 - Docker Push dependsOn is {depends_on}, expected to include 'Docker Build'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
