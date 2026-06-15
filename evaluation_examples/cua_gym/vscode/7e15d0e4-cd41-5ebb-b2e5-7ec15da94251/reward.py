"""
Reward Script: Install GitLens extension and enable current line blame annotation
Task ID: vscode_ext_027
Domain: vs_code
Scoring:
  Component 1: GitLens (eamodio.gitlens) extension is installed   — 0.6 points
  Component 2: gitlens.currentLine.enabled is set to true          — 0.4 points
  Total: 1.0
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ext_027'

EXTENSIONS_JSON = os.path.join(WORKDIR, '.vscode', 'extensions', 'extensions.json')
SETTINGS_JSON   = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')
GITLENS_EXT_DIR = os.path.join(WORKDIR, '.vscode', 'extensions')


def load_settings():
    """Load VSCode user settings.json, stripping JSONC comments."""
    try:
        with open(SETTINGS_JSON, 'r') as f:
            content = f.read()
        # Strip single-line // comments (VSCode uses JSONC)
        content_stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_stripped)
    except FileNotFoundError:
        return {}
    except json.JSONDecodeError:
        return {}


def load_extensions_registry():
    """Load the VSCode extensions registry JSON."""
    try:
        with open(EXTENSIONS_JSON, 'r') as f:
            return json.load(f)
    except (FileNotFoundError, json.JSONDecodeError):
        return []


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: GitLens extension (eamodio.gitlens) is installed (0.6 points)
    # Verified by checking the extensions registry JSON AND the extension directory.
    # On initial_env: extensions.json is [] and no extension directory exists → FAIL
    # On golden_env:  extensions.json contains eamodio.gitlens entry and directory exists → PASS
    try:
        registry = load_extensions_registry()
        gitlens_registered = any(
            entry.get('identifier', {}).get('id', '').lower() == 'eamodio.gitlens'
            for entry in registry
        )

        # Also check the physical directory as a cross-check
        gitlens_dir_exists = False
        try:
            entries = os.listdir(GITLENS_EXT_DIR)
            gitlens_dir_exists = any(
                e.lower().startswith('eamodio.gitlens') for e in entries
            )
        except OSError:
            gitlens_dir_exists = False

        if gitlens_registered and gitlens_dir_exists:
            print(f"PASS: Component 1 — GitLens extension is registered in extensions.json "
                  f"AND extension directory exists (0.6 pts)")
            total_score += 0.6
        elif gitlens_registered:
            print(f"PARTIAL: Component 1 — GitLens registered in extensions.json "
                  f"but extension directory not found (0.3 pts)")
            total_score += 0.3
        elif gitlens_dir_exists:
            print(f"PARTIAL: Component 1 — GitLens extension directory exists "
                  f"but not registered in extensions.json (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — GitLens extension not found. "
                  f"Registry entries: {len(registry)}, "
                  f"Dir has gitlens: {gitlens_dir_exists}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check GitLens extension: {e}")

    # Component 2: gitlens.currentLine.enabled is set to true in settings.json (0.4 points)
    # On initial_env: the setting is explicitly set to false → FAIL
    # On golden_env:  the setting is explicitly set to true  → PASS
    try:
        settings = load_settings()
        current_line_enabled = settings.get('gitlens.currentLine.enabled', None)

        if current_line_enabled is True:
            print(f"PASS: Component 2 — gitlens.currentLine.enabled is true in settings.json (0.4 pts)")
            total_score += 0.4
        elif current_line_enabled is False:
            print(f"FAIL: Component 2 — gitlens.currentLine.enabled is explicitly set to false "
                  f"(must be true)")
        elif current_line_enabled is None:
            # Key not present — GitLens default is true, but task context says to verify it's not disabled.
            # We require the explicit setting to be present and true.
            print(f"FAIL: Component 2 — gitlens.currentLine.enabled key not found in settings.json. "
                  f"Task requires it to be explicitly enabled (true).")
        else:
            print(f"FAIL: Component 2 — gitlens.currentLine.enabled has unexpected value: "
                  f"{current_line_enabled!r} (expected True)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check gitlens.currentLine.enabled: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
