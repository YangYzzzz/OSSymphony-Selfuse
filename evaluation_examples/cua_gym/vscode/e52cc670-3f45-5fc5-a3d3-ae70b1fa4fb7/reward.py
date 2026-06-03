"""
Reward Script: Configure VSCode Remote - SSH settings
Task ID: vscode_rrt_007
Domain: vscode
Scoring:
  Component 1 (0.5): remote.SSH.configFile == '~/.ssh/work_config'
  Component 2 (0.5): remote.SSH.connectTimeout == 30
"""

import os
import json
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
SETTINGS_PATH = os.path.join(VSCODE_USER, 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        return json.loads(cleaned)
    except FileNotFoundError:
        print(f"CRITICAL: Settings file not found at {SETTINGS_PATH}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
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

    print(f"Loaded settings keys: {list(settings.keys())}")

    # Component 1: remote.SSH.configFile is set to '~/.ssh/work_config' (0.5 points)
    try:
        config_file = settings.get('remote.SSH.configFile')
        if config_file is not None and config_file == '~/.ssh/work_config':
            print(f"PASS: Component 1 -- remote.SSH.configFile = '{config_file}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- expected remote.SSH.configFile = '~/.ssh/work_config', found: {config_file!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: remote.SSH.connectTimeout is set to 30 (0.5 points)
    try:
        connect_timeout = settings.get('remote.SSH.connectTimeout')
        if connect_timeout is not None and connect_timeout == 30:
            print(f"PASS: Component 2 -- remote.SSH.connectTimeout = {connect_timeout} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 -- expected remote.SSH.connectTimeout = 30, found: {connect_timeout!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
