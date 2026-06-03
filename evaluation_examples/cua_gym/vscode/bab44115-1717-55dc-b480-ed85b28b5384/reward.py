"""
Reward Script: Configure mypy as type checker for Python in VSCode workspace
Task ID: vscode_lp_037
Domain: vscode
Scoring:
  Component 1 (0.25): mypy.ini exists with [mypy] section header
  Component 2 (0.25): mypy.ini contains strict_optional = True
  Component 3 (0.25): mypy.ini contains warn_return_any = True
  Component 4 (0.25): .vscode/settings.json contains mypy-type-checker.args with --config-file=mypy.ini
"""

import os
import json
import re
import configparser

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_037'
PROJECT_DIR = os.path.join(WORKDIR, TASK_ID)
MYPY_INI_PATH = os.path.join(PROJECT_DIR, 'mypy.ini')
VSCODE_SETTINGS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: mypy.ini exists and has [mypy] section (0.25 points)
    try:
        if os.path.exists(MYPY_INI_PATH):
            config = configparser.ConfigParser()
            config.read(MYPY_INI_PATH)
            if 'mypy' in config.sections():
                print(f"PASS: Component 1 — mypy.ini exists with [mypy] section (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — mypy.ini exists but missing [mypy] section. Sections: {config.sections()}")
        else:
            print(f"FAIL: Component 1 — mypy.ini does not exist at {MYPY_INI_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: mypy.ini has strict_optional = True (0.25 points)
    try:
        if os.path.exists(MYPY_INI_PATH):
            config = configparser.ConfigParser()
            config.read(MYPY_INI_PATH)
            if 'mypy' in config.sections():
                val = config.get('mypy', 'strict_optional', fallback=None)
                if val is not None and val.strip().lower() == 'true':
                    print(f"PASS: Component 2 — strict_optional = True found (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — strict_optional expected True, found: {val}")
            else:
                print(f"FAIL: Component 2 — [mypy] section missing, cannot check strict_optional")
        else:
            print(f"FAIL: Component 2 — mypy.ini does not exist")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: mypy.ini has warn_return_any = True (0.25 points)
    try:
        if os.path.exists(MYPY_INI_PATH):
            config = configparser.ConfigParser()
            config.read(MYPY_INI_PATH)
            if 'mypy' in config.sections():
                val = config.get('mypy', 'warn_return_any', fallback=None)
                if val is not None and val.strip().lower() == 'true':
                    print(f"PASS: Component 3 — warn_return_any = True found (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 3 — warn_return_any expected True, found: {val}")
            else:
                print(f"FAIL: Component 3 — [mypy] section missing, cannot check warn_return_any")
        else:
            print(f"FAIL: Component 3 — mypy.ini does not exist")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: .vscode/settings.json has mypy-type-checker.args with --config-file=mypy.ini (0.25 points)
    try:
        if os.path.exists(VSCODE_SETTINGS_PATH):
            with open(VSCODE_SETTINGS_PATH, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            settings = json.loads(cleaned)
            args = settings.get('mypy-type-checker.args', None)
            if isinstance(args, list) and '--config-file=mypy.ini' in args:
                print(f"PASS: Component 4 — mypy-type-checker.args contains --config-file=mypy.ini (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — mypy-type-checker.args expected ['--config-file=mypy.ini'], found: {args}")
        else:
            print(f"FAIL: Component 4 — .vscode/settings.json does not exist at {VSCODE_SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
