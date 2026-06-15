"""
Reward Script: Verify workspace-specific Python settings for Black and pylint
Task ID: vscode_py_039
Domain: vscode
Scoring:
  - Component 1 (0.35): black-formatter.args contains ["--line-length", "100"]
  - Component 2 (0.35): python.linting.pylintArgs contains ["--disable=C0114,C0115,C0116"]
  - Component 3 (0.30): Both settings coexist correctly in .vscode/settings.json
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_039'
SETTINGS_PATH = os.path.join(WORKDIR, TASK_ID, '.vscode', 'settings.json')


def load_settings(path):
    """Load settings.json, handling JSONC (comments) gracefully."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be valid JSON
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_settings(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Black formatter line-length config (0.35 points)
    try:
        black_args = settings.get("black-formatter.args")
        if isinstance(black_args, list) and "--line-length" in black_args and "100" in black_args:
            # Verify they are adjacent: --line-length followed by 100
            idx = black_args.index("--line-length")
            if idx + 1 < len(black_args) and black_args[idx + 1] == "100":
                print(f"PASS: Component 1 -- black-formatter.args correct: {black_args} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 -- '--line-length' not followed by '100': {black_args}")
        else:
            print(f"FAIL: Component 1 -- black-formatter.args missing or incorrect: {black_args}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Pylint args to disable docstring warnings (0.35 points)
    try:
        pylint_args = settings.get("python.linting.pylintArgs")
        if isinstance(pylint_args, list):
            # Check for --disable=C0114,C0115,C0116 (all three codes must be present)
            matching_args = [
                arg for arg in pylint_args
                if isinstance(arg, str)
                and arg.startswith("--disable=")
                and {"C0114", "C0115", "C0116"}.issubset(
                    set(c.strip() for c in arg.replace("--disable=", "").split(","))
                )
            ]
            if len(matching_args) > 0:
                print(f"PASS: Component 2 -- pylintArgs correct: {pylint_args} (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 -- pylintArgs missing required disable codes: {pylint_args}")
        else:
            print(f"FAIL: Component 2 -- python.linting.pylintArgs missing or not a list: {pylint_args}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Both settings coexist in the same file (0.30 points)
    # This checks that both keys are present simultaneously (not just one)
    try:
        has_black = "black-formatter.args" in settings
        has_pylint = "python.linting.pylintArgs" in settings
        if has_black and has_pylint and total_score >= 0.70:
            print(f"PASS: Component 3 -- Both settings coexist in settings.json (0.30 pts)")
            total_score += 0.30
        elif has_black and has_pylint:
            print(f"FAIL: Component 3 -- Both keys present but values incorrect (need components 1&2 to pass)")
        else:
            missing = []
            if not has_black:
                missing.append("black-formatter.args")
            if not has_pylint:
                missing.append("python.linting.pylintArgs")
            print(f"FAIL: Component 3 -- Missing keys: {missing}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
