"""
FINAL REWARD SCRIPT - SUCCESS
Task: I recently moved over from Atom and really miss its “One Dark” look—could you help me switch VS Code to the “Atom One Dark” color theme?
Generated: 2025-09-11 19:07:25
Status: success
Model: azure-o3
Total Steps: 11
"""

import os
import json
import re
from pathlib import Path

# ------------------ Helper Functions ------------------

def strip_json_comments(content: str) -> str:
    """Remove // style comments from VS Code JSON settings files."""
    cleaned_lines = []
    for line in content.splitlines():
        stripped = line.lstrip()
        if stripped.startswith('//'):
            continue  # Skip full-line comments
        # Naively cut off inline comments
        if '//' in line:
            line = line.partition('//')[0]
        cleaned_lines.append(line)
    return '\n'.join(cleaned_lines)


def load_settings_json(path: Path) -> dict:
    """Load a VS Code settings.json, tolerating comments & dangling commas."""
    try:
        raw = path.read_text(encoding='utf-8')
        clean = strip_json_comments(raw)
        # remove dangling commas that break json.loads
        clean = re.sub(r',\s*([}\]])', r'\1', clean, flags=re.M)
        return json.loads(clean or '{}')
    except Exception as e:
        print(f"✗ Could not parse {path}: {e}")
        return {}


def is_atom_one_dark_theme(name: str | None) -> bool:
    if not name:
        return False
    n = name.lower().strip()
    exact = {
        'atom one dark', 'atom-one-dark', 'one dark',
        'one dark pro', 'one dark pro dark', 'onedark'
    }
    if n in exact:
        return True
    # Heuristic: must contain both "one" & "dark"
    return 'one' in n and 'dark' in n


def detect_theme_setting() -> tuple[bool, str | None, Path | None]:
    """Return (is_set, theme_value, settings_path)."""
    user_dirs = [
        Path.home()/'.config'/'Code'/'User',
        Path.home()/'.config'/'Code - OSS'/'User',
        Path.home()/'.config'/'Code - Insiders'/'User',
        Path.home()/'.config'/'VSCodium'/'User',
    ]
    for cfg_dir in user_dirs:
        settings_path = cfg_dir/'settings.json'
        if settings_path.exists():
            data = load_settings_json(settings_path)
            theme = data.get('workbench.colorTheme')
            if theme is not None:
                if is_atom_one_dark_theme(theme):
                    print(f"✓ workbench.colorTheme set to '{theme}' in {settings_path}")
                    return True, theme, settings_path
                else:
                    print(f"Theme found ('{theme}') in {settings_path} but it is NOT Atom One Dark")
    print("✗ Atom One Dark theme not set in any discovered settings.json file")
    return False, None, None


def is_one_dark_extension_folder(name: str) -> bool:
    ln = name.lower()
    return ('one-dark' in ln or 'onedark' in ln) and ('theme' in ln or 'dark' in ln)


def detect_extension_installed() -> bool:
    """Check typical extension directories for an Atom/One Dark theme folder."""
    roots = [
        Path.home()/'.vscode'/'extensions',
        Path.home()/'.vscode-insiders'/'extensions',
        Path.home()/'.vscode-oss'/'extensions',
        Path.home()/'.vscodium'/'extensions',
    ]
    found = False
    for root in roots:
        if root.exists():
            for child in root.iterdir():
                if child.is_dir() and is_one_dark_extension_folder(child.name):
                    print(f"✓ Found One Dark related extension directory: {child}")
                    found = True
    if not found:
        print("✗ No Atom/One Dark themed extension directory located")
    return found

# ------------------ Main Verification ------------------

def verify_task() -> float:
    score = 0.0

    # Requirement 1: Theme set correctly (0.8 pts)
    theme_ok, _, _ = detect_theme_setting()
    if theme_ok:
        score += 0.8
    else:
        print("No correct theme => 0 points for this requirement")

    # Requirement 2: Extension installed (0.2 pts)
    ext_ok = detect_extension_installed()
    if ext_ok:
        score += 0.2
    else:
        print("Required extension not found => 0 points for this requirement")

    final = round(min(score, 1.0), 2)
    print(f"REWARD: {final}")
    return final

# ------------------ Script Entry Point ------------------
if __name__ == '__main__':
    verify_task()
