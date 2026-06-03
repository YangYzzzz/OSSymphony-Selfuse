"""
Reward Script: Configure VSCode for web development workflow
Task ID: osworld_multi_apps_code_vscode_config_006
Domain: vs-code / multi-apps
Scoring:
  Component 1: Live Server extension installed           (0.35 pts)
  Component 2: HTML CSS Support extension installed      (0.20 pts)
  Component 3: Auto Rename Tag extension installed       (0.20 pts)
  Component 4: Workspace HTML 2-space indentation set    (0.125 pts)
  Component 5: Workspace CSS 2-space indentation set     (0.125 pts)
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_code_vscode_config_006'

# Paths
EXTENSIONS_JSON = os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json')
WORKSPACE_SETTINGS = os.path.join(WORKDIR, 'projects', 'portfolio', '.vscode', 'settings.json')

# Expected extension IDs (lower-case canonical)
LIVE_SERVER_ID = 'ritwickdey.liveserver'
HTML_CSS_SUPPORT_ID = 'ecmel.vscode-html-css'
AUTO_RENAME_TAG_ID = 'formulahendry.auto-rename-tag'


def load_extensions_json(path: str):
    """Load extensions.json from the user .vscode directory."""
    try:
        with open(path, 'r') as f:
            content = f.read().strip()
        if not content or content == '[]':
            return []
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot read extensions.json at {path}: {e}")
        return None


def is_extension_installed(extensions: list, ext_id: str) -> bool:
    """Check if a given extension ID is in the installed extensions list."""
    if extensions is None:
        return False
    ext_id_lower = ext_id.lower()
    for ext in extensions:
        installed_id = ext.get('identifier', {}).get('id', '').lower()
        if installed_id == ext_id_lower:
            return True
    return False


def load_json_with_comments(path: str):
    """Load a JSON file, stripping // comments (VSCode JSONC format)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line // comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except FileNotFoundError:
        return None
    except json.JSONDecodeError as e:
        print(f"ERROR: Cannot parse JSON at {path}: {e}")
        return None


def _is_subset(expected, actual) -> bool:
    """Check that all keys/values in expected exist in actual (subset match)."""
    if isinstance(expected, dict):
        if not isinstance(actual, dict):
            return False
        return all(k in actual and _is_subset(v, actual[k]) for k, v in expected.items())
    if isinstance(expected, list):
        return expected == actual
    return expected == actual


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load extensions list once (used for components 1-3)
    extensions = load_extensions_json(EXTENSIONS_JSON)
    if extensions is None:
        print("CRITICAL: extensions.json not readable — assuming no extensions installed")
        extensions = []

    # Component 1: Live Server extension installed (0.35 points)
    # This is the most important extension for the task (opens pages in browser)
    try:
        if is_extension_installed(extensions, LIVE_SERVER_ID):
            print(f"PASS: Component 1 — Live Server (ritwickdey.liveserver) is installed (0.35 pts)")
            total_score += 0.35
        else:
            installed_ids = [e.get('identifier', {}).get('id', '') for e in extensions]
            print(f"FAIL: Component 1 — Live Server not found. Installed: {installed_ids}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: HTML CSS Support extension installed (0.20 points)
    try:
        if is_extension_installed(extensions, HTML_CSS_SUPPORT_ID):
            print(f"PASS: Component 2 — HTML CSS Support (ecmel.vscode-html-css) is installed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — HTML CSS Support extension not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Auto Rename Tag extension installed (0.20 points)
    try:
        if is_extension_installed(extensions, AUTO_RENAME_TAG_ID):
            print(f"PASS: Component 3 — Auto Rename Tag (formulahendry.auto-rename-tag) is installed (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Auto Rename Tag extension not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Load workspace settings for components 4 & 5
    ws_settings = load_json_with_comments(WORKSPACE_SETTINGS)

    # Component 4: Workspace HTML editor uses 2-space indentation (0.125 points)
    # Verifies: .vscode/settings.json has "[html]": {"editor.tabSize": 2, ...}
    try:
        if ws_settings is None:
            print(f"FAIL: Component 4 — Workspace settings file not found at {WORKSPACE_SETTINGS}")
        else:
            expected_html = {"[html]": {"editor.tabSize": 2, "editor.insertSpaces": True}}
            if _is_subset(expected_html, ws_settings):
                print(f"PASS: Component 4 — HTML 2-space indentation set in workspace settings (0.125 pts)")
                total_score += 0.125
            else:
                html_section = ws_settings.get('[html]', 'MISSING')
                print(f"FAIL: Component 4 — Expected HTML tabSize=2 & insertSpaces=true, found: {html_section}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Workspace CSS editor uses 2-space indentation (0.125 points)
    # Verifies: .vscode/settings.json has "[css]": {"editor.tabSize": 2, ...}
    try:
        if ws_settings is None:
            print(f"FAIL: Component 5 — Workspace settings file not found at {WORKSPACE_SETTINGS}")
        else:
            expected_css = {"[css]": {"editor.tabSize": 2, "editor.insertSpaces": True}}
            if _is_subset(expected_css, ws_settings):
                print(f"PASS: Component 5 — CSS 2-space indentation set in workspace settings (0.125 pts)")
                total_score += 0.125
            else:
                css_section = ws_settings.get('[css]', 'MISSING')
                print(f"FAIL: Component 5 — Expected CSS tabSize=2 & insertSpaces=true, found: {css_section}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.3f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
