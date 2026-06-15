"""
Reward Script: Disable all installed VSCode extensions
Task ID: vscode_ext_018
Domain: vs_code
Scoring:
  Component 1: extensions.disabled key exists in settings.json (0.4 pts)
  Component 2: All 8 installed extensions are in extensions.disabled (0.6 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_018'

SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'

# The 8 extensions that must be disabled (from task context and VM exploration)
EXPECTED_DISABLED_EXTENSIONS = {
    "eamodio.gitlens",
    "esbenp.prettier-vscode",
    "formulahendry.code-runner",
    "ms-python.debugpy",
    "ms-python.python",
    "ms-python.vscode-pylance",
    "pkief.material-icon-theme",
    "streetsidesoftware.code-spell-checker",
}


def load_settings(path):
    """Load settings.json, handling JSONC (JSON with comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // line comments (JSONC support)
        content_no_comments = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_no_comments)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify that all installed VSCode extensions have been disabled.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot parse settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: extensions.disabled key exists in settings.json (0.4 points)
    # This key is NOT present in the initial state — only present after task is completed
    try:
        disabled_list = settings.get('extensions.disabled', None)
        if disabled_list is not None and isinstance(disabled_list, list):
            print(f"PASS: Component 1 — 'extensions.disabled' key exists in settings.json "
                  f"with {len(disabled_list)} entries (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — 'extensions.disabled' key not found in settings.json "
                  f"(found keys: {list(settings.keys())})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 8 installed extensions are in extensions.disabled (0.6 points)
    # Verifies that the task is FULLY completed — all extensions disabled, none missed
    try:
        disabled_list = settings.get('extensions.disabled', [])
        if not isinstance(disabled_list, list):
            print("FAIL: Component 2 — 'extensions.disabled' is not a list")
        else:
            # Normalize to lowercase for comparison (extension IDs are case-insensitive)
            disabled_set = {ext.lower() for ext in disabled_list}
            expected_lower = {ext.lower() for ext in EXPECTED_DISABLED_EXTENSIONS}
            missing = expected_lower - disabled_set
            if len(missing) == 0:
                print(f"PASS: Component 2 — All {len(EXPECTED_DISABLED_EXTENSIONS)} extensions "
                      f"are disabled: {sorted(disabled_set)} (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 2 — {len(missing)} extension(s) not disabled: {sorted(missing)}")
                print(f"  Currently disabled: {sorted(disabled_set)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
