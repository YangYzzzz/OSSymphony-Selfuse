"""
Reward Script: Set up Black formatter for Python project in VSCode
Task ID: vscode_wf_020
Domain: vscode
Scoring:
  Component 1 (0.35): black is installed via pip
  Component 2 (0.35): settings.json has [python] formatter config with formatOnSave
  Component 3 (0.30): settings.json has black-formatter.args with --line-length 88
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: black is installed via pip (0.35 points)
    # This checks that `black` package is importable, meaning it was pip-installed.
    try:
        import importlib
        spec = importlib.util.find_spec('black')
        if spec is not None:
            print(f"PASS: Component 1 — black is installed (spec: {spec.origin}) (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — black is not installed (importlib.util.find_spec returned None)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: settings.json has [python] block with formatter and formatOnSave (0.35 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 2 — settings.json could not be loaded")
        else:
            python_section = settings.get('[python]', None)
            if python_section is None:
                print(f"FAIL: Component 2 — '[python]' section not found in settings.json. Keys: {list(settings.keys())}")
            else:
                formatter = python_section.get('editor.defaultFormatter', None)
                format_on_save = python_section.get('editor.formatOnSave', None)

                formatter_ok = (formatter == 'ms-python.black-formatter')
                fos_ok = (format_on_save is True)

                if formatter_ok and fos_ok:
                    print(f"PASS: Component 2 — [python] defaultFormatter='{formatter}', formatOnSave={format_on_save} (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — defaultFormatter='{formatter}' (expected 'ms-python.black-formatter'), formatOnSave={format_on_save} (expected true)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: settings.json has black-formatter.args with --line-length 88 (0.30 points)
    try:
        settings = load_settings()
        if settings is None:
            print("FAIL: Component 3 — settings.json could not be loaded")
        else:
            args = settings.get('black-formatter.args', None)
            if args is None:
                print(f"FAIL: Component 3 — 'black-formatter.args' not found in settings.json")
            elif not isinstance(args, list):
                print(f"FAIL: Component 3 — 'black-formatter.args' is not a list: {args}")
            else:
                # Check that --line-length and 88 are present in the args list
                line_length_found = any(
                    args[i] == '--line-length' and i + 1 < len(args) and str(args[i + 1]) == '88'
                    for i in range(len(args))
                )

                if line_length_found:
                    print(f"PASS: Component 3 — black-formatter.args contains --line-length 88: {args} (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 — black-formatter.args does not contain --line-length 88. Found: {args}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
