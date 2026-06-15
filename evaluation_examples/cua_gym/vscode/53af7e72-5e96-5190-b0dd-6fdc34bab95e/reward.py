"""
Reward Script: Create VSCode tasks.json for Ansible deployment
Task ID: vscode_td_018
Domain: vscode
Scoring:
  - Component 1 (0.2): tasks.json exists and is valid JSON with tasks array
  - Component 2 (0.3): Task command matches "ansible-playbook -i inventory.yml deploy.yml"
  - Component 3 (0.3): options.cwd is "${workspaceFolder}/ops"
  - Component 4 (0.2): Task type is "shell"
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_018'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'infrastructure', '.vscode', 'tasks.json')

EXPECTED_COMMAND = 'ansible-playbook -i inventory.yml deploy.yml'
EXPECTED_CWD = '${workspaceFolder}/ops'
EXPECTED_TYPE = 'shell'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    tasks_data = None

    # Component 1: tasks.json exists and is valid JSON with a tasks array (0.2 points)
    try:
        with open(file_path, 'r') as f:
            tasks_data = json.load(f)
        if isinstance(tasks_data, dict) and isinstance(tasks_data.get('tasks'), list) and len(tasks_data['tasks']) > 0:
            print(f"PASS: Component 1 - tasks.json is valid JSON with {len(tasks_data['tasks'])} task(s) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 - tasks.json missing 'tasks' array or it is empty")
    except FileNotFoundError:
        print(f"FAIL: Component 1 - tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 - tasks.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    if tasks_data is None or not isinstance(tasks_data.get('tasks'), list) or len(tasks_data['tasks']) == 0:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Find the target task - look for the one with the ansible-playbook command
    target_task = None
    for task in tasks_data['tasks']:
        cmd = task.get('command', '')
        if 'ansible-playbook' in str(cmd):
            target_task = task
            break
    # If no ansible task found, just use first task
    if target_task is None:
        target_task = tasks_data['tasks'][0]

    # Component 2: Task command matches expected (0.3 points)
    try:
        actual_command = target_task.get('command', '')
        if str(actual_command).strip() == EXPECTED_COMMAND:
            print(f"PASS: Component 2 - command is '{actual_command}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - expected command '{EXPECTED_COMMAND}', found '{actual_command}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: options.cwd is "${workspaceFolder}/ops" (0.3 points)
    try:
        options = target_task.get('options', {})
        actual_cwd = options.get('cwd', '') if isinstance(options, dict) else ''
        if str(actual_cwd).strip() == EXPECTED_CWD:
            print(f"PASS: Component 3 - options.cwd is '{actual_cwd}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - expected cwd '{EXPECTED_CWD}', found '{actual_cwd}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Task type is "shell" (0.2 points)
    try:
        actual_type = target_task.get('type', '')
        if str(actual_type).strip() == EXPECTED_TYPE:
            print(f"PASS: Component 4 - type is '{actual_type}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 - expected type '{EXPECTED_TYPE}', found '{actual_type}'")
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
