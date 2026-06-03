"""
Reward Script: VSCode Data Science Profile Configuration
Task ID: vscode_gf5_040
Domain: vscode (libreoffice_calc label, but actually VSCode task)
Scoring:
  Component 1: Profile export file exists and has correct name (0.20)
  Component 2: Profile settings contain dark theme, fontSize 14, wordWrap on (0.25)
  Component 3: Profile lists 5 required extensions (0.25)
  Component 4: Extensions are actually installed in VSCode (0.15)
  Component 5: VSCode settings.json has required settings (0.15)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf5_040'
PROFILE_PATH = os.path.join(WORKDIR, 'profiles', 'data-science.code-profile')
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')

# Required extensions (canonical IDs, lowercase for comparison)
REQUIRED_EXTENSIONS = [
    'ms-python.python',
    'ms-toolsai.jupyter',
    'mechatroner.rainbow-csv',
    'grapeCity.gc-excelviewer',       # case-insensitive match
    'shd101wyy.markdown-preview-enhanced',
]

def load_jsonc(path):
    """Load JSON/JSONC file, stripping comments."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // comments for JSONC support
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"  Cannot load {path}: {e}")
        return None


def verify_task():
    total_score = 0.0

    # =========================================================
    # Component 1: Profile file exists with correct name (0.20)
    # =========================================================
    try:
        if not os.path.exists(PROFILE_PATH):
            print(f"FAIL: Component 1 — Profile file not found at {PROFILE_PATH}")
        else:
            with open(PROFILE_PATH, 'r') as f:
                profile_data = json.load(f)

            profile_name = profile_data.get('name', '')
            if profile_name == 'Data Science':
                print(f"PASS: Component 1 — Profile file exists with name='Data Science' (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 1 — Profile name is '{profile_name}', expected 'Data Science'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # =========================================================
    # Component 2: Profile settings correct (0.25)
    #   dark theme, editor.fontSize: 14, editor.wordWrap: on
    # =========================================================
    try:
        if not os.path.exists(PROFILE_PATH):
            print(f"FAIL: Component 2 — No profile file to check settings")
        else:
            with open(PROFILE_PATH, 'r') as f:
                profile_data = json.load(f)

            settings_str = profile_data.get('settings', '{}')
            settings = json.loads(settings_str) if isinstance(settings_str, str) else settings_str

            sub_score = 0.0
            sub_total = 3  # three sub-checks

            # Check dark theme
            theme = settings.get('workbench.colorTheme', '')
            if 'dark' in theme.lower() or 'Dark' in theme:
                sub_score += 1
                print(f"  PASS: Profile theme is '{theme}' (dark)")
            else:
                print(f"  FAIL: Profile theme is '{theme}', expected a dark theme")

            # Check fontSize 14
            font_size = settings.get('editor.fontSize', None)
            if font_size == 14:
                sub_score += 1
                print(f"  PASS: Profile fontSize is 14")
            else:
                print(f"  FAIL: Profile fontSize is {font_size}, expected 14")

            # Check wordWrap on
            word_wrap = settings.get('editor.wordWrap', '')
            if word_wrap == 'on':
                sub_score += 1
                print(f"  PASS: Profile wordWrap is 'on'")
            else:
                print(f"  FAIL: Profile wordWrap is '{word_wrap}', expected 'on'")

            comp2_points = round(0.25 * (sub_score / sub_total), 4)
            if comp2_points > 0:
                print(f"PASS: Component 2 — Profile settings {int(sub_score)}/{sub_total} correct ({comp2_points} pts)")
                total_score += comp2_points
            else:
                print(f"FAIL: Component 2 — No profile settings matched")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # =========================================================
    # Component 3: Profile lists 5 required extensions (0.25)
    # =========================================================
    try:
        if not os.path.exists(PROFILE_PATH):
            print(f"FAIL: Component 3 — No profile file to check extensions")
        else:
            with open(PROFILE_PATH, 'r') as f:
                profile_data = json.load(f)

            extensions_str = profile_data.get('extensions', '[]')
            extensions_list = json.loads(extensions_str) if isinstance(extensions_str, str) else extensions_str

            # Extract extension IDs from the profile
            profile_ext_ids = []
            for ext in extensions_list:
                if isinstance(ext, dict):
                    ident = ext.get('identifier', {})
                    if isinstance(ident, dict):
                        ext_id = ident.get('id', '')
                    else:
                        ext_id = str(ident)
                else:
                    ext_id = str(ext)
                profile_ext_ids.append(ext_id.lower())

            found_count = 0
            for req_ext in REQUIRED_EXTENSIONS:
                if req_ext.lower() in profile_ext_ids:
                    found_count += 1
                    print(f"  PASS: Profile contains extension '{req_ext}'")
                else:
                    print(f"  FAIL: Profile missing extension '{req_ext}'")

            comp3_points = round(0.25 * (found_count / len(REQUIRED_EXTENSIONS)), 4)
            if comp3_points > 0:
                print(f"PASS: Component 3 — {found_count}/{len(REQUIRED_EXTENSIONS)} extensions in profile ({comp3_points} pts)")
                total_score += comp3_points
            else:
                print(f"FAIL: Component 3 — No required extensions found in profile")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # =========================================================
    # Component 4: Extensions installed on system (0.15)
    # =========================================================
    try:
        # Check installed extensions via filesystem (no subprocess)
        ext_dir = os.path.join(WORKDIR, '.vscode', 'extensions')
        if not os.path.isdir(ext_dir):
            # Try alternative path
            ext_dir = os.path.join(WORKDIR, '.vscode-server', 'extensions')

        # List extension directories
        if os.path.isdir(ext_dir):
            installed_dirs = os.listdir(ext_dir)
            installed_lower = [d.lower() for d in installed_dirs]
        else:
            installed_dirs = []
            installed_lower = []

        # Also check via extensions.json in the vscode dir
        ext_json_path = os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json')
        installed_ids = set()
        if os.path.exists(ext_json_path):
            with open(ext_json_path, 'r') as f:
                ext_data = json.load(f)
            for ext in ext_data:
                ident = ext.get('identifier', {}).get('id', '')
                installed_ids.add(ident.lower())

        found_count = 0
        for req_ext in REQUIRED_EXTENSIONS:
            req_lower = req_ext.lower()
            # Check if extension ID is in extensions.json
            if req_lower in installed_ids:
                found_count += 1
                print(f"  PASS: Extension '{req_ext}' is installed (extensions.json)")
            # Fallback: check directory names
            elif any(req_lower in d for d in installed_lower):
                found_count += 1
                print(f"  PASS: Extension '{req_ext}' is installed (directory)")
            else:
                print(f"  FAIL: Extension '{req_ext}' not found installed")

        comp4_points = round(0.15 * (found_count / len(REQUIRED_EXTENSIONS)), 4)
        if comp4_points > 0:
            print(f"PASS: Component 4 — {found_count}/{len(REQUIRED_EXTENSIONS)} extensions installed ({comp4_points} pts)")
            total_score += comp4_points
        else:
            print(f"FAIL: Component 4 — No required extensions installed")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # =========================================================
    # Component 5: VSCode settings.json has required settings (0.15)
    #   Dark theme, fontSize 14, wordWrap on, workspace trust
    # =========================================================
    try:
        settings = load_jsonc(SETTINGS_PATH)
        if settings is None:
            print(f"FAIL: Component 5 — Cannot load settings.json")
        else:
            sub_score = 0.0
            sub_total = 4

            # Dark theme
            theme = settings.get('workbench.colorTheme', '')
            if 'dark' in theme.lower() or 'Dark' in theme:
                sub_score += 1
                print(f"  PASS: settings.json theme is '{theme}' (dark)")
            else:
                print(f"  FAIL: settings.json theme is '{theme}', expected dark")

            # fontSize 14
            font_size = settings.get('editor.fontSize', None)
            if font_size == 14:
                sub_score += 1
                print(f"  PASS: settings.json fontSize is 14")
            else:
                print(f"  FAIL: settings.json fontSize is {font_size}, expected 14")

            # wordWrap on
            word_wrap = settings.get('editor.wordWrap', '')
            if word_wrap == 'on':
                sub_score += 1
                print(f"  PASS: settings.json wordWrap is 'on'")
            else:
                print(f"  FAIL: settings.json wordWrap is '{word_wrap}', expected 'on'")

            # Workspace trust enabled
            trust = settings.get('security.workspace.trust.enabled', None)
            if trust is True:
                sub_score += 1
                print(f"  PASS: settings.json workspace trust is enabled")
            else:
                print(f"  FAIL: settings.json workspace trust is {trust}, expected true")

            comp5_points = round(0.15 * (sub_score / sub_total), 4)
            if comp5_points > 0:
                print(f"PASS: Component 5 — {int(sub_score)}/{sub_total} settings correct ({comp5_points} pts)")
                total_score += comp5_points
            else:
                print(f"FAIL: Component 5 — No settings matched")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
