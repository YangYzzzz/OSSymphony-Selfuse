"""
Reward Script: Configure ESLint extension settings in VSCode
Task ID: vscode_we_055
Domain: vscode (settings.json)
Scoring:
  Component 1: eslint.useFlatConfig == true          (0.3 pts)
  Component 2: eslint.workingDirectories == [{"mode":"auto"}] (0.3 pts)
  Component 3: eslint.validate contains js/ts/vue    (0.4 pts)
"""

import os
import json
import re

SETTINGS_PATH = os.path.expanduser("~/.config/Code/User/settings.json")


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip JSONC-style comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        content = re.sub(r'/\*.*?\*/', '', content, flags=re.DOTALL)
        return json.loads(content)
    except FileNotFoundError:
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        return None
    except json.JSONDecodeError as e:
        print(f"CRITICAL: settings.json parse error: {e}")
        return None


def verify_task():
    """
    Verify ESLint configuration in VSCode settings.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Component 1: eslint.useFlatConfig == true (0.3 points)
    try:
        flat_config = settings.get("eslint.useFlatConfig")
        if flat_config is True:
            print(f"PASS: Component 1 -- eslint.useFlatConfig is true (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 -- eslint.useFlatConfig expected true, found: {flat_config!r}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: eslint.workingDirectories == [{"mode": "auto"}] (0.3 points)
    try:
        working_dirs = settings.get("eslint.workingDirectories")
        expected_dirs = [{"mode": "auto"}]
        if working_dirs == expected_dirs:
            print(f"PASS: Component 2 -- eslint.workingDirectories is [{{'mode': 'auto'}}] (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- eslint.workingDirectories expected {expected_dirs}, found: {working_dirs!r}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: eslint.validate contains javascript, typescript, vue (0.4 points)
    try:
        validate = settings.get("eslint.validate")
        if isinstance(validate, list):
            expected_langs = {"javascript", "typescript", "vue"}
            # Normalize: entries can be strings or dicts with "language" key
            actual_langs = set()
            for entry in validate:
                if isinstance(entry, str):
                    actual_langs.add(entry.lower())
                elif isinstance(entry, dict) and "language" in entry:
                    actual_langs.add(entry["language"].lower())

            if expected_langs.issubset(actual_langs):
                print(f"PASS: Component 3 -- eslint.validate contains javascript, typescript, vue (0.4 pts)")
                total_score += 0.4
            else:
                missing = expected_langs - actual_langs
                print(f"FAIL: Component 3 -- eslint.validate missing: {missing}. Found: {actual_langs}")
        else:
            print(f"FAIL: Component 3 -- eslint.validate expected list, found: {validate!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
