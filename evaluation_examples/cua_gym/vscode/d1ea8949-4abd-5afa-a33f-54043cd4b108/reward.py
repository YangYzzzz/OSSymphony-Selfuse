"""
Reward Script: Change language mode of Makefile.config from Plain Text to JavaScript
Task ID: vscode_code_070
Domain: vs_code
Scoring:
  Component 1: files.associations key exists in settings.json with entry for Makefile.config (0.5 pts)
  Component 2: The association value for Makefile.config is 'javascript' (case-insensitive) (0.5 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_070'
SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'


def load_settings(path):
    """Load settings.json, stripping JSONC comments if present."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"WARN: JSON parse error in settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion: VSCode language mode for Makefile.config changed to JavaScript.
    The canonical mechanism is 'files.associations' in settings.json.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot parse settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.associations entry exists for Makefile.config (0.5 points)
    # This tests that the user added a file association for the extensionless file.
    try:
        associations = settings.get('files.associations', {})
        if not isinstance(associations, dict):
            associations = {}

        # Check if any key matches 'Makefile.config' (exact or glob pattern)
        makefile_config_key = None
        for key in associations:
            if key == 'Makefile.config' or key == '**/Makefile.config':
                makefile_config_key = key
                break

        if makefile_config_key is not None:
            print(f"PASS: Component 1 — files.associations contains entry for Makefile.config "
                  f"(key: '{makefile_config_key}') (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — files.associations does not contain entry for Makefile.config. "
                  f"Found associations: {associations}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The association value for Makefile.config is 'javascript' (0.5 points)
    # VSCode uses lowercase 'javascript' as the language identifier.
    try:
        associations = settings.get('files.associations', {})
        if not isinstance(associations, dict):
            associations = {}

        # Find the value for Makefile.config key
        assoc_value = None
        for key in associations:
            if key == 'Makefile.config' or key == '**/Makefile.config':
                assoc_value = associations[key]
                break

        if assoc_value is not None:
            normalized = str(assoc_value).strip().lower()
            # Accept 'javascript' or 'js' as valid language identifiers for JavaScript
            if normalized in ('javascript', 'js'):
                print(f"PASS: Component 2 — Language association for Makefile.config is "
                      f"'{assoc_value}' (JavaScript) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — Expected 'javascript' but found '{assoc_value}' "
                      f"for Makefile.config association")
        else:
            print(f"FAIL: Component 2 — No association found for Makefile.config; "
                  f"cannot verify language value")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
