"""
Reward Script: Create keybinding for terminal split + npm run watch
Task ID: vscode_rrt_092
Domain: vs-code (keybindings)
Scoring:
  - Component 1 (0.25): keybindings.json contains entry with key=ctrl+shift+s and command=runCommands
  - Component 2 (0.25): args.commands includes workbench.action.terminal.split
  - Component 3 (0.25): args.commands includes workbench.action.terminal.sendSequence with text="npm run watch\n"
  - Component 4 (0.25): when clause is terminalFocus
"""

import os
import json
import re

HOME = '/home/user'
KEYBINDINGS_PATH = os.path.join(HOME, '.config', 'Code', 'User', 'keybindings.json')


def load_keybindings(path):
    """Load keybindings.json, handling optional comment prefix line (JSONC)."""
    with open(path, 'r') as f:
        content = f.read()
    # Strip // comments for JSONC compatibility
    stripped = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
    try:
        return json.loads(stripped)
    except json.JSONDecodeError:
        # Try skipping first line
        lines = stripped.split('\n', 1)
        if len(lines) > 1:
            return json.loads(lines[1])
        raise


def verify_task():
    """
    Verify keybinding creation with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be parseable
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

    # Find the target keybinding entry
    target_entry = None
    for entry in bindings:
        if isinstance(entry, dict):
            key = entry.get('key', '').lower().replace(' ', '')
            if key == 'ctrl+shift+s':
                target_entry = entry
                break

    if target_entry is None:
        print("FAIL: No keybinding with key 'ctrl+shift+s' found")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: key=ctrl+shift+s and command=runCommands (0.25 points)
    try:
        cmd = target_entry.get('command', '')
        if cmd.lower() == 'runcommands':
            print(f"PASS: Component 1 — key=ctrl+shift+s with command=runCommands (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — expected command 'runCommands', found '{cmd}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: args.commands includes workbench.action.terminal.split (0.25 points)
    try:
        args = target_entry.get('args', {})
        commands = args.get('commands', [])
        has_split = False
        for c in commands:
            if isinstance(c, str) and c == 'workbench.action.terminal.split':
                has_split = True
                break
            elif isinstance(c, dict) and c.get('command') == 'workbench.action.terminal.split':
                has_split = True
                break
        if has_split:
            print(f"PASS: Component 2 — terminal.split command found in args.commands (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — workbench.action.terminal.split not found in commands: {commands}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: args.commands includes sendSequence with text="npm run watch\n" (0.25 points)
    try:
        args = target_entry.get('args', {})
        commands = args.get('commands', [])
        has_send = False
        for c in commands:
            if isinstance(c, dict):
                cmd_name = c.get('command', '')
                if cmd_name == 'workbench.action.terminal.sendSequence':
                    send_args = c.get('args', {})
                    text = send_args.get('text', '')
                    if 'npm run watch' in text:
                        has_send = True
                        break
        if has_send:
            print(f"PASS: Component 3 — sendSequence with 'npm run watch' found (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — sendSequence with 'npm run watch' not found in commands")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: when clause is terminalFocus (0.25 points)
    try:
        when = target_entry.get('when', '')
        if 'terminalFocus' in when or 'terminalfocus' in when.lower():
            print(f"PASS: Component 4 — when='terminalFocus' present (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — expected when='terminalFocus', found '{when}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
