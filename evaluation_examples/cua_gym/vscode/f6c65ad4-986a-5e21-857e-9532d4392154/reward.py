"""
Reward Script: Set up language-specific settings for JavaScript files
Task ID: vscode_lp_031
Domain: vs_code
Scoring:
  Component 1 (0.5): [javascript] section exists in settings.json
  Component 2 (0.3): [javascript].editor.tabSize == 2
  Component 3 (0.2): Global editor.tabSize remains 4 AND [javascript] section exists
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

    print(f"INFO: Loaded settings.json with keys: {list(settings.keys())}")

    # Component 1: [javascript] section exists in settings.json (0.5 points)
    # This is the core task-introduced change -- the section must be added.
    try:
        js_section = settings.get("[javascript]")
        if isinstance(js_section, dict):
            print(f"PASS: Component 1 — [javascript] section exists (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — [javascript] section not found or not a dict, got: {js_section}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [javascript].editor.tabSize == 2 (0.3 points)
    # Verifies the specific language-specific indentation override.
    try:
        js_section = settings.get("[javascript]")
        if isinstance(js_section, dict):
            js_tab_size = js_section.get("editor.tabSize")
            if js_tab_size == 2:
                print(f"PASS: Component 2 — [javascript].editor.tabSize == 2 (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — [javascript].editor.tabSize expected 2, found: {js_tab_size}")
        else:
            print(f"FAIL: Component 2 — [javascript] section missing, cannot check tabSize")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Global editor.tabSize == 4 AND [javascript] section exists (0.2 points)
    # Compound check: ensures global setting is preserved while JS override is present.
    # The compound condition prevents scoring on initial_env where [javascript] is absent.
    try:
        global_tab_size = settings.get("editor.tabSize")
        js_section_exists = isinstance(settings.get("[javascript]"), dict)
        if global_tab_size == 4 and js_section_exists:
            print(f"PASS: Component 3 — Global editor.tabSize == 4 and [javascript] section present (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Global tabSize={global_tab_size}, [javascript] exists={js_section_exists}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
