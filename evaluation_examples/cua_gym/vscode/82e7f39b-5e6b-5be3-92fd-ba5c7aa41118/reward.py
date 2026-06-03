"""
Reward Script: Create tasks.json with SSH disk-check tasks and compound parallel task
Task ID: vscode_td_026
Domain: vscode
Scoring:
  - Component 1 (0.10): tasks.json exists with valid JSON structure and version 2.0.0
  - Component 2 (0.25): "Check Prod Disk" shell task with correct SSH command
  - Component 3 (0.25): "Check Staging Disk" shell task with correct SSH command
  - Component 4 (0.20): "Check All Disks" compound task depends on both individual tasks
  - Component 5 (0.10): "Check All Disks" uses parallel execution (dependsOrder)
  - Component 6 (0.10): Exactly 3 tasks total
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_026'

# The tasks.json should be inside the .vscode folder of the workspace
# Task says: VSCode is open with ~/sysadmin/scripts, so .vscode is relative to that
TASKS_JSON_PATH = os.path.join(WORKDIR, 'sysadmin', 'scripts', '.vscode', 'tasks.json')


def find_task_by_label(tasks, label):
    """Find a task in the tasks list by its label (case-insensitive)."""
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

    # Load the tasks.json file
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        data = json.loads(content)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: tasks.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: Valid JSON structure with version "2.0.0" (0.10 points)
    # This checks the tasks.json has the standard VSCode task runner version
    # On initial_env, tasks.json does NOT exist, so this fails there.
    try:
        version = data.get('version', '')
        if version == '2.0.0' and isinstance(tasks, list) and len(tasks) > 0:
            print(f"PASS: Component 1 -- version={version}, {len(tasks)} tasks found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 -- version={version}, tasks count={len(tasks)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: "Check Prod Disk" task (0.25 points)
    # Must be type "shell" with command "ssh prod-server df -h"
    try:
        prod_task = find_task_by_label(tasks, "Check Prod Disk")
        if prod_task is None:
            print("FAIL: Component 2 -- 'Check Prod Disk' task not found")
        else:
            prod_type = prod_task.get('type', '')
            prod_cmd = prod_task.get('command', '')
            if prod_type == 'shell' and prod_cmd == 'ssh prod-server df -h':
                print(f"PASS: Component 2 -- Check Prod Disk: type={prod_type}, command={prod_cmd} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Check Prod Disk: type={prod_type}, command={prod_cmd}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: "Check Staging Disk" task (0.25 points)
    # Must be type "shell" with command "ssh staging-server df -h"
    try:
        staging_task = find_task_by_label(tasks, "Check Staging Disk")
        if staging_task is None:
            print("FAIL: Component 3 -- 'Check Staging Disk' task not found")
        else:
            staging_type = staging_task.get('type', '')
            staging_cmd = staging_task.get('command', '')
            if staging_type == 'shell' and staging_cmd == 'ssh staging-server df -h':
                print(f"PASS: Component 3 -- Check Staging Disk: type={staging_type}, command={staging_cmd} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Check Staging Disk: type={staging_type}, command={staging_cmd}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: "Check All Disks" compound task depends on both individual tasks (0.20 points)
    try:
        compound_task = find_task_by_label(tasks, "Check All Disks")
        if compound_task is None:
            print("FAIL: Component 4 -- 'Check All Disks' task not found")
        else:
            depends_on = compound_task.get('dependsOn', [])
            has_prod = 'Check Prod Disk' in depends_on
            has_staging = 'Check Staging Disk' in depends_on
            if has_prod and has_staging:
                print(f"PASS: Component 4 -- Check All Disks depends on both tasks: {depends_on} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- dependsOn={depends_on}, missing: prod={not has_prod}, staging={not has_staging}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: "Check All Disks" uses parallel execution (0.10 points)
    try:
        compound_task = find_task_by_label(tasks, "Check All Disks")
        if compound_task is None:
            print("FAIL: Component 5 -- 'Check All Disks' task not found")
        else:
            depends_order = compound_task.get('dependsOrder', '')
            if depends_order == 'parallel':
                print(f"PASS: Component 5 -- dependsOrder={depends_order} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 -- dependsOrder={depends_order}, expected 'parallel'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: Exactly 3 tasks total (0.10 points)
    try:
        task_count = len(tasks)
        if task_count == 3:
            print(f"PASS: Component 6 -- exactly 3 tasks found (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 -- expected 3 tasks, found {task_count}")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
