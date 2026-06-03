"""
Reward Script: Configure a tasks.json background watch task for npm run dev with webpack problem matcher
Task ID: vscode_td_035
Domain: vscode
Scoring:
  Component 1: tasks.json exists and has valid task entry (0.15)
  Component 2: Task runs npm dev script (0.15)
  Component 3: isBackground is true (0.20)
  Component 4: beginsPattern matches "Compiling..." (0.20)
  Component 5: endsPattern matches webpack compiled pattern (0.20)
  Component 6: activeOnStart is true (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_035'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'next-app', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with Comments) by stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_dev_task(tasks_data):
    """Find a task that runs the npm dev script. Returns the task dict or None."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        # Check npm type with script "dev"
        if task.get('type') == 'npm' and task.get('script') == 'dev':
            return task
        # Check shell type with "npm run dev" in command
        if task.get('type') == 'shell':
            cmd = task.get('command', '')
            if 'npm run dev' in cmd or 'npm run dev' in str(task.get('args', '')):
                return task
        # Check process type
        if task.get('type') == 'process':
            cmd = task.get('command', '')
            args = task.get('args', [])
            full_cmd = cmd + ' ' + ' '.join(args) if isinstance(args, list) else cmd
            if 'npm' in full_cmd and 'dev' in full_cmd:
                return task
    return None


def get_problem_matcher(task):
    """Extract the problem matcher from a task. Returns a dict or None.
    problemMatcher can be a string, dict, or list of dicts."""
    pm = task.get('problemMatcher')
    if isinstance(pm, dict):
        return pm
    if isinstance(pm, list) and len(pm) > 0:
        # Return the first dict matcher
        for item in pm:
            if isinstance(item, dict):
                return item
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and has valid task entry (0.15 points)
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 -- tasks.json not found at {TASKS_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_jsonc(TASKS_JSON_PATH)
        tasks_list = tasks_data.get('tasks', [])
        if not isinstance(tasks_list, list) or len(tasks_list) == 0:
            print("FAIL: Component 1 -- tasks.json has no tasks array or it is empty")
            print("REWARD: 0.0")
            return 0.0

        print(f"PASS: Component 1 -- tasks.json exists with {len(tasks_list)} task(s) (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Task runs npm dev script (0.15 points)
    dev_task = None
    try:
        dev_task = find_dev_task(tasks_data)
        if dev_task:
            print(f"PASS: Component 2 -- Found dev task (type={dev_task.get('type')}, script={dev_task.get('script', 'N/A')}) (0.15 pts)")
            total_score += 0.15
        else:
            print("FAIL: Component 2 -- No task found that runs npm dev script")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    if dev_task is None:
        # Cannot proceed with further checks without the dev task
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: isBackground is true (0.20 points)
    try:
        is_bg = dev_task.get('isBackground')
        if is_bg is True:
            print(f"PASS: Component 3 -- isBackground is true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- isBackground is {is_bg}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Extract problemMatcher for components 4-6
    pm = get_problem_matcher(dev_task)

    # Component 4: beginsPattern matches "Compiling..." (0.20 points)
    try:
        if pm is None:
            print("FAIL: Component 4 -- No problemMatcher found on dev task")
        else:
            bg = pm.get('background', {})
            begins = bg.get('beginsPattern', '')
            # beginsPattern can be a string or an object with "regexp" key
            if isinstance(begins, dict):
                begins_str = begins.get('regexp', '')
            else:
                begins_str = str(begins)

            if 'Compiling' in begins_str:
                print(f"PASS: Component 4 -- beginsPattern contains 'Compiling': '{begins_str}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- beginsPattern is '{begins_str}', expected to contain 'Compiling'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: endsPattern matches webpack compiled pattern (0.20 points)
    try:
        if pm is None:
            print("FAIL: Component 5 -- No problemMatcher found on dev task")
        else:
            bg = pm.get('background', {})
            ends = bg.get('endsPattern', '')
            # endsPattern can be a string or an object with "regexp" key
            if isinstance(ends, dict):
                ends_str = ends.get('regexp', '')
            else:
                ends_str = str(ends)

            # The pattern should match both "Compiled successfully" and "Compiled with warnings"
            # Check that it references "Compiled" and handles success/warning variants
            if 'Compiled' in ends_str and ('successfully' in ends_str or 'warning' in ends_str):
                print(f"PASS: Component 5 -- endsPattern matches compiled pattern: '{ends_str}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 -- endsPattern is '{ends_str}', expected pattern matching 'Compiled (successfully|with warnings)'")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: activeOnStart is true (0.10 points)
    try:
        if pm is None:
            print("FAIL: Component 6 -- No problemMatcher found on dev task")
        else:
            bg = pm.get('background', {})
            active = bg.get('activeOnStart')
            if active is True:
                print(f"PASS: Component 6 -- activeOnStart is true (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 -- activeOnStart is {active}, expected true")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
