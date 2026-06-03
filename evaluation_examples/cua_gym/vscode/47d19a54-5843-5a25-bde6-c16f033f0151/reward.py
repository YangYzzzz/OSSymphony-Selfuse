"""
Reward Script: Configure Pylance type checking, auto-import, and analysis memory limit
Task ID: vscode_we_078
Domain: vscode
Scoring:
  Component 1: typeCheckingMode == "strict"          — 0.4 points
  Component 2: autoImportCompletions == true          — 0.3 points
  Component 3: memory.keepLibraryAst == true          — 0.3 points
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
        # Strip JSONC comments (// style)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: python.analysis.typeCheckingMode == "strict" (0.4 points)
    try:
        actual_mode = settings.get("python.analysis.typeCheckingMode")
        if actual_mode == "strict":
            print(f"PASS: Component 1 — typeCheckingMode is 'strict' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected typeCheckingMode='strict', found: {actual_mode!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: python.analysis.autoImportCompletions == true (0.3 points)
    try:
        actual_auto_import = settings.get("python.analysis.autoImportCompletions")
        if actual_auto_import is True:
            print(f"PASS: Component 2 — autoImportCompletions is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — expected autoImportCompletions=true, found: {actual_auto_import!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: python.analysis.memory.keepLibraryAst == true (0.3 points)
    try:
        actual_keep_ast = settings.get("python.analysis.memory.keepLibraryAst")
        if actual_keep_ast is True:
            print(f"PASS: Component 3 — memory.keepLibraryAst is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — expected memory.keepLibraryAst=true, found: {actual_keep_ast!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
