"""
Reward Script: Create .vscode configuration folder with settings.json, launch.json, extensions.json
Task ID: vscode_file_037
Domain: vs_code
Scoring:
  - Component 1: settings.json exists with Python settings (tabSize:4, formatOnSave:true) — 0.35 pts
  - Component 2: launch.json exists with Python debug configuration (version 0.2.0, debugpy, launch, program) — 0.40 pts
  - Component 3: extensions.json exists recommending ms-python.python and ms-python.debugpy — 0.25 pts
"""

import os
import json

WORKDIR = '/home/user/analytics'
TASK_ID = 'vscode_file_037'
VSCODE_DIR = os.path.join(WORKDIR, '.vscode')


def _is_subset(expected, actual) -> bool:
    """Recursively check that expected is a subset of actual (containment check)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        # For lists, check all expected items appear in actual
        if not isinstance(actual, list):
            return False
        return all(item in actual for item in expected)
    return expected == actual


def load_json_file(path):
    """Load and parse a JSON file, handling JSONC (JSON with Comments) if needed."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Try direct parse first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Strip single-line comments for JSONC compatibility
            import re
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content_clean)
    except Exception as e:
        raise RuntimeError(f"Failed to load {path}: {e}")


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: .vscode directory must exist
    if not os.path.isdir(VSCODE_DIR):
        print(f"FAIL: .vscode directory does not exist at {VSCODE_DIR}")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: settings.json exists and contains Python-related settings (0.35 points)
    # Task requires: tabSize: 4, formatOnSave: true
    # These changes are not present in initial_env (no .vscode folder exists initially)
    settings_path = os.path.join(VSCODE_DIR, 'settings.json')
    try:
        if not os.path.isfile(settings_path):
            print(f"FAIL: Component 1 — settings.json does not exist at {settings_path}")
        else:
            settings = load_json_file(settings_path)
            # Verify required keys: tabSize = 4 and formatOnSave = true
            tab_size_ok = settings.get('editor.tabSize') == 4
            format_on_save_ok = settings.get('editor.formatOnSave') is True

            if tab_size_ok and format_on_save_ok:
                print(f"PASS: Component 1 — settings.json has editor.tabSize=4 and editor.formatOnSave=true (0.35 pts)")
                total_score += 0.35
            elif tab_size_ok:
                print(f"FAIL: Component 1 — settings.json has tabSize=4 but missing formatOnSave=true (found: {settings.get('editor.formatOnSave')})")
            elif format_on_save_ok:
                print(f"FAIL: Component 1 — settings.json has formatOnSave=true but tabSize is {settings.get('editor.tabSize')} (expected 4)")
            else:
                print(f"FAIL: Component 1 — settings.json missing required keys: tabSize={settings.get('editor.tabSize')}, formatOnSave={settings.get('editor.formatOnSave')}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: launch.json exists with Python debug configuration (0.40 points)
    # Task requires: version 0.2.0, type: debugpy, request: launch, program: ${workspaceFolder}/src/main.py
    launch_path = os.path.join(VSCODE_DIR, 'launch.json')
    try:
        if not os.path.isfile(launch_path):
            print(f"FAIL: Component 2 — launch.json does not exist at {launch_path}")
        else:
            launch = load_json_file(launch_path)
            version_ok = launch.get('version') == '0.2.0'
            configurations = launch.get('configurations', [])

            # Check that at least one configuration matches: type=debugpy, request=launch, program=${workspaceFolder}/src/main.py
            matching_configs = [
                c for c in configurations
                if (c.get('type') == 'debugpy' and
                    c.get('request') == 'launch' and
                    c.get('program') == '${workspaceFolder}/src/main.py')
            ]
            config_ok = len(matching_configs) > 0

            if version_ok and config_ok:
                print(f"PASS: Component 2 — launch.json has version=0.2.0 and valid debugpy configuration (0.40 pts)")
                total_score += 0.40
            elif version_ok:
                print(f"FAIL: Component 2 — launch.json has version=0.2.0 but configuration is missing or incorrect (configs: {configurations})")
            elif config_ok:
                print(f"FAIL: Component 2 — launch.json has valid configuration but version is '{launch.get('version')}' (expected '0.2.0')")
            else:
                print(f"FAIL: Component 2 — launch.json missing version=0.2.0 and/or debugpy config (version={launch.get('version')}, configs={configurations})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: extensions.json exists recommending ms-python.python and ms-python.debugpy (0.25 points)
    extensions_path = os.path.join(VSCODE_DIR, 'extensions.json')
    try:
        if not os.path.isfile(extensions_path):
            print(f"FAIL: Component 3 — extensions.json does not exist at {extensions_path}")
        else:
            extensions = load_json_file(extensions_path)
            recommendations = extensions.get('recommendations', [])

            has_python = 'ms-python.python' in recommendations
            has_debugpy = 'ms-python.debugpy' in recommendations

            if has_python and has_debugpy:
                print(f"PASS: Component 3 — extensions.json recommends ms-python.python and ms-python.debugpy (0.25 pts)")
                total_score += 0.25
            elif has_python:
                print(f"FAIL: Component 3 — extensions.json recommends ms-python.python but missing ms-python.debugpy (found: {recommendations})")
            elif has_debugpy:
                print(f"FAIL: Component 3 — extensions.json recommends ms-python.debugpy but missing ms-python.python (found: {recommendations})")
            else:
                print(f"FAIL: Component 3 — extensions.json missing required recommendations (found: {recommendations})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
