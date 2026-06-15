"""
Reward Script: Create comprehensive tasks.json for Python monorepo
Task ID: vscode_td_045
Domain: vscode
Scoring:
  Component 1: tasks.json exists and is valid JSON with version 2.0.0 (0.10)
  Component 2: "Lint All" task — flake8, shell type (0.20)
  Component 3: "Test Package" task — pytest, ${input:package} ref (0.20)
  Component 4: "Build Docs" task — sphinx-build docs/ docs/_build (0.15)
  Component 5: "CI" compound task — dependsOn all three, parallel (0.20)
  Component 6: inputs section — pickString with core/api/cli options (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_045'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'python-monorepo', '.vscode', 'tasks.json')


def strip_jsonc_comments(text):
    """Strip // and /* */ comments from JSONC content."""
    text = re.sub(r'//.*$', '', text, flags=re.MULTILINE)
    text = re.sub(r'/\*.*?\*/', '', text, flags=re.DOTALL)
    return text


def get_task_by_label(tasks, label):
    """Find a task dict by its label (case-insensitive)."""
    for t in tasks:
        if t.get('label', '').lower() == label.lower():
            return t
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Load and parse tasks.json ──────────────────────────────
    try:
        with open(file_path, 'r') as f:
            raw = f.read()
        cleaned = strip_jsonc_comments(raw)
        data = json.loads(cleaned)
    except FileNotFoundError:
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks_list = data.get('tasks', [])

    # Component 1: tasks.json is valid with version 2.0.0 (0.10 pts)
    try:
        version = data.get('version', '')
        if version == '2.0.0' and len(tasks_list) >= 4:
            print(f"PASS: Component 1 — valid tasks.json, version={version}, {len(tasks_list)} tasks (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — version={version}, task count={len(tasks_list)} (need 2.0.0 and >=4)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: "Lint All" task (0.20 pts)
    try:
        lint_task = get_task_by_label(tasks_list, 'Lint All')
        if lint_task is None:
            print("FAIL: Component 2 — 'Lint All' task not found")
        else:
            is_shell = lint_task.get('type', '').lower() == 'shell'
            # Check command contains flake8 (could be in command or args)
            cmd = str(lint_task.get('command', ''))
            args = lint_task.get('args', [])
            full_cmd = cmd + ' ' + ' '.join(str(a) for a in args)
            has_flake8 = 'flake8' in full_cmd.lower()

            if is_shell and has_flake8:
                print(f"PASS: Component 2 — 'Lint All' task: shell type, flake8 command (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 2 — shell={is_shell}, flake8={has_flake8}, cmd='{full_cmd}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: "Test Package" task with pytest and ${input:package} (0.20 pts)
    try:
        test_task = get_task_by_label(tasks_list, 'Test Package')
        if test_task is None:
            print("FAIL: Component 3 — 'Test Package' task not found")
        else:
            is_shell = test_task.get('type', '').lower() == 'shell'
            cmd = str(test_task.get('command', ''))
            args = test_task.get('args', [])
            full_cmd = cmd + ' ' + ' '.join(str(a) for a in args)
            has_pytest = 'pytest' in full_cmd.lower()
            has_input_ref = '${input:package}' in full_cmd

            if is_shell and has_pytest and has_input_ref:
                print(f"PASS: Component 3 — 'Test Package' task: shell, pytest, input ref (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — shell={is_shell}, pytest={has_pytest}, input_ref={has_input_ref}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: "Build Docs" task with sphinx-build (0.15 pts)
    try:
        docs_task = get_task_by_label(tasks_list, 'Build Docs')
        if docs_task is None:
            print("FAIL: Component 4 — 'Build Docs' task not found")
        else:
            is_shell = docs_task.get('type', '').lower() == 'shell'
            cmd = str(docs_task.get('command', ''))
            args = docs_task.get('args', [])
            full_cmd = cmd + ' ' + ' '.join(str(a) for a in args)
            has_sphinx = 'sphinx-build' in full_cmd.lower() or 'sphinx' in full_cmd.lower()
            has_docs_src = 'docs/' in full_cmd or 'docs' in [str(a) for a in args]
            has_docs_build = 'docs/_build' in full_cmd

            if is_shell and has_sphinx and has_docs_build:
                print(f"PASS: Component 4 — 'Build Docs' task: shell, sphinx-build, docs/_build (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — shell={is_shell}, sphinx={has_sphinx}, docs_build={has_docs_build}, cmd='{full_cmd}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: "CI" compound task with parallel execution (0.20 pts)
    try:
        ci_task = get_task_by_label(tasks_list, 'CI')
        if ci_task is None:
            print("FAIL: Component 5 — 'CI' task not found")
        else:
            depends_on = ci_task.get('dependsOn', [])
            depends_lower = [d.lower() for d in depends_on]
            has_lint = 'lint all' in depends_lower
            has_test = 'test package' in depends_lower
            has_docs = 'build docs' in depends_lower
            is_parallel = ci_task.get('dependsOrder', '').lower() == 'parallel'

            if has_lint and has_test and has_docs and is_parallel:
                print(f"PASS: Component 5 — 'CI' compound task: depends on all 3, parallel (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 — lint={has_lint}, test={has_test}, docs={has_docs}, parallel={is_parallel}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: inputs section with pickString for package (0.15 pts)
    try:
        inputs = data.get('inputs', [])
        pkg_input = None
        for inp in inputs:
            if inp.get('id', '') == 'package':
                pkg_input = inp
                break

        if pkg_input is None:
            print("FAIL: Component 6 — no input with id='package' found")
        else:
            is_pickstring = pkg_input.get('type', '').lower() == 'pickstring'
            options = [str(o).lower() for o in pkg_input.get('options', [])]
            has_core = 'core' in options
            has_api = 'api' in options
            has_cli = 'cli' in options

            if is_pickstring and has_core and has_api and has_cli:
                print(f"PASS: Component 6 — pickString input with core/api/cli options (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 6 — pickString={is_pickstring}, core={has_core}, api={has_api}, cli={has_cli}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# ── Entry point ────────────────────────────────────────────────
if not os.path.exists(TASKS_JSON_PATH):
    print(f"File not found: {TASKS_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(TASKS_JSON_PATH)
