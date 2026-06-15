"""
Reward Script: Terminal management keybindings in VSCode
Task ID: vscode_rrt_080
Domain: vscode
Scoring:
  - Component 1 (0.35): Ctrl+Shift+` → workbench.action.terminal.new
  - Component 2 (0.35): Ctrl+Shift+X → workbench.action.terminal.kill (when: terminalFocus)
  - Component 3 (0.30): Ctrl+Shift+M → workbench.action.toggleMaximizedPanel
"""

import os
import json
import re

HOME = os.path.expanduser("~")
KEYBINDINGS_PATH = os.path.join(HOME, ".config", "Code", "User", "keybindings.json")
TASK_ID = "vscode_rrt_080"


def load_keybindings():
    """Load keybindings.json, handling optional JSONC comment prefix."""
    try:
        with open(KEYBINDINGS_PATH, "r") as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(stripped)
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def normalize_key(key_str):
    """Normalize a keybinding key string for comparison.
    Lowercases, strips spaces, and sorts modifier parts."""
    parts = [p.strip().lower() for p in key_str.split("+")]
    # The last part is the actual key, modifiers precede it
    return "+".join(parts)


def find_binding(bindings, expected_key, expected_command, expected_when=None):
    """Search bindings list for a matching entry."""
    norm_expected_key = normalize_key(expected_key)
    for b in bindings:
        if not isinstance(b, dict):
            continue
        bkey = normalize_key(b.get("key", ""))
        bcmd = b.get("command", "").strip().lower()
        if bkey == norm_expected_key and bcmd == expected_command.strip().lower():
            if expected_when is not None:
                bwhen = b.get("when", "").strip().lower()
                if expected_when.strip().lower() not in bwhen:
                    continue
            return True
    return False


def verify_task():
    """Verify task completion with progressive scoring. Returns float 0.0-1.0."""
    total_score = 0.0

    # Load keybindings
    bindings = load_keybindings()
    if bindings is None:
        print("CRITICAL: Cannot load keybindings.json or file not found")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(bindings, list):
        print(f"CRITICAL: keybindings.json is not a list, got {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Ctrl+Shift+` → workbench.action.terminal.new (0.35 points)
    try:
        if find_binding(bindings, "ctrl+shift+`", "workbench.action.terminal.new"):
            print("PASS: Component 1 — ctrl+shift+` → workbench.action.terminal.new (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 — ctrl+shift+` → workbench.action.terminal.new not found")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Ctrl+Shift+X → workbench.action.terminal.kill with when=terminalFocus (0.35 points)
    try:
        if find_binding(bindings, "ctrl+shift+x", "workbench.action.terminal.kill", expected_when="terminalFocus"):
            print("PASS: Component 2 — ctrl+shift+x → workbench.action.terminal.kill (when: terminalFocus) (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 2 — ctrl+shift+x → workbench.action.terminal.kill (when: terminalFocus) not found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Ctrl+Shift+M → workbench.action.toggleMaximizedPanel (0.30 points)
    try:
        if find_binding(bindings, "ctrl+shift+m", "workbench.action.toggleMaximizedPanel"):
            print("PASS: Component 3 — ctrl+shift+m → workbench.action.toggleMaximizedPanel (0.30 pts)")
            total_score += 0.30
        else:
            print("FAIL: Component 3 — ctrl+shift+m → workbench.action.toggleMaximizedPanel not found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
