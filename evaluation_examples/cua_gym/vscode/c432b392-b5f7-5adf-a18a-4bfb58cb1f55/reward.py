"""
Reward Script: Set the default terminal shell to zsh and configure it to run a login shell
Task ID: vscode_rrt_070
Domain: vscode
Scoring:
  Component 1 (0.35) - terminal.integrated.defaultProfile.linux == 'zsh'
  Component 2 (0.35) - terminal.integrated.profiles.linux has 'zsh' profile with path '/usr/bin/zsh'
  Component 3 (0.30) - zsh profile args contains '-l' (login shell)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: terminal.integrated.defaultProfile.linux is set to 'zsh' (0.35 points)
    try:
        default_profile = settings.get("terminal.integrated.defaultProfile.linux")
        if default_profile is not None and str(default_profile).lower() == "zsh":
            print(f"PASS: Component 1 - defaultProfile.linux is '{default_profile}' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 - Expected defaultProfile.linux='zsh', found: {default_profile}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: terminal.integrated.profiles.linux has 'zsh' profile with path '/usr/bin/zsh' (0.35 points)
    try:
        profiles = settings.get("terminal.integrated.profiles.linux", {})
        zsh_profile = profiles.get("zsh") if isinstance(profiles, dict) else None
        if zsh_profile is not None and isinstance(zsh_profile, dict):
            zsh_path = zsh_profile.get("path", "")
            if zsh_path == "/usr/bin/zsh":
                print(f"PASS: Component 2 - zsh profile exists with path '/usr/bin/zsh' (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 - zsh profile path is '{zsh_path}', expected '/usr/bin/zsh'")
        else:
            print(f"FAIL: Component 2 - No 'zsh' profile found in profiles.linux. Profiles: {profiles}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: zsh profile args contains '-l' for login shell (0.30 points)
    try:
        profiles = settings.get("terminal.integrated.profiles.linux", {})
        zsh_profile = profiles.get("zsh") if isinstance(profiles, dict) else None
        if zsh_profile is not None and isinstance(zsh_profile, dict):
            args = zsh_profile.get("args", [])
            if isinstance(args, list) and "-l" in args:
                print(f"PASS: Component 3 - zsh profile args contains '-l' (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 - zsh profile args is {args}, expected ['-l'] or containing '-l'")
        else:
            print(f"FAIL: Component 3 - No 'zsh' profile found, cannot check args")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
