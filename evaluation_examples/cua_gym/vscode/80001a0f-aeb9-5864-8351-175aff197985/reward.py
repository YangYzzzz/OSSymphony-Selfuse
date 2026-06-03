"""
Reward Script: Add Ctrl+F12 keybinding for Go to Definition in VSCode
Task ID: vscode_gf2_010
Domain: vscode
Scoring:
  Component 1 (0.4): keybindings.json contains an entry with key "ctrl+f12"
  Component 2 (0.6): that entry maps to command "editor.action.revealDefinition"
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_gf2_010'

KEYBINDINGS_PATH = os.path.expanduser('~/.config/Code/User/keybindings.json')


def load_keybindings(path):
    """Load keybindings.json, handling optional JSONC comment prefix."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments (JSONC support)
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        # Try skipping first line (comment header)
        lines = stripped.split('\n', 1)
        if len(lines) > 1:
            return json.loads(lines[1])
        raise


def verify_task():
    """
    Verify that keybindings.json contains a Ctrl+F12 binding
    for editor.action.revealDefinition.
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

    print(f"INFO: Found {len(bindings)} keybinding entries")

    # Normalize keys for comparison (lowercase, strip whitespace)
    def normalize_key(k):
        return k.lower().replace(' ', '')

    # Component 1: An entry with key containing "ctrl+f12" exists (0.4 points)
    # This checks that the user added any keybinding with ctrl+f12
    try:
        has_ctrl_f12 = False
        for entry in bindings:
            if isinstance(entry, dict) and 'key' in entry:
                if normalize_key(entry['key']) == 'ctrl+f12':
                    has_ctrl_f12 = True
                    break
        if has_ctrl_f12:
            print(f"PASS: Component 1 — Found keybinding with key ctrl+f12 (0.4 pts)")
            total_score += 0.4
        else:
            keys_found = [e.get('key', '?') for e in bindings if isinstance(e, dict)]
            print(f"FAIL: Component 1 — No keybinding with key ctrl+f12. Keys found: {keys_found}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The ctrl+f12 entry maps to editor.action.revealDefinition (0.6 points)
    # This is the core verification: correct command bound to correct key
    try:
        correct_binding = False
        for entry in bindings:
            if isinstance(entry, dict) and 'key' in entry and 'command' in entry:
                if (normalize_key(entry['key']) == 'ctrl+f12' and
                        entry['command'] == 'editor.action.revealDefinition'):
                    correct_binding = True
                    break
        if correct_binding:
            print(f"PASS: Component 2 — ctrl+f12 correctly maps to editor.action.revealDefinition (0.6 pts)")
            total_score += 0.6
        else:
            # Show what ctrl+f12 maps to, if anything
            for entry in bindings:
                if isinstance(entry, dict) and 'key' in entry:
                    if normalize_key(entry['key']) == 'ctrl+f12':
                        print(f"FAIL: Component 2 — ctrl+f12 maps to '{entry.get('command', '?')}', expected 'editor.action.revealDefinition'")
                        break
            else:
                print(f"FAIL: Component 2 — No ctrl+f12 binding found to check command")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
