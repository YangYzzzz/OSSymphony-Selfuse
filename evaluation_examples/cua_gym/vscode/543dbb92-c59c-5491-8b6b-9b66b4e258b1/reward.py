"""
Reward Script: Create tasks.json with shell task running selected text
Task ID: vscode_td_038
Domain: vs_code
Scoring:
  Component 1 (0.25) - tasks.json is valid JSON with version 2.0.0 and tasks array
  Component 2 (0.25) - Task label is "Run Selected Text"
  Component 3 (0.25) - Task type is "shell"
  Component 4 (0.25) - Command is: bash -c "${selectedText}"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_038'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'scripting', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments), stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...) that are not inside strings
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: tasks.json must exist — if not, score is 0
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Gate: tasks.json must be valid JSON
    try:
        data = load_jsonc(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid structure with version "2.0.0" and tasks array (0.25 points)
    try:
        version_ok = data.get("version") == "2.0.0"
        tasks_is_list = isinstance(data.get("tasks"), list) and len(data.get("tasks", [])) > 0
        if version_ok and tasks_is_list:
            print(f"PASS: Component 1 — version is '2.0.0' and tasks is a non-empty array (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — version={data.get('version')}, tasks type={type(data.get('tasks')).__name__}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For remaining checks, find a task that could be the target task
    tasks = data.get("tasks", [])

    # Component 2: Task with label "Run Selected Text" exists (0.25 points)
    target_task = None
    try:
        for t in tasks:
            if isinstance(t, dict) and t.get("label", "").strip().lower() == "run selected text":
                target_task = t
                break
        if target_task is not None:
            print(f"PASS: Component 2 — Found task with label 'Run Selected Text' (0.25 pts)")
            total_score += 0.25
        else:
            labels = [t.get("label") for t in tasks if isinstance(t, dict)]
            print(f"FAIL: Component 2 — No task with label 'Run Selected Text'. Found labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if target_task is None:
        # Can't check further components without the target task
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: Task type is "shell" (0.25 points)
    try:
        task_type = target_task.get("type", "")
        if task_type.strip().lower() == "shell":
            print(f"PASS: Component 3 — Task type is 'shell' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected type 'shell', found '{task_type}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Command is 'bash -c "${selectedText}"' (0.25 points)
    try:
        command = target_task.get("command", "")
        # The expected command: bash -c "${selectedText}"
        # In JSON it is stored as: bash -c \"${selectedText}\"
        # When loaded, the string value is: bash -c "${selectedText}"
        expected_command = 'bash -c "${selectedText}"'
        if command.strip() == expected_command:
            print(f"PASS: Component 4 — Command matches expected: {command} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected command '{expected_command}', found '{command}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
