"""
Reward Script: Configure Ctrl+Shift+D keybinding for 'Deploy Staging' task
Task ID: vscode_ops_047
Domain: vscode
Scoring:
  Component 1 (0.4): keybindings.json has entry with key ctrl+shift+d
  Component 2 (0.3): That entry maps to workbench.action.tasks.runTask
  Component 3 (0.3): That entry has args 'Deploy Staging'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_ops_047'

# VSCode keybindings path on Linux
KEYBINDINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'keybindings.json')


def load_keybindings(path):
    """Load keybindings.json, handling optional JSONC comment prefix."""
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


def normalize_key(key_str):
    """Normalize a keybinding key string for comparison.
    VSCode accepts various forms: ctrl+shift+d, Ctrl+Shift+D, etc.
    """
    if not isinstance(key_str, str):
        return ''
    return key_str.lower().strip()


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
        print(f"CRITICAL: keybindings.json is not a list, found {type(bindings).__name__}")
        print("REWARD: 0.0")
        return 0.0

    # Find any entry that has key ctrl+shift+d
    target_entry = None
    for entry in bindings:
        if isinstance(entry, dict) and normalize_key(entry.get('key', '')) == 'ctrl+shift+d':
            target_entry = entry
            break

    # Component 1: keybindings.json has an entry with key ctrl+shift+d (0.4 points)
    try:
        if target_entry is not None:
            print(f"PASS: Component 1 - Found keybinding with key 'ctrl+shift+d' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 - No keybinding entry with key 'ctrl+shift+d' found")
            print(f"  Existing bindings: {json.dumps(bindings, indent=2)}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: The entry maps to workbench.action.tasks.runTask (0.3 points)
    try:
        if target_entry is not None:
            cmd = target_entry.get('command', '')
            if isinstance(cmd, str) and cmd.strip() == 'workbench.action.tasks.runTask':
                print(f"PASS: Component 2 - Command is 'workbench.action.tasks.runTask' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 - Expected command 'workbench.action.tasks.runTask', found '{cmd}'")
        else:
            print(f"FAIL: Component 2 - No target entry to check command (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: The entry has args 'Deploy Staging' (0.3 points)
    try:
        if target_entry is not None:
            args_val = target_entry.get('args', None)
            # args can be a string or could potentially be in other forms
            if isinstance(args_val, str) and args_val.strip() == 'Deploy Staging':
                print(f"PASS: Component 3 - Args is 'Deploy Staging' (0.3 pts)")
                total_score += 0.3
            elif isinstance(args_val, dict) and args_val.get('task', '') == 'Deploy Staging':
                # Alternative form: {"task": "Deploy Staging"}
                print(f"PASS: Component 3 - Args contains task 'Deploy Staging' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 - Expected args 'Deploy Staging', found '{args_val}'")
        else:
            print(f"FAIL: Component 3 - No target entry to check args (depends on Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
