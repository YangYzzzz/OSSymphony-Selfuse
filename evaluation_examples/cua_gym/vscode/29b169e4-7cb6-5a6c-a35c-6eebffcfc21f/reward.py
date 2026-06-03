"""
Reward Script: Configure VSCode path aliases for React project
Task ID: vscode_gf2_026
Domain: vscode
Scoring:
  Component 1 (0.25): javascript.preferences.importModuleSpecifier == "non-relative" in .vscode/settings.json
  Component 2 (0.25): typescript.preferences.importModuleSpecifier == "non-relative" in .vscode/settings.json
  Component 3 (0.25): jsconfig.json (or tsconfig.json) has @components/* -> src/components/* path alias
  Component 4 (0.25): jsconfig.json (or tsconfig.json) has @utils/* -> src/utils/* path alias
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_026'
PROJECT_DIR = os.path.join(WORKDIR, 'projects', 'react-app')
SETTINGS_PATH = os.path.join(PROJECT_DIR, '.vscode', 'settings.json')


def load_json_file(path):
    """Load a JSON file, stripping JSONC comments if needed."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC-style comments
    content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
    return json.loads(content)


def find_config_file():
    """Find jsconfig.json or tsconfig.json at project root."""
    for name in ['jsconfig.json', 'tsconfig.json']:
        path = os.path.join(PROJECT_DIR, name)
        if os.path.exists(path):
            return path, name
    return None, None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: .vscode/settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load settings
    try:
        settings = load_json_file(SETTINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse settings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: javascript.preferences.importModuleSpecifier == "non-relative" (0.25 points)
    try:
        js_import_spec = settings.get('javascript.preferences.importModuleSpecifier')
        if js_import_spec == 'non-relative':
            print(f"PASS: Component 1 — javascript.preferences.importModuleSpecifier = '{js_import_spec}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected 'non-relative', found: {js_import_spec!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: typescript.preferences.importModuleSpecifier == "non-relative" (0.25 points)
    try:
        ts_import_spec = settings.get('typescript.preferences.importModuleSpecifier')
        if ts_import_spec == 'non-relative':
            print(f"PASS: Component 2 — typescript.preferences.importModuleSpecifier = '{ts_import_spec}' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected 'non-relative', found: {ts_import_spec!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Find jsconfig.json or tsconfig.json
    config_path, config_name = find_config_file()

    if config_path is None:
        print(f"FAIL: Component 3 — No jsconfig.json or tsconfig.json found at project root")
        print(f"FAIL: Component 4 — No jsconfig.json or tsconfig.json found at project root")
    else:
        try:
            config = load_json_file(config_path)
        except Exception as e:
            print(f"ERROR: Cannot parse {config_name}: {e}")
            config = None

        if config is not None:
            paths = {}
            try:
                paths = config.get('compilerOptions', {}).get('paths', {})
            except Exception:
                pass

            # Component 3: @components/* path alias (0.25 points)
            try:
                comp_alias = paths.get('@components/*', None)
                if comp_alias is not None:
                    # Normalize: accept both list and string forms
                    if isinstance(comp_alias, list):
                        comp_targets = [s.strip() for s in comp_alias]
                    else:
                        comp_targets = [str(comp_alias).strip()]
                    if 'src/components/*' in comp_targets:
                        print(f"PASS: Component 3 — @components/* -> {comp_alias} in {config_name} (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 3 — @components/* maps to {comp_alias}, expected ['src/components/*']")
                else:
                    print(f"FAIL: Component 3 — @components/* alias not found in {config_name} paths")
            except Exception as e:
                print(f"ERROR: Component 3 — {e}")

            # Component 4: @utils/* path alias (0.25 points)
            try:
                utils_alias = paths.get('@utils/*', None)
                if utils_alias is not None:
                    if isinstance(utils_alias, list):
                        utils_targets = [s.strip() for s in utils_alias]
                    else:
                        utils_targets = [str(utils_alias).strip()]
                    if 'src/utils/*' in utils_targets:
                        print(f"PASS: Component 4 — @utils/* -> {utils_alias} in {config_name} (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 4 — @utils/* maps to {utils_alias}, expected ['src/utils/*']")
                else:
                    print(f"FAIL: Component 4 — @utils/* alias not found in {config_name} paths")
            except Exception as e:
                print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
