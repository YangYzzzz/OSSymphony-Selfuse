"""
Reward Script: Remove default Ctrl+W (close editor) and reassign to close terminal
Task ID: vscode_rrt_069
Domain: vscode
Scoring:
  Component 1 (0.5): Removal entry for default close editor binding exists
  Component 2 (0.5): New Ctrl+W binding to kill terminal with terminalFocus condition
"""

import os
import json
import re

HOME = '/home/user'
KEYBINDINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'keybindings.json')
TASK_ID = 'vscode_rrt_069'


def load_keybindings(path):
    """Load keybindings.json, handling optional comment prefix line."""
    with open(path, 'r') as f:
        content = f.read()
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        # Strip JSONC comments
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(stripped)


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
        print(f"CRITICAL: keybindings.json is not a list, got {type(bindings)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Removal of default Ctrl+W close editor binding (0.5 points)
    # Expected: {"key": "ctrl+w", "command": "-workbench.action.closeActiveEditor"}
    try:
        removal_found = False
        for entry in bindings:
            if not isinstance(entry, dict):
                continue
            key = entry.get("key", "").lower().replace(" ", "")
            command = entry.get("command", "")
            if key == "ctrl+w" and command == "-workbench.action.closeActiveEditor":
                removal_found = True
                break
        if removal_found:
            print("PASS: Component 1 — Removal entry for default Ctrl+W close editor found (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 1 — No removal entry for Ctrl+W closeActiveEditor found")
            print(f"  Bindings found: {json.dumps(bindings, indent=2)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: New Ctrl+W binding to kill terminal with terminalFocus (0.5 points)
    # Expected: {"key": "ctrl+w", "command": "workbench.action.terminal.kill", "when": "terminalFocus"}
    try:
        new_binding_found = False
        for entry in bindings:
            if not isinstance(entry, dict):
                continue
            key = entry.get("key", "").lower().replace(" ", "")
            command = entry.get("command", "")
            when = entry.get("when", "")
            if (key == "ctrl+w"
                    and command == "workbench.action.terminal.kill"
                    and "terminalFocus" in when):
                new_binding_found = True
                break
        if new_binding_found:
            print("PASS: Component 2 — New Ctrl+W terminal kill binding with terminalFocus found (0.5 pts)")
            total_score += 0.5
        else:
            print("FAIL: Component 2 — No Ctrl+W terminal kill binding with terminalFocus condition found")
            print(f"  Bindings found: {json.dumps(bindings, indent=2)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
