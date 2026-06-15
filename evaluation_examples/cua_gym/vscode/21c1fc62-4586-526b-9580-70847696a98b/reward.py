"""
Reward Script: Configure VSCode to use pytest as testing framework with tests/ directory
Task ID: vscode_lp_003
Domain: vscode
Scoring:
  Component 1: python.testing.pytestEnabled == true      (0.35 pts)
  Component 2: python.testing.unittestEnabled == false    (0.25 pts)
  Component 3: python.testing.pytestArgs == ["tests/"]   (0.40 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_lp_003'

# Settings locations to check (global and workspace)
GLOBAL_SETTINGS = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'projects', 'myapp', '.vscode', 'settings.json')


def load_json_with_comments(file_path):
    """Load JSON file, stripping JSONC comments if present."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Strip single-line comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None


def get_setting(key):
    """
    Get a setting value from either workspace or global settings.
    Workspace settings take priority (as in VSCode).
    Returns (value, found_in) or (None, None) if not found.
    """
    # Check workspace settings first
    ws_settings = load_json_with_comments(WORKSPACE_SETTINGS)
    if ws_settings and key in ws_settings:
        return ws_settings[key], 'workspace'

    # Then check global settings
    global_settings = load_json_with_comments(GLOBAL_SETTINGS)
    if global_settings and key in global_settings:
        return global_settings[key], 'global'

    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: at least one settings file must exist
    ws_settings = load_json_with_comments(WORKSPACE_SETTINGS)
    global_settings = load_json_with_comments(GLOBAL_SETTINGS)
    if ws_settings is None and global_settings is None:
        print("CRITICAL: No settings files found at all")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: python.testing.pytestEnabled is true (0.35 points)
    # This setting MUST be present and true to enable pytest
    try:
        value, location = get_setting("python.testing.pytestEnabled")
        if value is True:
            print(f"PASS: Component 1 - pytestEnabled is true (in {location}) (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - expected pytestEnabled=true, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: python.testing.unittestEnabled is false (0.25 points)
    # This ensures unittest is disabled so pytest is the sole framework
    try:
        value, location = get_setting("python.testing.unittestEnabled")
        if value is False:
            print(f"PASS: Component 2 - unittestEnabled is false (in {location}) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - expected unittestEnabled=false, found: {value}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: python.testing.pytestArgs includes "tests/" (0.40 points)
    # This configures the test directory to tests/
    try:
        value, location = get_setting("python.testing.pytestArgs")
        if isinstance(value, list) and "tests/" in value:
            print(f"PASS: Component 3 - pytestArgs contains 'tests/' (in {location}) (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 3 - expected pytestArgs containing 'tests/', found: {value}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
