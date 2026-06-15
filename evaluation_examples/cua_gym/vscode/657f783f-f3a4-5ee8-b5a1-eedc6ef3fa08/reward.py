"""
Reward Script: Install Code Spell Checker extension and add 'microservice' to user dictionary
Task ID: vscode_ext_026
Domain: vs_code
Scoring:
  Component 1: Code Spell Checker extension installed (0.5 pts)
  Component 2: 'microservice' added to cSpell.userWords in settings.json (0.5 pts)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_026'

SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'
EXTENSIONS_JSON_PATH = '/home/user/.vscode/extensions/extensions.json'
EXTENSIONS_DIR = '/home/user/.vscode/extensions'

EXTENSION_ID = 'streetsidesoftware.code-spell-checker'


def load_settings():
    """Load settings.json, stripping JSONC comments if present."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        print(f"FAIL: settings.json not found at {SETTINGS_PATH}")
        return {}
    except json.JSONDecodeError as e:
        print(f"FAIL: settings.json is invalid JSON: {e}")
        return {}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Code Spell Checker extension is installed (0.5 points)
    # Check the extensions.json registry and/or the extension directory
    try:
        extension_found = False

        # Check extensions.json registry
        if os.path.exists(EXTENSIONS_JSON_PATH):
            with open(EXTENSIONS_JSON_PATH, 'r') as f:
                extensions_list = json.load(f)
            for ext in extensions_list:
                ext_id = ext.get('identifier', {}).get('id', '')
                if ext_id.lower() == EXTENSION_ID.lower():
                    extension_found = True
                    print(f"PASS: Extension '{ext_id}' found in extensions registry (version: {ext.get('version', 'unknown')})")
                    break

        # Also check extension directory as fallback
        if not extension_found and os.path.isdir(EXTENSIONS_DIR):
            for entry in os.listdir(EXTENSIONS_DIR):
                if entry.lower().startswith(EXTENSION_ID.lower()):
                    extension_found = True
                    print(f"PASS: Extension directory '{entry}' found in extensions dir")
                    break

        if extension_found:
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Extension '{EXTENSION_ID}' not found. "
                  f"Neither in extensions.json nor as a directory under {EXTENSIONS_DIR}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check extension installation: {e}")

    # Component 2: 'microservice' is present in cSpell.userWords in settings.json (0.5 points)
    try:
        settings = load_settings()
        user_words = settings.get('cSpell.userWords', None)

        if user_words is None:
            print("FAIL: Component 2 — 'cSpell.userWords' key not found in settings.json")
        elif not isinstance(user_words, list):
            print(f"FAIL: Component 2 — 'cSpell.userWords' is not a list, got: {type(user_words)}")
        elif 'microservice' not in user_words:
            print(f"FAIL: Component 2 — 'microservice' not in cSpell.userWords. Current list: {user_words}")
        else:
            print(f"PASS: Component 2 — 'microservice' found in cSpell.userWords: {user_words}")
            total_score += 0.5
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check cSpell.userWords setting: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
