"""
Reward Script: Enable and configure Error Lens extension settings
Task ID: vscode_we_066
Domain: vscode
Scoring:
  Component 1: errorLens.enabled == true (0.3 pts)
  Component 2: errorLens.delay == 500 (0.35 pts)
  Component 3: errorLens.enabledDiagnosticLevels == ["error", "warning"] (0.35 pts)
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
        # Strip JSONC comments before parsing
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARNING: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify Error Lens extension configuration with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: errorLens.enabled == true (0.3 points)
    # This setting must be explicitly set to true to enable the extension
    try:
        enabled_val = settings.get("errorLens.enabled")
        if enabled_val is True:
            print(f"PASS: Component 1 — errorLens.enabled is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — errorLens.enabled expected true, found: {enabled_val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: errorLens.delay == 500 (0.35 points)
    # The delay in milliseconds before showing inline error messages
    try:
        delay_val = settings.get("errorLens.delay")
        if delay_val == 500:
            print(f"PASS: Component 2 — errorLens.delay is 500 (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — errorLens.delay expected 500, found: {delay_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: errorLens.enabledDiagnosticLevels == ["error", "warning"] (0.35 points)
    # Only errors and warnings should be shown, not info or hints
    try:
        levels_val = settings.get("errorLens.enabledDiagnosticLevels")
        if isinstance(levels_val, list) and set(levels_val) == {"error", "warning"} and len(levels_val) == 2:
            print(f"PASS: Component 3 — errorLens.enabledDiagnosticLevels is {levels_val} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 3 — errorLens.enabledDiagnosticLevels expected ['error', 'warning'], found: {levels_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
