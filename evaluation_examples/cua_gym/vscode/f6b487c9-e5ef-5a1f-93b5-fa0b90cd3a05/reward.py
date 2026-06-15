"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm editing lengthy Python scripts and keep needing to duplicate lines—could you help me set Ctrl+D to duplicate the current line and add a vertical ruler at column 80 so I can stay within PEP-8 limits?
Generated: 2025-09-11 21:46:36
Status: success
Model: azure-o3
Total Steps: 13
"""

import json
import os
import pathlib
import re
import sys
import traceback

"""
Reward Script for Verifying VS Code / Sublime Text Configuration
---------------------------------------------------------------
• 0.5 points – 80-column ruler is configured
• 0.5 points – Ctrl+D duplicates the current line
Returns a progressive score (0.0‒1.0) with detailed diagnostics.
The script inspects (recursively) the user-level configuration files under
$HOME/.config/**/User/ for VS Code / Codium / Code-OSS / Code-Insiders as well
as Sublime Text.* editors.
No points are awarded for merely existing files – only for the actual settings.
"""

# ---------------------------------------------------------------------------
# Helper utilities for JSONC (JSON with // & /* */ comments + trailing commas)
# ---------------------------------------------------------------------------
_comment_line_re = re.compile(r"//.*")
_block_comment_re = re.compile(r"/\*.*?\*/", re.DOTALL)
_trailing_comma_re = re.compile(r",\s*([}\]])")

def _strip_comments(text: str) -> str:
    text = _comment_line_re.sub("", text)
    text = _block_comment_re.sub("", text)
    return text

def _remove_trailing_commas(text: str) -> str:
    return _trailing_comma_re.sub(r"\1", text)

def _load_jsonc(path: pathlib.Path):
    """Load JSONC file (allows comments & dangling commas)."""
    raw = path.read_text(encoding="utf-8", errors="ignore")
    cleaned = _remove_trailing_commas(_strip_comments(raw)).strip()
    if cleaned == "":
        cleaned = "null"
    return json.loads(cleaned)

# ---------------------------------------------------------------------------
# File discovery helpers
# ---------------------------------------------------------------------------

def _search_files(glob_patterns):
    """Yield Path objects matching the provided glob patterns inside $HOME."""
    home = pathlib.Path.home()
    for pattern in glob_patterns:
        for p in home.glob(pattern):
            if p.is_file():
                yield p

# ---------------------------------------------------------------------------
# Verification logic – 80-column ruler
# ---------------------------------------------------------------------------

def _vscode_ruler_ok(data: dict) -> bool:
    rulers = data.get("editor.rulers")
    if rulers is None:
        return False
    if isinstance(rulers, int):
        return rulers == 80
    if isinstance(rulers, list):
        for r in rulers:
            if (isinstance(r, int) and r == 80) or (
                isinstance(r, dict) and r.get("column") == 80
            ):
                return True
    return False


def _sublime_ruler_ok(data: dict) -> bool:
    rulers = data.get("rulers")
    if rulers is None:
        return False
    if isinstance(rulers, int):
        return rulers == 80
    if isinstance(rulers, list):
        return 80 in rulers
    return False


def verify_ruler() -> bool:
    # VS Code family ---------------------------------------------------------
    vscode_settings_globs = [".config/**/User/settings.json"]
    for path in _search_files(vscode_settings_globs):
        try:
            if _vscode_ruler_ok(_load_jsonc(path)):
                print(f"✓ Found 80-column ruler in VS Code settings: {path}")
                return True
            else:
                print(f"Ruler 80 not configured in {path}")
        except Exception as e:
            print(f"Error reading {path}: {e}")

    # Sublime Text -----------------------------------------------------------
    sublime_settings_globs = [
        ".config/sublime-text*/Packages/User/Preferences.sublime-settings",
    ]
    for path in _search_files(sublime_settings_globs):
        try:
            if _sublime_ruler_ok(_load_jsonc(path)):
                print(f"✓ Found 80-column ruler in Sublime preferences: {path}")
                return True
            else:
                print(f"Ruler 80 not configured in {path}")
        except Exception as e:
            print(f"Error reading {path}: {e}")

    return False

# ---------------------------------------------------------------------------
# Verification logic – Ctrl+D duplicate line
# ---------------------------------------------------------------------------
_duplicate_cmds_vscode = {
    "editor.action.copyLinesDownAction",
    "editor.action.copyLinesUpAction",
    "editor.action.duplicateSelection",
}


def _vscode_ctrl_d_ok(bindings) -> bool:
    if not isinstance(bindings, list):
        return False
    for entry in bindings:
        if not isinstance(entry, dict):
            continue
        key = (entry.get("key") or "").lower().strip()
        cmd = entry.get("command", "").strip()
        if key == "ctrl+d" and cmd in _duplicate_cmds_vscode:
            return True
    return False


def _sublime_ctrl_d_ok(bindings) -> bool:
    if not isinstance(bindings, list):
        return False
    for entry in bindings:
        if not isinstance(entry, dict):
            continue
        keys = [k.lower() for k in entry.get("keys", [])]
        cmd = entry.get("command", "").lower()
        if ("ctrl+d" in keys or "ctrl+d" in "".join(keys)) and "duplicate" in cmd:
            return True
    return False


def verify_keybinding() -> bool:
    # VS Code family ---------------------------------------------------------
    vscode_key_globs = [".config/**/User/keybindings.json"]
    for path in _search_files(vscode_key_globs):
        try:
            if _vscode_ctrl_d_ok(_load_jsonc(path)):
                print(f"✓ Found Ctrl+D duplicate-line keybinding in VS Code: {path}")
                return True
            else:
                print(f"Ctrl+D duplicate keybinding not found in {path}")
        except Exception as e:
            print(f"Error reading {path}: {e}")

    # Sublime Text -----------------------------------------------------------
    sublime_key_globs = [
        ".config/sublime-text*/Packages/User/*.sublime-keymap",
    ]
    for path in _search_files(sublime_key_globs):
        try:
            if _sublime_ctrl_d_ok(_load_jsonc(path)):
                print(f"✓ Found Ctrl+D duplicate-line keybinding in Sublime: {path}")
                return True
            else:
                print(f"Ctrl+D duplicate keybinding not found in {path}")
        except Exception as e:
            print(f"Error reading {path}: {e}")

    return False

# ---------------------------------------------------------------------------
# Main scoring routine
# ---------------------------------------------------------------------------

def verify_task() -> float:
    total_score = 0.0

    # 1) Ruler verification --------------------------------------------------
    if verify_ruler():
        total_score += 0.5
    else:
        print("✗ 80-column ruler requirement not met.")

    # 2) Keybinding verification --------------------------------------------
    if verify_keybinding():
        total_score += 0.5
    else:
        print("✗ Ctrl+D duplicate-line keybinding requirement not met.")

    total_score = min(total_score, 1.0)
    print(f"Total score: {total_score}/1.0")
    print(f"REWARD: {total_score}")
    return total_score

# ---------------------------------------------------------------------------
# Script entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    try:
        verify_task()
    except Exception as exc:
        print("Unexpected error during verification:", exc)
        traceback.print_exc()
        print("REWARD: 0.0")
