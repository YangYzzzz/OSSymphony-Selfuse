"""
Reward Script: Configure VSCode search/watcher exclusions while keeping Explorer visibility
Task ID: vscode_web_040
Domain: vscode
Scoring:
  - Component 1 (0.35): search.exclude includes node_modules, .next, dist
  - Component 2 (0.35): files.watcherExclude includes node_modules, .next, dist
  - Component 3 (0.30): files.exclude does NOT include these directories
"""

import json
import os
import re

WORKDIR = '/home/user'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_web_040'

# The three directories that must be excluded from search and watcher
REQUIRED_DIRS = ['node_modules', '.next', 'dist']


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def pattern_matches_dir(pattern, dirname):
    """Check if a glob pattern targets the given directory name.

    Accepts patterns like:
      **/node_modules, **/node_modules/**, node_modules, node_modules/**,
      **/.next, .next, **/dist, dist, etc.
    """
    # Normalize: strip leading/trailing whitespace
    pattern = pattern.strip()
    # Check if the directory name appears in the pattern
    # Common VSCode patterns: **/dir, **/dir/**, dir, dir/**
    if dirname in pattern:
        return True
    return False


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

    # Component 1: search.exclude includes node_modules, .next, and dist (0.35 points)
    try:
        search_exclude = settings.get('search.exclude', {})
        if not isinstance(search_exclude, dict):
            print(f"FAIL: Component 1 -- search.exclude is not a dict: {type(search_exclude)}")
        else:
            found_dirs = [
                d for d in REQUIRED_DIRS
                if any(pattern_matches_dir(p, d) and search_exclude.get(p) for p in search_exclude)
            ]

            if len(found_dirs) == len(REQUIRED_DIRS):
                print(f"PASS: Component 1 -- search.exclude has all 3 dirs: {found_dirs} (0.35 pts)")
                total_score += 0.35
            else:
                missing = set(REQUIRED_DIRS) - set(found_dirs)
                print(f"FAIL: Component 1 -- search.exclude missing: {missing} (found: {found_dirs})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: files.watcherExclude includes node_modules, .next, and dist (0.35 points)
    try:
        watcher_exclude = settings.get('files.watcherExclude', {})
        if not isinstance(watcher_exclude, dict):
            print(f"FAIL: Component 2 -- files.watcherExclude is not a dict: {type(watcher_exclude)}")
        else:
            found_dirs = [
                d for d in REQUIRED_DIRS
                if any(pattern_matches_dir(p, d) and watcher_exclude.get(p) for p in watcher_exclude)
            ]

            if len(found_dirs) == len(REQUIRED_DIRS):
                print(f"PASS: Component 2 -- files.watcherExclude has all 3 dirs: {found_dirs} (0.35 pts)")
                total_score += 0.35
            else:
                missing = set(REQUIRED_DIRS) - set(found_dirs)
                print(f"FAIL: Component 2 -- files.watcherExclude missing: {missing} (found: {found_dirs})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Dirs excluded from search/watcher BUT still visible in Explorer (0.30 points)
    # Compound check: search.exclude and files.watcherExclude are configured (task change exists)
    # AND files.exclude does NOT hide any of these directories.
    # This ensures the check only passes AFTER the task is completed correctly.
    try:
        search_exclude = settings.get('search.exclude', {})
        watcher_exclude = settings.get('files.watcherExclude', {})
        files_exclude = settings.get('files.exclude', {})
        if not isinstance(files_exclude, dict):
            files_exclude = {}

        # First: verify search/watcher exclusions exist (anchors to task change)
        search_has_all = all(
            any(pattern_matches_dir(p, d) and search_exclude.get(p) for p in search_exclude)
            for d in REQUIRED_DIRS
        ) if isinstance(search_exclude, dict) else False

        watcher_has_all = all(
            any(pattern_matches_dir(p, d) and watcher_exclude.get(p) for p in watcher_exclude)
            for d in REQUIRED_DIRS
        ) if isinstance(watcher_exclude, dict) else False

        # Second: verify files.exclude does NOT hide them
        hidden_dirs = [
            d for d in REQUIRED_DIRS
            if any(pattern_matches_dir(p, d) and files_exclude.get(p) for p in files_exclude)
        ]

        if search_has_all and watcher_has_all and len(hidden_dirs) == 0:
            print(f"PASS: Component 3 -- Exclusions configured AND dirs remain visible in Explorer (0.30 pts)")
            total_score += 0.30
        elif not search_has_all or not watcher_has_all:
            print(f"FAIL: Component 3 -- search/watcher exclusions not fully configured (prerequisite)")
        else:
            print(f"FAIL: Component 3 -- files.exclude hides dirs that should be visible: {hidden_dirs}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
