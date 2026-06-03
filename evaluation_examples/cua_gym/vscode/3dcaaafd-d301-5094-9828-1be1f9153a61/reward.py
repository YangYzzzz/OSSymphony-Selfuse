"""
Reward Script: Configure file nesting to group related config files under package.json
Task ID: vscode_lp_074
Domain: vs_code
Scoring:
  Component 1 (0.4): explorer.fileNesting.enabled is true
  Component 2 (0.3): explorer.fileNesting.patterns has a package.json key
  Component 3 (0.3): package.json pattern lists all 4 required nested files
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")
TASK_ID = "vscode_lp_074"

# The 4 files that must be nested under package.json
REQUIRED_NESTED = {"package-lock.json", ".npmrc", ".nvmrc", "tsconfig.json"}


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
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

    # Component 1: explorer.fileNesting.enabled is true (0.4 points)
    try:
        nesting_enabled = settings.get("explorer.fileNesting.enabled")
        if nesting_enabled is True:
            print(f"PASS: Component 1 -- fileNesting.enabled is true (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- expected explorer.fileNesting.enabled=true, found: {nesting_enabled}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: explorer.fileNesting.patterns has a package.json key (0.3 points)
    try:
        patterns = settings.get("explorer.fileNesting.patterns")
        if isinstance(patterns, dict) and "package.json" in patterns:
            print(f"PASS: Component 2 -- fileNesting.patterns has package.json key (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- expected patterns dict with package.json key, found: {patterns}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: package.json pattern value contains all 4 required files (0.3 points)
    try:
        patterns = settings.get("explorer.fileNesting.patterns", {})
        if isinstance(patterns, dict) and "package.json" in patterns:
            pattern_value = patterns["package.json"]
            # Parse the comma-separated list of nested file names
            nested_files = {f.strip() for f in str(pattern_value).split(",")}
            missing = REQUIRED_NESTED - nested_files
            if not missing:
                print(f"PASS: Component 3 -- all 4 required files present in pattern: {nested_files} (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- missing nested files: {missing}. Found: {nested_files}")
        else:
            print(f"FAIL: Component 3 -- no package.json pattern key found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
