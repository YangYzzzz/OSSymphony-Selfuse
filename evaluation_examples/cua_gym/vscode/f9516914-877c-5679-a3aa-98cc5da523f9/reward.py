"""
Reward Script: Set up a keybinding to toggle word wrap in the terminal
Task ID: vscode_rrt_085
Domain: vscode
Scoring:
  Component 1 (0.3): keybindings.json has at least one keybinding entry
  Component 2 (0.3): A keybinding with key=alt+z, command=workbench.action.terminal.toggleWordWrap
  Component 3 (0.4): The matching keybinding includes when=terminalFocus
"""

import os
import json
import re

HOME = '/home/user'
KEYBINDINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'keybindings.json')


def load_keybindings(path):
    """Load keybindings.json, handling optional JSONC comment prefix."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip JSONC comments (// ...)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        data = json.loads(stripped)
    except json.JSONDecodeError:
        # Try skipping first line (common comment header)
        lines = stripped.split('\n', 1)
        if len(lines) > 1:
            data = json.loads(lines[1])
        else:
            raise
    return data


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: keybindings.json must exist
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
        print(f"CRITICAL: keybindings.json is not an array, found {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: keybindings.json has at least one keybinding entry (0.3 points)
    # This distinguishes an empty [] (initial) from a populated keybindings file (golden).
    try:
        if len(bindings) > 0:
            print(f"PASS: Component 1 — keybindings.json has {len(bindings)} entry/entries (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — keybindings.json is empty (0 entries)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: A keybinding with key=alt+z and command=workbench.action.terminal.toggleWordWrap (0.3 points)
    try:
        matching = [
            b for b in bindings
            if isinstance(b, dict)
            and b.get('key', '').lower() == 'alt+z'
            and b.get('command', '') == 'workbench.action.terminal.toggleWordWrap'
        ]
        if len(matching) > 0:
            print(f"PASS: Component 2 — Found alt+z -> workbench.action.terminal.toggleWordWrap (0.3 pts)")
            total_score += 0.3
        else:
            # Show what keys/commands exist for debugging
            for b in bindings:
                if isinstance(b, dict):
                    print(f"  Found binding: key={b.get('key')}, command={b.get('command')}")
            print(f"FAIL: Component 2 — No keybinding with key=alt+z and command=workbench.action.terminal.toggleWordWrap")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The matching keybinding has when=terminalFocus (0.4 points)
    try:
        matching_with_when = [
            b for b in bindings
            if isinstance(b, dict)
            and b.get('key', '').lower() == 'alt+z'
            and b.get('command', '') == 'workbench.action.terminal.toggleWordWrap'
            and 'terminalFocus' in b.get('when', '')
        ]
        if len(matching_with_when) > 0:
            when_val = matching_with_when[0].get('when', '')
            print(f"PASS: Component 3 — when condition includes 'terminalFocus': '{when_val}' (0.4 pts)")
            total_score += 0.4
        else:
            # Show what 'when' value exists
            for b in bindings:
                if isinstance(b, dict) and b.get('key', '').lower() == 'alt+z':
                    print(f"  Found alt+z binding with when={b.get('when', '<missing>')}")
            print(f"FAIL: Component 3 — No matching keybinding with when containing 'terminalFocus'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
