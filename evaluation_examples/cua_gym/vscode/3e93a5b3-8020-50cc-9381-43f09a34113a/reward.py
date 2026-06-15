"""
Reward Script: Create tasks.json with build task for Python package distribution
Task ID: vscode_py_027
Domain: vscode
Scoring:
  Component 1 (0.15): tasks.json exists and is valid JSON with version and tasks array
  Component 2 (0.25): A task with label "Build Python Package" exists
  Component 3 (0.25): Task command is "python -m build" and type is "shell"
  Component 4 (0.35): Task group is configured as default build (kind: "build", isDefault: true)
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_027'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'workspace', '.vscode', 'tasks.json')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        with open(file_path, 'r') as f:
            data = json.load(f)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: tasks.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tasks.json has version and tasks array (0.15 points)
    try:
        has_version = "version" in data
        has_tasks = isinstance(data.get("tasks"), list) and len(data["tasks"]) > 0
        if has_version and has_tasks:
            print(f"PASS: Component 1 — tasks.json has version='{data['version']}' and {len(data['tasks'])} task(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version present: {has_version}, tasks is non-empty list: {has_tasks}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the build task by label
    tasks = data.get("tasks", [])
    build_task = None
    for t in tasks:
        if isinstance(t, dict) and t.get("label") == "Build Python Package":
            build_task = t
            break

    # Component 2: Task with label "Build Python Package" exists (0.25 points)
    try:
        if build_task is not None:
            print(f"PASS: Component 2 — Found task with label 'Build Python Package' (0.25 pts)")
            total_score += 0.25
        else:
            labels = [t.get("label", "<no label>") for t in tasks if isinstance(t, dict)]
            print(f"FAIL: Component 2 — No task labeled 'Build Python Package'. Found labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Command is "python -m build" and type is "shell" (0.25 points)
    try:
        if build_task is not None:
            cmd = build_task.get("command", "")
            task_type = build_task.get("type", "")
            cmd_ok = cmd == "python -m build"
            type_ok = task_type == "shell"
            if cmd_ok and type_ok:
                print(f"PASS: Component 3 — command='{cmd}', type='{task_type}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — command='{cmd}' (expected 'python -m build'), type='{task_type}' (expected 'shell')")
        else:
            print(f"FAIL: Component 3 — Build task not found, cannot check command/type")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Group is default build task (kind: "build", isDefault: true) (0.35 points)
    try:
        if build_task is not None:
            group = build_task.get("group", {})
            if isinstance(group, dict):
                kind_ok = group.get("kind") == "build"
                default_ok = group.get("isDefault") is True
                if kind_ok and default_ok:
                    print(f"PASS: Component 4 — group.kind='build', group.isDefault=true (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 4 — group.kind='{group.get('kind')}' (expected 'build'), group.isDefault={group.get('isDefault')} (expected true)")
            elif group == "build":
                # Partial: group is "build" string but not configured as default
                print(f"FAIL: Component 4 — group='build' (string), but expected object with kind='build' and isDefault=true")
            else:
                print(f"FAIL: Component 4 — group={group}, expected object with kind='build' and isDefault=true")
        else:
            print(f"FAIL: Component 4 — Build task not found, cannot check group")
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
