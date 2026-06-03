"""
Reward Script: Configure files.exclude in workspace settings to hide node_modules and .log files
Task ID: vscode_file_025
Domain: vs_code
Scoring:
  - Component 1: files.exclude key exists in .vscode/settings.json (0.3 pts)
  - Component 2: **/node_modules is set to true in files.exclude (0.35 pts)
  - Component 3: **/*.log is set to true in files.exclude (0.35 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_025'

SETTINGS_FILE = os.path.join(WORKDIR, 'webapp', '.vscode', 'settings.json')


def load_settings(file_path):
    """Load settings.json, handling JSONC (JSON with Comments) format."""
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        # Strip single-line comments (// ...) for JSONC support
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_clean)
    except FileNotFoundError:
        print(f"ERROR: File not found: {file_path}")
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Failed to parse JSON in {file_path}: {e}")
        return None


def verify_task():
    """
    Verify that the .vscode/settings.json file has been configured with
    files.exclude settings to hide node_modules and .log files.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_FILE):
        print(f"CRITICAL: settings.json not found at {SETTINGS_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Load settings
    settings = load_settings(SETTINGS_FILE)
    if settings is None:
        print("CRITICAL: Could not parse settings.json")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Loaded settings: {json.dumps(settings, indent=2)}")

    # Component 1: files.exclude key exists in settings.json (0.3 points)
    # This FAILS on initial_env (empty {}) and PASSES on golden_env
    try:
        files_exclude = settings.get('files.exclude', None)
        if files_exclude is not None and isinstance(files_exclude, dict):
            print(f"PASS: Component 1 — 'files.exclude' key exists in settings.json (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — 'files.exclude' key not found or not a dict in settings.json. Found: {files_exclude}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: **/node_modules is set to true in files.exclude (0.35 points)
    # This FAILS on initial_env and PASSES on golden_env
    try:
        files_exclude = settings.get('files.exclude', {})
        node_modules_val = files_exclude.get('**/node_modules', None)
        if node_modules_val is True:
            print(f"PASS: Component 2 — '**/node_modules' is set to true in files.exclude (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — expected '**/node_modules': true, found: {node_modules_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: **/*.log is set to true in files.exclude (0.35 points)
    # This FAILS on initial_env and PASSES on golden_env
    try:
        files_exclude = settings.get('files.exclude', {})
        log_val = files_exclude.get('**/*.log', None)
        if log_val is True:
            print(f"PASS: Component 3 — '**/*.log' is set to true in files.exclude (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — expected '**/*.log': true, found: {log_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {round(total_score, 2)}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
verify_task()
