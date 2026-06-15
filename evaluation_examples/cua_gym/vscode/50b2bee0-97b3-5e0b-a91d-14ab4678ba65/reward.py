"""
Reward Script: Enable Emmet abbreviation expansion inside JSX
Task ID: vscode_web_008
Domain: vs_code
Scoring:
  Component 1 (0.5): emmet.includeLanguages key exists in workspace settings
  Component 2 (0.5): emmet.includeLanguages has correct mapping AND existing settings preserved
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_web_008'

# Workspace settings path
SETTINGS_PATH = os.path.join(WORKDIR, 'projects', 'react-app', '.vscode', 'settings.json')


def load_jsonc(path):
    """Load a JSON or JSONC file (strips // comments)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip single-line comments (VSCode JSONC format)
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: Workspace settings file not found: {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        settings = load_jsonc(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: emmet.includeLanguages key exists in workspace settings (0.5 points)
    # This FAILS on initial (no emmet settings), PASSES on golden
    try:
        if 'emmet.includeLanguages' in settings:
            emmet_langs = settings['emmet.includeLanguages']
            if isinstance(emmet_langs, dict) and len(emmet_langs) > 0:
                print(f"PASS: Component 1 - emmet.includeLanguages exists with {len(emmet_langs)} mapping(s) (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 - emmet.includeLanguages exists but is empty or not a dict: {emmet_langs}")
        else:
            print(f"FAIL: Component 1 - emmet.includeLanguages key not found in settings. Keys present: {list(settings.keys())}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Correct mapping AND existing settings preserved (0.5 points)
    # This FAILS on initial (no emmet settings at all), PASSES on golden
    try:
        emmet_langs = settings.get('emmet.includeLanguages', {})
        has_correct_mapping = (
            isinstance(emmet_langs, dict)
            and emmet_langs.get('javascript') == 'javascriptreact'
        )

        # Also verify existing settings were not destroyed
        existing_preserved = (
            settings.get('editor.tabSize') == 2
            and settings.get('editor.formatOnSave') is True
        )

        if has_correct_mapping and existing_preserved:
            print(f"PASS: Component 2 - javascript->javascriptreact mapping correct AND existing settings preserved (0.5 pts)")
            total_score += 0.5
        elif has_correct_mapping and not existing_preserved:
            print(f"FAIL: Component 2 - Emmet mapping correct but existing settings were overwritten. editor.tabSize={settings.get('editor.tabSize')}, editor.formatOnSave={settings.get('editor.formatOnSave')}")
        elif not has_correct_mapping:
            actual_js = emmet_langs.get('javascript', '<missing>') if isinstance(emmet_langs, dict) else '<not a dict>'
            print(f"FAIL: Component 2 - Expected javascript->javascriptreact, found javascript->{actual_js}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
