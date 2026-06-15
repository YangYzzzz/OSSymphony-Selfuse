"""
Reward Script: Create pre-launch TypeScript build task and wire into launch.json
Task ID: vscode_web_036
Domain: vscode
Scoring:
  Component 1 (0.25) — tasks.json exists with a task labeled "tsc: build"
  Component 2 (0.20) — Task command runs tsc build (npx tsc or tsc variant)
  Component 3 (0.20) — Task has problemMatcher "$tsc"
  Component 4 (0.35) — launch.json Debug Server has preLaunchTask "tsc: build"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_036'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'ts-server')
VSCODE_DIR = os.path.join(PROJECT_DIR, '.vscode')
TASKS_PATH = os.path.join(VSCODE_DIR, 'tasks.json')
LAUNCH_PATH = os.path.join(VSCODE_DIR, 'launch.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task_by_label(tasks_data, label):
    """Find a task object by its label (case-insensitive)."""
    for task in tasks_data.get('tasks', []):
        if task.get('label', '').strip().lower() == label.lower():
            return task
    return None


def find_launch_config(launch_data, name):
    """Find a launch configuration by name."""
    for config in launch_data.get('configurations', []):
        if config.get('name', '').strip() == name:
            return config
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ---- Component 1: tasks.json exists with task labeled "tsc: build" (0.25 pts) ----
    try:
        if not os.path.exists(TASKS_PATH):
            print(f"FAIL: Component 1 — tasks.json not found at {TASKS_PATH}")
            # No tasks.json means components 1-3 all fail; skip to component 4
            tasks_data = None
            task_obj = None
        else:
            tasks_data = load_jsonc(TASKS_PATH)
            task_obj = find_task_by_label(tasks_data, 'tsc: build')
            if task_obj is not None:
                print(f"PASS: Component 1 — tasks.json contains task 'tsc: build' (0.25 pts)")
                total_score += 0.25
            else:
                labels = [t.get('label', '?') for t in tasks_data.get('tasks', [])]
                print(f"FAIL: Component 1 — no task labeled 'tsc: build'; found labels: {labels}")
                task_obj = None
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        tasks_data = None
        task_obj = None

    # ---- Component 2: Task command runs tsc build (0.20 pts) ----
    try:
        if task_obj is None:
            print("FAIL: Component 2 — skipped (no task found)")
        else:
            # Accept either:
            #   type "typescript" (VSCode built-in tsc task)
            #   type "shell" with command containing "tsc" and "--build" or "-b"
            task_type = task_obj.get('type', '').lower()
            task_command = str(task_obj.get('command', '')).lower()

            if task_type == 'typescript':
                print(f"PASS: Component 2 — task type is 'typescript' (built-in tsc) (0.20 pts)")
                total_score += 0.20
            elif 'tsc' in task_command:
                print(f"PASS: Component 2 — task command contains tsc: '{task_obj.get('command')}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — task type='{task_type}', command='{task_obj.get('command', '')}'; expected tsc-related")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---- Component 3: Task has problemMatcher "$tsc" (0.20 pts) ----
    try:
        if task_obj is None:
            print("FAIL: Component 3 — skipped (no task found)")
        else:
            pm = task_obj.get('problemMatcher', None)
            # problemMatcher can be a string "$tsc" or a list ["$tsc"]
            if isinstance(pm, str):
                pm_list = [pm]
            elif isinstance(pm, list):
                pm_list = pm
            else:
                pm_list = []

            if '$tsc' in pm_list:
                print(f"PASS: Component 3 — problemMatcher includes '$tsc' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — problemMatcher is {pm}; expected '$tsc'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---- Component 4: launch.json Debug Server has preLaunchTask "tsc: build" (0.35 pts) ----
    try:
        if not os.path.exists(LAUNCH_PATH):
            print(f"FAIL: Component 4 — launch.json not found at {LAUNCH_PATH}")
        else:
            launch_data = load_jsonc(LAUNCH_PATH)
            config = find_launch_config(launch_data, 'Debug Server')
            if config is None:
                print("FAIL: Component 4 — no 'Debug Server' configuration found in launch.json")
            else:
                pre_task = config.get('preLaunchTask', None)
                if pre_task is not None and pre_task.strip().lower() == 'tsc: build':
                    print(f"PASS: Component 4 — preLaunchTask = '{pre_task}' (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 4 — preLaunchTask = '{pre_task}'; expected 'tsc: build'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
