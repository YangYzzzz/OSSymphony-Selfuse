"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm working with a huge CSV file and all the columns run together—could you help me install the "Rainbow CSV" extension so the data is easier to read?
Generated: 2025-09-11 15:34:50
Status: success
Model: azure-o3
Total Steps: 13
"""

# Reward script verifying installation of Rainbow CSV VS Code extension
import os
import re
import subprocess
import json
from typing import List

# ---------------- Helper Functions ----------------

def _search_extension_dirs() -> List[str]:
    """Return list of Rainbow CSV extension directories in common VS Code extension folders."""
    home = os.path.expanduser('~')
    base_dirs = [
        os.path.join(home, '.vscode', 'extensions'),              # Local VS Code
        os.path.join(home, '.vscode-server', 'extensions'),       # Remote server (SSH, WSL)
        os.path.join(home, '.vscode-server-insiders', 'extensions'),
        os.path.join(home, '.vscode-remote', 'extensions'),
    ]
    pattern = re.compile(r'rainbow[-_]csv', re.IGNORECASE)
    matches = []
    for base in base_dirs:
        if not os.path.isdir(base):
            continue
        try:
            for name in os.listdir(base):
                if pattern.search(name):
                    matches.append(os.path.join(base, name))
        except Exception as e:
            print(f'! Error reading {base}: {e}')
    return matches


def _list_cli_extensions() -> List[str]:
    """Use `code --list-extensions` to list installed extensions.
    Returns empty list if CLI unavailable or none found."""
    try:
        output = subprocess.check_output(['code', '--list-extensions'], text=True, stderr=subprocess.DEVNULL)
    except FileNotFoundError:
        # VS Code CLI not on PATH in this environment
        return []
    except Exception as e:
        print(f'! Error running code CLI: {e}')
        return []

    pattern = re.compile(r'rainbow[-_]csv', re.IGNORECASE)
    return [line.strip() for line in output.splitlines() if pattern.search(line)]


def _is_recommended() -> bool:
    """Check if Rainbow CSV is recommended in user/workspace extensions.json for partial credit."""
    home = os.path.expanduser('~')
    candidate_files = [
        os.path.join(home, '.vscode', 'extensions.json'),
        os.path.join(home, '.vscode', 'extensions', 'extensions.json'),
    ]
    pattern = re.compile(r'rainbow[-_]csv', re.IGNORECASE)
    for fpath in candidate_files:
        if not os.path.isfile(fpath):
            continue
        try:
            with open(fpath, 'r') as fp:
                data = json.load(fp)
            recs = data if isinstance(data, list) else data.get('recommendations', [])
            if any(pattern.search(rec) for rec in recs):
                return True
        except Exception as e:
            print(f'! Failed to parse {fpath}: {e}')
    return False

# ---------------- Verification Logic ----------------

def verify_task() -> float:
    print('Verifying Rainbow CSV VS Code extension installation...')
    print('------------------------------------------------------')

    # Evidence 1: Extension directory exists
    dir_matches = _search_extension_dirs()
    if dir_matches:
        print(f'✓ Found Rainbow CSV extension directory(ies) ({len(dir_matches)}):')
        for d in dir_matches[:5]:
            print('  -', d)
    else:
        print('✗ No Rainbow CSV extension directories found')

    # Evidence 2: Extension appears in code CLI list
    cli_matches = _list_cli_extensions()
    if cli_matches:
        print('✓ Rainbow CSV listed by `code --list-extensions`:')
        for ext in cli_matches:
            print('  -', ext)
    else:
        print('✗ Rainbow CSV not listed by code CLI or CLI unavailable')

    installed = bool(dir_matches or cli_matches)

    # Evidence 3: Recommendation (only counts if not installed)
    recommended = _is_recommended()
    if recommended:
        print('• Rainbow CSV is included in extensions.json recommendations')

    # Scoring rules:
    # 1.0  -> Extension installed (evidence via directory OR CLI)
    # 0.3  -> Not installed but recommended
    # 0.0  -> Neither installed nor recommended
    if installed:
        score = 1.0
    elif recommended:
        score = 0.3
    else:
        score = 0.0

    print('------------------------------------------------------')
    print(f'Final verification score: {score}')
    return score

if __name__ == '__main__':
    reward = verify_task()
    print(f'REWARD: {reward}')

