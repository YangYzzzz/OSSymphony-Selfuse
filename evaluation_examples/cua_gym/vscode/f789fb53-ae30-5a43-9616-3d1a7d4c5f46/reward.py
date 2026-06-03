"""
Reward Script: Create tasks.json with database migration tasks using promptString input
Task ID: vscode_td_034
Domain: vscode
Scoring:
  Component 1 (0.10): tasks.json exists and is valid JSON with version 2.0.0
  Component 2 (0.25): makemigrations task is shell type using ${input:migrationName}
  Component 3 (0.20): migrate task is shell type running python manage.py migrate
  Component 4 (0.20): migrate task depends on makemigrations
  Component 5 (0.25): inputs section has promptString with id migrationName
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_034'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'django-cms', '.vscode', 'tasks.json')


def load_jsonc(path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


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

    # Try to load the file
    try:
        data = load_jsonc(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tasks.json is valid with version 2.0.0 (0.10 points)
    try:
        version = data.get("version", "")
        if version == "2.0.0":
            print(f"PASS: Component 1 — version is '2.0.0' (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — expected version '2.0.0', found '{version}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Get tasks list for subsequent checks
    tasks = data.get("tasks", [])

    # Find makemigrations and migrate tasks by label (case-insensitive search)
    makemigrations_task = None
    migrate_task = None
    for t in tasks:
        label = str(t.get("label", "")).lower()
        if "makemigration" in label:
            makemigrations_task = t
        elif "migrate" in label:
            migrate_task = t

    # Component 2: makemigrations task is shell type using ${input:migrationName} (0.25 points)
    try:
        if makemigrations_task is not None:
            task_type = str(makemigrations_task.get("type", "")).lower()
            command = str(makemigrations_task.get("command", ""))
            is_shell = task_type == "shell"
            uses_input = "${input:migrationName}" in command
            has_makemigrations_cmd = "makemigrations" in command.lower()

            if is_shell and uses_input and has_makemigrations_cmd:
                print(f"PASS: Component 2 — makemigrations task is shell type with ${{input:migrationName}} (0.25 pts)")
                total_score += 0.25
            else:
                reasons = []
                if not is_shell:
                    reasons.append(f"type is '{task_type}' not 'shell'")
                if not uses_input:
                    reasons.append("command does not use ${input:migrationName}")
                if not has_makemigrations_cmd:
                    reasons.append("command does not include 'makemigrations'")
                print(f"FAIL: Component 2 — {'; '.join(reasons)}. Command: {command}")
        else:
            print(f"FAIL: Component 2 — no makemigrations task found in tasks list")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: migrate task is shell type running python manage.py migrate (0.20 points)
    try:
        if migrate_task is not None:
            task_type = str(migrate_task.get("type", "")).lower()
            command = str(migrate_task.get("command", ""))
            is_shell = task_type == "shell"
            has_migrate_cmd = "manage.py" in command and "migrate" in command.lower()

            if is_shell and has_migrate_cmd:
                print(f"PASS: Component 3 — migrate task is shell type with manage.py migrate (0.20 pts)")
                total_score += 0.20
            else:
                reasons = []
                if not is_shell:
                    reasons.append(f"type is '{task_type}' not 'shell'")
                if not has_migrate_cmd:
                    reasons.append("command does not include 'manage.py migrate'")
                print(f"FAIL: Component 3 — {'; '.join(reasons)}. Command: {command}")
        else:
            print(f"FAIL: Component 3 — no migrate task found in tasks list")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: migrate task depends on makemigrations (0.20 points)
    try:
        if migrate_task is not None:
            depends_on = migrate_task.get("dependsOn", "")
            # dependsOn can be a string or a list
            if isinstance(depends_on, str):
                depends_list = [depends_on.lower()]
            elif isinstance(depends_on, list):
                depends_list = [str(d).lower() for d in depends_on]
            else:
                depends_list = []

            has_dependency = any("makemigration" in d for d in depends_list)
            if has_dependency:
                print(f"PASS: Component 4 — migrate depends on makemigrations (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — migrate dependsOn is '{depends_on}', expected reference to makemigrations")
        else:
            print(f"FAIL: Component 4 — no migrate task found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: inputs section has promptString with id migrationName (0.25 points)
    try:
        inputs = data.get("inputs", [])
        matching_inputs = [
            inp for inp in inputs
            if str(inp.get("id", "")) == "migrationName"
            and str(inp.get("type", "")).lower() == "promptstring"
        ]

        if len(matching_inputs) > 0:
            print(f"PASS: Component 5 — inputs has promptString with id 'migrationName' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 5 — no promptString input with id 'migrationName' found. Inputs: {inputs}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
