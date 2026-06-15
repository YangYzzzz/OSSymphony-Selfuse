"""
Reward Script: Configure VSCode Git settings in User Settings JSON
Task ID: vscode_gf2_022
Domain: vs_code
Scoring: 5 components (0.2 each) — one per Git setting that must be added
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_022'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify that 5 Git settings are correctly configured in VSCode User Settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be parseable
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

    # Component 1: git.autofetch == true (0.2 points)
    try:
        val = settings.get("git.autofetch")
        if val is True:
            print(f"PASS: Component 1 — git.autofetch is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — git.autofetch expected true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: git.confirmSync == false (0.2 points)
    try:
        val = settings.get("git.confirmSync")
        if val is False:
            print(f"PASS: Component 2 — git.confirmSync is false (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — git.confirmSync expected false, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: git.enableSmartCommit == true (0.2 points)
    try:
        val = settings.get("git.enableSmartCommit")
        if val is True:
            print(f"PASS: Component 3 — git.enableSmartCommit is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — git.enableSmartCommit expected true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: git.postCommitCommand == "sync" (0.2 points)
    try:
        val = settings.get("git.postCommitCommand")
        if val == "sync":
            print(f"PASS: Component 4 — git.postCommitCommand is 'sync' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — git.postCommitCommand expected 'sync', found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: git.pruneOnFetch == true (0.2 points)
    try:
        val = settings.get("git.pruneOnFetch")
        if val is True:
            print(f"PASS: Component 5 — git.pruneOnFetch is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — git.pruneOnFetch expected true, found: {val!r}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
