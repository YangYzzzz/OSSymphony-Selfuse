"""
Reward Script: Create .vscode/tasks.json with 'Watch & Rebuild' tsc task
Task ID: vscode_gf2_024
Domain: vscode
Scoring:
  - Component 1 (0.15): tasks.json exists and is valid JSON with version 2.0.0
  - Component 2 (0.25): Task label, type, command, args correct
  - Component 3 (0.20): isBackground is true
  - Component 4 (0.25): problemMatcher uses $tsc-watch with background pattern
  - Component 5 (0.15): group is build, presentation.reveal is silent
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_024'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'api-server', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, handling JSONC (comments)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task(tasks_data, label):
    """Find a task by label in the tasks array."""
    for task in tasks_data.get('tasks', []):
        if task.get('label') == label:
            return task
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be valid JSON
    try:
        data = load_tasks_json(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Valid tasks.json with version 2.0.0 and a 'Watch & Rebuild' task exists (0.15 pts)
    try:
        version = data.get('version')
        task = find_task(data, 'Watch & Rebuild')
        if version == '2.0.0' and task is not None:
            print(f"PASS: Component 1 - tasks.json v2.0.0 with 'Watch & Rebuild' task found (0.15 pts)")
            total_score += 0.15
        else:
            if version != '2.0.0':
                print(f"FAIL: Component 1 - version is '{version}', expected '2.0.0'")
            if task is None:
                print(f"FAIL: Component 1 - no task with label 'Watch & Rebuild' found")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Find the task for subsequent checks
    task = find_task(data, 'Watch & Rebuild')
    if task is None:
        print("CRITICAL: 'Watch & Rebuild' task not found, cannot check remaining components")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: type=shell, command=tsc, args=[--watch, --outDir, dist] (0.25 pts)
    try:
        task_type = task.get('type')
        command = task.get('command')
        args = task.get('args', [])
        expected_args = ['--watch', '--outDir', 'dist']

        type_ok = (task_type == 'shell')
        command_ok = (command == 'tsc')
        args_ok = (args == expected_args)

        if type_ok and command_ok and args_ok:
            print(f"PASS: Component 2 - type=shell, command=tsc, args={args} (0.25 pts)")
            total_score += 0.25
        else:
            if not type_ok:
                print(f"FAIL: Component 2 - type is '{task_type}', expected 'shell'")
            if not command_ok:
                print(f"FAIL: Component 2 - command is '{command}', expected 'tsc'")
            if not args_ok:
                print(f"FAIL: Component 2 - args are {args}, expected {expected_args}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: isBackground is true (0.20 pts)
    try:
        is_bg = task.get('isBackground')
        if is_bg is True:
            print(f"PASS: Component 3 - isBackground is true (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - isBackground is {is_bg}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: problemMatcher uses $tsc-watch with background pattern (0.25 pts)
    try:
        pm = task.get('problemMatcher')
        if pm is None:
            print(f"FAIL: Component 4 - problemMatcher is missing")
        else:
            # problemMatcher can be a string, dict, or list
            pm_ok = False
            bg_ok = False

            if isinstance(pm, str):
                pm_ok = (pm == '$tsc-watch')
            elif isinstance(pm, dict):
                # Check base or direct reference
                pm_ok = (pm.get('base') == '$tsc-watch' or pm.get('name') == '$tsc-watch')
                bg = pm.get('background')
                if bg and isinstance(bg, dict):
                    # background pattern should have beginsPattern and endsPattern
                    bg_ok = ('beginsPattern' in bg and 'endsPattern' in bg)
            elif isinstance(pm, list):
                for m in pm:
                    if isinstance(m, dict) and m.get('base') == '$tsc-watch':
                        pm_ok = bool(m.get('base'))
                        bg = m.get('background')
                        if bg and isinstance(bg, dict):
                            bg_ok = ('beginsPattern' in bg and 'endsPattern' in bg)
                    elif isinstance(m, str) and m == '$tsc-watch':
                        pm_ok = bool(m)

            if pm_ok and bg_ok:
                print(f"PASS: Component 4 - problemMatcher uses $tsc-watch with background pattern (0.25 pts)")
                total_score += 0.25
            elif pm_ok and not bg_ok:
                # Partial: $tsc-watch referenced but no background pattern
                print(f"PARTIAL: Component 4 - $tsc-watch found but no background pattern (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - problemMatcher does not reference $tsc-watch: {pm}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: group=build, presentation.reveal=silent (0.15 pts)
    try:
        group = task.get('group')
        presentation = task.get('presentation', {})
        reveal = presentation.get('reveal') if isinstance(presentation, dict) else None

        # group can be string "build" or dict {"kind": "build", ...}
        group_ok = (
            (isinstance(group, str) and group == 'build') or
            (isinstance(group, dict) and group.get('kind') == 'build')
        )

        reveal_ok = (reveal == 'silent')

        if group_ok and reveal_ok:
            print(f"PASS: Component 5 - group=build, presentation.reveal=silent (0.15 pts)")
            total_score += 0.15
        else:
            if not group_ok:
                print(f"FAIL: Component 5 - group is {group}, expected 'build'")
            if not reveal_ok:
                print(f"FAIL: Component 5 - presentation.reveal is '{reveal}', expected 'silent'")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

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
