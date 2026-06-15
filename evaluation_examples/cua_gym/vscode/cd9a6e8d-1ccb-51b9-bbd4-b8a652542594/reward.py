"""
Reward Script: Auto-import suggestions for React/TypeScript in VSCode
Task ID: vscode_web_025
Domain: vscode
Scoring:
  Component 1 (0.4): typescript.preferences.importModuleSpecifier is 'relative' or 'non-relative'
  Component 2 (0.3): typescript.suggest.autoImports is true
  Component 3 (0.3): javascript.suggest.autoImports is true
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_025'
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'react-ts-app', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSONC file (JSON with Comments) by stripping comments first."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    # Strip multi-line comments
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings file must exist and be valid JSON
    try:
        settings = load_jsonc(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: typescript.preferences.importModuleSpecifier is set to 'relative' or 'non-relative' (0.4 points)
    try:
        import_specifier = settings.get('typescript.preferences.importModuleSpecifier')
        if import_specifier in ('relative', 'non-relative'):
            print(f"PASS: Component 1 — typescript.preferences.importModuleSpecifier = '{import_specifier}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 'relative' or 'non-relative', found: {import_specifier!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: typescript.suggest.autoImports is true (0.3 points)
    try:
        ts_auto_imports = settings.get('typescript.suggest.autoImports')
        if ts_auto_imports is True:
            print(f"PASS: Component 2 — typescript.suggest.autoImports = true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected true, found: {ts_auto_imports!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: javascript.suggest.autoImports is true (0.3 points)
    try:
        js_auto_imports = settings.get('javascript.suggest.autoImports')
        if js_auto_imports is True:
            print(f"PASS: Component 3 — javascript.suggest.autoImports = true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — expected true, found: {js_auto_imports!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
