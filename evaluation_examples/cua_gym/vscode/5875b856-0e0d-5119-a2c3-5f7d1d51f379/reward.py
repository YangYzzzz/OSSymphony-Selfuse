"""
FINAL REWARD SCRIPT - SUCCESS
Task: I keep forgetting to save my files while working on my TypeScript project, and it's messing up my live-reload workflow—could you show me how to turn on VS Code’s auto-save with a 1000 ms delay?
Generated: 2025-09-11 17:35:28
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import re
import json
import pathlib


def _strip_json_noise(text: str) -> str:
    """Remove comments and trailing commas from a VS Code-style JSONC file."""
    # Strip // line comments
    text = re.sub(r"//.*", "", text)
    # Strip /* multi-line */ comments
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # Remove trailing commas before }} or ]]
    text = re.sub(r",\s*([}\]])", r"\1", text)
    return text


def _load_json_safely(path: pathlib.Path):
    """Return dict if JSON parses, otherwise None."""
    try:
        raw = path.read_text(encoding="utf-8")
    except Exception:
        return None
    cleaned = _strip_json_noise(raw)
    try:
        return json.loads(cleaned)
    except Exception:
        return None


def _candidate_settings_files() -> list[pathlib.Path]:
    """Return a list of likely VS Code settings files (user + workspace)."""
    home = pathlib.Path.home()
    paths: set[pathlib.Path] = {
        home / ".config/Code/User/settings.json",                    # Linux user
        home / ".config/VSCodium/User/settings.json",               # VSCodium user
        home / "AppData/Roaming/Code/User/settings.json",           # Windows (WSL)
        home / "Library/Application Support/Code/User/settings.json",# macOS
        home / ".vscode/settings.json",                             # project root
    }

    # Discover additional *.code-workspace files & .vscode/settings.json (depth-limited)
    max_depth = 4
    for root, dirs, files in os.walk(home):
        depth = len(pathlib.Path(root).parts) - len(home.parts)
        if depth > max_depth:
            dirs[:] = []  # prune deep traversal
            continue
        if ".vscode" in dirs:
            paths.add(pathlib.Path(root) / ".vscode/settings.json")
        for fn in files:
            if fn.endswith(".code-workspace"):
                paths.add(pathlib.Path(root) / fn)
    return list(paths)


def verify_vscode_auto_save() -> float:
    """Verify VS Code auto-save is set to afterDelay with 1000 ms delay."""
    auto_save_ok = False
    delay_ok = False
    verified_path: str | None = None

    for fpath in _candidate_settings_files():
        if not fpath.exists():
            continue
        # ---------- Structured JSON check ----------
        settings = _load_json_safely(fpath)
        if settings is not None:
            auto_val = settings.get("files.autoSave")
            if isinstance(auto_val, str) and auto_val.lower() == "afterdelay":
                auto_save_ok = True
                delay_val = settings.get("files.autoSaveDelay")
                if isinstance(delay_val, (int, float, str)) and int(delay_val) == 1000:
                    delay_ok = True
                if auto_save_ok and delay_ok:
                    verified_path = str(fpath)
                    break  # full success found
        # ---------- Regex fallback for JSONC that couldn't be parsed ----------
        try:
            text = fpath.read_text(encoding="utf-8", errors="ignore")
        except Exception:
            continue
        if re.search(r"\"files\\.autoSave\"\s*:\s*\"afterDelay\"", text):
            auto_save_ok = True
            if re.search(r"\"files\\.autoSaveDelay\"\s*:\s*1000", text):
                delay_ok = True
                verified_path = str(fpath)
                break

    # Progressive scoring
    score = 0.0
    if auto_save_ok:
        score += 0.5
        if delay_ok:
            score += 0.5

    # ---------------- Debug output ----------------
    print("VS Code Auto-Save Verification Results")
    print(f"Auto-save set to 'afterDelay': {auto_save_ok}")
    print(f"Auto-save delay set to 1000 ms: {delay_ok}")
    if verified_path:
        print(f"Verified in settings file: {verified_path}")
    print(f"REWARD: {score}")
    return score


if __name__ == "__main__":
    verify_vscode_auto_save()
