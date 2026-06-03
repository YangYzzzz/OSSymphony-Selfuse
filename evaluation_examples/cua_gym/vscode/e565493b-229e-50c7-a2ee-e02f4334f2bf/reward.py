"""
Reward Script: Create tasks.json with jest --coverage test task and presentation options
Task ID: vscode_td_022
Domain: vscode
Scoring:
  - Component 1: tasks.json exists and is valid JSON (0.1)
  - Component 2: Task command is "jest --coverage" (0.25)
  - Component 3: Task is in the test group (0.25)
  - Component 4: presentation.reveal is "always" (0.15)
  - Component 5: presentation.panel is "dedicated" (0.15)
  - Component 6: presentation.clear is true (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_022'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'react-components', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strip // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_test_task(tasks_data):
    """Find a task that runs jest --coverage from the tasks array."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        cmd = task.get('command', '')
        # Check if command contains jest --coverage
        if 'jest' in str(cmd) and '--coverage' in str(cmd):
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON (0.1 points)
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 -- tasks.json not found at {TASKS_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0
        tasks_data = load_jsonc(TASKS_JSON_PATH)
        if isinstance(tasks_data, dict) and 'tasks' in tasks_data:
            print(f"PASS: Component 1 -- tasks.json exists and is valid JSON (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- tasks.json missing 'tasks' array")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 -- Could not parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the relevant task
    task_entry = find_test_task(tasks_data)

    # Component 2: Task command is "jest --coverage" (0.25 points)
    try:
        if task_entry is not None:
            cmd = str(task_entry.get('command', ''))
            print(f"PASS: Component 2 -- Found task with command: '{cmd}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- No task found with 'jest --coverage' command")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Task is in the test group (0.25 points)
    try:
        if task_entry is not None:
            group = task_entry.get('group', {})
            # group can be a string "test" or an object {"kind": "test", ...}
            if isinstance(group, str) and group == 'test':
                print(f"PASS: Component 3 -- Task group is 'test' (0.25 pts)")
                total_score += 0.25
            elif isinstance(group, dict) and group.get('kind') == 'test':
                print(f"PASS: Component 3 -- Task group kind is 'test' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Task group is {group}, expected test group")
        else:
            print(f"FAIL: Component 3 -- No matching task found to check group")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: presentation.reveal is "always" (0.15 points)
    try:
        if task_entry is not None:
            presentation = task_entry.get('presentation', {})
            reveal = presentation.get('reveal')
            if reveal == 'always':
                print(f"PASS: Component 4 -- presentation.reveal is 'always' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- presentation.reveal is '{reveal}', expected 'always'")
        else:
            print(f"FAIL: Component 4 -- No matching task found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: presentation.panel is "dedicated" (0.15 points)
    try:
        if task_entry is not None:
            presentation = task_entry.get('presentation', {})
            panel = presentation.get('panel')
            if panel == 'dedicated':
                print(f"PASS: Component 5 -- presentation.panel is 'dedicated' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 -- presentation.panel is '{panel}', expected 'dedicated'")
        else:
            print(f"FAIL: Component 5 -- No matching task found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: presentation.clear is true (0.10 points)
    try:
        if task_entry is not None:
            presentation = task_entry.get('presentation', {})
            clear_val = presentation.get('clear')
            if clear_val is True:
                print(f"PASS: Component 6 -- presentation.clear is true (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- presentation.clear is {clear_val}, expected true")
        else:
            print(f"FAIL: Component 6 -- No matching task found")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
