"""
Reward Script: Verify VSCode tasks.json with Docker Compose tasks
Task ID: vscode_td_027
Domain: vscode
Scoring:
  Component 1 (0.1): tasks.json exists and is valid JSON with version "2.0.0"
  Component 2 (0.3): "Docker Up" task with correct type and command
  Component 3 (0.2): "Docker Logs" task with correct type and command
  Component 4 (0.2): "Docker Logs" has isBackground: true
  Component 5 (0.2): "Docker Logs" has dependsOn including "Docker Up"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_027'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'microservices', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with Comments) by stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task_by_label(tasks, label):
    """Find a task dict by its label (case-insensitive)."""
    for t in tasks:
        if isinstance(t, dict) and t.get('label', '').strip().lower() == label.lower():
            return t
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load and parse the file
    try:
        data = load_jsonc(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks_list = data.get('tasks', [])

    # Component 1: Valid tasks.json with version "2.0.0" and tasks array (0.1 points)
    try:
        version = data.get('version', '')
        if version == '2.0.0' and isinstance(tasks_list, list) and len(tasks_list) >= 2:
            print(f"PASS: Component 1 -- valid tasks.json, version={version}, {len(tasks_list)} tasks (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- version={version}, tasks count={len(tasks_list)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: "Docker Up" task with type "shell" and command "docker-compose up -d" (0.3 points)
    try:
        up_task = find_task_by_label(tasks_list, 'Docker Up')
        if up_task is None:
            print("FAIL: Component 2 -- 'Docker Up' task not found")
        else:
            task_type = up_task.get('type', '').strip().lower()
            command = up_task.get('command', '').strip()
            type_ok = task_type == 'shell'
            cmd_ok = command == 'docker-compose up -d'
            if type_ok and cmd_ok:
                print(f"PASS: Component 2 -- Docker Up: type={task_type}, command={command} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- Docker Up: type={task_type} (expect shell), command={command} (expect 'docker-compose up -d')")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: "Docker Logs" task with type "shell" and command "docker-compose logs -f" (0.2 points)
    try:
        logs_task = find_task_by_label(tasks_list, 'Docker Logs')
        if logs_task is None:
            print("FAIL: Component 3 -- 'Docker Logs' task not found")
        else:
            task_type = logs_task.get('type', '').strip().lower()
            command = logs_task.get('command', '').strip()
            type_ok = task_type == 'shell'
            cmd_ok = command == 'docker-compose logs -f'
            if type_ok and cmd_ok:
                print(f"PASS: Component 3 -- Docker Logs: type={task_type}, command={command} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 -- Docker Logs: type={task_type} (expect shell), command={command} (expect 'docker-compose logs -f')")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: "Docker Logs" has isBackground: true (0.2 points)
    try:
        logs_task = find_task_by_label(tasks_list, 'Docker Logs')
        if logs_task is None:
            print("FAIL: Component 4 -- 'Docker Logs' task not found")
        else:
            is_bg = logs_task.get('isBackground')
            if is_bg is True:
                print(f"PASS: Component 4 -- Docker Logs isBackground={is_bg} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- Docker Logs isBackground={is_bg} (expect true)")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: "Docker Logs" has dependsOn including "Docker Up" (0.2 points)
    try:
        logs_task = find_task_by_label(tasks_list, 'Docker Logs')
        if logs_task is None:
            print("FAIL: Component 5 -- 'Docker Logs' task not found")
        else:
            depends_on = logs_task.get('dependsOn', [])
            if isinstance(depends_on, list):
                # Case-insensitive check for "Docker Up" in dependsOn
                depends_lower = [d.strip().lower() for d in depends_on if isinstance(d, str)]
                if 'docker up' in depends_lower:
                    print(f"PASS: Component 5 -- Docker Logs dependsOn={depends_on} (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 5 -- Docker Logs dependsOn={depends_on} (expect ['Docker Up'])")
            else:
                print(f"FAIL: Component 5 -- dependsOn is not a list: {depends_on}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point issues
    final_score = round(final_score, 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
