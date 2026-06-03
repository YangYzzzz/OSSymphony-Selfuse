"""
Reward Script: Install Prettier extension, configure as default JS formatter, enable format-on-save
Task ID: vscode_wf_006
Domain: vscode
Scoring:
  Component 1 (0.4): Extension esbenp.prettier-vscode is installed
  Component 2 (0.3): editor.formatOnSave is true in settings.json
  Component 3 (0.3): [javascript].editor.defaultFormatter is esbenp.prettier-vscode in settings.json
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Cannot load settings.json: {e}")
        return None


def check_extension_installed(extension_id):
    """Check if a VSCode extension is installed by scanning the extensions directory."""
    extensions_dir = os.path.join(HOME, '.vscode', 'extensions')
    if not os.path.isdir(extensions_dir):
        return False
    for entry in os.listdir(extensions_dir):
        if entry.lower().startswith(extension_id.lower()):
            return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension esbenp.prettier-vscode is installed (0.4 points)
    try:
        # Check via extensions directory (more reliable than CLI which needs display)
        ext_found = check_extension_installed('esbenp.prettier-vscode')

        if ext_found:
            print(f"PASS: Component 1 — Extension esbenp.prettier-vscode is installed (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Extension esbenp.prettier-vscode not found in extensions dir")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.formatOnSave is true (0.3 points)
    try:
        settings = load_settings()
        if settings is None:
            print(f"FAIL: Component 2 — settings.json cannot be loaded")
        else:
            format_on_save = settings.get('editor.formatOnSave', None)
            if format_on_save is True:
                print(f"PASS: Component 2 — editor.formatOnSave is true (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — editor.formatOnSave is {format_on_save}, expected true")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: [javascript].editor.defaultFormatter is esbenp.prettier-vscode (0.3 points)
    try:
        settings = load_settings()
        if settings is None:
            print(f"FAIL: Component 3 — settings.json cannot be loaded")
        else:
            js_section = settings.get('[javascript]', {})
            default_formatter = js_section.get('editor.defaultFormatter', None) if isinstance(js_section, dict) else None
            if default_formatter == 'esbenp.prettier-vscode':
                print(f"PASS: Component 3 — [javascript].editor.defaultFormatter is esbenp.prettier-vscode (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — [javascript].editor.defaultFormatter is '{default_formatter}', expected 'esbenp.prettier-vscode'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
