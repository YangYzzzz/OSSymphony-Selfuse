"""
Reward Script: Set up comprehensive file exclusion settings in VSCode
Task ID: vscode_we_039
Domain: vscode
Scoring:
  Component 1 (0.10): files.exclude key exists in settings
  Component 2 (0.10): **/*.pyc excluded
  Component 3 (0.10): **/__pycache__ excluded
  Component 4 (0.10): **/.DS_Store excluded
  Component 5 (0.10): **/.env excluded
  Component 6 (0.10): search.exclude key exists in settings
  Component 7 (0.20): **/node_modules excluded from search
  Component 8 (0.20): **/build excluded from search
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_039'
SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Try direct parse first; fall back to stripping JSONC comments
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
            return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.exclude key exists (0.10 points)
    try:
        files_exclude = settings.get("files.exclude")
        if isinstance(files_exclude, dict) and len(files_exclude) > 0:
            print(f"PASS: Component 1 — files.exclude exists with {len(files_exclude)} entries (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — files.exclude missing or empty, found: {files_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: **/*.pyc excluded (0.10 points)
    try:
        files_exclude = settings.get("files.exclude", {})
        if files_exclude.get("**/*.pyc") is True:
            print("PASS: Component 2 — **/*.pyc is excluded (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 2 — **/*.pyc not set to true, found: {files_exclude.get('**/*.pyc')}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/__pycache__ excluded (0.10 points)
    try:
        files_exclude = settings.get("files.exclude", {})
        if files_exclude.get("**/__pycache__") is True:
            print("PASS: Component 3 — **/__pycache__ is excluded (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 3 — **/__pycache__ not set to true, found: {files_exclude.get('**/__pycache__')}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: **/.DS_Store excluded (0.10 points)
    try:
        files_exclude = settings.get("files.exclude", {})
        if files_exclude.get("**/.DS_Store") is True:
            print("PASS: Component 4 — **/.DS_Store is excluded (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 — **/.DS_Store not set to true, found: {files_exclude.get('**/.DS_Store')}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: **/.env excluded (0.10 points)
    try:
        files_exclude = settings.get("files.exclude", {})
        if files_exclude.get("**/.env") is True:
            print("PASS: Component 5 — **/.env is excluded (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 5 — **/.env not set to true, found: {files_exclude.get('**/.env')}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: search.exclude key exists (0.10 points)
    try:
        search_exclude = settings.get("search.exclude")
        if isinstance(search_exclude, dict) and len(search_exclude) > 0:
            print(f"PASS: Component 6 — search.exclude exists with {len(search_exclude)} entries (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — search.exclude missing or empty, found: {search_exclude}")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    # Component 7: **/node_modules excluded from search (0.20 points)
    try:
        search_exclude = settings.get("search.exclude", {})
        if search_exclude.get("**/node_modules") is True:
            print("PASS: Component 7 — **/node_modules excluded from search (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 7 — **/node_modules not in search.exclude, found: {search_exclude.get('**/node_modules')}")
    except Exception as e:
        print(f"ERROR: Component 7 — {e}")

    # Component 8: **/build excluded from search (0.20 points)
    try:
        search_exclude = settings.get("search.exclude", {})
        if search_exclude.get("**/build") is True:
            print("PASS: Component 8 — **/build excluded from search (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 8 — **/build not in search.exclude, found: {search_exclude.get('**/build')}")
    except Exception as e:
        print(f"ERROR: Component 8 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist app state before verification (VSCode settings are file-based, no GUI persistence needed)
# Run verification
verify_task()
