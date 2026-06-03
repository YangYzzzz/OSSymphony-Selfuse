"""
FINAL REWARD SCRIPT - SUCCESS
Task: My team enforces a 100-character line limit for all our Python files—how can I get VS Code to display a vertical guide at that exact column while I’m coding?
Generated: 2025-09-11 16:12:37
Status: success
Model: azure-o3
Total Steps: 19
"""

import os
import re
import json
from pathlib import Path

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def _strip_json5_comments(text: str) -> str:
    """Remove // and /* */ comments and trailing commas from VS-Code-style JSON5."""
    # Remove // line comments
    text = re.sub(r"(^|\s)//.*", "", text, flags=re.MULTILINE)
    # Remove /*  */ block comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.DOTALL)
    # Remove trailing commas (best effort – keeps JSON valid in most cases)
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text


def _safe_load_json5(text: str):
    """Attempt to parse VS Code settings (JSON5). Returns None on failure."""
    try:
        cleaned = _strip_json5_comments(text)
        return json.loads(cleaned)
    except Exception:
        return None


def _list_contains_100(ruler_list):
    """Check if a VS Code ruler list specifies column 100."""
    for item in ruler_list:
        # item may be 100 or { "column": 100, ... }
        if isinstance(item, int) and item == 100:
            return True
        if isinstance(item, dict) and item.get("column") == 100:
            return True
    return False


def _settings_has_100_ruler(settings: dict) -> bool:
    """Return True if settings (global or language-specific) contain a 100-col ruler."""
    if not isinstance(settings, dict):
        return False

    # Global editor.rulers
    if _list_contains_100(settings.get("editor.rulers", [])):
        return True

    # Language-scoped blocks (e.g. "[python]")
    for key, value in settings.items():
        if isinstance(key, str) and key.startswith("[") and key.endswith("]") and isinstance(value, dict):
            if _list_contains_100(value.get("editor.rulers", [])):
                return True
    return False

# -----------------------------------------------------------------------------
# Verification logic
# -----------------------------------------------------------------------------

def verify_task() -> float:
    """Verify VS Code is configured with a 100-character ruler for Python files."""

    home = Path.home()
    candidate_files = set()

    # Common user-level settings locations
    candidate_files.add(home / ".config" / "Code" / "User" / "settings.json")
    candidate_files.add(home / ".vscode" / "settings.json")

    # Search workspaces under $HOME for .vscode/settings.json (prune heavy dirs)
    prune = {".cache", ".local", ".npm", ".cargo", ".rustup", ".vscode-server", ".conda"}
    for root, dirs, files in os.walk(home):
        dirs[:] = [d for d in dirs if d not in prune and not d.startswith(".git")]
        if ".vscode" in dirs:
            candidate_files.add(Path(root) / ".vscode" / "settings.json")

    found_rulers_key = False   # any appearance of "editor.rulers"
    found_100_ruler  = False   # explicit 100-column ruler

    for settings_path in candidate_files:
        if not settings_path.exists():
            continue
        try:
            raw = settings_path.read_text(encoding="utf-8")
        except Exception as e:
            print(f"⚠️  Could not read {settings_path}: {e}")
            continue

        # Quick string check for key presence (cheap)
        if "editor.rulers" in raw:
            found_rulers_key = True

        parsed = _safe_load_json5(raw)
        if parsed is not None and _settings_has_100_ruler(parsed):
            print(f"✓ 100-column ruler detected in: {settings_path}")
            found_100_ruler = True

    # ------------------------ Scoring ------------------------
    score = 0.0

    if found_rulers_key:
        print("✓ 'editor.rulers' setting present (0.4 points)")
        score += 0.4
    else:
        print("✗ No 'editor.rulers' setting found (0 points)")

    if found_100_ruler:
        print("✓ 100-character ruler configured (0.6 points)")
        score += 0.6
    else:
        print("✗ 100-character ruler not found (0 points)")

    score = min(score, 1.0)
    return score

# -----------------------------------------------------------------------------
if __name__ == "__main__":
    final_score = verify_task()
    print(f"REWARD: {final_score}")
