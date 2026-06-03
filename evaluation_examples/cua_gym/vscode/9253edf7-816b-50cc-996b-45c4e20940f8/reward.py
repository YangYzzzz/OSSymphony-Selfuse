"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m regularly updating the README for my project and it’s tedious to open the preview with the mouse each time—can you assign Ctrl + Shift + V to instantly bring up the Markdown preview in VS Code?
Generated: 2025-09-11 23:50:50
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import json
import re
import pathlib
import sys

# -----------------------------------------
# VS Code Markdown Preview Shortcut Verifier
# -----------------------------------------
# This reward script checks that the user has
# created a custom key-binding that maps
#   Ctrl + Shift + V    (or Cmd + Shift + V on macOS)
# to one of VS Code’s Markdown preview
# commands (e.g.  "markdown.showPreview").
# The script awards:
#   • 0.6 points if the shortcut exists at all
#   • 0.4 additional points if the shortcut
#     launches a Markdown preview command
# yielding a maximum reward of 1.0.
# -----------------------------------------

# Valid commands that open the Markdown preview
PREVIEW_COMMANDS = {
    "markdown.showPreview",
    "markdown.showpreview",
    "markdown.showPreviewToSide",
    "markdown.showpreviewtoside",
}

# ------------------------------------------------
# Helper: strip line (// …) & block (/* … */) notes
# because VS Code JSON files allow comments (JSONC)
# ------------------------------------------------

def _strip_comments(text: str) -> str:
    """Remove // and /* */ comments from VS Code JSON files."""
    # Remove block comments first
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove // comments that are not inside strings (best-effort)
    text = re.sub(r"(?<!:)//.*", "", text)
    return text

# --------------------------------------------
# Helper: load & parse keybindings.json safely
# --------------------------------------------

def _load_keybindings(path: pathlib.Path):
    try:
        raw = path.read_text(encoding="utf-8", errors="ignore")
    except Exception as e:
        print(f"✗ Error reading {path}: {e}")
        return None

    cleaned = _strip_comments(raw)
    try:
        data = json.loads(cleaned or "[]")
        if not isinstance(data, list):
            print("✗ keybindings.json content is not a list")
            return []
        return data
    except json.JSONDecodeError as e:
        print(f"✗ JSON parsing error in {path}: {e}")
        return None

# -------------------------------------------------------
# Helper: locate keybindings.json for the current platform
# -------------------------------------------------------

def _find_keybindings_file():
    home = pathlib.Path.home()
    # Standard VS Code locations on major OSes
    guesses = [
        home / ".config/Code/User/keybindings.json",                              # Linux
        home / "AppData/Roaming/Code/User/keybindings.json",                     # Windows
        home / "Library/Application Support/Code/User/keybindings.json",         # macOS
    ]
    for p in guesses:
        if p.exists():
            return p

    # Fallback: shallow search under ~ if user uses Insiders or OSS build
    for p in home.glob("**/keybindings.json"):
        if "Code" in str(p):
            return p
    return None

# ---------------------
# Main verification job
# ---------------------

def verify_task():
    total_score = 0.0
    max_score = 1.0

    kb_path = _find_keybindings_file()
    if not kb_path:
        print("✗ Could not find keybindings.json file in expected locations")
        print("REWARD: 0.0")
        return 0.0

    print(f"✓ Located keybindings.json at {kb_path}")
    data = _load_keybindings(kb_path)
    if data is None:
        print("REWARD: 0.0")
        return 0.0

    # Examine each key-binding entry
    binding_found = False
    correct_command = False

    for entry in data:
        if not isinstance(entry, dict):
            continue
        key_combo = entry.get("key") or entry.get("keys")
        if not key_combo:
            continue
        key_combo_norm = str(key_combo).lower().replace(" ", "")
        # Allow Cmd on macOS as functional equivalent
        if key_combo_norm in {"ctrl+shift+v", "cmd+shift+v"}:
            binding_found = True
            cmd = str(entry.get("command", ""))
            if cmd in PREVIEW_COMMANDS:
                correct_command = True
                break  # Full success achieved

    # Progressive scoring
    if binding_found:
        total_score += 0.6
        print("✓ A custom binding for Ctrl+Shift+V (or Cmd+Shift+V) was found (0.6 points)")
        if correct_command:
            total_score += 0.4
            print("✓ The binding triggers a Markdown Preview command (0.4 points)")
        else:
            print("✗ Binding does not trigger a Markdown Preview command (0 additional points)")
    else:
        print("✗ No binding for Ctrl+Shift+V (or Cmd+Shift+V) found (0 points)")

    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score

# Execute verification when run as a script
if __name__ == "__main__":
    verify_task()
