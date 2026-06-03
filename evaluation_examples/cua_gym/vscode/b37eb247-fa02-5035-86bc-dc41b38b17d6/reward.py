"""
Reward Script: Create .vscode/tasks.json with three build/test/server tasks
Task ID: vscode_gf2_018
Domain: vscode
Scoring:
  - Component 1 (0.10): tasks.json exists, valid JSON, version 2.0.0
  - Component 2 (0.25): Build TypeScript task correct
  - Component 3 (0.20): Run Tests task correct
  - Component 4 (0.30): Start Server task correct (dependsOn, isBackground, presentation)
  - Component 5 (0.15): Exactly 3 tasks defined
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_018'

TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'node-server', '.vscode', 'tasks.json')


def load_json_with_comments(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (not inside strings - best effort)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def find_task_by_label(tasks, label):
    """Find a task dict by its label (case-insensitive)."""
    for t in tasks:
        if isinstance(t, dict) and t.get('label', '').strip().lower() == label.lower():
            return t
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist
    if not os.path.exists(TASKS_JSON_PATH):
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: tasks.json must be valid JSON
    try:
        data = load_json_with_comments(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks = data.get('tasks', [])

    # Component 1: Version is 2.0.0 (0.10 points)
    # This is task-introduced since the file doesn't exist in initial_env
    try:
        version = data.get('version', '')
        if version == '2.0.0':
            print(f"PASS: Component 1 — version is '2.0.0' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — expected version '2.0.0', found '{version}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Build TypeScript task (0.25 points)
    # Must have: label "Build TypeScript", command "npx tsc", type "shell",
    #            group.kind "build" with group.isDefault true
    try:
        bt = find_task_by_label(tasks, 'Build TypeScript')
        if bt is None:
            print("FAIL: Component 2 — 'Build TypeScript' task not found")
        else:
            sub_score = 0.0
            sub_max = 0.25
            checks_passed = 0
            total_checks = 4

            # Check command
            cmd = bt.get('command', '')
            if cmd.strip() == 'npx tsc':
                checks_passed += 1
            else:
                print(f"  FAIL: Build TypeScript command expected 'npx tsc', found '{cmd}'")

            # Check type
            task_type = bt.get('type', '')
            if task_type.lower() == 'shell':
                checks_passed += 1
            else:
                print(f"  FAIL: Build TypeScript type expected 'shell', found '{task_type}'")

            # Check group kind is build
            group = bt.get('group', {})
            if isinstance(group, dict):
                if group.get('kind', '') == 'build':
                    checks_passed += 1
                else:
                    print(f"  FAIL: Build TypeScript group.kind expected 'build', found '{group.get('kind')}'")

                # Check isDefault
                if group.get('isDefault') is True:
                    checks_passed += 1
                else:
                    print(f"  FAIL: Build TypeScript group.isDefault expected true, found '{group.get('isDefault')}'")
            elif isinstance(group, str) and group == 'build':
                # group as string means not default
                checks_passed += 1  # kind is build
                print(f"  FAIL: Build TypeScript group.isDefault expected true, but group is a string (no isDefault)")
            else:
                print(f"  FAIL: Build TypeScript group expected build group, found '{group}'")

            sub_score = sub_max * (checks_passed / total_checks)
            if checks_passed == total_checks:
                print(f"PASS: Component 2 — 'Build TypeScript' task fully correct (0.25 pts)")
            else:
                print(f"PARTIAL: Component 2 — {checks_passed}/{total_checks} checks passed ({sub_score:.3f} pts)")
            total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Run Tests task (0.20 points)
    # Must have: label "Run Tests", command "npx jest", group "test"
    try:
        rt = find_task_by_label(tasks, 'Run Tests')
        if rt is None:
            print("FAIL: Component 3 — 'Run Tests' task not found")
        else:
            checks_passed = 0
            total_checks = 2

            # Check command
            cmd = rt.get('command', '')
            if cmd.strip() == 'npx jest':
                checks_passed += 1
            else:
                print(f"  FAIL: Run Tests command expected 'npx jest', found '{cmd}'")

            # Check group is test (can be string "test" or dict with kind "test")
            group = rt.get('group', '')
            if isinstance(group, str) and group == 'test':
                checks_passed += 1
            elif isinstance(group, dict) and group.get('kind') == 'test':
                checks_passed += 1
            else:
                print(f"  FAIL: Run Tests group expected 'test', found '{group}'")

            sub_score = 0.20 * (checks_passed / total_checks)
            if checks_passed == total_checks:
                print(f"PASS: Component 3 — 'Run Tests' task fully correct (0.20 pts)")
            else:
                print(f"PARTIAL: Component 3 — {checks_passed}/{total_checks} checks passed ({sub_score:.3f} pts)")
            total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Start Server task (0.30 points)
    # Must have: label "Start Server", command "node dist/index.js",
    #            dependsOn "Build TypeScript", isBackground true,
    #            presentation.reveal "always"
    try:
        ss = find_task_by_label(tasks, 'Start Server')
        if ss is None:
            print("FAIL: Component 4 — 'Start Server' task not found")
        else:
            checks_passed = 0
            total_checks = 4

            # Check command
            cmd = ss.get('command', '')
            if cmd.strip() == 'node dist/index.js':
                checks_passed += 1
            else:
                print(f"  FAIL: Start Server command expected 'node dist/index.js', found '{cmd}'")

            # Check dependsOn
            depends = ss.get('dependsOn', '')
            # dependsOn can be a string or list
            if isinstance(depends, str) and depends == 'Build TypeScript':
                checks_passed += 1
            elif isinstance(depends, list) and 'Build TypeScript' in depends:
                checks_passed += 1
            else:
                print(f"  FAIL: Start Server dependsOn expected 'Build TypeScript', found '{depends}'")

            # Check isBackground
            if ss.get('isBackground') is True:
                checks_passed += 1
            else:
                print(f"  FAIL: Start Server isBackground expected true, found '{ss.get('isBackground')}'")

            # Check presentation.reveal
            pres = ss.get('presentation', {})
            if isinstance(pres, dict) and pres.get('reveal') == 'always':
                checks_passed += 1
            else:
                print(f"  FAIL: Start Server presentation.reveal expected 'always', found '{pres}'")

            sub_score = 0.30 * (checks_passed / total_checks)
            if checks_passed == total_checks:
                print(f"PASS: Component 4 — 'Start Server' task fully correct (0.30 pts)")
            else:
                print(f"PARTIAL: Component 4 — {checks_passed}/{total_checks} checks passed ({sub_score:.3f} pts)")
            total_score += sub_score
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Exactly 3 tasks defined (0.15 points)
    try:
        num_tasks = len(tasks)
        if num_tasks == 3:
            print(f"PASS: Component 5 — exactly 3 tasks defined (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 — expected 3 tasks, found {num_tasks}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
