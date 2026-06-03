"""
Reward Script: Terminal workflow keybindings for full-stack developer
Task ID: vscode_rrt_095
Domain: vscode
Scoring:
  Component 1 (0.10): keybindings.json exists and is valid JSON array with 4+ entries
  Component 2 (0.20): Ctrl+1 -> focusAtIndex1 with terminalFocus
  Component 3 (0.20): Ctrl+2 -> focusAtIndex2 with terminalFocus
  Component 4 (0.20): Ctrl+3 -> focusAtIndex3 with terminalFocus
  Component 5 (0.20): Ctrl+4 -> focusAtIndex4 with terminalFocus
  Component 6 (0.10): All four when-clauses are "terminalFocus" (no missing when)
"""

import os
import json
import re

HOME = os.path.expanduser("~")
KEYBINDINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "keybindings.json")

def load_keybindings(path):
    """Load keybindings.json, handling optional JSONC comment prefix."""
    with open(path, "r") as f:
        content = f.read()
    # Strip single-line comments (JSONC)
    content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(content_clean)


def find_binding(bindings, key, command):
    """Find a keybinding entry matching key and command (case-insensitive key)."""
    for b in bindings:
        if (b.get("key", "").lower() == key.lower()
                and b.get("command", "") == command):
            return b
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(KEYBINDINGS_PATH):
        print(f"CRITICAL: keybindings.json not found at {KEYBINDINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Load keybindings
    try:
        bindings = load_keybindings(KEYBINDINGS_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot parse keybindings.json: {e}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(bindings, list):
        print(f"CRITICAL: keybindings.json is not a JSON array, got {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: At least 4 keybinding entries present (0.10 pts)
    # Initial has [] (0 entries), golden has 4 entries
    try:
        if len(bindings) >= 4:
            print(f"PASS: Component 1 — keybindings array has {len(bindings)} entries (>= 4) (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 1 — keybindings array has {len(bindings)} entries, expected >= 4")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Expected keybindings
    expected = [
        ("ctrl+1", "workbench.action.terminal.focusAtIndex1"),
        ("ctrl+2", "workbench.action.terminal.focusAtIndex2"),
        ("ctrl+3", "workbench.action.terminal.focusAtIndex3"),
        ("ctrl+4", "workbench.action.terminal.focusAtIndex4"),
    ]

    # Components 2-5: Each keybinding present with correct when clause (0.20 pts each)
    comp2to5_pass_count = 0
    for i, (key, command) in enumerate(expected):
        comp_num = i + 2
        try:
            binding = find_binding(bindings, key, command)
            if binding is not None:
                when_val = binding.get("when", "")
                if "terminalFocus" in when_val:
                    print(f"PASS: Component {comp_num} — {key} -> {command} with when='{when_val}' (0.20 pts)")
                    total_score += 0.20
                    comp2to5_pass_count += 1
                else:
                    # Binding exists but wrong/missing when clause
                    print(f"FAIL: Component {comp_num} — {key} -> {command} found but when='{when_val}', expected 'terminalFocus'")
            else:
                print(f"FAIL: Component {comp_num} — no binding for {key} -> {command}")
        except Exception as e:
            print(f"ERROR: Component {comp_num} — {e}")

    # Component 6: All four when-clauses are terminalFocus (0.10 pts)
    # This is a compound check: only passes if all 4 bindings exist AND all have terminalFocus
    try:
        valid_count = 0
        for key, command in expected:
            binding = find_binding(bindings, key, command)
            if binding is not None and "terminalFocus" in binding.get("when", ""):
                valid_count += 1
        if valid_count == 4:
            print(f"PASS: Component 6 — all 4 bindings have terminalFocus when-clause (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 6 — not all 4 bindings have correct terminalFocus when-clause")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
