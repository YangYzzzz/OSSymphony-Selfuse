"""
Reward Script: Configure Java import organization settings in VSCode
Task ID: vscode_lang_059
Domain: vscode (settings.json verification)
Scoring:
  Component 1: starThreshold == 5           (0.3 pts)
  Component 2: staticStarThreshold == 3     (0.3 pts)
  Component 3: [java] codeActionsOnSave     (0.4 pts)
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
        # Strip single-line comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify Java import organization settings are configured in VSCode.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not found or invalid")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: java.sources.organizeImports.starThreshold == 5 (0.3 points)
    try:
        star_threshold = settings.get("java.sources.organizeImports.starThreshold")
        if star_threshold == 5:
            print(f"PASS: Component 1 -- starThreshold is 5 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- expected starThreshold=5, found: {star_threshold}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: java.sources.organizeImports.staticStarThreshold == 3 (0.3 points)
    try:
        static_threshold = settings.get("java.sources.organizeImports.staticStarThreshold")
        if static_threshold == 3:
            print(f"PASS: Component 2 -- staticStarThreshold is 3 (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- expected staticStarThreshold=3, found: {static_threshold}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: [java] section with editor.codeActionsOnSave.source.organizeImports == true (0.4 points)
    try:
        java_section = settings.get("[java]")
        if isinstance(java_section, dict):
            code_actions = java_section.get("editor.codeActionsOnSave")
            if isinstance(code_actions, dict):
                organize_imports = code_actions.get("source.organizeImports")
                # Accept True (bool) or "always" (string variant)
                if organize_imports is True or organize_imports == "always":
                    print(f"PASS: Component 3 -- [java] codeActionsOnSave.source.organizeImports is {organize_imports} (0.4 pts)")
                    total_score += 0.4
                else:
                    print(f"FAIL: Component 3 -- source.organizeImports is {organize_imports}, expected true")
            else:
                print(f"FAIL: Component 3 -- editor.codeActionsOnSave not found or not a dict in [java] section")
        else:
            print(f"FAIL: Component 3 -- [java] section not found in settings.json")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
