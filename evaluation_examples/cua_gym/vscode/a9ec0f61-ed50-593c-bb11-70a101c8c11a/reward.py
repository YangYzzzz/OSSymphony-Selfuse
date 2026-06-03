"""
Reward Script: Sort Outline view by position and navigate CSS file
Task ID: vscode_code_077
Domain: vs_code
Scoring:
  Component 1 (0.6): VSCode settings.json has "outline.sortOrder": "position"
  Component 2 (0.4): Navigation marker file exists with correct selector and sort order
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_code_077'

SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'
NAV_MARKER_PATH = '/home/user/.vscode_outline_navigation'


def load_settings_json(path):
    """Load VSCode settings.json, handling JSONC (JSON with Comments)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        raise e


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: VSCode settings.json has "outline.sortOrder": "position" (0.6 points)
    # This is the primary task action — changing the Outline view sort order
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 1 — settings.json not found at {SETTINGS_PATH}")
        else:
            settings = load_settings_json(SETTINGS_PATH)
            outline_sort = settings.get('outline.sortOrder', None)
            if outline_sort == 'position':
                print(f"PASS: Component 1 — outline.sortOrder is 'position' in settings.json (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 1 — expected outline.sortOrder='position', found: {outline_sort!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — could not read settings.json: {e}")

    # Component 2: Navigation marker file exists, records navigation to .form-control
    # with outline_sort_order: position (0.4 points)
    # This verifies the agent navigated to .form-control via the Outline view
    try:
        if not os.path.exists(NAV_MARKER_PATH):
            print(f"FAIL: Component 2 — navigation marker file not found at {NAV_MARKER_PATH}")
        else:
            with open(NAV_MARKER_PATH, 'r') as f:
                nav_content = f.read()

            # Parse the key: value lines in the marker file
            nav_data = {}
            for line in nav_content.strip().splitlines():
                if ':' in line:
                    key, _, val = line.partition(':')
                    nav_data[key.strip()] = val.strip()

            navigated_to = nav_data.get('navigated_to', None)
            nav_file = nav_data.get('file', None)
            nav_sort = nav_data.get('outline_sort_order', None)

            navigated_ok = navigated_to == '.form-control'
            file_ok = nav_file == '/home/user/web/components.css'
            sort_ok = nav_sort == 'position'

            if navigated_ok and file_ok and sort_ok:
                print(f"PASS: Component 2 — navigation marker confirms .form-control navigation "
                      f"with sort_order=position in /home/user/web/components.css (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 2 — navigation marker content unexpected. "
                      f"navigated_to={navigated_to!r} (expected '.form-control'), "
                      f"file={nav_file!r}, outline_sort_order={nav_sort!r} (expected 'position')")
    except Exception as e:
        print(f"ERROR: Component 2 — could not read navigation marker: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
