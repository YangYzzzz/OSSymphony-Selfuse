"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’m frequently jumping between my Python code and the terminal while debugging—could you help me set Ctrl + E as a quick toggle for the integrated terminal in VS Code?
Generated: 2025-09-11 21:13:58
Status: success
Model: azure-o3
Total Steps: 15
"""

import json
import pathlib
import re
import sys
import os

"""
Reward Script: Verify that the user bound Ctrl+E to toggle the integrated
terminal in VS Code (workbench.action.terminal.toggleTerminal).
Progressive scoring is used:
    • 1.0 – Ctrl+E bound exactly to the toggleTerminal command
    • 0.7 – Ctrl+E bound to another workbench.action.terminal.* command
    • 0.4 – Ctrl+E bound to any command that contains the word "terminal"
    • 0.2 – Ctrl+E bound to some other command
    • 0.0 – No Ctrl+E binding found
The script inspects typical VS Code keybindings.json locations for Linux,
Windows and macOS.  Comments and trailing commas are stripped so that JSON
parsing succeeds even when the file contains VS Code-style comments.
"""

def strip_comments(text: str) -> str:
    """Remove // line comments and /* */ block comments from JSON-like text."""
    out_lines = []
    in_block = False
    for line in text.splitlines():
        # start of block comment
        if '/*' in line:
            in_block = True
            line = line.split('/*', 1)[0]
        # end of block comment (same line or later)
        if '*/' in line and in_block:
            line = line.split('*/', 1)[1]
            in_block = False
        if in_block:
            continue
        stripped = line.strip()
        # whole-line // comment
        if stripped.startswith('//'):
            continue
        # inline // comment outside quotes
        if '//' in line:
            idx = line.index('//')
            if line[:idx].count('"') % 2 == 0:  # even quotes ⇒ not inside string
                line = line[:idx]
        out_lines.append(line)
    return '\n'.join(out_lines)

def typical_keybinding_paths() -> list[pathlib.Path]:
    """Return list of typical keybindings.json paths for all OSes."""
    home = pathlib.Path.home()
    return [
        home / '.config' / 'Code' / 'User' / 'keybindings.json',          # Linux VS Code
        home / '.config' / 'Code - OSS' / 'User' / 'keybindings.json',   # Linux OSS build
        home / '.config' / 'Code - Insiders' / 'User' / 'keybindings.json',
        home / 'AppData' / 'Roaming' / 'Code' / 'User' / 'keybindings.json',  # Windows
        home / 'Library' / 'Application Support' / 'Code' / 'User' / 'keybindings.json',  # macOS
    ]

def load_keybindings(path: pathlib.Path) -> list:
    """Load keybindings array from file, returning empty list on failure."""
    try:
        data = path.read_text(encoding='utf-8')
    except Exception:
        return []
    cleaned = strip_comments(data).strip()
    if not cleaned:
        return []
    # remove trailing commas before ] or }
    cleaned = re.sub(r',\s*(\]|})', r'\1', cleaned)
    try:
        obj = json.loads(cleaned)
        return obj if isinstance(obj, list) else []
    except json.JSONDecodeError:
        return []

def normalize_key(key: str) -> str:
    return key.lower().replace(' ', '')

def active_key(entry: dict, platform_key: str) -> str | None:
    """Return the key combination active for current platform."""
    return (
        entry.get({
            'linux': 'linux',
            'windows': 'win',
            'darwin': 'mac'
        }[platform_key])
        or entry.get('key')
    )

def score_entry(entry: dict, platform_key: str) -> float:
    key_str = active_key(entry, platform_key)
    if not key_str or normalize_key(key_str) != 'ctrl+e':
        return 0.0
    command = entry.get('command', '')
    if not command or command.startswith('-'):  # unbound
        return 0.0
    cmd = command.lower()
    if cmd in ('workbench.action.terminal.toggleterminal', 'workbench.action.toggleterminal'):
        return 1.0
    if cmd.startswith('workbench.action.terminal.'):
        return 0.7
    if 'terminal' in cmd:
        return 0.4
    return 0.2

def verify_task() -> float:
    platform_key = (
        'windows' if sys.platform.startswith('win') else
        'darwin' if sys.platform == 'darwin' else
        'linux'
    )
    files = [p for p in typical_keybinding_paths() if p.exists()]
    if not files:
        print('✗ No keybindings.json file found in typical locations.')
        return 0.0

    best_score = 0.0
    for file in files:
        print(f'Checking {file} ...')
        bindings = load_keybindings(file)
        if not bindings:
            print('  File empty or contains no valid bindings.')
            continue
        # VS Code applies later entries last ⇒ iterate in reverse
        for entry in reversed(bindings):
            score = score_entry(entry, platform_key)
            if score:
                key_disp = active_key(entry, platform_key)
                print(f"  Found binding: {key_disp} → {entry.get('command')} | score {score}")
                best_score = max(best_score, score)
            if best_score == 1.0:
                break
        if best_score == 1.0:
            break

    if best_score == 0.0:
        print('✗ Ctrl+E not bound to integrated terminal toggle.')
    elif best_score < 1.0:
        print(f'Partial completion detected. Awarding score {best_score}.')
    else:
        print('✓ Full task completion verified.')
    return best_score

def main():
    score = verify_task()
    # clamp to [0,1]
    score = max(0.0, min(1.0, score))
    print(f'REWARD: {score}')

if __name__ == '__main__':
    main()

