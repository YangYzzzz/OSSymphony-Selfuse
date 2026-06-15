"""
Reward Script: Turn on breadcrumb navigation in VSCode
Task ID: vscode_stu_054
Domain: vscode
Scoring:
  Component 1 (0.6): breadcrumbs.enabled is set to true in settings.json
  Component 2 (0.4): breadcrumbs.enabled is exactly boolean True (not string/int)
                      AND settings file is well-formed JSON with no corruption
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_stu_054'


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments (VSCode supports JSONC)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify that breadcrumbs.enabled is set to true in VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be loadable
    try:
        settings = load_settings(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: breadcrumbs.enabled is truthy (0.6 points)
    # This checks that the key exists and evaluates to True
    try:
        breadcrumbs_value = settings.get('breadcrumbs.enabled')
        if breadcrumbs_value:
            print(f"PASS: Component 1 — breadcrumbs.enabled is truthy (value: {breadcrumbs_value!r}) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 — breadcrumbs.enabled is not truthy (value: {breadcrumbs_value!r})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: breadcrumbs.enabled is exactly boolean True (0.4 points)
    # This ensures the value is the correct type (bool True, not "true" string or 1)
    try:
        breadcrumbs_value = settings.get('breadcrumbs.enabled')
        if breadcrumbs_value is True:
            print(f"PASS: Component 2 — breadcrumbs.enabled is exactly boolean True (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — breadcrumbs.enabled is not boolean True (value: {breadcrumbs_value!r}, type: {type(breadcrumbs_value).__name__})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
