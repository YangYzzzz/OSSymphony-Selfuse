"""
Reward Script: Configure VSCode editor for Markdown writing
Task ID: vscode_we_043
Domain: vscode
Scoring:
  Component 1 (0.25): [markdown] block has editor.wordWrap = "wordWrapColumn"
  Component 2 (0.25): [markdown] block has editor.wordWrapColumn = 80
  Component 3 (0.25): [markdown] block has editor.quickSuggestions = {other: true, comments: false, strings: false}
  Component 4 (0.25): [markdown] block has editor.defaultFormatter = "yzhang.markdown-all-in-one"
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
        # Strip single-line JSONC comments
        content = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        # Strip trailing commas before } or ]
        content = re.sub(r',\s*([}\]])', r'\1', content)
        return json.loads(content)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"CRITICAL: Cannot load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that VSCode settings.json contains a [markdown] language-specific
    block with the required Markdown writing configuration.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    settings = load_settings()
    if settings is None:
        print("REWARD: 0.0")
        return 0.0

    # Get the [markdown] language-specific block
    md_block = settings.get("[markdown]")
    if not isinstance(md_block, dict):
        print("FAIL: No [markdown] language-specific block found in settings.json")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: editor.wordWrap = "wordWrapColumn" (0.25 points)
    try:
        word_wrap = md_block.get("editor.wordWrap")
        if word_wrap == "wordWrapColumn":
            print(f"PASS: Component 1 — editor.wordWrap = 'wordWrapColumn' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected editor.wordWrap = 'wordWrapColumn', found: {word_wrap!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: editor.wordWrapColumn = 80 (0.25 points)
    try:
        wrap_col = md_block.get("editor.wordWrapColumn")
        if wrap_col == 80:
            print(f"PASS: Component 2 — editor.wordWrapColumn = 80 (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — expected editor.wordWrapColumn = 80, found: {wrap_col!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: editor.quickSuggestions = {"other": true, "comments": false, "strings": false} (0.25 points)
    try:
        quick_sugg = md_block.get("editor.quickSuggestions")
        expected_qs = {"other": True, "comments": False, "strings": False}
        if isinstance(quick_sugg, dict) and quick_sugg == expected_qs:
            print(f"PASS: Component 3 — editor.quickSuggestions matches expected (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — expected editor.quickSuggestions = {expected_qs}, found: {quick_sugg!r}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: editor.defaultFormatter = "yzhang.markdown-all-in-one" (0.25 points)
    try:
        formatter = md_block.get("editor.defaultFormatter")
        if formatter == "yzhang.markdown-all-in-one":
            print(f"PASS: Component 4 — editor.defaultFormatter = 'yzhang.markdown-all-in-one' (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected editor.defaultFormatter = 'yzhang.markdown-all-in-one', found: {formatter!r}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(SETTINGS_PATH):
    print(f"File not found: {SETTINGS_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
