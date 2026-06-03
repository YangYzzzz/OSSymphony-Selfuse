"""
Reward Script: Install the Prettier extension and set it as the default formatter for the workspace.
Task ID: vscode_we_052
Domain: vscode
Scoring:
  - Component 1 (0.5): esbenp.prettier-vscode extension is installed
  - Component 2 (0.5): Workspace settings.json contains editor.defaultFormatter = esbenp.prettier-vscode
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_we_052'
WORKSPACE_DIR = os.path.join(WORKDIR, 'projects', 'webapp')
SETTINGS_PATH = os.path.join(WORKSPACE_DIR, '.vscode', 'settings.json')
EXTENSIONS_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Prettier extension is installed (0.5 points)
    # Checks that a directory starting with 'esbenp.prettier-vscode' exists
    # in ~/.vscode/extensions/, which is where VSCode installs extensions.
    # On initial_env: no such directory -> FAIL
    # On golden_env: esbenp.prettier-vscode-<version> directory exists -> PASS
    try:
        if os.path.isdir(EXTENSIONS_DIR):
            ext_entries = os.listdir(EXTENSIONS_DIR)
            prettier_dirs = [d for d in ext_entries
                            if d.lower().startswith('esbenp.prettier-vscode')]
            if prettier_dirs:
                print(f"PASS: Component 1 -- Prettier extension installed: {prettier_dirs[0]} (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 -- esbenp.prettier-vscode not found in {EXTENSIONS_DIR}. Found: {ext_entries}")
        else:
            print(f"FAIL: Component 1 -- Extensions directory does not exist: {EXTENSIONS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Workspace settings.json sets Prettier as the default formatter (0.5 points)
    # Checks that ~/projects/webapp/.vscode/settings.json exists and contains
    # "editor.defaultFormatter": "esbenp.prettier-vscode"
    # On initial_env: no .vscode/settings.json -> FAIL
    # On golden_env: settings.json with correct value -> PASS
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 2 -- {SETTINGS_PATH} does not exist")
        else:
            with open(SETTINGS_PATH, 'r') as f:
                content = f.read()
            # Strip JSONC comments before parsing
            cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            cleaned = re.sub(r'/\*.*?\*/', '', cleaned, flags=re.DOTALL)
            settings = json.loads(cleaned)

            formatter = settings.get('editor.defaultFormatter', '')
            if formatter and formatter.lower() == 'esbenp.prettier-vscode':
                print(f"PASS: Component 2 -- editor.defaultFormatter is '{formatter}' (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 -- editor.defaultFormatter is '{formatter}', expected 'esbenp.prettier-vscode'")
    except json.JSONDecodeError as e:
        print(f"ERROR: Component 2 -- Could not parse settings.json: {e}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
