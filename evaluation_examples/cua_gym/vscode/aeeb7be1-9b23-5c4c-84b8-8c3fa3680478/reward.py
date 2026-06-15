"""
Reward Script: Override workspace settings to disable telemetry, hide activity bar, move sidebar right
Task ID: vscode_we_037
Domain: vscode
Scoring:
  - Component 1: .vscode/settings.json exists and is valid JSON (0.1 pts)
  - Component 2: telemetry.telemetryLevel == "off" (0.3 pts)
  - Component 3: workbench.activityBar.location == "hidden" (0.3 pts)
  - Component 4: workbench.sideBar.location == "right" (0.3 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_037'
WORKSPACE_SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'secure-app', '.vscode', 'settings.json')


def load_jsonc(file_path):
    """Load a JSON/JSONC file, stripping // comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .vscode/settings.json exists and is valid JSON (0.1 points)
    # This file does NOT exist on initial_env, so this differentiates initial from golden.
    settings = None
    try:
        if os.path.isfile(WORKSPACE_SETTINGS_PATH):
            settings = load_jsonc(WORKSPACE_SETTINGS_PATH)
            if isinstance(settings, dict):
                print(f"PASS: Component 1 - .vscode/settings.json exists and is valid JSON (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 1 - .vscode/settings.json is not a JSON object, got {type(settings).__name__}")
        else:
            print(f"FAIL: Component 1 - .vscode/settings.json does not exist at {WORKSPACE_SETTINGS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 - Could not load .vscode/settings.json: {e}")

    if settings is None or not isinstance(settings, dict):
        # Cannot check further components without valid settings
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: telemetry.telemetryLevel == "off" (0.3 points)
    try:
        telemetry_val = settings.get("telemetry.telemetryLevel")
        if telemetry_val == "off":
            print(f"PASS: Component 2 - telemetry.telemetryLevel == 'off' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 - telemetry.telemetryLevel expected 'off', found: {telemetry_val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: workbench.activityBar.location == "hidden" (0.3 points)
    try:
        activity_val = settings.get("workbench.activityBar.location")
        if activity_val == "hidden":
            print(f"PASS: Component 3 - workbench.activityBar.location == 'hidden' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 - workbench.activityBar.location expected 'hidden', found: {activity_val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: workbench.sideBar.location == "right" (0.3 points)
    try:
        sidebar_val = settings.get("workbench.sideBar.location")
        if sidebar_val == "right":
            print(f"PASS: Component 4 - workbench.sideBar.location == 'right' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 - workbench.sideBar.location expected 'right', found: {sidebar_val!r}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
