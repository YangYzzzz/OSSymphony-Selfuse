"""
Reward Script: Set up terminal shell integration and command decoration
Task ID: vscode_rrt_079
Domain: vs_code
Scoring:
  Component 1 (0.5): terminal.integrated.shellIntegration.enabled == true
  Component 2 (0.5): terminal.integrated.shellIntegration.decorationsEnabled == "both"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_079'
SETTINGS_PATH = os.path.expanduser('~/.config/Code/User/settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
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

    # Component 1: terminal.integrated.shellIntegration.enabled == true (0.5 points)
    # This setting must be explicitly set to true in settings.json.
    # It is NOT present in the initial_env, so scoring it measures a task-introduced change.
    try:
        value = settings.get('terminal.integrated.shellIntegration.enabled')
        if value is True:
            print(f"PASS: Component 1 -- shellIntegration.enabled is true (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- expected shellIntegration.enabled=true, found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: terminal.integrated.shellIntegration.decorationsEnabled == "both" (0.5 points)
    # This setting must be explicitly set to "both" in settings.json.
    # It is NOT present in the initial_env, so scoring it measures a task-introduced change.
    try:
        value = settings.get('terminal.integrated.shellIntegration.decorationsEnabled')
        if value == 'both':
            print(f"PASS: Component 2 -- shellIntegration.decorationsEnabled is 'both' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- expected decorationsEnabled='both', found: {value!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
