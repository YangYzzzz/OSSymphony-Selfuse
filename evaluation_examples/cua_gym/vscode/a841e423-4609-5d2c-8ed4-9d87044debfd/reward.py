"""
Reward Script: Create tasks.json with three Cargo tasks
Task ID: vscode_lang_031
Domain: vscode
Scoring:
  - Component 1 (0.15): tasks.json exists, valid JSON, version 2.0.0, 3 tasks
  - Component 2 (0.20): 'Cargo Build' task with type shell, command 'cargo build'
  - Component 3 (0.20): 'Cargo Build' has group build + isDefault true
  - Component 4 (0.20): 'Cargo Test' task with type shell, command 'cargo test', group test + isDefault true
  - Component 5 (0.25): 'Cargo Clippy' task with type shell, command 'cargo clippy -- -D warnings'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_031'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'myrustapp', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_task_by_label(tasks, label):
    """Find a task dict by its label (case-sensitive)."""
    for t in tasks:
        if t.get('label') == label:
            return t
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists, valid JSON, version 2.0.0, has 3 tasks (0.15 pts)
    try:
        data = load_jsonc(file_path)
        version_ok = data.get('version') == '2.0.0'
        tasks_list = data.get('tasks', [])
        count_ok = len(tasks_list) == 3
        if version_ok and count_ok:
            print(f"PASS: Component 1 -- tasks.json valid, version 2.0.0, 3 tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- version={data.get('version')}, task_count={len(tasks_list)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- cannot load tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: 'Cargo Build' task with type 'shell' and command 'cargo build' (0.20 pts)
    try:
        build_task = find_task_by_label(tasks_list, 'Cargo Build')
        if build_task is not None:
            type_ok = build_task.get('type') == 'shell'
            cmd_ok = build_task.get('command') == 'cargo build'
            if type_ok and cmd_ok:
                print(f"PASS: Component 2 -- 'Cargo Build' type=shell, command='cargo build' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 -- type={build_task.get('type')}, command={build_task.get('command')}")
        else:
            print(f"FAIL: Component 2 -- 'Cargo Build' task not found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: 'Cargo Build' has group build + isDefault true (0.20 pts)
    try:
        build_task = find_task_by_label(tasks_list, 'Cargo Build')
        if build_task is not None:
            group = build_task.get('group', {})
            if isinstance(group, dict):
                kind_ok = group.get('kind') == 'build'
                default_ok = group.get('isDefault') is True
                if kind_ok and default_ok:
                    print(f"PASS: Component 3 -- 'Cargo Build' is default build task (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 3 -- group kind={group.get('kind')}, isDefault={group.get('isDefault')}")
            else:
                print(f"FAIL: Component 3 -- group is not a dict with kind/isDefault, found: {group}")
        else:
            print(f"FAIL: Component 3 -- 'Cargo Build' task not found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: 'Cargo Test' task with type 'shell', command 'cargo test', group test + isDefault true (0.20 pts)
    try:
        test_task = find_task_by_label(tasks_list, 'Cargo Test')
        if test_task is not None:
            type_ok = test_task.get('type') == 'shell'
            cmd_ok = test_task.get('command') == 'cargo test'
            group = test_task.get('group', {})
            group_ok = False
            if isinstance(group, dict):
                group_ok = group.get('kind') == 'test' and group.get('isDefault') is True
            if type_ok and cmd_ok and group_ok:
                print(f"PASS: Component 4 -- 'Cargo Test' type=shell, command='cargo test', default test task (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 -- type={test_task.get('type')}, command={test_task.get('command')}, group={group}")
        else:
            print(f"FAIL: Component 4 -- 'Cargo Test' task not found")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: 'Cargo Clippy' task with type 'shell', command 'cargo clippy -- -D warnings' (0.25 pts)
    try:
        clippy_task = find_task_by_label(tasks_list, 'Cargo Clippy')
        if clippy_task is not None:
            type_ok = clippy_task.get('type') == 'shell'
            cmd_ok = clippy_task.get('command') == 'cargo clippy -- -D warnings'
            if type_ok and cmd_ok:
                print(f"PASS: Component 5 -- 'Cargo Clippy' type=shell, command='cargo clippy -- -D warnings' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 5 -- type={clippy_task.get('type')}, command={clippy_task.get('command')}")
        else:
            print(f"FAIL: Component 5 -- 'Cargo Clippy' task not found")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
