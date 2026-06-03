"""
Reward Script: VSCode keybinding conflict resolution
Task ID: vscode_rrt_073
Domain: vs-code (keybindings)
Scoring:
  Component 1 (0.5): keybindings.json contains a removal entry for myext.quickAction
  Component 2 (0.5): The removal entry binds to ctrl+shift+p specifically
"""

import os
import json
import re

HOME = '/home/user'
VSCODE_USER = os.path.join(HOME, '.config', 'Code', 'User')
KEYBINDINGS_PATH = os.path.join(VSCODE_USER, 'keybindings.json')
TASK_ID = 'vscode_rrt_073'


def load_keybindings(path):
    """Load keybindings.json, handling optional comment prefix line (JSONC)."""
    with open(path, 'r') as f:
        content = f.read()

    # Strip single-line comments (// ...) for JSONC compatibility
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)

    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        # Try skipping the first line as fallback
        lines = stripped.split('\n', 1)
        if len(lines) > 1:
            return json.loads(lines[1])
        raise


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: keybindings.json must exist and be parseable
    if not os.path.exists(KEYBINDINGS_PATH):
        print(f"CRITICAL: keybindings.json not found at {KEYBINDINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        bindings = load_keybindings(KEYBINDINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse keybindings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(bindings, list):
        print(f"CRITICAL: keybindings.json is not a JSON array, found {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Find all removal entries for myext.quickAction
    removal_entries = [
        b for b in bindings
        if isinstance(b, dict) and b.get('command') == '-myext.quickAction'
    ]

    # Component 1: keybindings.json contains a removal entry for myext.quickAction (0.5 points)
    # This FAILS on initial (no -myext.quickAction entry) and PASSES on golden
    try:
        if len(removal_entries) > 0:
            print(f"PASS: Component 1 - Found {len(removal_entries)} removal entry(ies) for myext.quickAction (0.5 pts)")
            total_score += 0.5
        else:
            commands = [b.get('command', '') for b in bindings if isinstance(b, dict)]
            print(f"FAIL: Component 1 - No removal entry for myext.quickAction found. Commands present: {commands}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The removal entry specifically targets ctrl+shift+p (0.5 points)
    # This FAILS on initial (no removal entry at all) and PASSES on golden
    try:
        matching = [
            b for b in removal_entries
            if isinstance(b, dict) and b.get('key', '').lower() == 'ctrl+shift+p'
        ]
        if len(matching) > 0:
            print(f"PASS: Component 2 - Removal entry correctly targets key 'ctrl+shift+p' (0.5 pts)")
            total_score += 0.5
        else:
            if removal_entries:
                keys = [b.get('key', '') for b in removal_entries]
                print(f"FAIL: Component 2 - Removal entry exists but targets key(s): {keys}, expected 'ctrl+shift+p'")
            else:
                print(f"FAIL: Component 2 - No removal entry found (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
