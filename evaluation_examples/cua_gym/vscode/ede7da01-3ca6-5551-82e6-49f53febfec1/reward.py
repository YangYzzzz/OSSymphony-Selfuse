"""
Reward Script: Create tasks.json with a "Hello World" shell task in .vscode folder
Task ID: vscode_td_001
Domain: vscode
Scoring:
  Component 1 (0.2): tasks.json exists, is valid JSON, has version "2.0.0"
  Component 2 (0.3): Task with label "Hello World" exists in tasks array
  Component 3 (0.2): The "Hello World" task has type "shell"
  Component 4 (0.3): The "Hello World" task has command "echo Hello World"
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_001'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'demo-app', '.vscode', 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists, is valid JSON, has version "2.0.0" (0.2 points)
    tasks_data = None
    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            content = f.read()
        tasks_data = json.loads(content)
        version = tasks_data.get('version', '')
        if version == '2.0.0':
            print(f"PASS: Component 1 — tasks.json exists, valid JSON, version is '2.0.0' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — version is '{version}', expected '2.0.0'")
    except FileNotFoundError:
        print(f"FAIL: Component 1 — tasks.json not found at {TASKS_JSON_PATH}")
        # No file means nothing else can pass
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 1 — tasks.json is not valid JSON: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the "Hello World" task in the tasks array
    hello_world_task = None
    tasks_list = tasks_data.get('tasks', []) if tasks_data else []
    for task in tasks_list:
        if isinstance(task, dict) and task.get('label') == 'Hello World':
            hello_world_task = task
            break

    # Component 2: Task with label "Hello World" exists (0.3 points)
    try:
        if hello_world_task is not None:
            print(f"PASS: Component 2 — Task with label 'Hello World' found (0.3 pts)")
            total_score += 0.3
        else:
            labels = [t.get('label', '<no label>') for t in tasks_list if isinstance(t, dict)]
            print(f"FAIL: Component 2 — No task with label 'Hello World'. Found labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Task type is "shell" (0.2 points)
    try:
        if hello_world_task is not None:
            task_type = hello_world_task.get('type', '')
            if task_type == 'shell':
                print(f"PASS: Component 3 — Task type is 'shell' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Task type is '{task_type}', expected 'shell'")
        else:
            print(f"FAIL: Component 3 — Cannot check type, 'Hello World' task not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Task command is "echo Hello World" (0.3 points)
    try:
        if hello_world_task is not None:
            command = hello_world_task.get('command', '')
            if command == 'echo Hello World':
                print(f"PASS: Component 4 — Task command is 'echo Hello World' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 4 — Task command is '{command}', expected 'echo Hello World'")
        else:
            print(f"FAIL: Component 4 — Cannot check command, 'Hello World' task not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
