"""
Reward Script: Configure VSCode file nesting for .module.css and .test.tsx under .tsx
Task ID: vscode_web_032
Domain: vscode
Scoring:
  Component 1 (0.3): explorer.fileNesting.enabled is true
  Component 2 (0.3): explorer.fileNesting.patterns has a *.tsx key
  Component 3 (0.2): *.tsx pattern nests .module.css files
  Component 4 (0.2): *.tsx pattern nests .test.tsx files
"""

import os
import json
import re

HOME = os.path.expanduser("~")
VSCODE_USER = os.path.join(HOME, ".config", "Code", "User")
SETTINGS_PATH = os.path.join(VSCODE_USER, "settings.json")
TASK_ID = "vscode_web_032"


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

    # Component 1: explorer.fileNesting.enabled is true (0.3 points)
    try:
        nesting_enabled = settings.get("explorer.fileNesting.enabled")
        if nesting_enabled is True:
            print(f"PASS: Component 1 -- fileNesting.enabled is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- expected explorer.fileNesting.enabled=true, found: {nesting_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: explorer.fileNesting.patterns has a *.tsx key (0.3 points)
    try:
        patterns = settings.get("explorer.fileNesting.patterns", {})
        if isinstance(patterns, dict) and "*.tsx" in patterns:
            print(f"PASS: Component 2 -- fileNesting.patterns has '*.tsx' key (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- expected '*.tsx' key in fileNesting.patterns, found keys: {list(patterns.keys()) if isinstance(patterns, dict) else type(patterns)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: *.tsx pattern nests .module.css files (0.2 points)
    try:
        patterns = settings.get("explorer.fileNesting.patterns", {})
        tsx_pattern = patterns.get("*.tsx", "") if isinstance(patterns, dict) else ""
        # Check that the pattern value contains a reference to .module.css
        # Valid forms: "${capture}.module.css", "$(capture).module.css", etc.
        if ".module.css" in tsx_pattern:
            print(f"PASS: Component 3 -- *.tsx pattern includes .module.css nesting: '{tsx_pattern}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- expected .module.css in *.tsx pattern value, found: '{tsx_pattern}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: *.tsx pattern nests .test.tsx files (0.2 points)
    try:
        patterns = settings.get("explorer.fileNesting.patterns", {})
        tsx_pattern = patterns.get("*.tsx", "") if isinstance(patterns, dict) else ""
        # Check that the pattern value contains a reference to .test.tsx
        if ".test.tsx" in tsx_pattern:
            print(f"PASS: Component 4 -- *.tsx pattern includes .test.tsx nesting: '{tsx_pattern}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- expected .test.tsx in *.tsx pattern value, found: '{tsx_pattern}'")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
