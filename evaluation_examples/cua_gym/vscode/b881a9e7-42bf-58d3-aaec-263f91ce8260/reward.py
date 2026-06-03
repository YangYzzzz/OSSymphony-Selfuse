"""
Reward Script: Configure TypeScript Watch task in tasks.json
Task ID: vscode_web_058
Domain: vscode
Scoring:
  Component 1: tasks.json exists and contains a task labeled "TypeScript Watch" (0.2 pts)
  Component 2: Task command is "npx tsc --watch --noEmit" (0.3 pts)
  Component 3: Task has isBackground: true (0.2 pts)
  Component 4: Task uses "$tsc-watch" problemMatcher (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_058'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'ts-app', '.vscode', 'tasks.json')


def load_json_with_comments(path):
    """Load a JSON file that may contain // comments (JSONC)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def find_watch_task(tasks_data):
    """Find the TypeScript Watch task in the tasks array."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        label = task.get('label', '')
        if isinstance(label, str) and label.lower() == 'typescript watch':
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
        tasks_data = load_json_with_comments(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Task labeled "TypeScript Watch" exists (0.2 points)
    try:
        watch_task = find_watch_task(tasks_data)
        if watch_task is not None:
            print(f"PASS: Component 1 -- 'TypeScript Watch' task found (0.2 pts)")
            total_score += 0.2
        else:
            labels = [t.get('label', '???') for t in tasks_data.get('tasks', [])]
            print(f"FAIL: Component 1 -- No task labeled 'TypeScript Watch'. Found labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If no watch task found, remaining components cannot pass
    if watch_task is None:
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Command is "npx tsc --watch --noEmit" (0.3 points)
    try:
        command = watch_task.get('command', '')
        if isinstance(command, str):
            # Normalize whitespace for comparison
            cmd_normalized = ' '.join(command.strip().split())
            expected_cmd = 'npx tsc --watch --noEmit'
            if cmd_normalized == expected_cmd:
                print(f"PASS: Component 2 -- command is '{command}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 -- expected command '{expected_cmd}', found '{command}'")
        else:
            print(f"FAIL: Component 2 -- command is not a string: {command}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: isBackground is true (0.2 points)
    try:
        is_background = watch_task.get('isBackground')
        if is_background is True:
            print(f"PASS: Component 3 -- isBackground is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected isBackground: true, found: {is_background}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: problemMatcher is "$tsc-watch" (0.3 points)
    try:
        matcher = watch_task.get('problemMatcher')
        # problemMatcher can be a string or an array
        if isinstance(matcher, str) and matcher == '$tsc-watch':
            print(f"PASS: Component 4 -- problemMatcher is '$tsc-watch' (0.3 pts)")
            total_score += 0.3
        elif isinstance(matcher, list) and '$tsc-watch' in matcher:
            print(f"PASS: Component 4 -- problemMatcher list contains '$tsc-watch' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 -- expected problemMatcher '$tsc-watch', found: {matcher}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
