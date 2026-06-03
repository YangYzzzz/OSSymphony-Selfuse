"""
FINAL REWARD SCRIPT - SUCCESS
Task: My TypeScript files all look different, and it’s hard to keep them consistent—could you help me add the “Prettier – Code formatter” extension to VS Code so it formats them automatically?
Generated: 2025-09-11 15:10:06
Status: success
Model: azure-o3
Total Steps: 13
"""

import os
import re
import json
from pathlib import Path

PRETTIER_ID_PREFIX = 'esbenp.prettier-vscode'

###############################
# Helper utilities
###############################

def strip_json_comments(text: str) -> str:
    """Remove // line comments from JSON (sufficient for VS Code settings)."""
    # Matches // comment till line end that is preceded by beginning-of-line or whitespace.
    return re.sub(r'(^|\s)//.*?$', '', text, flags=re.MULTILINE)


def load_json(path: Path) -> dict:
    """Load JSON file with comment stripping. Return empty dict on failure."""
    if not path.exists():
        return {}
    try:
        cleaned = strip_json_comments(path.read_text(encoding='utf-8'))
        data = json.loads(cleaned)
        return data if isinstance(data, dict) else {}
    except Exception as e:
        print(f"   - Failed to parse {path}: {e}")
        return {}


###############################
# Verification helpers
###############################

def prettier_extension_installed() -> bool:
    """Check common VS Code extension folders for the Prettier extension."""
    potential_dirs = [
        Path.home()/'.vscode'/'extensions',          # local
        Path.home()/'.vscode-server'/'extensions',   # remote (SSH / WSL)
        Path.home()/'.vscode-test'/'extensions',     # test harness
    ]
    found = []
    for base in potential_dirs:
        if base.exists():
            for entry in base.iterdir():
                if entry.is_dir() and entry.name.startswith(PRETTIER_ID_PREFIX):
                    found.append(entry.name)
    if found:
        print(f" ✓ Found Prettier extension(s): {found}")
        return True
    print(" ✗ Prettier extension not found in expected locations")
    return False


def gather_user_settings() -> dict:
    """Merge user settings from typical VS Code paths into a single dict."""
    paths = [
        Path.home()/'.config'/'Code'/'User'/'settings.json',           # Linux
        Path.home()/'.config'/'Code - Insiders'/'User'/'settings.json',
        Path.home()/'.vscode'/'settings.json',                         # Portable mode
    ]
    merged = {}
    for p in paths:
        if p.exists():
            print(f" - Loading settings from {p}")
            merged.update(load_json(p))  # Later files override earlier keys
    return merged


def format_on_save_enabled(settings: dict) -> bool:
    """Determine if automatic formatting on save is enabled for TS/JS or globally."""
    # Global switch
    if settings.get('editor.formatOnSave') is True:
        print(' ✓ editor.formatOnSave enabled globally')
        return True
    # Scope-specific switches
    scopes = ['[typescript]', '[typescriptreact]', '[javascript]', '[javascriptreact]']
    for scope in scopes:
        scope_cfg = settings.get(scope)
        if isinstance(scope_cfg, dict) and scope_cfg.get('editor.formatOnSave') is True:
            print(f' ✓ editor.formatOnSave enabled in scope {scope}')
            return True
    print(' ✗ editor.formatOnSave not enabled')
    return False


def prettier_default_formatter(settings: dict) -> bool:
    """Check if Prettier is configured as the default formatter (optional bonus)."""
    if settings.get('editor.defaultFormatter') == PRETTIER_ID_PREFIX:
        print(' ✓ Prettier set as global default formatter')
        return True
    scopes = ['[typescript]', '[typescriptreact]', '[javascript]', '[javascriptreact]']
    for scope in scopes:
        scope_cfg = settings.get(scope)
        if isinstance(scope_cfg, dict) and scope_cfg.get('editor.defaultFormatter') == PRETTIER_ID_PREFIX:
            print(f' ✓ Prettier set as default formatter in scope {scope}')
            return True
    print(' - Prettier not explicitly set as default formatter')
    return False


###############################
# Main verification routine
###############################

def verify_task() -> float:
    print('--- Verifying VS Code is set up with Prettier & auto-format ---')
    score = 0.0

    # Requirement 1: Extension must be installed (0.6 pts)
    if prettier_extension_installed():
        score += 0.6

    # Load user settings
    settings = gather_user_settings()
    if not settings:
        print(' - No VS Code user settings found; using VS Code defaults')

    # Requirement 2: Automatic format on save must be enabled (0.4 pts)
    if format_on_save_enabled(settings):
        score += 0.4

    # Optional: Prettier selected as default formatter (0.1 bonus, score capped at 1.0)
    if prettier_default_formatter(settings):
        score += 0.1

    # Ensure progressive scoring does not exceed 1.0
    final_score = min(round(score, 2), 1.0)
    print(f'Final score: {final_score}')
    print(f'REWARD: {final_score}')
    return final_score


if __name__ == '__main__':
    verify_task()
