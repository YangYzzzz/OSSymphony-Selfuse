"""
Reward Script: Set the default terminal shell in VSCode to /bin/zsh on Linux
Task ID: vscode_we_007
Domain: vscode
Scoring:
  Component 1 (0.5): terminal.integrated.defaultProfile.linux == "zsh"
  Component 2 (0.5): terminal.integrated.profiles.linux contains zsh profile with path /bin/zsh
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_007"


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load VSCode settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: terminal.integrated.defaultProfile.linux is set to "zsh" (0.5 points)
    try:
        default_profile = settings.get("terminal.integrated.defaultProfile.linux")
        if default_profile is not None and str(default_profile).lower() == "zsh":
            print(f"PASS: Component 1 - defaultProfile.linux is '{default_profile}' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Expected defaultProfile.linux='zsh', found: {default_profile!r}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: terminal.integrated.profiles.linux contains zsh profile with path /bin/zsh (0.5 points)
    try:
        profiles = settings.get("terminal.integrated.profiles.linux", {})
        if isinstance(profiles, dict):
            # Look for a zsh profile (case-insensitive key match)
            zsh_profile = None
            for key, val in profiles.items():
                if key.lower() == "zsh":
                    zsh_profile = val
                    break

            if zsh_profile is not None and isinstance(zsh_profile, dict):
                zsh_path = zsh_profile.get("path", "")
                if zsh_path == "/bin/zsh":
                    print(f"PASS: Component 2 - zsh profile found with path '/bin/zsh' (0.5 pts)")
                    total_score += 0.5
                else:
                    print(f"FAIL: Component 2 - zsh profile exists but path is '{zsh_path}', expected '/bin/zsh'")
            else:
                print(f"FAIL: Component 2 - No 'zsh' profile found in terminal.integrated.profiles.linux. Profiles: {profiles}")
        else:
            print(f"FAIL: Component 2 - terminal.integrated.profiles.linux is not a dict: {type(profiles)}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
