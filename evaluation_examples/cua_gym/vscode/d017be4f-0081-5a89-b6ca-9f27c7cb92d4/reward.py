"""
Reward Script: Configure terminal sendSequence keybinding
Task ID: vscode_rrt_078
Domain: vscode
Scoring:
  Component 1 (0.35): Keybinding with key=ctrl+shift+r and command=workbench.action.terminal.sendSequence exists
  Component 2 (0.35): args.text is exactly 'clear && npm run dev\n'
  Component 3 (0.30): The text ends with newline (ensures command auto-executes)
"""

import os
import json
import re

HOME = '/home/user'
KEYBINDINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'keybindings.json')
TASK_ID = 'vscode_rrt_078'


def load_keybindings(path):
    """Load keybindings.json, handling optional comment prefix line (JSONC)."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip // comments (JSONC support)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        # Try skipping first line
        lines = content.split('\n', 1)
        if len(lines) > 1:
            return json.loads(lines[1])
        raise


def find_matching_binding(bindings, key, command):
    """Find a keybinding entry matching the given key and command."""
    for b in bindings:
        if not isinstance(b, dict):
            continue
        b_key = str(b.get('key', '')).lower().strip()
        b_cmd = str(b.get('command', '')).lower().strip()
        if b_key == key.lower() and b_cmd == command.lower():
            return b
    return None


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
        print(f"CRITICAL: keybindings.json is not a list, got {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Keybinding with key=ctrl+shift+r and command=workbench.action.terminal.sendSequence exists (0.35 points)
    try:
        match = find_matching_binding(bindings, 'ctrl+shift+r', 'workbench.action.terminal.sendSequence')
        if match is not None:
            print(f"PASS: Component 1 — Found keybinding: key={match.get('key')}, command={match.get('command')} (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — No keybinding found with key=ctrl+shift+r and command=workbench.action.terminal.sendSequence")
            print(f"  Found bindings: {json.dumps(bindings, indent=2)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: args.text is exactly 'clear && npm run dev\n' (0.35 points)
    try:
        if match is not None:
            args = match.get('args', {})
            if isinstance(args, dict):
                text = args.get('text', '')
                expected_text = 'clear && npm run dev\n'
                if text == expected_text:
                    print(f"PASS: Component 2 — args.text matches exactly: {repr(text)} (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — args.text mismatch: expected {repr(expected_text)}, got {repr(text)}")
            else:
                print(f"FAIL: Component 2 — args is not a dict: {type(args).__name__}")
        else:
            print(f"FAIL: Component 2 — No matching keybinding found (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The text ends with newline character (ensures command auto-executes) (0.30 points)
    try:
        if match is not None:
            args = match.get('args', {})
            if isinstance(args, dict):
                text = args.get('text', '')
                if text.endswith('\n'):
                    print(f"PASS: Component 3 — text ends with newline (auto-execute enabled) (0.30 pts)")
                    total_score += 0.30
                else:
                    print(f"FAIL: Component 3 — text does not end with newline: {repr(text)}")
            else:
                print(f"FAIL: Component 3 — args is not a dict")
        else:
            print(f"FAIL: Component 3 — No matching keybinding found (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
