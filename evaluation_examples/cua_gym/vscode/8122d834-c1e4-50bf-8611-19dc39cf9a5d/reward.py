"""
Reward Script: Set the cwd of the debug configuration in launch.json
Task ID: vscode_dbg_040
Domain: vs_code
Scoring:
  Component 1 (0.5 pts): 'cwd' property exists in the launch configuration
  Component 2 (0.5 pts): 'cwd' value is exactly '${workspaceFolder}/backend'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_dbg_040'
LAUNCH_JSON_PATH = '/home/user/projects/cwd-debug/.vscode/launch.json'


def load_json_with_comments(file_path):
    """Load a JSON file that may contain JSONC-style comments."""
    with open(file_path, 'r') as f:
        content = f.read()
    # Strip single-line comments (// ...)
    content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content_stripped)


def verify_task(launch_json_path):
    """
    Verify that the launch.json debug configuration includes a 'cwd' property
    set to '${workspaceFolder}/backend'.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition gate: file must exist and be parseable
    try:
        data = load_json_with_comments(launch_json_path)
    except FileNotFoundError:
        print(f"CRITICAL: launch.json not found at {launch_json_path}")
        print("REWARD: 0.0")
        return 0.0
    except json.JSONDecodeError as e:
        print(f"CRITICAL: Cannot parse launch.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: configurations array must be present and non-empty
    configurations = data.get('configurations', [])
    if not configurations:
        print("CRITICAL: No configurations found in launch.json")
        print("REWARD: 0.0")
        return 0.0

    # Find the first (and expected only) configuration
    config = configurations[0]

    # Component 1: 'cwd' property exists in the configuration (0.5 points)
    # This fails on initial_env (no 'cwd') and passes on golden_env (has 'cwd')
    try:
        if 'cwd' in config:
            print(f"PASS: Component 1 — 'cwd' property exists in configuration (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — 'cwd' property is missing from configuration")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 'cwd' value is exactly '${workspaceFolder}/backend' (0.5 points)
    # This fails on initial_env (no 'cwd') and passes on golden_env
    try:
        actual_cwd = config.get('cwd', None)
        expected_cwd = '${workspaceFolder}/backend'
        if actual_cwd == expected_cwd:
            print(f"PASS: Component 2 — 'cwd' value is '{actual_cwd}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — expected 'cwd' == '{expected_cwd}', found: {actual_cwd!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(LAUNCH_JSON_PATH):
    print(f"File not found: {LAUNCH_JSON_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(LAUNCH_JSON_PATH)
