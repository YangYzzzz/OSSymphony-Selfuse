"""
Reward Script: VSCode tasks.json for C++ build/run workflow
Task ID: vscode_gf5_016
Domain: vscode
Scoring:
  - Component 1 (0.15): tasks.json exists with valid JSON and version 2.0.0
  - Component 2 (0.25): 'build' task with correct g++ command
  - Component 3 (0.25): build task has default build group and problemMatcher
  - Component 4 (0.20): 'run' task with correct command
  - Component 5 (0.15): bin/ directory and app binary exist
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_016'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'cpp-project')
TASKS_JSON = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load tasks.json — precondition for all checks
    try:
        with open(TASKS_JSON, 'r') as f:
            content = f.read()
        tasks_config = json.loads(content)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: tasks.json is not valid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tasks.json has version "2.0.0" and tasks array (0.15 pts)
    try:
        version = tasks_config.get('version')
        tasks_list = tasks_config.get('tasks')
        if version == '2.0.0' and isinstance(tasks_list, list) and len(tasks_list) >= 2:
            print(f"PASS: Component 1 — tasks.json valid with version {version} and {len(tasks_list)} tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — version={version}, tasks type={type(tasks_list).__name__}, count={len(tasks_list) if isinstance(tasks_list, list) else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Helper: find task by label
    tasks_list = tasks_config.get('tasks', [])

    def find_task(label):
        for t in tasks_list:
            if isinstance(t, dict) and t.get('label', '').lower() == label.lower():
                return t
        return None

    # Component 2: 'build' task with correct g++ command (0.25 pts)
    try:
        build_task = find_task('build')
        if build_task is None:
            print("FAIL: Component 2 — no task with label 'build' found")
        else:
            cmd = build_task.get('command', '')
            # Normalize whitespace for comparison
            cmd_normalized = ' '.join(cmd.split())
            expected_cmd = 'g++ -o bin/app src/main.cpp -std=c++17'
            if cmd_normalized == expected_cmd:
                print(f"PASS: Component 2 — build command matches: '{cmd_normalized}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — expected command '{expected_cmd}', found '{cmd_normalized}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: build task has default build group and problemMatcher '$gcc' (0.25 pts)
    try:
        build_task = find_task('build')
        if build_task is None:
            print("FAIL: Component 3 — no build task found")
        else:
            group = build_task.get('group', {})
            problem_matcher = build_task.get('problemMatcher', '')

            group_ok = False
            if isinstance(group, dict):
                group_ok = (group.get('kind') == 'build' and group.get('isDefault') is True)
            elif isinstance(group, str):
                # Some implementations use "group": "build" — but task requires isDefault: true
                group_ok = False

            matcher_ok = False
            if isinstance(problem_matcher, str):
                matcher_ok = (problem_matcher == '$gcc')
            elif isinstance(problem_matcher, list):
                matcher_ok = ('$gcc' in problem_matcher)

            if group_ok and matcher_ok:
                print(f"PASS: Component 3 — build group default=true, problemMatcher=$gcc (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — group_ok={group_ok} (group={group}), matcher_ok={matcher_ok} (matcher={problem_matcher})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: 'run' task with correct command (0.20 pts)
    try:
        run_task = find_task('run')
        if run_task is None:
            print("FAIL: Component 4 — no task with label 'run' found")
        else:
            cmd = run_task.get('command', '')
            cmd_normalized = cmd.strip()
            if cmd_normalized == './bin/app':
                print(f"PASS: Component 4 — run command matches: '{cmd_normalized}' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — expected './bin/app', found '{cmd_normalized}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: bin/ directory exists with app binary (0.15 pts)
    # This verifies the build was actually executed successfully
    try:
        bin_dir = os.path.join(PROJECT_DIR, 'bin')
        app_path = os.path.join(bin_dir, 'app')
        if os.path.isdir(bin_dir) and os.path.isfile(app_path):
            # Check it's executable
            if os.access(app_path, os.X_OK):
                print(f"PASS: Component 5 — bin/app exists and is executable (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — bin/app exists but is not executable")
        else:
            print(f"FAIL: Component 5 — bin/app not found (dir exists={os.path.isdir(bin_dir)}, file exists={os.path.isfile(app_path)})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
