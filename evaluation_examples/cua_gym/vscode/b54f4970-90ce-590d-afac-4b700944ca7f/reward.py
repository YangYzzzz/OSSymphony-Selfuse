"""
Reward Script: Disable auto-closing brackets for Markdown files only
Task ID: vscode_code_051
Domain: vs_code
Scoring:
  Component 1 (0.5): [markdown] override sets editor.autoClosingBrackets to "never"
  Component 2 (0.5): [markdown] override sets editor.autoClosingQuotes to "never"
"""

import os
import json
import re

SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'


def load_settings(path):
    """Load settings.json, stripping JSONC-style comments if needed."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Try direct parse first
        try:
            return json.loads(content)
        except json.JSONDecodeError:
            # Strip // comments (JSONC support)
            content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
            return json.loads(content_clean)
    except Exception as e:
        return None, e


def verify_task():
    """
    Verify that settings.json has been updated to include a [markdown]
    language-specific override that disables auto-closing brackets and quotes.

    Task requires:
      "[markdown]": {
          "editor.autoClosingBrackets": "never",
          "editor.autoClosingQuotes": "never"
      }

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: verify settings.json exists and is readable
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print(f"CRITICAL: Cannot parse settings.json at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: [markdown] section exists with editor.autoClosingBrackets = "never" (0.5 points)
    # This FAILS on initial_env (no [markdown] key) and PASSES on golden_env
    try:
        markdown_section = settings.get("[markdown]", None)
        if markdown_section is None:
            print("FAIL: Component 1 — [markdown] language override section not found in settings.json")
        else:
            brackets_value = markdown_section.get("editor.autoClosingBrackets", None)
            if brackets_value == "never":
                print(f"PASS: Component 1 — [markdown].editor.autoClosingBrackets = 'never' (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 1 — [markdown].editor.autoClosingBrackets expected 'never', found: {repr(brackets_value)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: [markdown] section has editor.autoClosingQuotes = "never" (0.5 points)
    # This FAILS on initial_env (no [markdown] key) and PASSES on golden_env
    try:
        markdown_section = settings.get("[markdown]", None)
        if markdown_section is None:
            print("FAIL: Component 2 — [markdown] language override section not found in settings.json")
        else:
            quotes_value = markdown_section.get("editor.autoClosingQuotes", None)
            if quotes_value == "never":
                print(f"PASS: Component 2 — [markdown].editor.autoClosingQuotes = 'never' (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — [markdown].editor.autoClosingQuotes expected 'never', found: {repr(quotes_value)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
