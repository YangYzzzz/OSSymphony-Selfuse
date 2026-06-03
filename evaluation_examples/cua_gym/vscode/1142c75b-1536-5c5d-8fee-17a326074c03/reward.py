"""
Reward Script: Configure Thunder Client extension settings
Task ID: vscode_we_087
Domain: vscode
Scoring:
  Component 1 (0.35): thunder-client.saveToWorkspace == true
  Component 2 (0.35): thunder-client.requestTimeout == 30000
  Component 3 (0.30): thunder-client.workspaceRelativePath == ".vscode/thunder"
"""

import os
import json
import re

HOME = '/home/user'
USER_SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')

# Workspace settings could be in any workspace .vscode/settings.json
# The task mentions an API project workspace
WORKSPACE_SETTINGS_CANDIDATES = [
    os.path.join(HOME, 'api-project', '.vscode', 'settings.json'),
]


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def get_merged_settings():
    """
    Load user-level and workspace-level settings.
    Return a merged dict where workspace settings override user settings
    (mimicking VSCode behavior).
    Also return individual dicts for debugging.
    """
    user_settings = load_jsonc(USER_SETTINGS_PATH)
    workspace_settings = {}
    for candidate in WORKSPACE_SETTINGS_CANDIDATES:
        ws = load_jsonc(candidate)
        if ws:
            workspace_settings = ws
            break

    # Merge: workspace overrides user
    merged = {}
    merged.update(user_settings)
    merged.update(workspace_settings)
    return merged, user_settings, workspace_settings


def verify_task():
    """
    Verify Thunder Client extension configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    merged, user_s, workspace_s = get_merged_settings()
    print(f"User settings keys: {list(user_s.keys())}")
    print(f"Workspace settings keys: {list(workspace_s.keys())}")

    # Component 1: thunder-client.saveToWorkspace == true (0.35 points)
    # This setting must be true to save requests in the workspace .vscode directory
    try:
        val = merged.get('thunder-client.saveToWorkspace')
        if val is True:
            print(f"PASS: Component 1 - thunder-client.saveToWorkspace is true (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - thunder-client.saveToWorkspace: expected true, found {val!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: thunder-client.requestTimeout == 30000 (0.35 points)
    # 30 seconds = 30000 milliseconds
    try:
        val = merged.get('thunder-client.requestTimeout')
        if val == 30000:
            print(f"PASS: Component 2 - thunder-client.requestTimeout is 30000 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 - thunder-client.requestTimeout: expected 30000, found {val!r}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: thunder-client.workspaceRelativePath == ".vscode/thunder" (0.30 points)
    # This sets where Thunder Client stores workspace data
    try:
        val = merged.get('thunder-client.workspaceRelativePath')
        if val == '.vscode/thunder':
            print(f"PASS: Component 3 - thunder-client.workspaceRelativePath is '.vscode/thunder' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 - thunder-client.workspaceRelativePath: expected '.vscode/thunder', found {val!r}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
