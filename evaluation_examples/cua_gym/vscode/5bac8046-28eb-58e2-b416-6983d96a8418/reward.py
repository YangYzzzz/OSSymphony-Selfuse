"""
Reward Script: Create tasks.json with 'npm test' task and bind to Ctrl+Shift+F10
Task ID: vscode_rrt_075
Domain: vscode
Scoring:
  Component 1 (0.25) - tasks.json exists with label 'Run Tests' and type 'shell'
  Component 2 (0.25) - tasks.json command is 'npm test' with correct test group
  Component 3 (0.25) - keybindings.json has ctrl+shift+f10 entry
  Component 4 (0.25) - keybinding maps to workbench.action.tasks.runTask with args 'Run Tests'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_075'

# Paths
WORKSPACE_DIR = os.path.join(WORKDIR, 'workspace')
TASKS_JSON_PATH = os.path.join(WORKSPACE_DIR, '.vscode', 'tasks.json')
KEYBINDINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'keybindings.json')


def load_json_with_comments(file_path):
    """Load a JSON file, stripping // comments that VSCode allows (JSONC)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    content = re.sub(r',\s*([}\]])', r'\1', content)
    return json.loads(content)


def find_task_by_label(tasks_data, label):
    """Find a task by its label in tasks.json data."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        if task.get('label', '').strip().lower() == label.strip().lower():
            return task
    return None


def find_keybinding(bindings, key_pattern):
    """Find a keybinding by key string (case-insensitive)."""
    for binding in bindings:
        if binding.get('key', '').strip().lower() == key_pattern.strip().lower():
            return binding
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # =========================================================
    # Component 1: tasks.json exists with label 'Run Tests' and type 'shell' (0.25 pts)
    # =========================================================
    task_entry = None
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 - tasks.json not found at {TASKS_JSON_PATH}")
        else:
            tasks_data = load_json_with_comments(TASKS_JSON_PATH)
            task_entry = find_task_by_label(tasks_data, 'Run Tests')
            if task_entry is None:
                print(f"FAIL: Component 1 - No task with label 'Run Tests' found. Tasks: {[t.get('label') for t in tasks_data.get('tasks', [])]}")
            elif task_entry.get('type', '').lower() != 'shell':
                print(f"FAIL: Component 1 - Task type is '{task_entry.get('type')}', expected 'shell'")
            else:
                print(f"PASS: Component 1 - tasks.json has 'Run Tests' task with type 'shell' (0.25 pts)")
                total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # =========================================================
    # Component 2: Task command is 'npm test' with group kind='test', isDefault=true (0.25 pts)
    # =========================================================
    try:
        if task_entry is None:
            print(f"FAIL: Component 2 - No 'Run Tests' task found (depends on Component 1)")
        else:
            command = task_entry.get('command', '').strip()
            group = task_entry.get('group', {})

            command_ok = command.lower() == 'npm test'
            # group can be a string or dict
            if isinstance(group, dict):
                kind_ok = group.get('kind', '').lower() == 'test'
                default_ok = group.get('isDefault') is True
            elif isinstance(group, str):
                kind_ok = group.lower() == 'test'
                default_ok = False  # string form doesn't specify isDefault
            else:
                kind_ok = False
                default_ok = False

            if command_ok and kind_ok and default_ok:
                print(f"PASS: Component 2 - command='npm test', group kind='test', isDefault=true (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not command_ok:
                    details.append(f"command='{command}' (expected 'npm test')")
                if not kind_ok:
                    details.append(f"group kind mismatch (got {group})")
                if not default_ok:
                    details.append(f"isDefault not true (got {group})")
                print(f"FAIL: Component 2 - {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # =========================================================
    # Component 3: keybindings.json has entry with key 'ctrl+shift+f10' (0.25 pts)
    # =========================================================
    kb_entry = None
    try:
        if not os.path.exists(KEYBINDINGS_PATH):
            print(f"FAIL: Component 3 - keybindings.json not found at {KEYBINDINGS_PATH}")
        else:
            bindings = load_json_with_comments(KEYBINDINGS_PATH)
            if not isinstance(bindings, list):
                print(f"FAIL: Component 3 - keybindings.json is not a list")
            else:
                kb_entry = find_keybinding(bindings, 'ctrl+shift+f10')
                if kb_entry is None:
                    keys_found = [b.get('key') for b in bindings]
                    print(f"FAIL: Component 3 - No keybinding with key 'ctrl+shift+f10'. Keys found: {keys_found}")
                else:
                    print(f"PASS: Component 3 - keybinding with key 'ctrl+shift+f10' exists (0.25 pts)")
                    total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # =========================================================
    # Component 4: Keybinding maps to runTask with args 'Run Tests' (0.25 pts)
    # =========================================================
    try:
        if kb_entry is None:
            print(f"FAIL: Component 4 - No ctrl+shift+f10 keybinding found (depends on Component 3)")
        else:
            cmd = kb_entry.get('command', '').strip()
            args = kb_entry.get('args', '')

            cmd_ok = cmd == 'workbench.action.tasks.runTask'
            # args can be a string or dict with 'task' key
            if isinstance(args, str):
                args_ok = args.strip().lower() == 'run tests'
            elif isinstance(args, dict):
                args_ok = args.get('task', '').strip().lower() == 'run tests'
            else:
                args_ok = False

            if cmd_ok and args_ok:
                print(f"PASS: Component 4 - command='workbench.action.tasks.runTask', args='Run Tests' (0.25 pts)")
                total_score += 0.25
            else:
                details = []
                if not cmd_ok:
                    details.append(f"command='{cmd}' (expected 'workbench.action.tasks.runTask')")
                if not args_ok:
                    details.append(f"args='{args}' (expected 'Run Tests')")
                print(f"FAIL: Component 4 - {'; '.join(details)}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
