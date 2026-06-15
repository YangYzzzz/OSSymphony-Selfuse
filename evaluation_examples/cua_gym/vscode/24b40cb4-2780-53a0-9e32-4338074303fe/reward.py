"""
Reward Script: Add Ctrl+Shift+L keybinding for editor.action.transformToLowercase
Task ID: vscode_prod_016
Domain: vscode
Scoring:
  Component 1 (0.5): keybindings.json contains an entry with key=ctrl+shift+l and command=editor.action.transformToLowercase
  Component 2 (0.3): The keybinding entry has the exact correct command string
  Component 3 (0.2): keybindings.json is valid JSON and the binding is the only/primary entry (no extraneous conflicting bindings for the same key)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_prod_016'

KEYBINDINGS_PATH = os.path.join(
    os.path.expanduser('~'), '.config', 'Code', 'User', 'keybindings.json'
)

TARGET_KEY = 'ctrl+shift+l'
TARGET_COMMAND = 'editor.action.transformToLowercase'


def load_keybindings(path):
    """Load keybindings.json, handling optional comment prefix line."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct parse first
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip JSONC comments and retry
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        pass
    # Skip first line (comment) and retry
    lines = content.split('\n', 1)
    if len(lines) > 1:
        return json.loads(lines[1])
    raise ValueError(f"Cannot parse keybindings from {path}")


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

    # Component 1: An entry exists with key ctrl+shift+l mapped to the lowercase command (0.5 points)
    try:
        matching_entries = [
            b for b in bindings
            if isinstance(b, dict)
            and b.get('key', '').lower().replace(' ', '') == TARGET_KEY
            and b.get('command', '').lower() == TARGET_COMMAND.lower()
        ]
        if len(matching_entries) > 0:
            print(f"PASS: Component 1 — Found keybinding: key='{matching_entries[0].get('key')}', command='{matching_entries[0].get('command')}' (0.5 pts)")
            total_score += 0.5
        else:
            # Check partial: key exists but wrong command
            key_matches = [b for b in bindings if isinstance(b, dict) and b.get('key', '').lower().replace(' ', '') == TARGET_KEY]
            cmd_matches = [b for b in bindings if isinstance(b, dict) and b.get('command', '').lower() == TARGET_COMMAND.lower()]
            print(f"FAIL: Component 1 — No entry with key='{TARGET_KEY}' and command='{TARGET_COMMAND}'")
            if key_matches:
                print(f"  Found key='{TARGET_KEY}' but command='{key_matches[0].get('command')}'")
            if cmd_matches:
                print(f"  Found command='{TARGET_COMMAND}' but key='{cmd_matches[0].get('key')}'")
            if not key_matches and not cmd_matches:
                print(f"  Bindings found: {bindings}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The command string is exactly 'editor.action.transformToLowercase' (case-sensitive exact match) (0.3 points)
    try:
        exact_matches = [
            b for b in bindings
            if isinstance(b, dict)
            and b.get('key', '').lower().replace(' ', '') == TARGET_KEY
            and b.get('command') == TARGET_COMMAND
        ]
        if len(exact_matches) > 0:
            print(f"PASS: Component 2 — Exact command match: '{exact_matches[0].get('command')}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No exact case-sensitive match for command '{TARGET_COMMAND}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: No conflicting bindings for the same key that would override the desired one (0.2 points)
    # A negative command (prefixed with '-') for the same key would disable it
    try:
        key_entries = [
            b for b in bindings
            if isinstance(b, dict)
            and b.get('key', '').lower().replace(' ', '') == TARGET_KEY
        ]
        # Check no negative/disabling entries for this key
        negative_entries = [
            b for b in key_entries
            if isinstance(b, dict)
            and b.get('command', '').startswith('-')
        ]
        # Check that desired command entry exists AND is not overridden
        desired_entries = [
            b for b in key_entries
            if isinstance(b, dict)
            and b.get('command') == TARGET_COMMAND
        ]
        if len(desired_entries) > 0 and len(negative_entries) == 0:
            print(f"PASS: Component 3 — Binding is clean, no conflicting overrides ({len(key_entries)} total entries for this key) (0.2 pts)")
            total_score += 0.2
        else:
            if negative_entries:
                print(f"FAIL: Component 3 — Found {len(negative_entries)} negative/disabling entries for key '{TARGET_KEY}'")
            else:
                print(f"FAIL: Component 3 — Desired binding not found among {len(key_entries)} entries for key '{TARGET_KEY}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
