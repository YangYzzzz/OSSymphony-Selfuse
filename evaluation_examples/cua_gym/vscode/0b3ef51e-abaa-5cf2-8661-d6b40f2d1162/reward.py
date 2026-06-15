"""
Reward Script: Security scanner VSCode task setup
Task ID: vscode_gf5_026
Domain: vscode
Scoring:
  - Component 1: src/scan.py exists and is a Python file (0.10)
  - Component 2: scan.py uses subprocess to invoke bandit (0.20)
  - Component 3: scan.py parses JSON output from bandit (0.15)
  - Component 4: scan.py reports HIGH, MEDIUM, LOW severity counts (0.15)
  - Component 5: scan.py handles non-zero exit code (no sys.exit on findings) (0.10)
  - Component 6: .vscode/tasks.json exists and is valid JSON (0.10)
  - Component 7: tasks.json has 'Security Scan' task with type 'shell' (0.20)
"""

import os
import json
import re
import ast

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_026'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'security-scanner')
SCAN_PY = os.path.join(PROJECT_DIR, 'src', 'scan.py')
TASKS_JSON = os.path.join(PROJECT_DIR, '.vscode', 'tasks.json')


def _check_security_scan_task(tasks_list):
    """Check if a Security Scan shell task exists. Returns 'pass' or 'fail'."""
    for task in tasks_list:
        label = task.get('label', '')
        task_type = task.get('type', '')
        command = task.get('command', '')
        if 'security' in label.lower() and 'scan' in label.lower():
            if task_type == 'shell' and ('scan.py' in command or 'scan' in command.lower()):
                print(f"PASS: Component 7 — 'Security Scan' task found (type=shell, cmd={command}) (0.20 pts)")
                return 'pass'
            elif task_type != 'shell':
                print(f"FAIL: Component 7 — task '{label}' has type '{task_type}', expected 'shell'")
                return 'fail'
            else:
                print(f"FAIL: Component 7 — task '{label}' command does not reference scan.py: {command}")
                return 'fail'
    labels = [t.get('label', '?') for t in tasks_list]
    print(f"FAIL: Component 7 — no 'Security Scan' task found. Tasks: {labels}")
    return 'fail'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Component 1: src/scan.py exists and is non-empty Python (0.10 points)
    # -------------------------------------------------------------------------
    scan_content = None
    try:
        if os.path.isfile(SCAN_PY):
            with open(SCAN_PY, 'r') as f:
                scan_content = f.read()
            if len(scan_content.strip()) > 20:
                print(f"PASS: Component 1 — src/scan.py exists ({len(scan_content)} chars) (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 1 — src/scan.py exists but is too short ({len(scan_content)} chars)")
        else:
            print(f"FAIL: Component 1 — src/scan.py does not exist")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if scan_content is None:
        # No scan.py, no point continuing scan.py checks
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # -------------------------------------------------------------------------
    # Component 2: scan.py uses subprocess to run bandit with -r src/ (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        uses_subprocess = 'subprocess' in scan_content
        invokes_bandit = bool(re.search(r'bandit', scan_content, re.IGNORECASE))
        scans_src = bool(re.search(r'src/', scan_content))
        if uses_subprocess and invokes_bandit and scans_src:
            print(f"PASS: Component 2 — scan.py uses subprocess to run bandit on src/ (0.20 pts)")
            total_score += 0.20
        else:
            missing = []
            if not uses_subprocess:
                missing.append('subprocess import/usage')
            if not invokes_bandit:
                missing.append('bandit invocation')
            if not scans_src:
                missing.append('src/ target')
            print(f"FAIL: Component 2 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: scan.py parses JSON output from bandit (0.15 pts)
    # Uses -f json or --format json flag AND json.loads/json.load
    # -------------------------------------------------------------------------
    try:
        uses_json_parse = bool(re.search(r'json\.loads?\(', scan_content))
        requests_json_format = bool(re.search(r'(-f|--format).*json', scan_content, re.IGNORECASE))
        # Also accept if "json" appears as an argument in a list with bandit
        requests_json_format_list = bool(re.search(r'["\']json["\']', scan_content))
        if uses_json_parse and (requests_json_format or requests_json_format_list):
            print(f"PASS: Component 3 — scan.py parses bandit JSON output (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not uses_json_parse:
                missing.append('json.loads/json.load call')
            if not (requests_json_format or requests_json_format_list):
                missing.append('-f json / --format json flag')
            print(f"FAIL: Component 3 — missing: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: scan.py reports HIGH, MEDIUM, LOW severity counts (0.15 pts)
    # The script should print/format all three severity levels
    # -------------------------------------------------------------------------
    try:
        has_high = bool(re.search(r'HIGH', scan_content))
        has_medium = bool(re.search(r'MEDIUM', scan_content))
        has_low = bool(re.search(r'LOW', scan_content))
        if has_high and has_medium and has_low:
            print(f"PASS: Component 4 — scan.py reports HIGH, MEDIUM, LOW counts (0.15 pts)")
            total_score += 0.15
        else:
            missing = []
            if not has_high:
                missing.append('HIGH')
            if not has_medium:
                missing.append('MEDIUM')
            if not has_low:
                missing.append('LOW')
            print(f"FAIL: Component 4 — missing severity levels: {', '.join(missing)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -------------------------------------------------------------------------
    # Component 5: scan.py handles non-zero exit code from bandit (0.10 pts)
    # bandit returns non-zero when findings exist. Script should NOT crash.
    # Check: does NOT have check=True for the bandit subprocess call, OR
    # wraps it in try/except CalledProcessError, OR checks returncode explicitly.
    # -------------------------------------------------------------------------
    try:
        # If check=True is used without exception handling, script would crash
        has_check_true = bool(re.search(r'check\s*=\s*True', scan_content))
        has_exception_handling = bool(re.search(r'except.*(?:CalledProcessError|subprocess|Exception)', scan_content))
        handles_returncode = bool(re.search(r'returncode|return_code', scan_content))
        captures_output = bool(re.search(r'capture_output|stdout|PIPE', scan_content))

        if not has_check_true or has_exception_handling:
            # Either doesn't use check=True (good) or catches the error (good)
            if captures_output:
                print(f"PASS: Component 5 — handles non-zero exit code from bandit (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — does not capture bandit output")
        else:
            print(f"FAIL: Component 5 — uses check=True without CalledProcessError handling")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # -------------------------------------------------------------------------
    # Component 6: .vscode/tasks.json exists and is valid JSON (0.10 pts)
    # -------------------------------------------------------------------------
    tasks_data = None
    try:
        if os.path.isfile(TASKS_JSON):
            with open(TASKS_JSON, 'r') as f:
                content = f.read()
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            tasks_data = json.loads(cleaned)
            if isinstance(tasks_data, dict):
                print(f"PASS: Component 6 — .vscode/tasks.json exists and is valid JSON (0.10 pts)")
                total_score += 0.10
        else:
            print(f"FAIL: Component 6 — .vscode/tasks.json does not exist")
    except json.JSONDecodeError as e:
        print(f"FAIL: Component 6 — tasks.json is not valid JSON: {e}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # -------------------------------------------------------------------------
    # Component 7: tasks.json has 'Security Scan' task with type 'shell' (0.20 pts)
    # -------------------------------------------------------------------------
    try:
        if tasks_data is not None:
            tasks_list = tasks_data.get('tasks', [])
            comp7_result = _check_security_scan_task(tasks_list)
            if comp7_result == 'pass':
                total_score += 0.20
        else:
            print(f"FAIL: Component 7 — tasks.json not loaded (prerequisite failed)")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
