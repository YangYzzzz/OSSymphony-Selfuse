"""
Reward Script: Configure Live Server extension settings in VSCode
Task ID: vscode_ext_022
Domain: vs_code
Scoring:
  - Component 1 (0.5 pts): liveServer.settings.port is set to 5500
  - Component 2 (0.5 pts): liveServer.settings.NoBrowser is set to false
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_022'

SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings(path):
    """Load VSCode settings.json, handling JSONC (JSON with Comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC format)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"ERROR: settings.json not found at {path}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse settings.json: {e}")
        return None


def verify_task():
    """
    Verify that the Live Server extension settings have been configured correctly.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load settings — gate check
    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print("CRITICAL: Cannot load settings.json — cannot verify task.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: liveServer.settings.port is set to 5500 (0.5 points)
    # This must FAIL on initial_env (key absent) and PASS on golden_env (5500 present)
    try:
        port_value = settings.get('liveServer.settings.port', None)
        if port_value is not None and int(port_value) == 5500:
            print(f"PASS: Component 1 — liveServer.settings.port is 5500 (found: {port_value}) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected liveServer.settings.port = 5500, found: {port_value}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: liveServer.settings.NoBrowser is set to false (0.5 points)
    # This must FAIL on initial_env (key absent) and PASS on golden_env (false present)
    # Note: 'false' means the browser WILL open automatically (NoBrowser=false → browser opens)
    try:
        no_browser_value = settings.get('liveServer.settings.NoBrowser', None)
        if no_browser_value is not None and no_browser_value is False:
            print(f"PASS: Component 2 — liveServer.settings.NoBrowser is false (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected liveServer.settings.NoBrowser = false, found: {no_browser_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
