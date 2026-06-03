"""
Reward Script: Create .vscode/tasks.json with Build All, Test All, Install All tasks
Task ID: vscode_gf3_046
Domain: vscode
Scoring:
  - Component 1: tasks.json is valid JSON with version 2.0.0 and tasks array (0.1)
  - Component 2: "Build All" task exists with correct command (0.25)
  - Component 3: "Build All" is default build task (group.kind=build, isDefault=true) (0.25)
  - Component 4: "Test All" task exists with correct command (0.2)
  - Component 5: "Install All" task exists with correct command (0.2)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf3_046'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'monorepo', '.vscode', 'tasks.json')


def find_task_by_label(tasks, label):
    """Find a task object by its label (case-insensitive)."""
    for task in tasks:
        if isinstance(task, dict) and task.get('label', '').lower() == label.lower():
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
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be valid JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse JSON from {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have tasks array
    tasks = data.get('tasks', [])
    if not isinstance(tasks, list):
        print(f"CRITICAL: 'tasks' is not a list: {type(tasks)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with version "2.0.0" and non-empty tasks (0.1 points)
    try:
        version = data.get('version', '')
        if version == '2.0.0' and len(tasks) >= 3:
            print(f"PASS: Component 1 -- version is '2.0.0' and {len(tasks)} tasks found (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- version='{version}', task_count={len(tasks)} (expected '2.0.0' and >=3)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: "Build All" task with correct command (0.25 points)
    try:
        build_task = find_task_by_label(tasks, 'Build All')
        if build_task is None:
            print("FAIL: Component 2 -- 'Build All' task not found")
        else:
            cmd = build_task.get('command', '')
            # The command should contain 'npm run build' and '--workspaces'
            if 'npm run build' in cmd and '--workspaces' in cmd:
                print(f"PASS: Component 2 -- 'Build All' command: '{cmd}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- 'Build All' command '{cmd}' does not match expected 'npm run build --workspaces'")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: "Build All" is default build task (0.25 points)
    try:
        build_task = find_task_by_label(tasks, 'Build All')
        if build_task is None:
            print("FAIL: Component 3 -- 'Build All' task not found")
        else:
            group = build_task.get('group', {})
            if isinstance(group, dict):
                kind = group.get('kind', '')
                is_default = group.get('isDefault', False)
                if kind == 'build' and is_default is True:
                    print(f"PASS: Component 3 -- 'Build All' is default build task (group.kind='build', isDefault=true) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 -- group kind='{kind}', isDefault={is_default} (expected 'build', true)")
            elif isinstance(group, str) and group == 'build':
                # group can be just a string "build" but that doesn't set isDefault
                print(f"FAIL: Component 3 -- group is string 'build' but isDefault not set")
            else:
                print(f"FAIL: Component 3 -- unexpected group format: {group}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: "Test All" task with correct command (0.2 points)
    try:
        test_task = find_task_by_label(tasks, 'Test All')
        if test_task is None:
            print("FAIL: Component 4 -- 'Test All' task not found")
        else:
            cmd = test_task.get('command', '')
            # The command should contain 'npm run test', '--workspaces', and '--if-present'
            if 'npm run test' in cmd and '--workspaces' in cmd and '--if-present' in cmd:
                print(f"PASS: Component 4 -- 'Test All' command: '{cmd}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 -- 'Test All' command '{cmd}' does not match expected 'npm run test --workspaces --if-present'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: "Install All" task with correct command (0.2 points)
    try:
        install_task = find_task_by_label(tasks, 'Install All')
        if install_task is None:
            print("FAIL: Component 5 -- 'Install All' task not found")
        else:
            cmd = install_task.get('command', '')
            if cmd.strip() == 'npm install':
                print(f"PASS: Component 5 -- 'Install All' command: '{cmd}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 5 -- 'Install All' command '{cmd}' does not match expected 'npm install'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

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
