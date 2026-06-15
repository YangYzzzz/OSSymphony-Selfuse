"""
Reward Script: Configure VSCode terminal settings
Task ID: vscode_web_028
Domain: vscode
Scoring:
  - Component 1 (0.35): terminal.integrated.defaultProfile.linux == "bash"
  - Component 2 (0.30): terminal.integrated.fontSize == 14
  - Component 3 (0.35): terminal.integrated.env.linux.NODE_ENV == "development"
"""

import json
import os
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC format)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify VSCode terminal configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: terminal.integrated.defaultProfile.linux == "bash" (0.35 points)
    try:
        default_profile = settings.get("terminal.integrated.defaultProfile.linux")
        if default_profile == "bash":
            print(f"PASS: Component 1 — defaultProfile.linux is 'bash' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected defaultProfile.linux='bash', found: {default_profile!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: terminal.integrated.fontSize == 14 (0.30 points)
    try:
        font_size = settings.get("terminal.integrated.fontSize")
        if font_size == 14:
            print(f"PASS: Component 2 — terminal fontSize is 14 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — expected terminal fontSize=14, found: {font_size!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: terminal.integrated.env.linux contains NODE_ENV=development (0.35 points)
    try:
        env_linux = settings.get("terminal.integrated.env.linux")
        if isinstance(env_linux, dict) and env_linux.get("NODE_ENV") == "development":
            print(f"PASS: Component 3 — env.linux.NODE_ENV is 'development' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — expected env.linux with NODE_ENV='development', found: {env_linux!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
