"""
Reward Script: Create a VSCode workspace setting profile for web development
Task ID: vscode_web_077
Domain: vscode
Scoring:
  Component 1 (0.30): .code-profile export file exists with correct name "Web Development"
  Component 2 (0.25): Profile directory created under ~/.config/Code/User/profiles/ with settings
  Component 3 (0.20): .code-profile contains keybindings, snippets, and extensions sections
  Component 4 (0.25): Profile is associated with the webapp workspace in globalStorage/storage.json
"""

import os
import json
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
PROFILE_EXPORT = os.path.join(HOME, 'vscode_web_077.code-profile')
PROFILES_DIR = os.path.join(VSCODE_USER, 'profiles')
STORAGE_PATH = os.path.join(VSCODE_USER, 'globalStorage', 'storage.json')


def load_jsonc(path):
    """Load a JSON file, stripping // comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Strip single-line comments
        cleaned = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(cleaned)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: .code-profile export file exists with name "Web Development" (0.30 points)
    # This file does NOT exist on initial_env, only on golden_env after profile export.
    try:
        if os.path.isfile(PROFILE_EXPORT):
            profile_data = load_jsonc(PROFILE_EXPORT)
            profile_name = profile_data.get('name', '')
            if profile_name.lower() == 'web development':
                print(f"PASS: Component 1 — .code-profile export exists with name '{profile_name}' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 1 — .code-profile name is '{profile_name}', expected 'Web Development'")
        else:
            print(f"FAIL: Component 1 — .code-profile export file not found at {PROFILE_EXPORT}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Profile directory created with settings.json inside (0.25 points)
    # Initial_env has NO profiles/ directory at all; golden has one with a profile UUID dir.
    try:
        if os.path.isdir(PROFILES_DIR):
            profile_uuids = [d for d in os.listdir(PROFILES_DIR)
                             if os.path.isdir(os.path.join(PROFILES_DIR, d))]
            if len(profile_uuids) > 0:
                # Check that at least one profile subdir has a settings.json
                valid_profile_dirs = [
                    uuid_dir for uuid_dir in profile_uuids
                    if os.path.isfile(os.path.join(PROFILES_DIR, uuid_dir, 'settings.json'))
                    and isinstance(load_jsonc(os.path.join(PROFILES_DIR, uuid_dir, 'settings.json')), dict)
                    and len(load_jsonc(os.path.join(PROFILES_DIR, uuid_dir, 'settings.json'))) > 5
                ]
                if len(valid_profile_dirs) > 0:
                    print(f"PASS: Component 2 — Profile directory exists with settings.json (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Profile directory found but no valid settings.json inside")
            else:
                print(f"FAIL: Component 2 — profiles/ dir exists but no profile subdirectories")
        else:
            print(f"FAIL: Component 2 — profiles/ directory not found at {PROFILES_DIR}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: .code-profile export contains keybindings, snippets, and extensions (0.20 points)
    # These are embedded as JSON-in-string fields in the export. Only exists on golden.
    try:
        if os.path.isfile(PROFILE_EXPORT):
            profile_data = load_jsonc(PROFILE_EXPORT)
            has_keybindings = 'keybindings' in profile_data and len(profile_data['keybindings']) > 10
            has_snippets = 'snippets' in profile_data and len(profile_data['snippets']) > 10
            has_extensions = 'extensions' in profile_data and len(profile_data['extensions']) > 10
            has_settings = 'settings' in profile_data and len(profile_data['settings']) > 10

            checks_passed = sum([has_keybindings, has_snippets, has_extensions, has_settings])
            if checks_passed == 4:
                print(f"PASS: Component 3 — .code-profile has settings, keybindings, snippets, and extensions (0.20 pts)")
                total_score += 0.20
            else:
                missing = []
                if not has_settings:
                    missing.append('settings')
                if not has_keybindings:
                    missing.append('keybindings')
                if not has_snippets:
                    missing.append('snippets')
                if not has_extensions:
                    missing.append('extensions')
                print(f"FAIL: Component 3 — .code-profile missing or empty sections: {', '.join(missing)}")
        else:
            print(f"FAIL: Component 3 — .code-profile not found (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Profile is associated with webapp workspace in storage.json (0.25 points)
    # Initial_env maps /home/user/projects/webapp to __default__profile__.
    # Golden_env maps it to a real profile UUID (not __default__profile__).
    try:
        if os.path.isfile(STORAGE_PATH):
            storage = load_jsonc(STORAGE_PATH)
            profile_assoc = storage.get('profileAssociations', {})
            workspaces = profile_assoc.get('workspaces', {})

            # Check both URI forms (with or without file:// prefix)
            webapp_profile = None
            for key, val in workspaces.items():
                if 'projects/webapp' in key:
                    webapp_profile = val
                    break

            if webapp_profile and webapp_profile != '__default__profile__':
                print(f"PASS: Component 4 — Workspace associated with profile '{webapp_profile}' (0.25 pts)")
                total_score += 0.25
            elif webapp_profile == '__default__profile__':
                print(f"FAIL: Component 4 — Workspace still using __default__profile__, expected custom profile")
            else:
                print(f"FAIL: Component 4 — No workspace association found for projects/webapp")
        else:
            print(f"FAIL: Component 4 — storage.json not found at {STORAGE_PATH}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
