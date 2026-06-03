"""
Reward Script: Create VSCode tasks.json for Python migration with env vars
Task ID: vscode_py_066
Domain: vs_code
Scoring:
  C1 (0.20) - tasks.json exists and is valid JSON with version 2.0.0 and tasks array
  C2 (0.20) - Task labeled "Run Migration" exists
  C3 (0.20) - Task command runs "python database/migrate.py"
  C4 (0.20) - options.env contains MIGRATION_MODE=upgrade
  C5 (0.20) - DATABASE_URL loaded via envFile or explicit env entry
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_066'
TASKS_JSON_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'tasks.json')


def load_tasks_json(path):
    """Load tasks.json, handling optional JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (VSCode JSONC format)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip trailing commas before } or ]
    stripped = re.sub(r',\s*([}\]])', r'\1', stripped)
    return json.loads(stripped)


def find_migration_task(tasks_data):
    """Find a task whose label matches 'Run Migration' (case-insensitive)."""
    tasks = tasks_data.get('tasks', [])
    for task in tasks:
        label = task.get('label', '')
        if label.lower() == 'run migration':
            return task
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

    # Precondition: tasks.json must be parseable
    try:
        tasks_data = load_tasks_json(TASKS_JSON_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tasks.json has valid structure with version and tasks array (0.2 pts)
    try:
        version = tasks_data.get('version', '')
        has_tasks_array = isinstance(tasks_data.get('tasks'), list) and len(tasks_data.get('tasks', [])) > 0
        if version == '2.0.0' and has_tasks_array:
            print(f"PASS: Component 1 — valid tasks.json structure (version={version}, tasks count={len(tasks_data['tasks'])}) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — version={version}, has_tasks_array={has_tasks_array}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Task labeled "Run Migration" exists (0.2 pts)
    try:
        migration_task = find_migration_task(tasks_data)
        if migration_task is not None:
            print(f"PASS: Component 2 — found task with label '{migration_task.get('label')}' (0.2 pts)")
            total_score += 0.2
        else:
            labels = [t.get('label', '<no label>') for t in tasks_data.get('tasks', [])]
            print(f"FAIL: Component 2 — no 'Run Migration' task found. Labels: {labels}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Components 3-5 require the migration task to exist
    if migration_task is None:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 3: Task command runs "python database/migrate.py" (0.2 pts)
    try:
        command = migration_task.get('command', '')
        # Normalize: strip extra whitespace, accept variations like "python3" or path forms
        cmd_lower = command.strip().lower()
        # Accept: "python database/migrate.py" or "python3 database/migrate.py"
        # Also accept with ${workspaceFolder} prefix
        valid_commands = [
            'python database/migrate.py',
            'python3 database/migrate.py',
            'python ./database/migrate.py',
            'python3 ./database/migrate.py',
        ]
        # Also check for ${workspaceFolder}-prefixed paths
        cmd_normalized = re.sub(r'\$\{workspaceFolder\}/', '', cmd_lower)
        if cmd_normalized in valid_commands or cmd_lower in valid_commands:
            print(f"PASS: Component 3 — command='{command}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — command='{command}', expected 'python database/migrate.py'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: options.env has MIGRATION_MODE=upgrade (0.2 pts)
    try:
        options = migration_task.get('options', {})
        env = options.get('env', {})
        migration_mode = env.get('MIGRATION_MODE', None)
        if migration_mode == 'upgrade':
            print(f"PASS: Component 4 — MIGRATION_MODE='{migration_mode}' in options.env (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — MIGRATION_MODE='{migration_mode}' in options.env, expected 'upgrade'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: DATABASE_URL loaded via envFile or explicit env entry (0.2 pts)
    try:
        options = migration_task.get('options', {})
        env = options.get('env', {})
        env_file = options.get('envFile', '')

        # Option A: envFile references .env (which contains DATABASE_URL)
        env_file_str = str(env_file).lower() if env_file else ''
        env_file_refs_dotenv = '.env' in env_file_str

        # Option B: DATABASE_URL explicitly set in env
        if env_file_refs_dotenv:
            print(f"PASS: Component 5 — envFile='{env_file}' loads DATABASE_URL (0.2 pts)")
            total_score += 0.2
        elif 'DATABASE_URL' in env:
            print(f"PASS: Component 5 — DATABASE_URL='{env.get('DATABASE_URL')}' in options.env (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — no envFile or DATABASE_URL in env. options={json.dumps(options)}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
