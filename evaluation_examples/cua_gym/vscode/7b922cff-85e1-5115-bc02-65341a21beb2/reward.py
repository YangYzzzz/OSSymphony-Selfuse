"""
Reward Script: Configure VSCode Git settings (autofetch, autofetchPeriod, defaultBranchName)
Task ID: vscode_git_042
Domain: vs_code
Scoring:
  Component 1: git.autofetch == true         (0.35 pts)
  Component 2: git.autofetchPeriod == 120    (0.35 pts)
  Component 3: git.defaultBranchName == main (0.30 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_git_042'
SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'


def load_settings(path):
    """Load VSCode settings.json, stripping JSONC comments if present."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip JSONC-style single-line comments
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Failed to parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings — if file is missing or unparseable, return 0.0 immediately
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: git.autofetch is set to true (0.35 points)
    # This key does NOT exist in initial_env and MUST be true in golden_env
    try:
        autofetch = settings.get('git.autofetch', None)
        if autofetch is True:
            print(f"PASS: Component 1 — git.autofetch == true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected git.autofetch=true, found: {autofetch!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: git.autofetchPeriod is set to 120 (0.35 points)
    # This key does NOT exist in initial_env and MUST be 120 in golden_env
    try:
        period = settings.get('git.autofetchPeriod', None)
        if period == 120:
            print(f"PASS: Component 2 — git.autofetchPeriod == 120 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected git.autofetchPeriod=120, found: {period!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: git.defaultBranchName is set to 'main' (0.30 points)
    # This key does NOT exist in initial_env and MUST be 'main' in golden_env
    try:
        branch = settings.get('git.defaultBranchName', None)
        if branch == 'main':
            print(f"PASS: Component 3 — git.defaultBranchName == 'main' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 — expected git.defaultBranchName='main', found: {branch!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
