"""
Reward Script: Add search exclude patterns to VSCode settings
Task ID: vscode_we_016
Domain: vscode
Scoring:
  - Component 1: search.exclude key exists (0.1 pts)
  - Component 2: **/node_modules excluded (0.3 pts)
  - Component 3: **/dist excluded (0.3 pts)
  - Component 4: **/.cache excluded (0.3 pts)
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that search.exclude patterns have been added to VSCode settings.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: search.exclude key exists in settings (0.1 points)
    try:
        search_exclude = settings.get("search.exclude")
        if isinstance(search_exclude, dict) and len(search_exclude) > 0:
            print(f"PASS: Component 1 — search.exclude exists with {len(search_exclude)} entries (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 — search.exclude missing or empty, found: {search_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: **/node_modules is set to true (0.3 points)
    try:
        search_exclude = settings.get("search.exclude", {})
        if isinstance(search_exclude, dict) and search_exclude.get("**/node_modules") is True:
            print(f"PASS: Component 2 — **/node_modules excluded (0.3 pts)")
            total_score += 0.3
        else:
            val = search_exclude.get("**/node_modules") if isinstance(search_exclude, dict) else None
            print(f"FAIL: Component 2 — **/node_modules not set to true, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/dist is set to true (0.3 points)
    try:
        search_exclude = settings.get("search.exclude", {})
        if isinstance(search_exclude, dict) and search_exclude.get("**/dist") is True:
            print(f"PASS: Component 3 — **/dist excluded (0.3 pts)")
            total_score += 0.3
        else:
            val = search_exclude.get("**/dist") if isinstance(search_exclude, dict) else None
            print(f"FAIL: Component 3 — **/dist not set to true, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: **/.cache is set to true (0.3 points)
    try:
        search_exclude = settings.get("search.exclude", {})
        if isinstance(search_exclude, dict) and search_exclude.get("**/.cache") is True:
            print(f"PASS: Component 4 — **/.cache excluded (0.3 pts)")
            total_score += 0.3
        else:
            val = search_exclude.get("**/.cache") if isinstance(search_exclude, dict) else None
            print(f"FAIL: Component 4 — **/.cache not set to true, found: {val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
