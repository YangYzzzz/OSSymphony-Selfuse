"""
Reward Script: VSCode ShellCheck setup and shell script fixes
Task ID: vscode_cm_062
Domain: vscode (libreoffice_calc listed but actually vscode task)
Scoring:
  Component 1: ShellCheck extension installed          — 0.20 points
  Component 2: SC2006 fixed ($() instead of backticks) — 0.25 points
  Component 3: SC2086 fixed (double-quoted variables)  — 0.25 points
  Component 4: SC2164 fixed (cd with || exit)          — 0.15 points
  Component 5: tasks.json with shellcheck task exists  — 0.15 points
  Total: 1.0
"""

import os
import re
import json
import glob as glob_mod

WORKDIR = '/home/user'
TASK_ID = 'vscode_cm_062'
DEPLOY_SH = os.path.join(WORKDIR, 'projects', 'deployment', 'deploy.sh')
TASKS_JSON = os.path.join(WORKDIR, 'projects', 'deployment', '.vscode', 'tasks.json')
EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ── Component 1: ShellCheck extension installed (0.20 pts) ──
    try:
        # Check for shellcheck extension directory in ~/.vscode/extensions/
        ext_dirs = os.listdir(EXTENSIONS_DIR) if os.path.isdir(EXTENSIONS_DIR) else []
        shellcheck_found = any(
            'shellcheck' in d.lower() and os.path.isdir(os.path.join(EXTENSIONS_DIR, d))
            for d in ext_dirs
            if d != 'extensions.json'
        )
        if shellcheck_found:
            print(f"PASS: Component 1 — ShellCheck extension directory found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — ShellCheck extension not found in {EXTENSIONS_DIR}. Dirs: {ext_dirs}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ── Load deploy.sh for components 2-4 ──
    try:
        with open(DEPLOY_SH, 'r') as f:
            deploy_content = f.read()
        deploy_lines = deploy_content.split('\n')
    except Exception as e:
        print(f"CRITICAL: Cannot read {DEPLOY_SH}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ── Component 2: SC2006 fixed — no backtick command substitution (0.25 pts) ──
    # In the initial file, backticks are used for command substitution like `date ...`
    # The fix replaces all backtick command substitution with $()
    try:
        # Find backtick command substitutions (not inside comments or echo strings)
        # We look for patterns like VARIABLE=`command` which is the SC2006 pattern
        backtick_assignments = []
        for i, line in enumerate(deploy_lines, 1):
            stripped = line.strip()
            # Skip comments
            if stripped.startswith('#'):
                continue
            # Check for backtick command substitution (variable=`...` pattern)
            if re.search(r'=`[^`]+`', line):
                backtick_assignments.append((i, stripped))

        if len(backtick_assignments) == 0:
            # Also verify $() is actually used instead (positive check)
            dollar_paren_subs = re.findall(r'=\$\([^)]+\)', deploy_content)
            if len(dollar_paren_subs) >= 3:
                # Original had 5 backtick assignments; at least 3 should now be $()
                print(f"PASS: Component 2 — SC2006 fixed: no backtick substitutions, found {len(dollar_paren_subs)} $() substitutions (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — No backticks but only {len(dollar_paren_subs)} $() substitutions found (expected >=3)")
        else:
            print(f"FAIL: Component 2 — SC2006 not fixed: {len(backtick_assignments)} backtick substitution(s) remain: {backtick_assignments[:3]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ── Component 3: SC2086 fixed — variables are double-quoted (0.25 pts) ──
    # Key lines that need quoting: mkdir -p, cp -r, cd, if [ -f ... ], if [ -d ... ], systemctl
    try:
        unquoted_count = 0
        lines_to_check = []

        for i, line in enumerate(deploy_lines, 1):
            stripped = line.strip()
            # Skip comments and empty lines
            if stripped.startswith('#') or not stripped:
                continue
            # Skip echo lines and lines that only set variables
            if stripped.startswith('echo') or stripped.startswith('set '):
                continue

            # Check for unquoted variable usage in commands (not in variable assignments)
            # Look for $VAR or ${VAR} not inside quotes in command arguments
            # Specific patterns from the task: mkdir -p $VAR, cp -r $VAR, cd $VAR, [ -f $VAR ], systemctl restart $VAR
            if re.search(r'(mkdir|cp|cd|systemctl|\[ -[fd])\s+[^"]*\$\w+', line):
                # Make sure the variable isn't already inside quotes
                # Simple heuristic: if $VAR appears and is not between double-quotes
                # Check if the variable references are quoted
                if not re.search(r'"[^"]*\$', line):
                    unquoted_count += 1
                    lines_to_check.append((i, stripped))

        if unquoted_count == 0:
            # Positive check: verify quoted variables are present
            quoted_var_lines = [
                l for l in deploy_lines
                if re.search(r'".*\$.*"', l) and not l.strip().startswith('#') and not l.strip().startswith('echo')
            ]
            if len(quoted_var_lines) >= 3:
                print(f"PASS: Component 3 — SC2086 fixed: variables are properly double-quoted ({len(quoted_var_lines)} quoted-var lines found) (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — No unquoted vars found but only {len(quoted_var_lines)} quoted-var lines (expected >=3)")
        else:
            print(f"FAIL: Component 3 — SC2086 not fixed: {unquoted_count} unquoted variable usage(s): {lines_to_check[:3]}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ── Component 4: SC2164 fixed — cd commands have error handling (0.15 pts) ──
    # The fix adds || exit (or || return) after cd commands
    try:
        cd_lines = []
        cd_fixed = 0
        for i, line in enumerate(deploy_lines, 1):
            stripped = line.strip()
            if stripped.startswith('#'):
                continue
            # Match cd commands (not in comments)
            if re.match(r'cd\s+', stripped):
                cd_lines.append((i, stripped))
                # Check if cd has error handling: || exit, || return, || { ... }
                if re.search(r'\|\|\s*(exit|return|\{)', stripped):
                    cd_fixed += 1

        if len(cd_lines) == 0:
            print(f"FAIL: Component 4 — No cd commands found in deploy.sh")
        elif cd_fixed == len(cd_lines):
            print(f"PASS: Component 4 — SC2164 fixed: all {len(cd_lines)} cd commands have error handling (0.15 pts)")
            total_score += 0.15
        else:
            unfixed = [(ln, txt) for ln, txt in cd_lines if not re.search(r'\|\|\s*(exit|return|\{)', txt)]
            print(f"FAIL: Component 4 — SC2164: {cd_fixed}/{len(cd_lines)} cd commands fixed. Unfixed: {unfixed[:3]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # ── Component 5: tasks.json with shellcheck task (0.15 pts) ──
    try:
        if not os.path.exists(TASKS_JSON):
            print(f"FAIL: Component 5 — tasks.json not found at {TASKS_JSON}")
        else:
            with open(TASKS_JSON, 'r') as f:
                tasks_data = json.load(f)

            tasks = tasks_data.get('tasks', [])
            shellcheck_task_found = False
            for task in tasks:
                # Check if there's a task that runs shellcheck on .sh files
                cmd = str(task.get('command', '')).lower()
                args = task.get('args', [])
                args_str = ' '.join(str(a) for a in args).lower()
                label = str(task.get('label', '')).lower()

                has_shellcheck_cmd = 'shellcheck' in cmd or 'shellcheck' in args_str or 'shellcheck' in label
                has_sh_pattern = '.sh' in args_str or '*.sh' in args_str or 'scripts/' in args_str or 'scripts' in args_str

                if has_shellcheck_cmd and has_sh_pattern:
                    print(f"PASS: Component 5 — tasks.json contains shellcheck task targeting .sh files in scripts/ (0.15 pts)")
                    total_score += 0.15
                    shellcheck_task_found = len(tasks) > 0  # derived from actual data
                    break

            if not shellcheck_task_found:
                print(f"FAIL: Component 5 — No shellcheck task targeting scripts/*.sh found in tasks.json. Tasks: {[t.get('label', 'unlabeled') for t in tasks]}")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 5 — Invalid JSON in tasks.json: {e}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
