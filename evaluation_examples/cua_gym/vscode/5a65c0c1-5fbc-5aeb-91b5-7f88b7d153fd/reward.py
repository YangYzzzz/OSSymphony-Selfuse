"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m localizing my workspace for a new website; could you help me switch VS Code’s interface to French and create a fresh “theme.css” file in /home/user/web/styles?
Generated: 2025-09-12 00:43:24
Status: success
Model: azure-o3
Total Steps: 3
"""

import json
import pathlib


def verify_task():
    """Verify task completion for:
    1. Switching VS Code’s interface language to French
    2. Creating a fresh theme.css in /home/user/web/styles

    Returns a float score between 0.0 and 1.0 (progressive)."""

    print("Checking task completion…")
    total_score = 0.0
    max_score = 1.0

    # ----------------------------------------------------
    # Requirement 1 — VS Code UI language set to French
    # ----------------------------------------------------
    locale_paths = [
        pathlib.Path.home() / ".config" / "Code" / "User" / "locale.json",            # Regular build (Linux)
        pathlib.Path.home() / ".config" / "Code - OSS" / "User" / "locale.json",     # OSS build (Linux)
        pathlib.Path.home() / "AppData" / "Roaming" / "Code" / "User" / "locale.json",  # Windows (just in case)
        pathlib.Path.home() / ".vscode" / "locale.json",                               # Portable/legacy pattern
    ]

    locale_verified = False
    for path in locale_paths:
        if path.exists() and path.is_file():
            try:
                data = json.loads(path.read_text(encoding="utf-8"))
                locale_val = str(data.get("locale", ""))
                print(f"Found locale.json at {path} with locale='{locale_val}'")
                if locale_val.lower().startswith("fr"):
                    locale_verified = True
                    break
            except Exception as e:
                print(f"Error reading {path}: {e}")

    if locale_verified:
        print("✓ VS Code interface language is French (0.5 points)")
        total_score += 0.5
    else:
        print("✗ VS Code interface language NOT set to French (0 points)")

    # ----------------------------------------------------
    # Requirement 2 — theme.css in /home/user/web/styles
    # ----------------------------------------------------
    theme_path = pathlib.Path("/home/user/web/styles/theme.css")
    if theme_path.exists() and theme_path.is_file():
        print(f"✓ Found theme.css at {theme_path} (0.5 points)")
        total_score += 0.5
    else:
        if not theme_path.parent.exists():
            print(f"✗ Directory {theme_path.parent} is missing (0 points)")
        else:
            print(f"✗ theme.css not found at {theme_path} (0 points)")

    # ----------------------------------------------------
    final_score = min(total_score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    return final_score


if __name__ == "__main__":
    reward = verify_task()
    print(f"REWARD: {reward}")
