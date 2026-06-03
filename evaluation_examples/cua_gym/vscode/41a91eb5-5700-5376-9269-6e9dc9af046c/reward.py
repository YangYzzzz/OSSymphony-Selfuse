"""
Reward Script: Code quality dashboard workflow in ~/project
Task ID: vscode_wf_061
Domain: vs_code
Scoring:
  Component 1 (0.15): tasks.json exists and is valid JSON with version 2.0.0
  Component 2 (0.20): lint-report task with correct command and $eslint-compact problem matcher
  Component 3 (0.15): test-coverage task with coverage output to reports/coverage/
  Component 4 (0.15): count-todos task using grep to count TODO/FIXME
  Component 5 (0.20): quality-report compound task depending on all three
  Component 6 (0.15): reports/ directory structure created (reports/ and reports/coverage/)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_061'
TASKS_JSON_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'tasks.json')
REPORTS_DIR = os.path.join(WORKDIR, 'project', 'reports')
COVERAGE_DIR = os.path.join(WORKDIR, 'project', 'reports', 'coverage')


def load_tasks_json(path):
    """Load tasks.json, handling JSONC (comments) if present."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments for JSONC compatibility
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def find_task_by_label(tasks, label):
    """Find a task by its label (case-insensitive)."""
    for task in tasks:
        if task.get('label', '').lower() == label.lower():
            return task
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: tasks.json exists and is valid JSON with version 2.0.0 (0.15 points)
    tasks_data = None
    try:
        if not os.path.exists(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 -- tasks.json not found at {TASKS_JSON_PATH}")
        else:
            tasks_data = load_tasks_json(TASKS_JSON_PATH)
            if tasks_data.get('version') == '2.0.0' and isinstance(tasks_data.get('tasks'), list):
                print(f"PASS: Component 1 -- tasks.json valid with version 2.0.0, {len(tasks_data['tasks'])} tasks (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- tasks.json missing version 2.0.0 or tasks array. Got version={tasks_data.get('version')}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    if tasks_data is None:
        # Cannot proceed without tasks.json
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    tasks_list = tasks_data.get('tasks', [])

    # Component 2: lint-report task with ESLint JSON output and $eslint-compact problem matcher (0.20 points)
    try:
        lint_task = find_task_by_label(tasks_list, 'lint-report')
        if lint_task is None:
            print("FAIL: Component 2 -- No task with label 'lint-report' found")
        else:
            command = lint_task.get('command', '')
            # Check command references eslint and outputs JSON to reports/lint.json
            has_eslint = 'eslint' in command.lower()
            has_json_output = ('--format json' in command or '--format=json' in command or '-f json' in command)
            has_lint_json_path = 'reports/lint.json' in command or 'reports\\lint.json' in command

            # Check problem matcher
            pm = lint_task.get('problemMatcher', '')
            if isinstance(pm, list):
                has_eslint_matcher = any('eslint-compact' in str(m) for m in pm)
            else:
                has_eslint_matcher = 'eslint-compact' in str(pm)

            sub_score = 0.0
            if has_eslint and has_json_output and has_lint_json_path:
                sub_score += 0.10
                print(f"  PASS: lint-report command OK: {command}")
            else:
                print(f"  FAIL: lint-report command issues: eslint={has_eslint}, json_format={has_json_output}, lint_json_path={has_lint_json_path}. Command: {command}")

            if has_eslint_matcher:
                sub_score += 0.10
                print(f"  PASS: lint-report has $eslint-compact problem matcher")
            else:
                print(f"  FAIL: lint-report missing $eslint-compact problem matcher. Got: {pm}")

            if sub_score > 0:
                print(f"PASS: Component 2 -- lint-report ({sub_score} pts)")
                total_score += sub_score
            else:
                print(f"FAIL: Component 2 -- lint-report checks all failed")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: test-coverage task with coverage output to reports/coverage/ (0.15 points)
    try:
        coverage_task = find_task_by_label(tasks_list, 'test-coverage')
        if coverage_task is None:
            print("FAIL: Component 3 -- No task with label 'test-coverage' found")
        else:
            command = coverage_task.get('command', '')
            has_jest = 'jest' in command.lower()
            has_coverage = '--coverage' in command
            has_coverage_dir = 'reports/coverage' in command

            if has_jest and has_coverage and has_coverage_dir:
                print(f"PASS: Component 3 -- test-coverage task correct: {command} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- test-coverage issues: jest={has_jest}, coverage_flag={has_coverage}, coverage_dir={has_coverage_dir}. Command: {command}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: count-todos task using grep to count TODO/FIXME (0.15 points)
    try:
        todos_task = find_task_by_label(tasks_list, 'count-todos')
        if todos_task is None:
            print("FAIL: Component 4 -- No task with label 'count-todos' found")
        else:
            command = todos_task.get('command', '')
            has_grep = 'grep' in command.lower()
            has_todo = 'todo' in command.lower() or 'TODO' in command
            has_fixme = 'fixme' in command.lower() or 'FIXME' in command

            if has_grep and has_todo and has_fixme:
                print(f"PASS: Component 4 -- count-todos task correct: {command} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- count-todos issues: grep={has_grep}, todo={has_todo}, fixme={has_fixme}. Command: {command}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: quality-report compound task depending on all three subtasks (0.20 points)
    try:
        compound_task = find_task_by_label(tasks_list, 'quality-report')
        if compound_task is None:
            print("FAIL: Component 5 -- No task with label 'quality-report' found")
        else:
            depends_on = compound_task.get('dependsOn', [])
            # Normalize to lowercase for comparison
            depends_lower = [d.lower() for d in depends_on]

            has_lint = 'lint-report' in depends_lower
            has_test = 'test-coverage' in depends_lower
            has_todos = 'count-todos' in depends_lower
            is_compound = len(depends_on) >= 3

            if has_lint and has_test and has_todos and is_compound:
                print(f"PASS: Component 5 -- quality-report compound task depends on all three: {depends_on} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 5 -- quality-report dependsOn issues: lint={has_lint}, test={has_test}, todos={has_todos}, count={len(depends_on)}. dependsOn: {depends_on}")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    # Component 6: reports/ directory structure created (0.15 points)
    try:
        reports_exists = os.path.isdir(REPORTS_DIR)
        coverage_exists = os.path.isdir(COVERAGE_DIR)

        if reports_exists and coverage_exists:
            print(f"PASS: Component 6 -- reports/ and reports/coverage/ directories exist (0.15 pts)")
            total_score += 0.15
        elif reports_exists:
            print(f"PARTIAL: Component 6 -- reports/ exists but reports/coverage/ missing (0.07 pts)")
            total_score += 0.07
        else:
            print(f"FAIL: Component 6 -- reports/ directory does not exist")
    except Exception as e:
        print(f"ERROR: Component 6 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
