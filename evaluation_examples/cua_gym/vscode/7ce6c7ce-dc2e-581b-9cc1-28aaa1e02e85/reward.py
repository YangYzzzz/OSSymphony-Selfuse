"""
Reward Script: VSCode keybinding for Ctrl+Shift+R to run Python in terminal
Task ID: vscode_stu_073
Domain: vscode
Scoring:
  Component 1 (0.4): keybindings.json exists and is a valid JSON array
  Component 2 (0.3): An entry with key "ctrl+shift+r" is present
  Component 3 (0.3): That entry's command runs Python file in terminal
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_073'
KEYBINDINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'keybindings.json')

# Valid commands that run the current Python file in terminal
VALID_COMMANDS = [
    'python.execInTerminal',
    'python.execInTerminal-icon',
    'workbench.action.terminal.runActiveFile',
]


def load_keybindings_json(path):
    """Load keybindings.json, handling optional JSONC comment prefix."""
    with open(path, 'r') as f:
        content = f.read()
    # Try direct parse
    try:
        return json.loads(content)
    except json.JSONDecodeError:
        pass
    # Strip single-line comments and try again
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    return json.loads(stripped)


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: keybindings.json exists and is a valid JSON array (0.4 points)
    bindings = None
    try:
        if not os.path.isfile(KEYBINDINGS_PATH):
            print(f"FAIL: Component 1 — keybindings.json not found at {KEYBINDINGS_PATH}")
        else:
            data = load_keybindings_json(KEYBINDINGS_PATH)
            if isinstance(data, list):
                bindings = data
                print(f"PASS: Component 1 — keybindings.json exists and is a valid JSON array with {len(bindings)} entries (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — keybindings.json is not a JSON array, got {type(data).__name__}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if bindings is None:
        # Cannot proceed without valid bindings
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: An entry with key "ctrl+shift+r" exists (0.3 points)
    matching_entries = []
    try:
        for entry in bindings:
            if isinstance(entry, dict) and 'key' in entry:
                key_val = entry['key'].strip().lower().replace(' ', '')
                if key_val == 'ctrl+shift+r':
                    matching_entries.append(entry)
        if matching_entries:
            print(f"PASS: Component 2 — Found {len(matching_entries)} entry(ies) with key ctrl+shift+r (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No entry with key ctrl+shift+r found. Keys present: {[e.get('key') for e in bindings if isinstance(e, dict)]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The ctrl+shift+r entry has a valid Python-run-in-terminal command (0.3 points)
    try:
        if matching_entries:
            matched_command = None
            for entry in matching_entries:
                cmd = entry.get('command', '').strip().lower()
                for valid_cmd in VALID_COMMANDS:
                    if cmd == valid_cmd.lower():
                        matched_command = entry.get('command')
                        break
                if matched_command is not None:
                    break
            if matched_command is not None:
                print(f"PASS: Component 3 — ctrl+shift+r bound to '{matched_command}' (0.3 pts)")
                total_score += 0.3
            else:
                commands_found = [e.get('command') for e in matching_entries]
                print(f"FAIL: Component 3 — ctrl+shift+r bound to {commands_found}, expected one of {VALID_COMMANDS}")
        else:
            print(f"FAIL: Component 3 — No ctrl+shift+r entry to check command for")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
