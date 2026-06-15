"""
Reward Script: Create keybindings for terminal navigation (Ctrl+PageUp/PageDown)
Task ID: vscode_rrt_077
Domain: vscode
Scoring:
  Component 1 (0.5): Ctrl+PageUp -> workbench.action.terminal.focusPrevious with when=terminalFocus
  Component 2 (0.5): Ctrl+PageDown -> workbench.action.terminal.focusNext with when=terminalFocus
"""

import os
import json
import re

HOME = os.path.expanduser("~")
KEYBINDINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "keybindings.json")


def load_keybindings():
    """Load keybindings.json, handling optional comment prefix line (JSONC)."""
    try:
        with open(KEYBINDINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (VSCode JSONC format)
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            # Try skipping the first line (comment header)
            lines = content.split("\n", 1)
            if len(lines) > 1:
                return json.loads(lines[1])
            return []
    except FileNotFoundError:
        return []
    except json.JSONDecodeError:
        return []


def find_keybinding(bindings, key, command, when=None):
    """
    Check if a keybinding entry exists matching key, command, and optionally when.
    Comparison is case-insensitive for key and command.
    """
    for b in bindings:
        key_match = b.get("key", "").lower() == key.lower()
        cmd_match = b.get("command", "").lower() == command.lower()
        if when is not None:
            when_match = b.get("when", "").lower() == when.lower()
        else:
            when_match = (when is None)  # always matches if no when filter
        if key_match and cmd_match and when_match:
            return True
    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: keybindings.json must exist and be parseable
    bindings = load_keybindings()
    if not isinstance(bindings, list):
        print(f"CRITICAL: keybindings.json is not a valid JSON array")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Ctrl+PageUp keybinding for focusPrevious (0.5 points)
    try:
        has_full_1 = find_keybinding(bindings, "ctrl+pageup", "workbench.action.terminal.focusPrevious", when="terminalFocus")
        has_partial_1 = find_keybinding(bindings, "ctrl+pageup", "workbench.action.terminal.focusPrevious")
        if has_full_1:
            print(f"PASS: Component 1 — Ctrl+PageUp -> focusPrevious with terminalFocus (0.5 pts)")
            total_score += 0.5
        elif has_partial_1:
            print(f"PARTIAL: Component 1 — Ctrl+PageUp -> focusPrevious found but 'when' condition mismatch (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Ctrl+PageUp -> focusPrevious with terminalFocus not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Ctrl+PageDown keybinding for focusNext (0.5 points)
    try:
        has_full_2 = find_keybinding(bindings, "ctrl+pagedown", "workbench.action.terminal.focusNext", when="terminalFocus")
        has_partial_2 = find_keybinding(bindings, "ctrl+pagedown", "workbench.action.terminal.focusNext")
        if has_full_2:
            print(f"PASS: Component 2 — Ctrl+PageDown -> focusNext with terminalFocus (0.5 pts)")
            total_score += 0.5
        elif has_partial_2:
            print(f"PARTIAL: Component 2 — Ctrl+PageDown -> focusNext found but 'when' condition mismatch (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Ctrl+PageDown -> focusNext with terminalFocus not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
