"""
Reward Script: Toggle Block Comment keybinding change
Task ID: vscode_stu_083
Domain: vscode
Scoring:
  Component 1 (0.4): keybindings.json contains an entry for editor.action.blockComment
  Component 2 (0.3): The keybinding key is exactly ctrl+shift+/
  Component 3 (0.3): No duplicate or conflicting blockComment entries exist (exactly one)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
KEYBINDINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "keybindings.json")


def load_keybindings(path):
    """Load keybindings.json, handling optional JSONC comment prefix."""
    try:
        with open(path, "r") as f:
            content = f.read()
    except FileNotFoundError:
        print(f"FAIL: keybindings.json not found at {path}")
        return None

    # Try direct JSON parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass

    # Strip JSONC single-line comments and retry
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError as e:
        print(f"FAIL: Cannot parse keybindings.json: {e}")
        return None


def verify_task():
    """
    Verify that the Toggle Block Comment keybinding has been changed to Ctrl+Shift+/.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load keybindings
    bindings = load_keybindings(KEYBINDINGS_PATH)
    if bindings is None:
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(bindings, list):
        print(f"FAIL: keybindings.json is not a list, found: {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Find all entries for editor.action.blockComment
    block_comment_entries = [
        entry for entry in bindings
        if isinstance(entry, dict) and entry.get("command") == "editor.action.blockComment"
    ]

    # Component 1: An entry for editor.action.blockComment exists (0.4 points)
    try:
        if len(block_comment_entries) >= 1:
            print(f"PASS: Component 1 -- Found {len(block_comment_entries)} entry(ies) for editor.action.blockComment (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- No entry for editor.action.blockComment found in keybindings.json")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The keybinding key is exactly ctrl+shift+/ (0.3 points)
    try:
        matching_key_entries = [
            entry for entry in block_comment_entries
            if entry.get("key", "").lower().replace(" ", "") == "ctrl+shift+/"
        ]
        if len(matching_key_entries) >= 1:
            print(f"PASS: Component 2 -- blockComment keybinding has key 'ctrl+shift+/' (0.3 pts)")
            total_score += 0.3
        else:
            keys_found = [entry.get("key") for entry in block_comment_entries]
            print(f"FAIL: Component 2 -- Expected key 'ctrl+shift+/', found keys: {keys_found}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Exactly one blockComment binding (no duplicates/conflicts) (0.3 points)
    try:
        if len(block_comment_entries) == 1:
            print(f"PASS: Component 3 -- Exactly one blockComment entry, no duplicates (0.3 pts)")
            total_score += 0.3
        elif len(block_comment_entries) > 1:
            print(f"FAIL: Component 3 -- Found {len(block_comment_entries)} blockComment entries, expected exactly 1")
        else:
            print(f"FAIL: Component 3 -- No blockComment entries found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
