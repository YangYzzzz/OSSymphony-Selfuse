"""
Reward Script: Verify VSCode tasks.json with task variables
Task ID: vscode_td_032
Domain: vscode
Scoring:
  C1 (0.15) - tasks.json exists with valid JSON, version 2.0.0, and has tasks array
  C2 (0.25) - Build task with label "Build", type "shell", command "g++"
  C3 (0.20) - Build task args reference ${workspaceFolder} for source path
  C4 (0.20) - Build task output uses ${workspaceFolder}/bin/${workspaceFolderBasename}
  C5 (0.10) - Run task with label "Run" and type "shell"
  C6 (0.10) - Run task references ${workspaceFolderBasename} in command/args
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_td_032'

TASKS_JSON_PATH = os.path.join(WORKDIR, 'projects', 'myapp', '.vscode', 'tasks.json')


def strip_jsonc_comments(content):
    """Strip // and /* */ comments from JSONC content."""
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return content


def find_task_by_label(tasks, label):
    """Find a task object by its label (case-insensitive)."""
    for t in tasks:
        if isinstance(t, dict) and t.get('label', '').lower() == label.lower():
            return t
    return None


def task_has_variable_in_field(task, field, variable):
    """Check if a task's field (string or list) contains the given variable."""
    val = task.get(field)
    if isinstance(val, str) and variable in val:
        return True
    if isinstance(val, list):
        for item in val:
            if isinstance(item, str) and variable in item:
                return True
    return False


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # -----------------------------------------------------------
    # Component 1: tasks.json exists, valid JSON, version 2.0.0
    # (0.15 points)
    # -----------------------------------------------------------
    tasks_data = None
    try:
        if not os.path.isfile(TASKS_JSON_PATH):
            print(f"FAIL: Component 1 - tasks.json not found at {TASKS_JSON_PATH}")
            print("REWARD: 0.0")
            return 0.0

        with open(TASKS_JSON_PATH, 'r') as f:
            raw = f.read()

        cleaned = strip_jsonc_comments(raw)
        tasks_data = json.loads(cleaned)

        has_version = tasks_data.get('version') == '2.0.0'
        has_tasks = isinstance(tasks_data.get('tasks'), list) and len(tasks_data['tasks']) >= 2

        if has_version and has_tasks:
            print(f"PASS: Component 1 - tasks.json valid, version 2.0.0, {len(tasks_data['tasks'])} tasks (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - version={tasks_data.get('version')}, tasks count={len(tasks_data.get('tasks', []))}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 1 - Invalid JSON: {e}")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")
        print("REWARD: 0.0")
        return 0.0

    tasks_list = tasks_data.get('tasks', [])

    # -----------------------------------------------------------
    # Component 2: Build task - label "Build", type "shell", command "g++"
    # (0.25 points)
    # -----------------------------------------------------------
    build_task = None
    try:
        build_task = find_task_by_label(tasks_list, 'Build')
        if build_task is None:
            print("FAIL: Component 2 - No task with label 'Build' found")
        else:
            is_shell = build_task.get('type', '').lower() == 'shell'
            cmd = build_task.get('command', '')
            # Accept g++ anywhere in the command string
            is_gpp = 'g++' in str(cmd)

            if is_shell and is_gpp:
                print(f"PASS: Component 2 - Build task: type=shell, command contains g++ (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 - Build task: type={build_task.get('type')}, command={cmd}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # -----------------------------------------------------------
    # Component 3: Build task args use ${workspaceFolder} for source
    # (0.20 points)
    # -----------------------------------------------------------
    try:
        if build_task is None:
            print("FAIL: Component 3 - No Build task to check")
        else:
            # Check if ${workspaceFolder} appears in args or command
            has_wsf_in_args = task_has_variable_in_field(build_task, 'args', '${workspaceFolder}')
            has_wsf_in_cmd = '${workspaceFolder}' in str(build_task.get('command', ''))

            if has_wsf_in_args or has_wsf_in_cmd:
                print(f"PASS: Component 3 - Build task references ${{workspaceFolder}} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 - Build task does not reference ${{workspaceFolder}} in args or command")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # -----------------------------------------------------------
    # Component 4: Build output target is ${workspaceFolder}/bin/${workspaceFolderBasename}
    # (0.20 points)
    # -----------------------------------------------------------
    try:
        if build_task is None:
            print("FAIL: Component 4 - No Build task to check")
        else:
            # Look for the output pattern in args or command
            expected_output = '${workspaceFolder}/bin/${workspaceFolderBasename}'
            all_strings = []
            if isinstance(build_task.get('args'), list):
                all_strings.extend([str(a) for a in build_task['args']])
            if isinstance(build_task.get('command'), str):
                all_strings.append(build_task['command'])

            combined = ' '.join(all_strings)
            if expected_output in combined:
                print(f"PASS: Component 4 - Build output target: ${{workspaceFolder}}/bin/${{workspaceFolderBasename}} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 - Output target pattern not found. Combined: {combined}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    # -----------------------------------------------------------
    # Component 5: Run task exists with label "Run", type "shell"
    # (0.10 points)
    # -----------------------------------------------------------
    run_task = None
    try:
        run_task = find_task_by_label(tasks_list, 'Run')
        if run_task is None:
            print("FAIL: Component 5 - No task with label 'Run' found")
        else:
            is_shell = run_task.get('type', '').lower() == 'shell'
            if is_shell:
                print(f"PASS: Component 5 - Run task: type=shell (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 - Run task: type={run_task.get('type')}")
    except Exception as e:
        print(f"ERROR: Component 5 - {e}")

    # -----------------------------------------------------------
    # Component 6: Run task references ${workspaceFolderBasename}
    # (0.10 points)
    # -----------------------------------------------------------
    try:
        if run_task is None:
            print("FAIL: Component 6 - No Run task to check")
        else:
            has_wsfbn_cmd = '${workspaceFolderBasename}' in str(run_task.get('command', ''))
            has_wsfbn_args = task_has_variable_in_field(run_task, 'args', '${workspaceFolderBasename}')
            # Also check presentation/message fields
            pres = run_task.get('presentation', {})
            has_wsfbn_pres = '${workspaceFolderBasename}' in json.dumps(pres) if pres else False

            if has_wsfbn_cmd or has_wsfbn_args or has_wsfbn_pres:
                print(f"PASS: Component 6 - Run task references ${{workspaceFolderBasename}} (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 6 - Run task does not reference ${{workspaceFolderBasename}}")
    except Exception as e:
        print(f"ERROR: Component 6 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
