"""
Reward Script: Change language mode of current file from Plain Text to C
Task ID: vscode_stu_012
Domain: vscode
Scoring:
  Component 1 (0.6): files.associations no longer maps *.c to plaintext
  Component 2 (0.4): *.c is either unmapped (default C detection) or explicitly mapped to 'c'
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_stu_012'
SETTINGS_PATH = os.path.join(WORKDIR, '.config', 'Code', 'User', 'settings.json')


def load_settings():
    """Load VSCode settings.json, handling JSONC comments."""
    try:
        with open(SETTINGS_PATH, 'r') as f:
            content = f.read()
        # Strip single-line comments (JSONC)
        clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(clean)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        print(f"WARN: Could not load settings.json: {e}")
        return None


def verify_task():
    """
    Verify that the language mode for .c files is changed from Plain Text to C.

    Initial state: settings.json has files.associations mapping *.c to plaintext
    Golden state: that mapping is removed (or changed to 'c')

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: settings.json must exist and be loadable
    settings = load_settings()
    if settings is None:
        print("CRITICAL: Cannot load settings.json")
        print("REWARD: 0.0")
        return 0.0

    # Get the files.associations section
    file_assocs = settings.get('files.associations', {})
    c_mapping = file_assocs.get('*.c', None)

    # Component 1: *.c is NOT mapped to 'plaintext' (0.6 points)
    # This is the core task requirement: remove the plaintext override
    # Initial state has {"*.c": "plaintext"} -> this check FAILS on initial
    # Golden state removed it -> this check PASSES on golden
    try:
        if c_mapping is None or str(c_mapping).lower() != 'plaintext':
            print(f"PASS: Component 1 - *.c is not mapped to plaintext (mapping: {c_mapping}) (0.6 pts)")
            total_score += 0.6
        else:
            print(f"FAIL: Component 1 - *.c is still mapped to '{c_mapping}', expected it to not be 'plaintext'")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: *.c mapping is properly resolved to C language (0.4 points)
    # Valid golden states: no mapping at all (VSCode auto-detects C from extension),
    # or explicitly mapped to 'c'. Must NOT be mapped to any non-C language.
    # Initial state maps to 'plaintext' -> FAILS
    # Golden state has no mapping -> PASSES (VSCode defaults to C for .c files)
    try:
        if c_mapping is None:
            # No explicit mapping: VSCode will auto-detect .c as C language
            print(f"PASS: Component 2 - No explicit mapping for *.c, VSCode will auto-detect C (0.4 pts)")
            total_score += 0.4
        elif str(c_mapping).lower() == 'c':
            # Explicitly mapped to C
            print(f"PASS: Component 2 - *.c explicitly mapped to 'c' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 - *.c mapped to '{c_mapping}', expected no mapping or 'c'")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
