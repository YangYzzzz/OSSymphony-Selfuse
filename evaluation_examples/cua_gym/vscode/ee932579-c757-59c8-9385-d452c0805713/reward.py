"""
Reward Script: Set up ESLint for web development in VSCode
Task ID: vscode_stu_060
Domain: vscode
Scoring:
  - Component 1 (0.4): ESLint extension installed
  - Component 2 (0.35): .eslintrc.json exists with eslint:recommended
  - Component 3 (0.25): VSCode settings enable ESLint validation
"""

import os
import json
import re

HOME = '/home/user'
TASK_ID = 'vscode_stu_060'
PROJECT_DIR = os.path.join(HOME, 'webdev', 'project')
ESLINTRC_PATH = os.path.join(PROJECT_DIR, '.eslintrc.json')
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def check_extension_installed(ext_id):
    """Check if a VSCode extension is installed by scanning the extensions directory."""
    ext_dir = os.path.join(HOME, '.vscode', 'extensions')
    if not os.path.isdir(ext_dir):
        return False
    for entry in os.listdir(ext_dir):
        if entry.lower().startswith(ext_id.lower()):
            return True
    return False


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments (JSONC support)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ESLint extension is installed (0.4 points)
    try:
        eslint_installed = check_extension_installed('dbaeumer.vscode-eslint')
        if eslint_installed:
            print(f"PASS: Component 1 — ESLint extension (dbaeumer.vscode-eslint) is installed (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — ESLint extension not found in ~/.vscode/extensions/")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: .eslintrc.json exists with eslint:recommended (0.35 points)
    try:
        if not os.path.exists(ESLINTRC_PATH):
            print(f"FAIL: Component 2 — .eslintrc.json not found at {ESLINTRC_PATH}")
        else:
            config = load_json_file(ESLINTRC_PATH)
            extends_val = config.get('extends', [])
            # extends can be a string or a list
            if isinstance(extends_val, str):
                extends_list = [extends_val]
            elif isinstance(extends_val, list):
                extends_list = extends_val
            else:
                extends_list = []

            if 'eslint:recommended' in extends_list:
                print(f"PASS: Component 2 — .eslintrc.json exists with 'eslint:recommended' in extends (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — .eslintrc.json exists but 'eslint:recommended' not in extends: {extends_list}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: VSCode settings enable ESLint (0.25 points)
    # The task says "make sure VSCode shows lint errors in the editor"
    # This requires eslint.enable set to true in settings
    try:
        if not os.path.exists(SETTINGS_PATH):
            print(f"FAIL: Component 3 — VSCode settings.json not found at {SETTINGS_PATH}")
        else:
            settings = load_json_file(SETTINGS_PATH)
            eslint_enabled = settings.get('eslint.enable', None)
            if eslint_enabled is True:
                print(f"PASS: Component 3 — VSCode settings have eslint.enable=true (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — eslint.enable not set to true in settings.json (found: {eslint_enabled})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
