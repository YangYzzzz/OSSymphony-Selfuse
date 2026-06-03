"""
Reward Script: Configure a background watch task in tasks.json for tsc --watch
Task ID: vscode_td_016
Domain: vscode
Scoring:
  Component 1: tasks.json exists and is valid JSON with a task (0.10)
  Component 2: Task command runs tsc --watch (0.20)
  Component 3: isBackground is true (0.20)
  Component 4: problemMatcher has background section with activeOnStart (0.15)
  Component 5: problemMatcher background has beginsPattern (0.15)
  Component 6: problemMatcher background has endsPattern (0.20)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_016'
TASKS_PATH = os.path.join(WORKDIR, 'projects', 'ts-lib', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (VSCode JSONC format)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_watch_task(tasks_data):
    """Find a task that runs tsc --watch among the tasks list."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        cmd = task.get('command', '')
        args = task.get('args', [])
        # Check if the task runs tsc --watch in various forms
        # Form 1: command="tsc", args=["--watch"]
        if 'tsc' in str(cmd).lower() and '--watch' in [str(a).lower() for a in args]:
            return task
        # Form 2: command="tsc --watch" (single string)
        if 'tsc' in str(cmd).lower() and '--watch' in str(cmd).lower():
            return task
        # Form 3: Check label or other indicators
        # Also check shell type commands where command might be full string
        if task.get('type') == 'shell':
            full_cmd = str(cmd) + ' ' + ' '.join(str(a) for a in args)
            if 'tsc' in full_cmd.lower() and '--watch' in full_cmd.lower():
                return task
    return None


def get_problem_matcher(task):
    """Extract the problem matcher, handling both string and object forms."""
    pm = task.get('problemMatcher', None)
    if pm is None:
        return None
    # problemMatcher can be a string like "$tsc-watch", an object, or a list
    if isinstance(pm, str):
        return pm
    if isinstance(pm, list):
        # Return first object matcher that has background, or first item
        for item in pm:
            if isinstance(item, dict) and 'background' in item:
                return item
        return pm[0] if pm else None
    if isinstance(pm, dict):
        return pm
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with tasks array (0.10 points)
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — tasks.json does not exist at {file_path}")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_jsonc(file_path)
        tasks_list = tasks_data.get('tasks', [])
        if isinstance(tasks_list, list) and len(tasks_list) > 0:
            print(f"PASS: Component 1 — tasks.json valid with {len(tasks_list)} task(s) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — tasks.json has no tasks array or it is empty")
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Task command runs tsc --watch (0.20 points)
    watch_task = None
    try:
        watch_task = find_watch_task(tasks_data)
        if watch_task:
            print(f"PASS: Component 2 — Found tsc --watch task (label: {watch_task.get('label', 'N/A')}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — No task found that runs tsc --watch")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    if watch_task is None:
        # Cannot proceed with further checks without the watch task
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 3: isBackground is true (0.20 points)
    try:
        is_bg = watch_task.get('isBackground', None)
        if is_bg is True:
            print(f"PASS: Component 3 — isBackground is true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — isBackground is {is_bg}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Get problem matcher for remaining checks
    pm = get_problem_matcher(watch_task)

    # Handle $tsc-watch string matcher — it is a built-in that includes background patterns
    is_builtin_tsc_watch = isinstance(pm, str) and pm.lower() in ('$tsc-watch',)

    # Component 4: problemMatcher has background section with activeOnStart (0.15 points)
    try:
        if is_builtin_tsc_watch:
            # $tsc-watch is a built-in matcher with background support
            print(f"PASS: Component 4 — Uses built-in $tsc-watch matcher which includes background/activeOnStart (0.15 pts)")
            total_score += 0.15
        elif isinstance(pm, dict):
            bg = pm.get('background', None)
            if isinstance(bg, dict):
                aos = bg.get('activeOnStart', None)
                if aos is True:
                    print(f"PASS: Component 4 — background.activeOnStart is true (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 4 — background.activeOnStart is {aos}, expected true")
            else:
                print(f"FAIL: Component 4 — problemMatcher has no 'background' section")
        else:
            print(f"FAIL: Component 4 — problemMatcher is not an object or recognized built-in: {type(pm)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: problemMatcher background has beginsPattern (0.15 points)
    try:
        if is_builtin_tsc_watch:
            print(f"PASS: Component 5 — $tsc-watch built-in includes beginsPattern (0.15 pts)")
            total_score += 0.15
        elif isinstance(pm, dict):
            bg = pm.get('background', {})
            begins = bg.get('beginsPattern', None)
            if begins is not None and str(begins).strip():
                # beginsPattern can be a string or an object with "regexp" key
                pattern_str = begins if isinstance(begins, str) else begins.get('regexp', '')
                print(f"PASS: Component 5 — beginsPattern found: {pattern_str[:80]}... (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — No beginsPattern in background section")
        else:
            print(f"FAIL: Component 5 — Cannot check beginsPattern without object problemMatcher")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: problemMatcher background has endsPattern (0.20 points)
    try:
        if is_builtin_tsc_watch:
            print(f"PASS: Component 6 — $tsc-watch built-in includes endsPattern (0.20 pts)")
            total_score += 0.20
        elif isinstance(pm, dict):
            bg = pm.get('background', {})
            ends = bg.get('endsPattern', None)
            if ends is not None and str(ends).strip():
                pattern_str = ends if isinstance(ends, str) else ends.get('regexp', '')
                print(f"PASS: Component 6 — endsPattern found: {pattern_str[:80]}... (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 6 — No endsPattern in background section")
        else:
            print(f"FAIL: Component 6 — Cannot check endsPattern without object problemMatcher")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(TASKS_PATH):
    print(f"File not found: {TASKS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_PATH)
