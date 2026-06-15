"""
Reward Script: Set up a Terraform Plan task in VSCode tasks.json
Task ID: vscode_td_036
Domain: vscode
Scoring:
  Component 1 (0.25): Task label is "Terraform Plan (Staging)"
  Component 2 (0.15): Task type is "shell"
  Component 3 (0.30): Command matches expected terraform plan command
  Component 4 (0.30): options.cwd is "${workspaceFolder}/infra"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_036'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'infrastructure-repo', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (JSONC support)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task(tasks_data, label_substring):
    """Find a task by label substring (case-insensitive)."""
    for task in tasks_data.get('tasks', []):
        if isinstance(task.get('label'), str) and label_substring.lower() in task['label'].lower():
            return task
    return None


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
        tasks_data = load_jsonc(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(tasks_data.get('tasks'), list) or len(tasks_data['tasks']) == 0:
        print("CRITICAL: tasks.json has no tasks array or it is empty")
        print("REWARD: 0.0")
        return 0.0

    # Find the terraform task by label
    task = find_task(tasks_data, 'terraform plan')
    if task is None:
        # Try finding any task at all (maybe label differs)
        task = tasks_data['tasks'][0] if tasks_data['tasks'] else None
        if task is None:
            print("FAIL: No tasks found in tasks.json")
            print("REWARD: 0.0")
            return 0.0
        print(f"WARN: No task with 'terraform plan' in label, using first task: {task.get('label', 'N/A')}")

    # Component 1: Task label is "Terraform Plan (Staging)" (0.25 points)
    try:
        label = task.get('label', '')
        if isinstance(label, str) and label.strip().lower() == 'terraform plan (staging)':
            print(f"PASS: Component 1 — label is '{label}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected 'Terraform Plan (Staging)', found: '{label}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Task type is "shell" (0.15 points)
    try:
        task_type = task.get('type', '')
        if isinstance(task_type, str) and task_type.strip().lower() == 'shell':
            print(f"PASS: Component 2 — type is '{task_type}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — expected type 'shell', found: '{task_type}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Command is "terraform plan -out=tfplan -var-file=environments/staging.tfvars" (0.30 points)
    try:
        command = task.get('command', '')
        if isinstance(command, str):
            cmd_normalized = command.strip()
            expected_cmd = 'terraform plan -out=tfplan -var-file=environments/staging.tfvars'
            if cmd_normalized == expected_cmd:
                print(f"PASS: Component 3 — command matches exactly (0.30 pts)")
                total_score += 0.30
            elif 'terraform plan' in cmd_normalized and '-out=tfplan' in cmd_normalized and 'staging.tfvars' in cmd_normalized:
                # Partial credit if key parts present but not exact match
                print(f"PASS (partial): Component 3 — command contains key parts (0.15 pts)")
                print(f"  Expected: '{expected_cmd}'")
                print(f"  Found:    '{cmd_normalized}'")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — expected '{expected_cmd}', found: '{cmd_normalized}'")
        else:
            print(f"FAIL: Component 3 — command is not a string: {command}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: options.cwd is "${workspaceFolder}/infra" (0.30 points)
    try:
        options = task.get('options', {})
        cwd_value = options.get('cwd', '') if isinstance(options, dict) else ''
        if isinstance(cwd_value, str) and cwd_value.strip() == '${workspaceFolder}/infra':
            print(f"PASS: Component 4 — options.cwd is '{cwd_value}' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 4 — expected options.cwd '${'{workspaceFolder}'}/infra', found: '{cwd_value}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
