"""
Reward Script: Create a chord keybinding (Ctrl+K Ctrl+D) for duplicating the current line
Task ID: vscode_rrt_067
Domain: vscode
Scoring:
  Component 1 (0.5): Chord keybinding with key "ctrl+k ctrl+d" exists in keybindings.json
  Component 2 (0.3): The keybinding maps to "editor.action.copyLinesDownAction"
  Component 3 (0.2): Existing keybindings are preserved alongside the new chord keybinding
"""

import os
import json
import re

HOME = '/home/user'
KEYBINDINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'keybindings.json')


def load_keybindings(path):
    """Load keybindings.json, handling optional comment prefix line (JSONC)."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip single-line comments for JSONC compatibility
        stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        try:
            return json.loads(stripped)
        except json.JSONDecodeError:
            # Try skipping first line
            lines = stripped.split('\n', 1)
            if len(lines) > 1:
                return json.loads(lines[1])
            return None
    except (FileNotFoundError, OSError):
        return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: keybindings.json must exist and be parseable
    bindings = load_keybindings(KEYBINDINGS_PATH)
    if bindings is None:
        print(f"CRITICAL: Cannot load keybindings from {KEYBINDINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    if not isinstance(bindings, list):
        print(f"CRITICAL: keybindings.json is not a list, got {type(bindings)}")
        print("REWARD: 0.0")
        return 0.0

    # Find the chord keybinding entry
    chord_entry = None
    for entry in bindings:
        if isinstance(entry, dict):
            key_val = entry.get('key', '').lower().strip()
            # Normalize whitespace: "ctrl+k  ctrl+d" -> "ctrl+k ctrl+d"
            key_normalized = ' '.join(key_val.split())
            if key_normalized == 'ctrl+k ctrl+d':
                chord_entry = entry
                break

    # Component 1: Chord keybinding with key "ctrl+k ctrl+d" exists (0.5 points)
    try:
        if chord_entry is not None:
            print(f"PASS: Component 1 — chord keybinding 'ctrl+k ctrl+d' found (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — chord keybinding 'ctrl+k ctrl+d' not found in {len(bindings)} entries")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The keybinding maps to "editor.action.copyLinesDownAction" (0.3 points)
    try:
        if chord_entry is not None:
            cmd = chord_entry.get('command', '').strip()
            if cmd == 'editor.action.copyLinesDownAction':
                print(f"PASS: Component 2 — command is 'editor.action.copyLinesDownAction' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — expected command 'editor.action.copyLinesDownAction', found '{cmd}'")
        else:
            print(f"FAIL: Component 2 — chord keybinding not found, cannot check command")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Existing keybindings preserved alongside the new chord keybinding (0.2 points)
    # This is a compound check: the chord keybinding must exist AND the pre-existing
    # ctrl+shift+l keybinding must still be present. Since the chord keybinding existence
    # anchors this check, it fails on initial_env (where chord keybinding is absent).
    try:
        if chord_entry is not None:
            # Check that the pre-existing keybinding is still there
            existing_preserved = any(
                isinstance(entry, dict)
                and ' '.join(entry.get('key', '').lower().strip().split()) == 'ctrl+shift+l'
                and entry.get('command') == 'editor.action.selectHighlights'
                for entry in bindings
            )
            if existing_preserved:
                print(f"PASS: Component 3 — existing keybinding preserved alongside new chord keybinding (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — chord keybinding exists but pre-existing ctrl+shift+l keybinding was lost")
        else:
            print(f"FAIL: Component 3 — chord keybinding not found, compound check fails")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
