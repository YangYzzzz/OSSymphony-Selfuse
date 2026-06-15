"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m developing an Express API in /home/user/projects/todo-app and need the “REST Client” extension for testing my endpoints; could you also hide every “.env” file anywhere under /home/user/ in the Explorer view?
Generated: 2025-09-12 00:32:58
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import re
import json
from pathlib import Path

"""
Reward Verification Script
Task verification for:
1. "REST Client" (humao.rest-client) extension installed in VS Code.
2. All .env files hidden from Explorer via VS Code settings (files.exclude / explorer.exclude / search.exclude / files.watcherExclude).

Scoring (progressive):
 • 0.5 – REST Client extension detected in any standard extension directory.
 • 0.5 – An exclusion pattern containing ".env" with a truthy value found in any settings.json (user or workspace).

A perfect setup yields REWARD: 1.0.
"""

# ------------------------------------------------------------
# Helper functions
# ------------------------------------------------------------

def strip_json_comments(text: str) -> str:
    """Remove //-style comments and trailing commas from JSON text."""
    lines = []
    for line in text.splitlines():
        stripped = line.lstrip()
        if stripped.startswith("//"):
            continue
        if "//" in line:
            line = line.split("//", 1)[0]
        lines.append(line)
    cleaned = "\n".join(lines)
    cleaned = re.sub(r",\s*([}\]])", r"\1", cleaned)  # remove trailing commas
    return cleaned

def load_json(path: Path):
    """Load JSON from *settings.json* while tolerating comments & trailing commas."""
    try:
        text = path.read_text(encoding="utf-8", errors="replace")
        return json.loads(strip_json_comments(text))
    except Exception as exc:
        print(f"   - Could not parse JSON in {path}: {exc}")
        return None

# ------------------------------------------------------------
# Requirement 1 – REST Client extension
# ------------------------------------------------------------

def rest_client_installed() -> bool:
    home = Path.home()
    roots = [
        home/".vscode",                 # local VS Code
        home/".vscode-insiders",        # insiders build
        home/".vscode-server",          # remote-SSH/WSL
        home/".local"/"share"/"code-server",  # code-server
        home/".local"/"share"/"vscode"        # other variants
    ]

    for root in roots:
        ext_dir = root/"extensions"
        if not ext_dir.is_dir():
            continue
        for item in ext_dir.iterdir():
            # Folder name pattern: humao.rest-client-<version>
            if "humao.rest-client" in item.name.lower():
                print(f"✓ Found REST Client extension: {item}")
                return True
    print("✗ REST Client extension not found in expected directories")
    return False

# ------------------------------------------------------------
# Requirement 2 – .env exclusion in Explorer
# ------------------------------------------------------------

def key_hides_env(key: str, value) -> bool:
    """True if key contains '.env' and value is truthy (True / 'true')."""
    if re.search(r"\.env", key, re.IGNORECASE):
        return (isinstance(value, bool) and value) or (isinstance(value, str) and value.lower() == "true")
    return False

def env_files_hidden() -> bool:
    home = Path.home()
    settings_files = set()

    # Known global-user settings locations
    user_settings_candidates = [
        home/".config"/"Code"/"User"/"settings.json",
        home/".local"/"share"/"code-server"/"User"/"settings.json",
        home/".vscode-server"/"data"/"User"/"settings.json",
        home/".vscode-oss"/"data"/"User"/"settings.json",
    ]

    for p in user_settings_candidates:
        if p.is_file():
            settings_files.add(p)

    # Workspace-level settings (any *.vscode/settings.json* under home)
    for dirpath, _, filenames in os.walk(home):
        if "settings.json" in filenames and ".vscode" in dirpath:
            settings_files.add(Path(dirpath)/"settings.json")

    for sfile in settings_files:
        data = load_json(sfile)
        if not isinstance(data, dict):
            continue
        for section in ("files.exclude", "explorer.exclude", "search.exclude", "files.watcherExclude"):
            sect_val = data.get(section)
            if isinstance(sect_val, dict):
                print(f"-- Checking {section} in {sfile}")
                for k, v in sect_val.items():
                    if key_hides_env(k, v):
                        print(f"     ✓ Exclude entry found → '{k}': {v}")
                        print("✓ .env exclusion verified")
                        return True
    print("✗ No .env exclusion pattern found in any settings.json file")
    return False

# ------------------------------------------------------------
# Scoring aggregation
# ------------------------------------------------------------

def calculate_score() -> float:
    score = 0.0
    if rest_client_installed():
        score += 0.5
    if env_files_hidden():
        score += 0.5
    return min(score, 1.0)

# ------------------------------------------------------------
# Script entry point
# ------------------------------------------------------------

def main():
    print("Starting task verification …")
    reward = calculate_score()
    print(f"REWARD: {reward}")
    return reward

if __name__ == "__main__":
    main()
