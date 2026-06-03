"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve been cleaning up our Python code all afternoon—could you switch VS Code to the “Dark+” theme and add a 100-column ruler for Python files so I can stick to our style guide?
Generated: 2025-09-11 23:15:30
Status: success
Model: azure-o3
Total Steps: 1
"""

import os
import re
import json

# ---------------- Helper Functions ----------------

def strip_json_comments(data: str) -> str:
    """Remove // line comments and dangling commas from a JSON-like VS Code settings file."""
    # Remove // … comments
    data = re.sub(r"//.*", "", data)
    # Remove trailing commas before } or ] (very small heuristic)
    data = re.sub(r",\s*([}\]])", r"\1", data)
    return data


def load_loose_json(path: str):
    """Load VS Code settings.json while tolerating comments & trailing commas."""
    try:
        with open(path, "r", encoding="utf-8") as f:
            raw = f.read()
        return json.loads(strip_json_comments(raw))
    except Exception:
        return None  # Caller can fall back to regex parsing

# ---------------- Actual Verification ----------------

def find_settings_files():
    """Return a list of plausible VS Code user-level settings.json paths (deduplicated)."""
    candidates = [
        os.path.expanduser("~/.config/Code/User/settings.json"),          # Standard Linux VS Code
        os.path.expanduser("~/.config/Code - OSS/User/settings.json"),   # VS Code OSS
        os.path.expanduser("~/.config/Code - Insiders/User/settings.json"),
        os.path.expanduser("~/.vscode/settings.json"),                   # Portable folder config
    ]

    # Also walk a bit under ~/.config & ~/.vscode for nested settings.json
    for base in (os.path.expanduser("~/.config"), os.path.expanduser("~/.vscode")):
        if os.path.exists(base):
            for root, _, files in os.walk(base):
                if "settings.json" in files:
                    candidates.append(os.path.join(root, "settings.json"))

    # Deduplicate while preserving order
    seen, unique = set(), []
    for p in candidates:
        if os.path.exists(p) and p not in seen:
            unique.append(p)
            seen.add(p)
    return unique


def theme_is_dark_plus(settings: dict):
    """Check if workbench.colorTheme contains the phrase 'dark+'."""
    theme = settings.get("workbench.colorTheme") if isinstance(settings, dict) else None
    return bool(isinstance(theme, str) and "dark+" in theme.lower()), theme


def rulers_contain_100(rulers):
    return isinstance(rulers, list) and any(r == 100 for r in rulers if isinstance(r, int))


def ruler_is_set(settings: dict):
    """Check for a 100-column ruler globally or in the Python language override."""
    global_ok = rulers_contain_100(settings.get("editor.rulers"))

    python_part = settings.get("[python]")
    python_ok = False
    if isinstance(python_part, dict):
        python_ok = rulers_contain_100(python_part.get("editor.rulers"))

    return global_ok or python_ok, {"global": global_ok, "python": python_ok}

# ---------------- Scoring ----------------

def verify_task():
    print("--- VS Code Settings Verification ---")

    settings_files = find_settings_files()
    if not settings_files:
        print("✗ No VS Code settings.json files found.")
        print("REWARD: 0.0")
        return 0.0

    print(f"Found {len(settings_files)} settings file(s):")
    for p in settings_files:
        print("  •", p)

    theme_ok = False
    ruler_ok = False

    for path in settings_files:
        data = load_loose_json(path)

        # ---------- THEME ----------
        if data is not None:
            t_ok, theme_val = theme_is_dark_plus(data)
            if t_ok:
                theme_ok = True
                print(f"✓ Dark+ theme set in {path} (value: {theme_val})")
            elif theme_val is not None:
                print(f"Theme in {path} is '{theme_val}' – not Dark+.")
        else:
            # Fallback: regex scan file text
            with open(path, "r", encoding="utf-8") as f:
                raw = f.read().lower()
            if "workbench.colortheme" in raw and "dark+" in raw:
                theme_ok = True
                print(f"✓ Dark+ theme detected via fallback in {path}")

        # ---------- RULER ----------
        if data is not None:
            r_ok, details = ruler_is_set(data)
            if r_ok:
                ruler_ok = True
                where = "global" if details["global"] else "python section"
                print(f"✓ 100-column ruler configured in {path} ({where})")
        else:
            if re.search(r"editor\.rulers.*100", raw):
                ruler_ok = True
                print(f"✓ 100-column ruler detected via fallback in {path}")

    # ---------------- Final Scoring ----------------
    score = 0.0
    if theme_ok:
        score += 0.5
    else:
        print("✗ Dark+ theme not configured anywhere.")

    if ruler_ok:
        score += 0.5
    else:
        print("✗ No 100-column ruler for Python found.")

    score = min(score, 1.0)
    print(f"Total Score: {score} / 1.0")
    print(f"REWARD: {score}")
    return score

# --------------- Script Entry Point ---------------
if __name__ == "__main__":
    verify_task()

