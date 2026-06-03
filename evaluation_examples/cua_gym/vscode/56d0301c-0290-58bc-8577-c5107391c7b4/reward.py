"""
Reward Script: Verify tasks.json with build and test tasks for a Rust project
Task ID: vscode_td_037
Domain: vscode
Scoring:
  - Component 1 (0.15): tasks.json exists, valid JSON, version 2.0.0, exactly 2 tasks
  - Component 2 (0.35): Build task with cargo build, group build/isDefault, problemMatcher $rustc
  - Component 3 (0.35): Test task with cargo test -- --nocapture, group test/isDefault, problemMatcher $rustc
  - Component 4 (0.15): Both tasks use shell type
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_037'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'rust-web', '.vscode', 'tasks.json')


def load_jsonc(file_path):
    """Load a JSONC file (JSON with comments) by stripping comments first."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_task_by_group_kind(tasks, kind):
    """Find a task by its group kind (build or test)."""
    for task in tasks:
        group = task.get('group', {})
        if isinstance(group, dict) and group.get('kind') == kind:
            return task
        elif isinstance(group, str) and group == kind:
            return task
    return None


def check_problem_matcher(task, expected='$rustc'):
    """Check if task has the expected problem matcher."""
    pm = task.get('problemMatcher', [])
    if isinstance(pm, str):
        return pm == expected
    elif isinstance(pm, list):
        return expected in pm
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must be valid JSON
    try:
        data = load_jsonc(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: Structure - version 2.0.0 and exactly 2 tasks (0.15 points)
    try:
        version_ok = data.get('version') == '2.0.0'
        count_ok = len(tasks) == 2
        if version_ok and count_ok:
            print(f"PASS: Component 1 -- version=2.0.0, task count=2 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- version={data.get('version')}, task count={len(tasks)}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Build task (0.35 points)
    try:
        build_task = find_task_by_group_kind(tasks, 'build')
        if build_task is None:
            print("FAIL: Component 2 -- No task with group kind 'build' found")
        else:
            c2_score = 0.0
            # Check command is cargo build
            cmd = build_task.get('command', '')
            if cmd == 'cargo build':
                c2_score += 0.15
                print(f"PASS: Component 2a -- command='cargo build'")
            else:
                print(f"FAIL: Component 2a -- expected command 'cargo build', found '{cmd}'")

            # Check group isDefault true
            group = build_task.get('group', {})
            if isinstance(group, dict) and group.get('isDefault') is True:
                c2_score += 0.10
                print(f"PASS: Component 2b -- group.isDefault=true")
            else:
                print(f"FAIL: Component 2b -- group.isDefault not true, group={group}")

            # Check problemMatcher $rustc
            if check_problem_matcher(build_task, '$rustc'):
                c2_score += 0.10
                print(f"PASS: Component 2c -- problemMatcher includes '$rustc'")
            else:
                print(f"FAIL: Component 2c -- problemMatcher missing '$rustc', found {build_task.get('problemMatcher')}")

            if c2_score > 0:
                total_score += c2_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Test task (0.35 points)
    try:
        test_task = find_task_by_group_kind(tasks, 'test')
        if test_task is None:
            print("FAIL: Component 3 -- No task with group kind 'test' found")
        else:
            c3_score = 0.0
            # Check command is cargo test -- --nocapture
            cmd = test_task.get('command', '')
            if cmd == 'cargo test -- --nocapture':
                c3_score += 0.15
                print(f"PASS: Component 3a -- command='cargo test -- --nocapture'")
            else:
                print(f"FAIL: Component 3a -- expected command 'cargo test -- --nocapture', found '{cmd}'")

            # Check group isDefault true
            group = test_task.get('group', {})
            if isinstance(group, dict) and group.get('isDefault') is True:
                c3_score += 0.10
                print(f"PASS: Component 3b -- group.isDefault=true")
            else:
                print(f"FAIL: Component 3b -- group.isDefault not true, group={group}")

            # Check problemMatcher $rustc
            if check_problem_matcher(test_task, '$rustc'):
                c3_score += 0.10
                print(f"PASS: Component 3c -- problemMatcher includes '$rustc'")
            else:
                print(f"FAIL: Component 3c -- problemMatcher missing '$rustc', found {test_task.get('problemMatcher')}")

            if c3_score > 0:
                total_score += c3_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Both tasks use shell type (0.15 points)
    try:
        build_task = find_task_by_group_kind(tasks, 'build')
        test_task = find_task_by_group_kind(tasks, 'test')
        if build_task and test_task:
            build_type = build_task.get('type', '')
            test_type = test_task.get('type', '')
            if build_type == 'shell' and test_type == 'shell':
                print(f"PASS: Component 4 -- Both tasks have type='shell' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- build type='{build_type}', test type='{test_type}'")
        else:
            print(f"FAIL: Component 4 -- Cannot check types, missing build or test task")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
