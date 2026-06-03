"""
Reward Script: Install Path Intellisense extension and configure mappings/exclusions
Task ID: vscode_we_082
Domain: vscode
Scoring:
  - Component 1 (0.30): Extension christian-kohler.path-intellisense is installed
  - Component 2 (0.30): settings.json contains path-intellisense.mappings with "@" -> "${workspaceFolder}/src"
  - Component 3 (0.15): settings.json contains path-intellisense.autoTriggerNextSuggestion = true
  - Component 4 (0.25): settings.json contains path-intellisense.excludePatterns = ["**/node_modules"]
"""

import os
import json
import re

TASK_ID = 'vscode_we_082'
HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Extension christian-kohler.path-intellisense is installed (0.30 points)
    try:
        import subprocess
        # Note: subprocess is used ONLY for extension listing (no file alternative)
        result = subprocess.run(
            ["code", "--list-extensions"],
            capture_output=True, text=True, timeout=15
        )
        extensions = [ext.strip().lower() for ext in result.stdout.strip().split('\n') if ext.strip()]
        if "christian-kohler.path-intellisense" in extensions:
            print(f"PASS: Component 1 — Extension path-intellisense is installed (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Extension path-intellisense not found. Installed: {extensions}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Load settings for remaining components
    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json — remaining components cannot be checked")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: path-intellisense.mappings contains "@" -> "${workspaceFolder}/src" (0.30 points)
    try:
        mappings = settings.get("path-intellisense.mappings", None)
        if isinstance(mappings, dict) and mappings.get("@") == "${workspaceFolder}/src":
            print(f"PASS: Component 2 — Mappings '@' -> '${{workspaceFolder}}/src' found (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Expected mappings with '@' -> '${{workspaceFolder}}/src', found: {mappings}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: path-intellisense.autoTriggerNextSuggestion is true (0.15 points)
    try:
        auto_trigger = settings.get("path-intellisense.autoTriggerNextSuggestion", None)
        if auto_trigger is True:
            print(f"PASS: Component 3 — autoTriggerNextSuggestion is true (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected autoTriggerNextSuggestion=true, found: {auto_trigger}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: path-intellisense.excludePatterns contains "**/node_modules" (0.25 points)
    try:
        exclude = settings.get("path-intellisense.excludePatterns", None)
        if isinstance(exclude, list) and "**/node_modules" in exclude:
            print(f"PASS: Component 4 — excludePatterns contains '**/node_modules' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Expected excludePatterns with '**/node_modules', found: {exclude}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
