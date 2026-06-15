"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m working on the React client in /home/user/frontend.code-workspace—could you help me open that workspace and map “Format Document” to Ctrl + Shift + F?
Generated: 2025-09-12 00:02:51
Status: success
Model: azure-o3
Total Steps: 16
"""

import os
import json
import re
import pathlib

# ----------------------------------------------------------------------------
# Helper: Load JSON / JSONC (JSON with comments) safely
# ----------------------------------------------------------------------------

def load_jsonc(path: str):
    """Load a VS Code JSON/JSONC file.

    VS Code configuration files may contain:
    • // single-line comments
    • /* multi-line comments */
    • trailing commas before a closing } or ]

    This helper removes those constructs so the file can be parsed by
    json.loads().  If the file cannot be read or parsed, it returns None.
    """
    try:
        text = pathlib.Path(path).read_text(encoding="utf-8")
    except (FileNotFoundError, PermissionError):
        return None

    # Strip /* … */ comments (can span lines)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Strip // … comments (to end of line)
    text = re.sub(r"//.*", "", text)
    # Remove trailing commas before } or ]
    text = re.sub(r",\s*([}\]])", r"\1", text)

    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return None

# ----------------------------------------------------------------------------
# Workspace verification (max 0.4 points)
# ----------------------------------------------------------------------------

def verify_workspace(ws_path: str) -> float:
    """Verify that the requested VS Code workspace exists and is valid."""
    score = 0.0

    if not os.path.exists(ws_path):
        print(f"✗ Workspace file not found at {ws_path}")
        return score  # 0.0

    print(f"✓ Workspace file found: {ws_path} (+0.3)")
    score += 0.3

    data = load_jsonc(ws_path)
    if not data or not isinstance(data, dict):
        print("✗ Workspace file cannot be parsed – skipping deep checks")
        return score  # keep the 0.3 already earned

    folders = data.get("folders")
    if folders and isinstance(folders, list):
        print(f"✓ 'folders' array present with {len(folders)} item(s) (+0.1)")
        score += 0.1
    else:
        print("✗ 'folders' array missing or invalid")

    if "settings" in data:
        print("✓ 'settings' section present (+0.1)")
        score += 0.1

    # Cap workspace score at 0.4
    return min(score, 0.4)

# ----------------------------------------------------------------------------
# Keybinding verification (max 0.6 points)
# ----------------------------------------------------------------------------

def _normalize_key_string(key: str) -> str:
    """Normalise keybinding string for comparison (case & space insensitive)."""
    return key.lower().replace(" ", "").replace("cmd", "ctrl")


def _scan_keybinding_file(path: str) -> bool:
    """Return True if file maps Ctrl+Shift+F → editor.action.formatDocument."""
    data = load_jsonc(path)
    if not isinstance(data, list):
        return False

    for entry in data:
        if not isinstance(entry, dict):
            continue
        key = entry.get("key") or entry.get("keybinding")  # be tolerant
        cmd = entry.get("command")
        if key and cmd and _normalize_key_string(key) == "ctrl+shift+f" and cmd == "editor.action.formatDocument":
            print(f"✓ Desired keybinding found in {path}: {entry} (+0.6)")
            return True
    return False


def verify_keybindings() -> float:
    """Search all plausible keybinding locations for the required mapping."""
    candidate_paths = [
        os.path.expanduser("~/.config/Code/User/keybindings.json"),
        os.path.expanduser("~/.config/Code - OSS/User/keybindings.json"),
        os.path.expanduser("~/.config/Code - Insiders/User/keybindings.json"),
        os.path.expanduser("~/.vscode-server/data/Machine/keybindings.json"),  # Remote server install
    ]

    # Also search recursively for keybindings.json inside any .vscode directory
    for path_obj in pathlib.Path("/home/user").rglob("keybindings.json"):
        candidate_paths.append(str(path_obj))

    checked: set[str] = set()
    for path in candidate_paths:
        real = os.path.realpath(path)
        if real in checked or not os.path.exists(real):
            continue
        checked.add(real)
        if _scan_keybinding_file(real):
            return 0.6  # Full points for keybinding requirement

    print("✗ Desired keybinding (Ctrl+Shift+F → Format Document) NOT found in any searched file")
    return 0.0

# ----------------------------------------------------------------------------
# Main verification entry‐point
# ----------------------------------------------------------------------------

def verify_task() -> float:
    total_score = 0.0

    # 1. Workspace check (max 0.4)
    total_score += verify_workspace("/home/user/frontend.code-workspace")

    # 2. Keybinding check (max 0.6)
    total_score += verify_keybindings()

    # Ensure final score does not exceed 1.0
    total_score = min(total_score, 1.0)

    print(f"Total score: {total_score}")
    print(f"REWARD: {total_score}")

    return total_score

# Execute when run as a script
if __name__ == "__main__":
    verify_task()
