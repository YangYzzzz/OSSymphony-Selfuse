"""
Reward Script: Configure Java Lombok support in VSCode
Task ID: vscode_lang_067
Domain: vscode
Scoring:
  - Component 1 (0.5): vscjava.vscode-lombok extension is installed
  - Component 2 (0.5): java.jdt.ls.lombokSupport.enabled is true in user settings.json
"""

import os
import json
import re

HOME = '/home/user'
SETTINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'settings.json')
TASK_ID = 'vscode_lang_067'


def load_settings():
    """Load VSCode user settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return {}


def check_extension_installed(extension_id):
    """Check if a VSCode extension is installed by scanning the extensions directory."""
    extensions_dir = os.path.join(HOME, '.vscode', 'extensions')
    if not os.path.isdir(extensions_dir):
        return False
    for entry in os.listdir(extensions_dir):
        # Extension directories are named like "publisher.name-version"
        if entry.lower().startswith(extension_id.lower()):
            ext_path = os.path.join(extensions_dir, entry)
            if os.path.isdir(ext_path):
                return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: vscjava.vscode-lombok extension is installed (0.5 points)
    # This check FAILS on initial_env (no extension) and PASSES on golden_env
    try:
        lombok_installed = check_extension_installed('vscjava.vscode-lombok')
        if lombok_installed:
            print(f"PASS: Component 1 - Lombok extension (vscjava.vscode-lombok) is installed (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Lombok extension (vscjava.vscode-lombok) is NOT installed")
    except Exception as e:
        print(f"ERROR: Component 1 - Could not check extension: {e}")

    # Component 2: java.jdt.ls.lombokSupport.enabled is true in user settings (0.5 points)
    # This check FAILS on initial_env (setting absent) and PASSES on golden_env
    try:
        settings = load_settings()
        lombok_enabled = settings.get('java.jdt.ls.lombokSupport.enabled')
        if lombok_enabled is True:
            print(f"PASS: Component 2 - java.jdt.ls.lombokSupport.enabled is true in settings.json (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 - java.jdt.ls.lombokSupport.enabled is {lombok_enabled!r}, expected true")
    except Exception as e:
        print(f"ERROR: Component 2 - Could not check settings: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
