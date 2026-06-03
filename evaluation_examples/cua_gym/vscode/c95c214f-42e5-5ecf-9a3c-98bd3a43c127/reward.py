"""
Reward Script: Configure workspace file watcher exclusion patterns
Task ID: vscode_lp_069
Domain: vs_code
Scoring:
  Component 1 (0.30) - files.watcherExclude key exists in settings.json
  Component 2 (0.25) - **/node_modules/** exclusion is true
  Component 3 (0.25) - **/.git/** exclusion is true
  Component 4 (0.20) - **/build/** exclusion is true
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        cleaned = re.sub(r',\s*([}\]])', r'\1', cleaned)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that files.watcherExclude is configured with the required patterns.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.watcherExclude key exists and is a dict (0.30 points)
    try:
        watcher_exclude = settings.get("files.watcherExclude")
        if isinstance(watcher_exclude, dict) and len(watcher_exclude) > 0:
            print(f"PASS: Component 1 - files.watcherExclude exists with {len(watcher_exclude)} patterns (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 - files.watcherExclude not found or not a non-empty dict, got: {watcher_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Components 2-4 require watcher_exclude to be a dict
    if not isinstance(watcher_exclude, dict):
        watcher_exclude = {}

    # Component 2: **/node_modules/** exclusion pattern is true (0.25 points)
    try:
        nm_value = watcher_exclude.get("**/node_modules/**")
        if nm_value is True:
            print(f"PASS: Component 2 - **/node_modules/** is excluded (true) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 - **/node_modules/** expected true, got: {nm_value}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: **/.git/** exclusion pattern is true (0.25 points)
    try:
        git_value = watcher_exclude.get("**/.git/**")
        if git_value is True:
            print(f"PASS: Component 3 - **/.git/** is excluded (true) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 - **/.git/** expected true, got: {git_value}")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: **/build/** exclusion pattern is true (0.20 points)
    try:
        build_value = watcher_exclude.get("**/build/**")
        if build_value is True:
            print(f"PASS: Component 4 - **/build/** is excluded (true) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 - **/build/** expected true, got: {build_value}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
