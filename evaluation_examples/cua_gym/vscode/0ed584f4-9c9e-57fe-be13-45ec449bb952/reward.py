"""
Reward Script: Configure a Valgrind debug task in tasks.json
Task ID: vscode_lang_095
Domain: vscode
Scoring:
  - Component 1 (0.25): Task with label 'Valgrind Memcheck' exists
  - Component 2 (0.30): Command is 'valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes build/main'
  - Component 3 (0.20): Task type is 'shell'
  - Component 4 (0.25): dependsOn is 'Build C'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lang_095'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'workspace', '.vscode', 'tasks.json')


def load_tasks_json(file_path):
    """Load tasks.json, stripping JSONC comments if present."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_valgrind_task(tasks_data):
    """Find a task with label containing 'Valgrind Memcheck' (case-insensitive)."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        label = task.get('label', '')
        if label.lower() == 'valgrind memcheck':
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
        tasks_data = load_tasks_json(file_path)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Valgrind Memcheck task
    valgrind_task = find_valgrind_task(tasks_data)

    # Component 1: Task with label 'Valgrind Memcheck' exists (0.25 points)
    try:
        if valgrind_task is not None:
            print(f"PASS: Component 1 - Task 'Valgrind Memcheck' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 - No task with label 'Valgrind Memcheck' found")
            # If no Valgrind task exists at all, no other components can pass
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Command matches expected valgrind invocation (0.30 points)
    try:
        command = valgrind_task.get('command', '')
        expected_command = 'valgrind --leak-check=full --show-leak-kinds=all --track-origins=yes build/main'
        if command.strip() == expected_command:
            print(f"PASS: Component 2 - Command matches exactly (0.30 pts)")
            total_score += 0.30
        else:
            # Partial: check if valgrind with key flags is present
            has_valgrind = 'valgrind' in command.lower()
            has_leak_check = '--leak-check=full' in command
            has_show_kinds = '--show-leak-kinds=all' in command
            has_track = '--track-origins=yes' in command
            has_target = 'build/main' in command
            flags_present = sum([has_valgrind, has_leak_check, has_show_kinds, has_track, has_target])
            if flags_present >= 4:
                print(f"PARTIAL: Component 2 - Command has {flags_present}/5 expected parts: '{command}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 - Expected '{expected_command}', found '{command}'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Task type is 'shell' (0.20 points)
    try:
        task_type = valgrind_task.get('type', '')
        if task_type.lower() == 'shell':
            print(f"PASS: Component 3 - Task type is 'shell' (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 - Expected type 'shell', found '{task_type}'")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: dependsOn is 'Build C' (0.25 points)
    try:
        depends_on = valgrind_task.get('dependsOn', None)
        # dependsOn can be a string or a list
        if isinstance(depends_on, str):
            depends_match = depends_on == 'Build C'
        elif isinstance(depends_on, list):
            depends_match = 'Build C' in depends_on
        else:
            depends_match = False

        if depends_match:
            print(f"PASS: Component 4 - dependsOn is 'Build C' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 - Expected dependsOn 'Build C', found '{depends_on}'")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

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
