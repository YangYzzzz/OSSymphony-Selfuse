"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m coding on my Django project well past midnight, and the default light theme is glaring; could you help me change VS Code to the “Night Owl” color theme to ease the eye strain?
Generated: 2025-09-11 19:57:32
Status: success
Model: azure-o3
Total Steps: 8
"""

import re
import json
from pathlib import Path


def _strip_json_comments(raw: str) -> str:
    """Remove // and /* */ comments so the file can be JSON-parsed."""
    # Remove /* ... */ style comments (including new lines inside)
    raw = re.sub(r"/\*.*?\*/", "", raw, flags=re.DOTALL)

    cleaned_lines = []
    for line in raw.splitlines():
        stripped = line.strip()
        # Skip full-line // comments
        if stripped.startswith("//"):
            continue
        # Remove trailing // comments
        if "//" in line:
            line = line.split("//", 1)[0]
        cleaned_lines.append(line)
    return "\n".join(cleaned_lines)


def verify_vscode_night_owl() -> float:
    """Verify that VS Code is using the ‘Night Owl’ colour theme.

    Scoring rules:
      • 1.0  → workbench.colorTheme is set to something containing
                the text “night owl” (case-insensitive).
      • 0.3  → Night Owl extension installed but theme not active.
      • 0.0  → Neither condition satisfied.
    """

    home = Path.home()

    # Common locations for VS Code settings on Linux (regular, OSS, VSCodium, Insiders).
    settings_candidates = [
        home / ".config" / "Code" / "User" / "settings.json",
        home / ".config" / "Code - OSS" / "User" / "settings.json",
        home / ".config" / "VSCodium" / "User" / "settings.json",
        home / ".config" / "Code - Insiders" / "User" / "settings.json",
    ]

    colour_theme = None
    settings_file_used = None

    print("--- Checking VS Code settings for active colour theme ---")
    for settings_path in settings_candidates:
        if not settings_path.exists():
            continue

        print(f"Found potential settings file: {settings_path}")
        try:
            raw_text = settings_path.read_text(encoding="utf-8", errors="ignore")
        except Exception as e:
            print(f"  ✗ Could not read file: {e}")
            continue

        # First, attempt proper JSON parsing after stripping comments.
        try:
            stripped = _strip_json_comments(raw_text)
            data = json.loads(stripped)
            if isinstance(data, dict) and "workbench.colorTheme" in data:
                colour_theme = str(data["workbench.colorTheme"]).strip()
                settings_file_used = settings_path
                print(
                    f"  ✓ Parsed JSON successfully. workbench.colorTheme = '{colour_theme}'"
                )
                break
        except json.JSONDecodeError:
            # Fall back to regex if JSON parse fails (file may be badly formed).
            pass

        regex_match = re.search(
            r"\"workbench\\.colorTheme\"\s*:\s*\"([^\"]+)\"",
            raw_text,
            re.IGNORECASE,
        )
        if regex_match:
            colour_theme = regex_match.group(1).strip()
            settings_file_used = settings_path
            print(f"  ✓ Found via regex. workbench.colorTheme = '{colour_theme}'")
            break

    if colour_theme is None:
        print("  ✗ Could not locate an active colour theme setting in any settings.json file.")
    else:
        print(f"  → Active colour theme: {colour_theme} (from {settings_file_used})")

    # ------------------------------------------------------------------
    # Check whether the Night Owl extension is installed (folder name contains
    # ‘night-owl’ – this is what VS Code uses when unpacking extensions).
    # ------------------------------------------------------------------
    print("\n--- Scanning ~/.vscode/extensions for Night Owl extension ---")
    ext_dir = home / ".vscode" / "extensions"
    night_owl_extension_found = False

    if ext_dir.is_dir():
        for subdir in ext_dir.iterdir():
            if subdir.is_dir() and "night-owl" in subdir.name.lower():
                night_owl_extension_found = True
                print(f"  ✓ Night Owl extension directory found: {subdir.name}")
                break
        if not night_owl_extension_found:
            print("  – Night Owl extension directory NOT found in ~/.vscode/extensions")
    else:
        print("  – Extensions directory does not exist at ~/.vscode/extensions")

    # ------------------------------------------------------------------
    # Scoring logic
    # ------------------------------------------------------------------
    theme_is_night_owl = colour_theme is not None and "night owl" in colour_theme.lower()

    if theme_is_night_owl:
        score = 1.0
        print("\n🎉 Success: VS Code is using the Night Owl theme.")
    elif night_owl_extension_found:
        score = 0.3
        print("\n⚠️  Partial: Night Owl extension installed but not the active theme.")
    else:
        score = 0.0
        print("\n✗ Failure: Night Owl theme neither installed nor active.")

    print(f"Computed reward score: {score}")
    return score


if __name__ == "__main__":
    final_score = verify_vscode_night_owl()
    # Ensure the returned value is a float bounded in [0, 1].
    final_score = float(max(0.0, min(1.0, final_score)))
    print(f"REWARD: {final_score}")

