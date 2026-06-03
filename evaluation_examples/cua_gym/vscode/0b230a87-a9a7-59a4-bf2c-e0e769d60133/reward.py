"""
Reward Script: Monorepo task configuration in tasks.json
Task ID: vscode_web_071
Domain: vscode
Scoring:
  - Component 1: tasks.json exists and is valid JSON with version 2.0.0 (0.1)
  - Component 2: "Build Shared" task with correct --workspace command (0.2)
  - Component 3: "Build Frontend" task with correct command + dependsOn Shared (0.2)
  - Component 4: "Build Backend" task with correct command + dependsOn Shared (0.2)
  - Component 5: "Build All" task with dependsOn Frontend+Backend, parallel (0.3)
"""

import json
import os
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_071'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'monorepo', '.vscode', 'tasks.json')


def _strip_jsonc_comments(text):
    """Strip // and /* */ comments from JSONC content."""
    # Remove single-line comments
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    # Remove multi-line comments
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def _find_task_by_label(tasks, label):
    """Find a task by its label (case-insensitive)."""
    for task in tasks:
        if isinstance(task, dict) and task.get('label', '').lower() == label.lower():
            return task
    return None


def _check_workspace_command(task, package_name):
    """Check if a task's command uses the correct --workspace flag for the package."""
    cmd = task.get('command', '')
    # The command should contain 'npm run build' and '--workspace=packages/<name>'
    has_npm_build = 'npm' in cmd and 'build' in cmd
    has_workspace = f'--workspace=packages/{package_name}' in cmd
    return has_npm_build and has_workspace


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: tasks.json must exist and be parseable
    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            raw_content = f.read()
        # Handle JSONC (JSON with comments)
        cleaned = _strip_jsonc_comments(raw_content)
        tasks_config = json.loads(cleaned)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks_list = tasks_config.get('tasks', [])

    # Component 1: tasks.json has version "2.0.0" and contains tasks array (0.1 points)
    # This is a structural requirement that only exists in golden (initial has no tasks.json)
    try:
        version = tasks_config.get('version', '')
        has_tasks = isinstance(tasks_list, list) and len(tasks_list) >= 4
        if version == '2.0.0' and has_tasks:
            print(f"PASS: Component 1 — tasks.json version={version}, {len(tasks_list)} tasks (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — version={version}, tasks count={len(tasks_list) if isinstance(tasks_list, list) else 'N/A'}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: "Build Shared" task with npm build --workspace=packages/shared (0.2 points)
    try:
        task = _find_task_by_label(tasks_list, 'Build Shared')
        if task and _check_workspace_command(task, 'shared'):
            print(f"PASS: Component 2 — 'Build Shared' task with correct workspace command (0.2 pts)")
            total_score += 0.2
        elif task:
            print(f"FAIL: Component 2 — 'Build Shared' found but command incorrect: {task.get('command', 'N/A')}")
        else:
            print(f"FAIL: Component 2 — 'Build Shared' task not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "Build Frontend" task with correct command AND dependsOn "Build Shared" (0.2 points)
    try:
        task = _find_task_by_label(tasks_list, 'Build Frontend')
        if task:
            has_correct_cmd = _check_workspace_command(task, 'frontend')
            depends_on = task.get('dependsOn', [])
            depends_on_shared = 'Build Shared' in depends_on if isinstance(depends_on, list) else depends_on == 'Build Shared'
            if has_correct_cmd and depends_on_shared:
                print(f"PASS: Component 3 — 'Build Frontend' with correct command and dependsOn Shared (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — cmd_ok={has_correct_cmd}, depends_shared={depends_on_shared}, cmd={task.get('command','')}, dependsOn={depends_on}")
        else:
            print(f"FAIL: Component 3 — 'Build Frontend' task not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: "Build Backend" task with correct command AND dependsOn "Build Shared" (0.2 points)
    try:
        task = _find_task_by_label(tasks_list, 'Build Backend')
        if task:
            has_correct_cmd = _check_workspace_command(task, 'backend')
            depends_on = task.get('dependsOn', [])
            depends_on_shared = 'Build Shared' in depends_on if isinstance(depends_on, list) else depends_on == 'Build Shared'
            if has_correct_cmd and depends_on_shared:
                print(f"PASS: Component 4 — 'Build Backend' with correct command and dependsOn Shared (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — cmd_ok={has_correct_cmd}, depends_shared={depends_on_shared}, cmd={task.get('command','')}, dependsOn={depends_on}")
        else:
            print(f"FAIL: Component 4 — 'Build Backend' task not found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: "Build All" task with dependsOn Frontend+Backend, parallel execution (0.3 points)
    try:
        task = _find_task_by_label(tasks_list, 'Build All')
        if task:
            depends_on = task.get('dependsOn', [])
            if isinstance(depends_on, list):
                has_frontend = 'Build Frontend' in depends_on
                has_backend = 'Build Backend' in depends_on
            else:
                has_frontend = False
                has_backend = False

            # Check dependsOrder is "parallel" (or that Frontend/Backend are both listed,
            # which implies they can run in parallel after Shared completes via transitive deps)
            depends_order = task.get('dependsOrder', '')
            is_parallel = depends_order == 'parallel'

            # Award partial credit: 0.2 for correct dependsOn, 0.1 for parallel order
            if has_frontend and has_backend:
                total_score += 0.2
                print(f"PASS: Component 5a — 'Build All' dependsOn includes Frontend and Backend (0.2 pts)")
            else:
                print(f"FAIL: Component 5a — dependsOn={depends_on}, frontend={has_frontend}, backend={has_backend}")

            if is_parallel:
                total_score += 0.1
                print(f"PASS: Component 5b — 'Build All' dependsOrder is 'parallel' (0.1 pts)")
            else:
                print(f"FAIL: Component 5b — dependsOrder='{depends_order}', expected 'parallel'")
        else:
            print(f"FAIL: Component 5 — 'Build All' task not found")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
