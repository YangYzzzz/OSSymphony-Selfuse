"""
Reward Script: Configure VSCode to use workspace TypeScript version
Task ID: vscode_fix_054
Domain: vscode
Scoring:
  Component 1 (0.4): .vscode/settings.json exists and contains typescript.tsdk key
  Component 2 (0.6): typescript.tsdk is set to 'node_modules/typescript/lib'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_fix_054'
PROJECT_DIR = os.path.join(WORKDIR, 'ts-project')
SETTINGS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments (VSCode JSONC format)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: project directory exists
    if not os.path.isdir(PROJECT_DIR):
        print(f"CRITICAL: Project directory not found: {PROJECT_DIR}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: .vscode/settings.json exists and contains typescript.tsdk key (0.4 points)
    # Initial env has no .vscode/settings.json, so this fails on initial.
    try:
        if not os.path.isfile(SETTINGS_PATH):
            print(f"FAIL: Component 1 — .vscode/settings.json does not exist at {SETTINGS_PATH}")
        else:
            settings = load_jsonc(SETTINGS_PATH)
            if 'typescript.tsdk' in settings:
                print(f"PASS: Component 1 — .vscode/settings.json exists and contains 'typescript.tsdk' key (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — .vscode/settings.json exists but 'typescript.tsdk' key not found. Keys: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: typescript.tsdk value is 'node_modules/typescript/lib' (0.6 points)
    # This verifies the exact correct value pointing to the workspace TS installation.
    try:
        if not os.path.isfile(SETTINGS_PATH):
            print(f"FAIL: Component 2 — .vscode/settings.json does not exist")
        else:
            settings = load_jsonc(SETTINGS_PATH)
            tsdk_value = settings.get('typescript.tsdk', None)
            expected_value = 'node_modules/typescript/lib'
            if tsdk_value == expected_value:
                print(f"PASS: Component 2 — typescript.tsdk is '{tsdk_value}' (0.6 pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 2 — typescript.tsdk is '{tsdk_value}', expected '{expected_value}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
