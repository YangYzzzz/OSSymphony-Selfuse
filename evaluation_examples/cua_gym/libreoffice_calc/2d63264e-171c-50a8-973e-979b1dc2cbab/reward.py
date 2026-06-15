"""
Reward Script: Install Dark Reader Chrome extension and configure dark mode for all sites
Task ID: osworld_multi_apps_ext_install_010
Domain: chrome
Scoring:
  Component 1 (0.4): Dark Reader extension is installed (manifest.json present)
  Component 2 (0.3): Dark Reader extension is enabled in Chrome preferences (state=1)
  Component 3 (0.3): Dark Reader configured to apply dark mode to all websites
                      (managed_preferences.enabled=True, applyToListedOnly=False, theme.mode=1)
"""

import os
import json

DARK_READER_ID = "eimadpbcbfnmbkopoojfekhnkhdbieeh"
CHROME_DEFAULT = os.path.expanduser("~/.config/google-chrome/Default")
EXTENSIONS_DIR = os.path.join(CHROME_DEFAULT, "Extensions")
PREFS_FILE = os.path.join(CHROME_DEFAULT, "Preferences")


def verify_task():
    """
    Verify Dark Reader installation and configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Dark Reader extension is installed (0.4 points)
    # The extension directory and manifest.json must exist — this is the primary task-change indicator
    try:
        ext_base_dir = os.path.join(EXTENSIONS_DIR, DARK_READER_ID)
        manifest_found = False
        manifest_name = None
        if os.path.isdir(ext_base_dir):
            for version_dir in os.listdir(ext_base_dir):
                manifest_path = os.path.join(ext_base_dir, version_dir, "manifest.json")
                if os.path.exists(manifest_path):
                    with open(manifest_path, "r") as f:
                        manifest_data = json.load(f)
                    manifest_name = manifest_data.get("name", "")
                    if "Dark Reader" in manifest_name:
                        manifest_found = True
                        break

        if manifest_found:
            print(f"PASS: Component 1 — Dark Reader manifest found, name='{manifest_name}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Dark Reader extension not installed (ID: {DARK_READER_ID})")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check extension directory: {e}")

    # Component 2: Dark Reader extension is enabled in Chrome preferences (0.3 points)
    # Extension state=1 means enabled; state=0 means disabled
    try:
        with open(PREFS_FILE, "r") as f:
            prefs = json.load(f)

        ext_settings = prefs.get("extensions", {}).get("settings", {})
        dr_settings = ext_settings.get(DARK_READER_ID)

        if dr_settings is None:
            print(f"FAIL: Component 2 — Dark Reader not found in Chrome extension settings")
        else:
            ext_state = dr_settings.get("state")
            # state=1 means enabled
            if ext_state == 1:
                print(f"PASS: Component 2 — Dark Reader is enabled (state={ext_state}) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Dark Reader is not enabled (state={ext_state}, expected 1)")
    except FileNotFoundError:
        print(f"ERROR: Component 2 — Chrome Preferences file not found at {PREFS_FILE}")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check extension enabled state: {e}")

    # Component 3: Dark Reader configured to apply dark mode to ALL websites (0.3 points)
    # Requires: managed_preferences.enabled=True, applyToListedOnly=False, theme.mode=1
    try:
        with open(PREFS_FILE, "r") as f:
            prefs = json.load(f)

        ext_settings = prefs.get("extensions", {}).get("settings", {})
        dr_settings = ext_settings.get(DARK_READER_ID)

        if dr_settings is None:
            print(f"FAIL: Component 3 — Dark Reader not found in Chrome extension settings")
        else:
            managed_prefs = dr_settings.get("managed_preferences", {})
            dr_enabled = managed_prefs.get("enabled", False)
            apply_to_listed_only = managed_prefs.get("applyToListedOnly", True)
            theme = managed_prefs.get("theme", {})
            theme_mode = theme.get("mode", None)  # mode=1 means dark mode

            # All three conditions must be true for dark mode to apply to all websites:
            # 1. enabled=True (dark mode is on)
            # 2. applyToListedOnly=False (applies to ALL websites, not just listed ones)
            # 3. theme.mode=1 (dark mode selected, not light=0 or auto=-1)
            conditions_met = dr_enabled and (not apply_to_listed_only) and (theme_mode == 1)

            if conditions_met:
                print(
                    f"PASS: Component 3 — Dark Reader configured for all websites: "
                    f"enabled={dr_enabled}, applyToListedOnly={apply_to_listed_only}, "
                    f"theme.mode={theme_mode} (0.3 pts)"
                )
                total_score += 0.3
            else:
                print(
                    f"FAIL: Component 3 — Dark Reader not fully configured for all websites: "
                    f"enabled={dr_enabled} (expected True), "
                    f"applyToListedOnly={apply_to_listed_only} (expected False), "
                    f"theme.mode={theme_mode} (expected 1)"
                )
    except FileNotFoundError:
        print(f"ERROR: Component 3 — Chrome Preferences file not found at {PREFS_FILE}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check Dark Reader configuration: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
