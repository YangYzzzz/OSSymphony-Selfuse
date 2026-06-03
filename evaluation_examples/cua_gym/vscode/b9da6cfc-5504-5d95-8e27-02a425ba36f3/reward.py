"""
Reward Script: Set up language-specific formatter settings in VSCode
Task ID: vscode_ext_028
Domain: vs_code
Scoring:
  Component 1: [javascript] section with editor.defaultFormatter = esbenp.prettier-vscode (0.35 pts)
  Component 2: [typescript] section with editor.defaultFormatter = esbenp.prettier-vscode (0.35 pts)
  Component 3: [python] section with editor.defaultFormatter = ms-python.python (0.30 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_028'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load settings.json, stripping JSONC comments if present."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content_no_comments = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_no_comments)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Could not parse settings.json as JSON: {e}")
        return None


def verify_task():
    """
    Verify that VSCode settings.json contains language-specific formatter settings:
    - [javascript] section with editor.defaultFormatter = esbenp.prettier-vscode
    - [typescript] section with editor.defaultFormatter = esbenp.prettier-vscode
    - [python] section with editor.defaultFormatter = ms-python.python
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Load settings.json — precondition gate
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print(f"CRITICAL: Cannot load settings.json at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Loaded settings.json successfully, keys: {list(settings.keys())}")

    # Component 1: [javascript] section with Prettier formatter (0.35 points)
    # This FAILS on initial (no [javascript] key) and PASSES on golden (key present with correct value)
    try:
        js_section = settings.get('[javascript]', None)
        if js_section is not None:
            js_formatter = js_section.get('editor.defaultFormatter', None)
            if js_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 1 — [javascript] section has editor.defaultFormatter = 'esbenp.prettier-vscode' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 1 — [javascript] section exists but editor.defaultFormatter = '{js_formatter}', expected 'esbenp.prettier-vscode'")
        else:
            print(f"FAIL: Component 1 — [javascript] section not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [typescript] section with Prettier formatter (0.35 points)
    # This FAILS on initial (no [typescript] key) and PASSES on golden (key present with correct value)
    try:
        ts_section = settings.get('[typescript]', None)
        if ts_section is not None:
            ts_formatter = ts_section.get('editor.defaultFormatter', None)
            if ts_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 2 — [typescript] section has editor.defaultFormatter = 'esbenp.prettier-vscode' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — [typescript] section exists but editor.defaultFormatter = '{ts_formatter}', expected 'esbenp.prettier-vscode'")
        else:
            print(f"FAIL: Component 2 — [typescript] section not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [python] section with Python extension formatter (0.30 points)
    # This FAILS on initial (no [python] key) and PASSES on golden (key present with correct value)
    try:
        py_section = settings.get('[python]', None)
        if py_section is not None:
            py_formatter = py_section.get('editor.defaultFormatter', None)
            if py_formatter == 'ms-python.python':
                print(f"PASS: Component 3 — [python] section has editor.defaultFormatter = 'ms-python.python' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — [python] section exists but editor.defaultFormatter = '{py_formatter}', expected 'ms-python.python'")
        else:
            print(f"FAIL: Component 3 — [python] section not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
