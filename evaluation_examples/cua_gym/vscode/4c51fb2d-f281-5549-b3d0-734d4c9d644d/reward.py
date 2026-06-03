"""
Reward Script: Configure VSCode file watcher exclusions
Task ID: vscode_we_023
Domain: vscode
Scoring:
  Component 1 (0.35) — files.watcherExclude key exists with a dict value
  Component 2 (0.25) — **/.git/objects/** pattern present and true
  Component 3 (0.20) — **/node_modules/**/* pattern present and true
  Component 4 (0.20) — **/.hg/store/** pattern present and true
"""

import os
import json
import re

WORKDIR = '/home/user'
SETTINGS_DIR = os.path.expanduser('~/.config/Code/User')
SETTINGS_PATH = os.path.join(SETTINGS_DIR, 'settings.json')
TASK_ID = 'vscode_we_023'


def load_settings(path):
    """Load VSCode settings.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be valid JSON
    try:
        settings = load_settings(SETTINGS_PATH)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0
    except (json.JSONDecodeError, Exception) as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Loaded settings.json with {len(settings)} top-level keys")

    # Component 1: files.watcherExclude key exists and is a dict (0.35 points)
    try:
        watcher_exclude = settings.get('files.watcherExclude')
        if isinstance(watcher_exclude, dict) and len(watcher_exclude) > 0:
            print(f"PASS: Component 1 — files.watcherExclude exists with {len(watcher_exclude)} patterns (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — files.watcherExclude missing or not a non-empty dict, found: {watcher_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # For components 2-4, we need watcher_exclude to be a dict
    if not isinstance(settings.get('files.watcherExclude'), dict):
        watcher_exclude = {}
    else:
        watcher_exclude = settings['files.watcherExclude']

    # Component 2: **/.git/objects/** pattern present and set to true (0.25 points)
    try:
        git_pattern = '**/.git/objects/**'
        if watcher_exclude.get(git_pattern) is True:
            print(f"PASS: Component 2 — '{git_pattern}': true found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected '{git_pattern}': true, found: {watcher_exclude.get(git_pattern, '<missing>')}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/node_modules/**/* pattern present and set to true (0.20 points)
    try:
        node_pattern = '**/node_modules/**/*'
        if watcher_exclude.get(node_pattern) is True:
            print(f"PASS: Component 3 — '{node_pattern}': true found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — expected '{node_pattern}': true, found: {watcher_exclude.get(node_pattern, '<missing>')}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: **/.hg/store/** pattern present and set to true (0.20 points)
    try:
        hg_pattern = '**/.hg/store/**'
        if watcher_exclude.get(hg_pattern) is True:
            print(f"PASS: Component 4 — '{hg_pattern}': true found (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — expected '{hg_pattern}': true, found: {watcher_exclude.get(hg_pattern, '<missing>')}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
