"""
Reward Script: Verify context-aware Ctrl+Space keybindings in VSCode
Task ID: vscode_rrt_083
Domain: vscode
Scoring:
  - Component 1 (0.4): IntelliSense keybinding with editorTextFocus when clause
  - Component 2 (0.4): Terminal suggest keybinding with terminalFocus when clause
  - Component 3 (0.2): Both bindings coexist with correct key (ctrl+space)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_rrt_083'

KEYBINDINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'keybindings.json')


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
        # Skip first line (comment) and retry
        lines = content.split('\n', 1)
        if len(lines) > 1:
            return json.loads(lines[1])
        raise


def normalize(s):
    """Normalize a string for comparison: lowercase and strip whitespace."""
    if s is None:
        return ''
    return str(s).lower().strip()


def has_keybinding(bindings, expected_key, expected_command, expected_when_parts):
    """
    Check if a keybinding entry exists matching key, command, and all required
    when-clause parts. The when clause may contain the required parts in any
    order, combined with && or other operators.

    Returns the matching entry or None.
    """
    for entry in bindings:
        key = normalize(entry.get('key', ''))
        command = normalize(entry.get('command', ''))
        when = normalize(entry.get('when', ''))

        if key != normalize(expected_key):
            continue
        if command != normalize(expected_command):
            continue

        # Check that all required when-clause parts are present
        if all(normalize(part) in when for part in expected_when_parts):
            return entry
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

    # Component 1: IntelliSense keybinding (0.4 points)
    # ctrl+space -> editor.action.triggerSuggest with when clause containing
    # "editorTextFocus" and "!suggestWidgetVisible"
    try:
        match1 = has_keybinding(
            bindings,
            'ctrl+space',
            'editor.action.triggerSuggest',
            ['editortextfocus', '!suggestwidgetvisible']
        )
        if match1:
            print(f"PASS: Component 1 - IntelliSense keybinding found: {json.dumps(match1)} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - No keybinding for ctrl+space -> editor.action.triggerSuggest "
                  f"with editorTextFocus && !suggestWidgetVisible when clause")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Terminal suggest keybinding (0.4 points)
    # ctrl+space -> workbench.action.terminal.suggestShow with when clause
    # containing "terminalFocus"
    try:
        match2 = has_keybinding(
            bindings,
            'ctrl+space',
            'workbench.action.terminal.suggestShow',
            ['terminalfocus']
        )
        if match2:
            print(f"PASS: Component 2 - Terminal suggest keybinding found: {json.dumps(match2)} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - No keybinding for ctrl+space -> workbench.action.terminal.suggestShow "
                  f"with terminalFocus when clause")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Both bindings coexist with ctrl+space (0.2 points)
    # Verify that both context-aware bindings are present together (not just one)
    try:
        if match1 and match2:
            # Count how many ctrl+space bindings exist
            ctrl_space_count = sum(
                1 for entry in bindings
                if normalize(entry.get('key', '')) == 'ctrl+space'
            )
            if ctrl_space_count >= 2:
                print(f"PASS: Component 3 - Both ctrl+space bindings coexist ({ctrl_space_count} entries) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 - Expected at least 2 ctrl+space bindings, found {ctrl_space_count}")
        else:
            print(f"FAIL: Component 3 - Cannot verify coexistence: one or both bindings missing")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
