"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m juggling several projects and don’t have time to check for new versions of my Python, GitLens, and Prettier extensions—could you show me how to turn on auto-updates for every extension I’ve installed in VS Code?
Generated: 2025-09-11 12:19:33
Status: success
Model: azure-o3
Total Steps: 6
"""

import json
import re
import pathlib


def strip_json_comments(text: str) -> str:
    """Remove line (`//`) and block (`/* */`) comments from a JSON-like string
    so it can be parsed by the standard json module."""
    # remove block comments first (including newlines)
    text = re.sub(r"/\*.*?\*/", "", text, flags=re.S)
    # remove single-line comments
    text = re.sub(r"//.*", "", text)
    return text


def locate_settings_json() -> pathlib.Path | None:
    """Return the first VS Code settings.json that exists for the current user."""
    home = pathlib.Path.home()
    # Typical locations for stable VS Code, Insiders, and Windows roaming profile
    candidates = [
        home / ".config/Code/User/settings.json",                    # Linux/macOS – Stable
        home / ".config/Code - Insiders/User/settings.json",        # Linux/macOS – Insiders
        home / "AppData/Roaming/Code/User/settings.json",           # Windows – Stable (for completeness)
    ]
    for path in candidates:
        if path.exists():
            return path
    return None


def verify_task() -> float:
    """Verify that VS Code is configured to auto-update *all* extensions.

    Scoring (progressive):
      • extensions.autoUpdate = true ............. 0.6 pts
      • extensions.autoCheckUpdates = true ....... 0.3 pts
      • NO extensions.autoUpdateIgnore list ...... 0.1 pts
    Returns a float between 0.0 and 1.0 inclusive and prints diagnostics.
    """
    print("Checking VS Code extension auto-update settings…")
    max_score = 1.0
    total_score = 0.0

    settings_path = locate_settings_json()
    if not settings_path:
        print("✗ settings.json not found – cannot verify task")
        return 0.0

    print(f"✓ Found settings.json at {settings_path}")

    raw_text = settings_path.read_text(encoding="utf-8", errors="ignore")
    try:
        data = json.loads(strip_json_comments(raw_text) or "{}")
    except Exception as e:
        print(f"✗ Failed to parse JSON: {e}")
        return 0.0

    # Requirement 1 – global auto-update must be enabled
    if data.get("extensions.autoUpdate") is True:
        print("✓ \"extensions.autoUpdate\" is set to true (+0.6)")
        total_score += 0.6
    else:
        print("✗ \"extensions.autoUpdate\" is not enabled")

    # Requirement 2 – VS Code must regularly check for extension updates
    if data.get("extensions.autoCheckUpdates") is True:
        print("✓ \"extensions.autoCheckUpdates\" is set to true (+0.3)")
        total_score += 0.3
    else:
        print("✗ \"extensions.autoCheckUpdates\" is not enabled")

    # Requirement 3 – there must be no ignore list disabling updates for particular extensions
    if data.get("extensions.autoUpdateIgnore"):
        print("⚠ \"extensions.autoUpdateIgnore\" is defined; some extensions might not auto-update")
    else:
        print("✓ No \"extensions.autoUpdateIgnore\" setting detected (+0.1)")
        total_score += 0.1

    final_score = round(min(total_score, max_score), 2)
    print(f"Total score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_task()
    print(f"REWARD: {reward}")
