"""
Reward Script: Configure Tailwind CSS IntelliSense extension settings
Task ID: vscode_we_070
Domain: vscode
Scoring:
  Component 1 (0.3): configFile path set correctly
  Component 2 (0.35): includeLanguages mapping correct
  Component 3 (0.35): classAttributes list correct
"""

import os
import json
import re

HOME = os.path.expanduser("~")
SETTINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "settings.json")
TASK_ID = "vscode_we_070"


def load_settings():
    """Load VSCode settings.json, handling JSONC (comments)."""
    try:
        with open(SETTINGS_PATH, "r") as f:
            content = f.read()
        # Strip // comments (JSONC support)
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"ERROR: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("CRITICAL: settings.json not loadable")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: tailwindCSS.experimental.configFile (0.3 points)
    # Task requires: "./tailwind.config.ts"
    try:
        config_file = settings.get("tailwindCSS.experimental.configFile")
        if config_file == "./tailwind.config.ts":
            print(f"PASS: Component 1 — configFile is './tailwind.config.ts' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — expected './tailwind.config.ts', found: {config_file!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: tailwindCSS.includeLanguages (0.35 points)
    # Task requires: {"javascript": "javascript", "typescriptreact": "html"}
    try:
        include_langs = settings.get("tailwindCSS.includeLanguages")
        expected_langs = {"javascript": "javascript", "typescriptreact": "html"}
        if isinstance(include_langs, dict):
            # Check that expected mappings are present (subset check)
            all_match = all(
                include_langs.get(k) == v for k, v in expected_langs.items()
            )
            if all_match:
                print(f"PASS: Component 2 — includeLanguages contains correct mappings (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — includeLanguages mismatch. Expected subset {expected_langs}, found: {include_langs}")
        else:
            print(f"FAIL: Component 2 — includeLanguages not a dict, found: {include_langs!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: tailwindCSS.classAttributes (0.35 points)
    # Task requires: ["class", "className", "tw", "variants"]
    try:
        class_attrs = settings.get("tailwindCSS.classAttributes")
        expected_attrs = ["class", "className", "tw", "variants"]
        if isinstance(class_attrs, list):
            # Check that all expected attributes are present
            if set(expected_attrs).issubset(set(class_attrs)):
                print(f"PASS: Component 3 — classAttributes contains all required entries (0.35 pts)")
                total_score += 0.35
            else:
                missing = set(expected_attrs) - set(class_attrs)
                print(f"FAIL: Component 3 — classAttributes missing: {missing}. Found: {class_attrs}")
        else:
            print(f"FAIL: Component 3 — classAttributes not a list, found: {class_attrs!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
