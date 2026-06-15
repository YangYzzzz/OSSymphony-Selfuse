"""
Reward Script: Configure VSCode workspace settings for ~/project
Task ID: vscode_wf_022
Domain: vscode
Scoring:
  Component 1 (0.3): files.exclude contains node_modules/, dist/, .cache/ all true
  Component 2 (0.3): search.exclude contains node_modules/, dist/, .cache/ all true
  Component 3 (0.2): explorer.fileNesting.enabled is true
  Component 4 (0.2): explorer.fileNesting.patterns has *.js -> ${capture}.js.map
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_wf_022'
SETTINGS_PATH = os.path.join(WORKDIR, 'project', '.vscode', 'settings.json')


def load_settings(path):
    """Load settings.json, handling JSONC comments."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (JSONC support)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(stripped)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_settings(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.exclude contains node_modules/, dist/, .cache/ (0.3 points)
    try:
        files_exclude = settings.get('files.exclude', {})
        required_excludes = ['node_modules/', 'dist/', '.cache/']
        matched = 0
        for pattern in required_excludes:
            if files_exclude.get(pattern) is True:
                matched += 1
            else:
                print(f"FAIL: Component 1 — files.exclude missing or not true for '{pattern}', found: {files_exclude.get(pattern)}")
        if matched == len(required_excludes):
            print(f"PASS: Component 1 — files.exclude has all 3 entries ({matched}/3) (0.3 pts)")
            total_score += 0.3
        elif matched > 0:
            partial = round(0.3 * matched / len(required_excludes), 2)
            print(f"PARTIAL: Component 1 — files.exclude has {matched}/3 entries ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — files.exclude has none of the required entries")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: search.exclude contains node_modules/, dist/, .cache/ (0.3 points)
    try:
        search_exclude = settings.get('search.exclude', {})
        required_excludes = ['node_modules/', 'dist/', '.cache/']
        matched = 0
        for pattern in required_excludes:
            if search_exclude.get(pattern) is True:
                matched += 1
            else:
                print(f"FAIL: Component 2 — search.exclude missing or not true for '{pattern}', found: {search_exclude.get(pattern)}")
        if matched == len(required_excludes):
            print(f"PASS: Component 2 — search.exclude has all 3 entries ({matched}/3) (0.3 pts)")
            total_score += 0.3
        elif matched > 0:
            partial = round(0.3 * matched / len(required_excludes), 2)
            print(f"PARTIAL: Component 2 — search.exclude has {matched}/3 entries ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — search.exclude has none of the required entries")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: explorer.fileNesting.enabled is true (0.2 points)
    try:
        nesting_enabled = settings.get('explorer.fileNesting.enabled')
        if nesting_enabled is True:
            print(f"PASS: Component 3 — explorer.fileNesting.enabled is true (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — explorer.fileNesting.enabled is {nesting_enabled}, expected true")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: explorer.fileNesting.patterns has *.js -> ${capture}.js.map (0.2 points)
    try:
        nesting_patterns = settings.get('explorer.fileNesting.patterns', {})
        js_pattern = nesting_patterns.get('*.js')
        if js_pattern is not None and '${capture}.js.map' in str(js_pattern):
            print(f"PASS: Component 4 — fileNesting pattern *.js -> {js_pattern} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — expected *.js -> ${{capture}}.js.map, found: {nesting_patterns}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
