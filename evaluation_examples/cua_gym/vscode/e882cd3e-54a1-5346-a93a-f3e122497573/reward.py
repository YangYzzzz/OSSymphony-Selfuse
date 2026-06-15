"""
Reward Script: Configure autopep8 as the Python formatter with custom settings
Task ID: vscode_py_050
Domain: vscode
Scoring:
  - Component 1 (0.35): [python] defaultFormatter set to ms-python.autopep8
  - Component 2 (0.25): autopep8.args contains --max-line-length 110
  - Component 3 (0.20): autopep8.args contains --aggressive --aggressive (level 2)
  - Component 4 (0.20): autopep8.args contains --ignore E501
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_py_050'
SETTINGS_PATH = os.path.expanduser('~/.config/Code/User/settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded settings with {len(settings)} top-level keys")

    # Component 1: [python] section with defaultFormatter = ms-python.autopep8 (0.35 points)
    try:
        python_section = settings.get("[python]", {})
        formatter = python_section.get("editor.defaultFormatter", None)
        if isinstance(python_section, dict) and formatter == "ms-python.autopep8":
            print(f"PASS: Component 1 — [python].editor.defaultFormatter = 'ms-python.autopep8' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected [python].editor.defaultFormatter = 'ms-python.autopep8', found: {formatter}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: autopep8.args contains --max-line-length 110 (0.25 points)
    try:
        args = settings.get("autopep8.args", [])
        if isinstance(args, list):
            # Check for --max-line-length followed by 110
            # Find --max-line-length followed by 110
            max_line_idx = [i for i in range(len(args) - 1)
                           if args[i] == "--max-line-length" and str(args[i + 1]) == "110"]
            if len(max_line_idx) > 0:
                print(f"PASS: Component 2 — autopep8.args contains --max-line-length 110 (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — --max-line-length 110 not found in autopep8.args: {args}")
        else:
            print(f"FAIL: Component 2 — autopep8.args is not a list: {type(args)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: autopep8.args contains --aggressive --aggressive (level 2) (0.20 points)
    try:
        args = settings.get("autopep8.args", [])
        if isinstance(args, list):
            # Count occurrences of --aggressive
            aggressive_count = args.count("--aggressive")
            if aggressive_count >= 2:
                print(f"PASS: Component 3 — autopep8.args contains {aggressive_count} --aggressive flags (level 2+) (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 3 — expected >= 2 --aggressive flags, found {aggressive_count} in: {args}")
        else:
            print(f"FAIL: Component 3 — autopep8.args is not a list: {type(args)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: autopep8.args contains --ignore E501 (0.20 points)
    try:
        args = settings.get("autopep8.args", [])
        if isinstance(args, list):
            # Check for --ignore followed by E501
            # Find --ignore followed by E501
            ignore_idx = [i for i in range(len(args) - 1)
                         if args[i] == "--ignore" and args[i + 1] == "E501"]
            if len(ignore_idx) > 0:
                print(f"PASS: Component 4 — autopep8.args contains --ignore E501 (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — --ignore E501 not found in autopep8.args: {args}")
        else:
            print(f"FAIL: Component 4 — autopep8.args is not a list: {type(args)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
