"""
Reward Script: VSCode Custom Problem Matchers Configuration
Task ID: vscode_gf6_086
Domain: vscode
Scoring:
  C1: tasks.json exists, valid JSON, version 2.0.0 (0.10)
  C2: Build task with ERROR problemMatcher regexp + capture groups (0.25)
  C3: Lint task with WARN problemMatcher regexp + capture groups (0.25)
  C4: Compound 'Build and Lint' task referencing both (0.15)
  C5: All individual tasks use type:'shell' and cwd:'${workspaceFolder}' (0.15)
  C6: Problem matchers have fileLocation config (0.10)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf6_086'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'vscode-problem-matchers')
TASKS_JSON_PATH = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load tasks.json
    try:
        with open(TASKS_JSON_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments if present
        clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        tasks_config = json.loads(clean)
    except FileNotFoundError:
        print(f"CRITICAL: tasks.json not found at {TASKS_JSON_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse tasks.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Helper: find a task by label (case-insensitive)
    def find_task(label_lower):
        for t in tasks_config.get('tasks', []):
            if t.get('label', '').lower() == label_lower:
                return t
        return None

    # Component 1: tasks.json valid with version 2.0.0 (0.10 points)
    try:
        version = tasks_config.get('version', '')
        tasks_list = tasks_config.get('tasks', [])
        if version == '2.0.0' and len(tasks_list) >= 3:
            print(f"PASS: Component 1 - tasks.json valid, version={version}, {len(tasks_list)} tasks (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 - version={version}, tasks count={len(tasks_list)} (need 2.0.0 and >=3)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Build task with ERROR problemMatcher (0.25 points)
    try:
        build_task = find_task('build')
        if build_task is None:
            print("FAIL: Component 2 - No task with label 'Build' found")
        else:
            pm = build_task.get('problemMatcher', {})
            # problemMatcher can be a dict or a list with one dict
            if isinstance(pm, list) and len(pm) > 0:
                pm = pm[0]
            if not isinstance(pm, dict):
                print(f"FAIL: Component 2 - problemMatcher is not a dict: {type(pm)}")
            else:
                pattern = pm.get('pattern', {})
                if isinstance(pattern, list) and len(pattern) > 0:
                    pattern = pattern[0]
                regexp_str = pattern.get('regexp', '')
                # The regexp should match: ERROR: filename.py:23:10: message text
                # It needs to capture file, line, column, message
                has_error_match = 'ERROR' in regexp_str
                has_file_group = pattern.get('file') is not None
                has_line_group = pattern.get('line') is not None
                has_column_group = pattern.get('column') is not None
                has_message_group = pattern.get('message') is not None

                # Test the regex against the expected format
                try:
                    compiled = re.compile(regexp_str)
                    test_line = "ERROR: src/app.py:17:42: SyntaxError: expected colon after expression"
                    match = compiled.match(test_line)
                    regex_works = match is not None
                except Exception:
                    regex_works = False

                if has_error_match and has_file_group and has_line_group and has_column_group and has_message_group and regex_works:
                    print(f"PASS: Component 2 - Build task has valid ERROR problemMatcher (regexp={regexp_str}) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 - Build problemMatcher incomplete: error_match={has_error_match}, "
                          f"file={has_file_group}, line={has_line_group}, col={has_column_group}, "
                          f"msg={has_message_group}, regex_works={regex_works}, regexp={regexp_str}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Lint task with WARN problemMatcher (0.25 points)
    try:
        lint_task = find_task('lint')
        if lint_task is None:
            print("FAIL: Component 3 - No task with label 'Lint' found")
        else:
            pm = lint_task.get('problemMatcher', {})
            if isinstance(pm, list) and len(pm) > 0:
                pm = pm[0]
            if not isinstance(pm, dict):
                print(f"FAIL: Component 3 - problemMatcher is not a dict: {type(pm)}")
            else:
                pattern = pm.get('pattern', {})
                if isinstance(pattern, list) and len(pattern) > 0:
                    pattern = pattern[0]
                regexp_str = pattern.get('regexp', '')
                # The regexp should match: WARN [rule-name] filename.py line 15: description
                has_warn_match = 'WARN' in regexp_str
                has_file_group = pattern.get('file') is not None
                has_line_group = pattern.get('line') is not None
                has_message_group = pattern.get('message') is not None

                # Test the regex against the expected format
                try:
                    compiled = re.compile(regexp_str)
                    test_line = "WARN [missing-import] src/app.py line 1: Module 'json' is used but not imported"
                    match = compiled.match(test_line)
                    regex_works = match is not None
                except Exception:
                    regex_works = False

                if has_warn_match and has_file_group and has_line_group and has_message_group and regex_works:
                    print(f"PASS: Component 3 - Lint task has valid WARN problemMatcher (regexp={regexp_str}) (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 - Lint problemMatcher incomplete: warn_match={has_warn_match}, "
                          f"file={has_file_group}, line={has_line_group}, msg={has_message_group}, "
                          f"regex_works={regex_works}, regexp={regexp_str}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Compound 'Build and Lint' task (0.15 points)
    try:
        compound_task = find_task('build and lint')
        if compound_task is None:
            print("FAIL: Component 4 - No task with label 'Build and Lint' found")
        else:
            depends_on = compound_task.get('dependsOn', [])
            # Check it references both Build and Lint tasks
            depends_labels = [d.lower() if isinstance(d, str) else d.get('label', '').lower() for d in depends_on]
            has_build_dep = 'build' in depends_labels
            has_lint_dep = 'lint' in depends_labels

            if has_build_dep and has_lint_dep:
                print(f"PASS: Component 4 - Compound task 'Build and Lint' references both tasks (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 - Compound task dependsOn={depends_on}, missing build={not has_build_dep}, lint={not has_lint_dep}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # Component 5: Individual tasks use type:'shell' and cwd:'${workspaceFolder}' (0.15 points)
    try:
        build_task = find_task('build')
        lint_task = find_task('lint')
        checks_pass = 0
        total_checks = 0

        for task_name, task in [('Build', build_task), ('Lint', lint_task)]:
            if task is None:
                continue
            total_checks += 2

            # Check type: shell
            if task.get('type', '').lower() == 'shell':
                checks_pass += 1
            else:
                print(f"  DETAIL: {task_name} type={task.get('type')}, expected 'shell'")

            # Check cwd
            cwd = task.get('options', {}).get('cwd', '')
            if '${workspaceFolder}' in cwd or '${workspacefolder}' in cwd.lower():
                checks_pass += 1
            else:
                print(f"  DETAIL: {task_name} cwd={cwd}, expected '${{workspaceFolder}}'")

        if total_checks > 0 and checks_pass == total_checks:
            print(f"PASS: Component 5 - All tasks use type:'shell' and cwd:'${{workspaceFolder}}' (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 5 - {checks_pass}/{total_checks} checks passed")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # Component 6: Problem matchers have fileLocation config (0.10 points)
    try:
        build_task = find_task('build')
        lint_task = find_task('lint')
        fl_count = 0

        for task_name, task in [('Build', build_task), ('Lint', lint_task)]:
            if task is None:
                continue
            pm = task.get('problemMatcher', {})
            if isinstance(pm, list) and len(pm) > 0:
                pm = pm[0]
            if isinstance(pm, dict):
                fl = pm.get('fileLocation')
                if fl is not None:
                    fl_count += 1
                else:
                    print(f"  DETAIL: {task_name} problemMatcher missing fileLocation")

        # Need at least the build task to have fileLocation (it's more critical)
        if fl_count >= 1:
            print(f"PASS: Component 6 - {fl_count}/2 problem matchers have fileLocation (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 - No problem matchers have fileLocation configured")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = min(total_score, 1.0)
    # Round to avoid floating point artifacts
    final_score = round(final_score, 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
