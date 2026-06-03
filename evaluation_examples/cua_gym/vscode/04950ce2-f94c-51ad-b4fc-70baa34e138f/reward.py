"""
Reward Script: Set up search.exclude settings in VSCode
Task ID: vscode_lp_070
Domain: vs_code
Scoring:
  Component 1 — search.exclude key exists (0.2 pts)
  Component 2 — **/dist excluded (0.25 pts)
  Component 3 — **/coverage excluded (0.25 pts)
  Component 4 — **/docs/generated excluded (0.3 pts)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC single-line comments
        clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(clean)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that search.exclude is configured with the required directories.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: search.exclude key exists in settings (0.2 points)
    # This checks a task-introduced change: initial has no search.exclude
    try:
        search_exclude = settings.get("search.exclude")
        if isinstance(search_exclude, dict) and len(search_exclude) > 0:
            print(f"PASS: Component 1 — search.exclude exists with {len(search_exclude)} entries (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — search.exclude not found or empty, found: {search_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For remaining components, we need search_exclude to be a dict
    search_exclude = settings.get("search.exclude", {})
    if not isinstance(search_exclude, dict):
        search_exclude = {}

    # Component 2: **/dist is excluded (0.25 points)
    try:
        dist_val = search_exclude.get("**/dist")
        if dist_val is True:
            print(f"PASS: Component 2 — '**/dist': true found in search.exclude (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected '**/dist': true, found: {dist_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/coverage is excluded (0.25 points)
    try:
        cov_val = search_exclude.get("**/coverage")
        if cov_val is True:
            print(f"PASS: Component 3 — '**/coverage': true found in search.exclude (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected '**/coverage': true, found: {cov_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: **/docs/generated is excluded (0.3 points)
    try:
        docs_val = search_exclude.get("**/docs/generated")
        if docs_val is True:
            print(f"PASS: Component 4 — '**/docs/generated': true found in search.exclude (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 4 — expected '**/docs/generated': true, found: {docs_val}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
