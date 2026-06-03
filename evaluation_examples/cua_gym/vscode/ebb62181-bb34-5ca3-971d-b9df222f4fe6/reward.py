"""
Reward Script: Add workspace-specific search exclusions in settings.json
Task ID: vscode_file_074
Domain: vs_code
Scoring:
  Component 1: search.exclude key exists in settings.json (0.3 points)
  Component 2: All three directories (**/build, **/dist, **/coverage) are excluded with true (0.5 points)
  Component 3: Settings file is valid JSON and the excluded dirs are strictly the required three (0.2 points)
  Total: 1.0
"""

import os
import json

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_074'

SETTINGS_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'settings.json')

REQUIRED_EXCLUDES = {
    "**/build": True,
    "**/dist": True,
    "**/coverage": True,
}


def load_settings(path):
    """Load settings.json, stripping JSONC comments if present."""
    import re
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"JSON parse error in {path}: {e}")
        return None


def verify_task(settings_path):
    """
    Verify task completion: workspace settings.json has search.exclude
    with **/build, **/dist, and **/coverage all set to true.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition gate: file must exist and be valid JSON
    settings = load_settings(settings_path)
    if settings is None:
        print(f"CRITICAL: Cannot load settings.json at {settings_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: 'search.exclude' key exists in settings.json (0.3 points)
    # This FAILS on initial (file is {}) and PASSES on golden
    try:
        if 'search.exclude' in settings:
            print("PASS: Component 1 — 'search.exclude' key exists in settings.json (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — 'search.exclude' key not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All three required exclusions exist and are set to true (0.5 points)
    # This FAILS on initial (no search.exclude) and PASSES on golden
    try:
        search_exclude = settings.get('search.exclude', {})
        if not isinstance(search_exclude, dict):
            print(f"FAIL: Component 2 — 'search.exclude' is not a dict, got: {type(search_exclude)}")
        else:
            missing = [k for k in REQUIRED_EXCLUDES if k not in search_exclude]
            wrong_value = [
                f"{k}: expected {v}, got {search_exclude[k]}"
                for k, v in REQUIRED_EXCLUDES.items()
                if k in search_exclude and search_exclude[k] != v
            ]
            if not missing and not wrong_value:
                print(f"PASS: Component 2 — All three exclusions present with correct values: "
                      f"**/build=true, **/dist=true, **/coverage=true (0.5 pts)")
                total_score += 0.5
            else:
                if missing:
                    print(f"FAIL: Component 2 — Missing exclusion keys: {missing}")
                if wrong_value:
                    print(f"FAIL: Component 2 — Wrong values for: {wrong_value}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: search.exclude contains exactly the required three keys (no extra, no missing) (0.2 points)
    # This FAILS on initial (no search.exclude) and PASSES on golden
    try:
        search_exclude = settings.get('search.exclude', {})
        if isinstance(search_exclude, dict):
            actual_keys = set(search_exclude.keys())
            required_keys = set(REQUIRED_EXCLUDES.keys())
            if actual_keys == required_keys:
                print(f"PASS: Component 3 — search.exclude contains exactly the required keys: "
                      f"{sorted(actual_keys)} (0.2 pts)")
                total_score += 0.2
            else:
                extra = actual_keys - required_keys
                missing = required_keys - actual_keys
                if extra:
                    print(f"FAIL: Component 3 — Extra exclusion keys found: {sorted(extra)}")
                if missing:
                    print(f"FAIL: Component 3 — Missing exclusion keys: {sorted(missing)}")
        else:
            print("FAIL: Component 3 — 'search.exclude' is not a dict")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: run verification against the workspace settings.json
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(SETTINGS_PATH)
