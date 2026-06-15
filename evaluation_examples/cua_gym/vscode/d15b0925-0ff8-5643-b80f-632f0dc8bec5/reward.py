"""
Reward Script: Change language mode of data.txt to Python in VSCode
Task ID: vscode_file_024
Domain: vs_code
Scoring:
  - Component 1 (0.7 pts): files.associations contains 'data.txt' -> 'python' in settings.json
  - Component 2 (0.3 pts): Compound check — language association is python AND data.txt still exists
                            (gated on comp1 passing — prevents scoring pre-existing file presence)
"""

import os
import json
import re

WORKDIR = '/home/user'
TASK_ID = 'vscode_file_024'

SETTINGS_PATH = '/home/user/.config/Code/User/settings.json'
DATA_FILE_PATH = '/home/user/project/data.txt'


def load_settings(path):
    """Load VSCode settings.json, stripping JSONC comments if necessary."""
    try:
        with open(path, 'r') as f:
            content = f.read()
        # Strip // comments (JSONC format used by VSCode)
        content_clean = re.sub(r'//.*$', '', content, flags=re.MULTILINE)
        return json.loads(content_clean)
    except (FileNotFoundError, json.JSONDecodeError) as e:
        return None


def get_data_txt_language_association(settings):
    """
    Return the language value associated with 'data.txt' in files.associations,
    or None if not found.
    """
    files_associations = settings.get('files.associations', {})
    for key, value in files_associations.items():
        if key == 'data.txt' or key == '**/data.txt':
            return value
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: settings.json must exist and be parseable
    if not os.path.exists(SETTINGS_PATH):
        print(f"CRITICAL: settings.json not found at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    settings = load_settings(SETTINGS_PATH)
    if settings is None:
        print(f"CRITICAL: Cannot parse settings.json at {SETTINGS_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: files.associations maps 'data.txt' to 'python' (0.7 points)
    # This verifies the core task: language mode is set to Python for data.txt
    # FAILS on initial (no files.associations) — PASSES on golden (has the mapping)
    association_value = get_data_txt_language_association(settings)
    try:
        if association_value is not None and str(association_value).lower() == 'python':
            print(f"PASS: Component 1 — files.associations contains 'data.txt' -> '{association_value}' (0.7 pts)")
            total_score += 0.7
        else:
            files_associations = settings.get('files.associations', {})
            if not files_associations:
                print(f"FAIL: Component 1 — files.associations is empty or missing; expected 'data.txt': 'python'")
            else:
                print(f"FAIL: Component 1 — files.associations: {files_associations}; expected 'data.txt' -> 'python'")
            association_value = None  # ensure it's explicitly None on failure
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        association_value = None

    # Component 2: Compound check — language association is python AND data.txt still exists (0.3 points)
    # The task requires the file NOT be renamed. This is only a meaningful check WHEN the
    # language association has been set — gating ensures initial_env cannot score this component.
    try:
        if association_value is not None and str(association_value).lower() == 'python':
            if os.path.exists(DATA_FILE_PATH) and os.path.getsize(DATA_FILE_PATH) > 0:
                file_size = os.path.getsize(DATA_FILE_PATH)
                print(f"PASS: Component 2 — data.txt exists at {DATA_FILE_PATH} (size: {file_size} bytes) (0.3 pts)")
                total_score += 0.3
            elif os.path.exists(DATA_FILE_PATH):
                print(f"FAIL: Component 2 — data.txt exists but is empty; file content may have been lost")
            else:
                print(f"FAIL: Component 2 — data.txt not found at {DATA_FILE_PATH} (file was renamed or deleted)")
        else:
            print(f"SKIP: Component 2 — skipped because Component 1 failed (language association not python)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
