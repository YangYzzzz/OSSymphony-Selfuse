"""
Reward Script: Create tasks.json with Gradle build task
Task ID: vscode_td_031
Domain: vscode
Scoring:
  Component 1 (0.25): tasks.json exists, valid JSON, version 2.0.0, tasks array present
  Component 2 (0.25): Task labeled "Gradle Build" with command "./gradlew build"
  Component 3 (0.20): problemMatcher is "$javac"
  Component 4 (0.15): presentation.reveal is "silent"
  Component 5 (0.15): Task is default build task (group.kind=build, group.isDefault=true)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_031'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'android-app', '.vscode', 'tasks.json')


def load_jsonc(file_path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_gradle_build_task(tasks_data):
    """Find the Gradle Build task in the tasks array. Case-insensitive label match."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        label = task.get('label', '')
        if isinstance(label, str) and label.lower() == 'gradle build':
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists, valid JSON, version 2.0.0, tasks array (0.25 points)
    tasks_data = None
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 — tasks.json not found at {TASKS_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        tasks_data = load_jsonc(TASKS_JSON_PATH)

        has_version = tasks_data.get('version') == '2.0.0'
        has_tasks_array = isinstance(tasks_data.get('tasks'), list) and len(tasks_data.get('tasks', [])) > 0

        if has_version and has_tasks_array:
            print(f"PASS: Component 1 — tasks.json valid, version=2.0.0, {len(tasks_data['tasks'])} task(s) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — version={tasks_data.get('version')}, tasks is list={isinstance(tasks_data.get('tasks'), list)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Gradle Build task for subsequent checks
    gradle_task = find_gradle_build_task(tasks_data)

    # Component 2: Task labeled "Gradle Build" with command "./gradlew build" (0.25 points)
    try:
        if gradle_task is None:
            print("FAIL: Component 2 — No task with label 'Gradle Build' found")
        else:
            command = gradle_task.get('command', '')
            if isinstance(command, str) and command.strip() == './gradlew build':
                print(f"PASS: Component 2 — label='Gradle Build', command='./gradlew build' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — command expected './gradlew build', found '{command}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: problemMatcher is "$javac" (0.20 points)
    try:
        if gradle_task is None:
            print("FAIL: Component 3 — No Gradle Build task found")
        else:
            matcher = gradle_task.get('problemMatcher')
            # problemMatcher can be a string or a list containing "$javac"
            matcher_ok = False
            if matcher == '$javac':
                matcher_ok = True
            elif isinstance(matcher, list) and '$javac' in matcher:
                matcher_ok = True

            if matcher_ok:
                print(f"PASS: Component 3 — problemMatcher='$javac' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — problemMatcher expected '$javac', found '{matcher}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: presentation.reveal is "silent" (0.15 points)
    try:
        if gradle_task is None:
            print("FAIL: Component 4 — No Gradle Build task found")
        else:
            presentation = gradle_task.get('presentation', {})
            reveal = presentation.get('reveal', '')
            if isinstance(reveal, str) and reveal.lower() == 'silent':
                print(f"PASS: Component 4 — presentation.reveal='silent' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — presentation.reveal expected 'silent', found '{reveal}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Task is default build task (group.kind=build, group.isDefault=true) (0.15 points)
    try:
        if gradle_task is None:
            print("FAIL: Component 5 — No Gradle Build task found")
        else:
            group = gradle_task.get('group', {})
            # group can be a string "build" or an object {"kind": "build", "isDefault": true}
            is_default_build = False
            if isinstance(group, dict):
                kind = group.get('kind', '')
                is_default = group.get('isDefault', False)
                if kind == 'build' and is_default is True:
                    is_default_build = True
            elif isinstance(group, str) and group == 'build':
                # Just "build" without isDefault — partial, but the task says "default build task"
                pass

            if is_default_build:
                print(f"PASS: Component 5 — group.kind='build', group.isDefault=true (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 5 — expected default build task, found group={group}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
