"""
Reward Script: Remove sheet protection and re-protect with new password
Task ID: calc_ps_034
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Password hash matches 'arch2024' (ED91)
  Component 2 (0.25): Password is new AND sheet protection is still enabled
  Component 3 (0.25): Password is new AND sorting is still allowed
"""

import os

import openpyxl
from openpyxl.worksheet.protection import SheetProtection

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_034'

# Pre-compute expected password hashes
EXPECTED_NEW_HASH = 'ED91'   # hash of 'arch2024'
OLD_HASH = 'EA91'            # hash of 'arch2023'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Archive' sheet must exist
    if 'Archive' not in wb.sheetnames:
        print("FAIL: 'Archive' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Archive']
    prot = ws.protection
    password_hash = prot.password

    # Also verify via SheetProtection API what arch2024 should hash to
    sp_check = SheetProtection(password='arch2024')
    computed_new_hash = sp_check.password

    print(f"INFO: Found password hash: {password_hash}")
    print(f"INFO: Expected new hash (arch2024): {EXPECTED_NEW_HASH}")
    print(f"INFO: Computed new hash (arch2024): {computed_new_hash}")
    print(f"INFO: Old hash (arch2023): {OLD_HASH}")

    # Determine if password has been changed to 'arch2024'
    password_is_new = (password_hash is not None and
                       password_hash == EXPECTED_NEW_HASH)

    # Component 1: Password hash matches 'arch2024' (0.5 points)
    # This is THE primary task-introduced change: password EA91 -> ED91
    try:
        if password_is_new:
            print(f"PASS: Component 1 - Password hash is '{password_hash}' matching 'arch2024' (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 - Password hash is '{password_hash}', expected '{EXPECTED_NEW_HASH}' (arch2024)")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Password changed AND sheet protection still enabled (0.25 points)
    # Anchored to the password change so it fails on initial_env
    try:
        if password_is_new and prot.sheet:
            print(f"PASS: Component 2 - Password is new AND sheet protection enabled (0.25 pts)")
            total_score += 0.25
        else:
            if not password_is_new:
                print(f"FAIL: Component 2 - Password not updated (prerequisite failed)")
            else:
                print(f"FAIL: Component 2 - Sheet protection is disabled (sheet={prot.sheet})")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Password changed AND sorting is still allowed (0.25 points)
    # In openpyxl, protection.sort=False means sorting IS allowed (not restricted)
    try:
        if password_is_new and not prot.sort:
            print(f"PASS: Component 3 - Password is new AND sorting is allowed (sort={prot.sort}) (0.25 pts)")
            total_score += 0.25
        else:
            if not password_is_new:
                print(f"FAIL: Component 3 - Password not updated (prerequisite failed)")
            else:
                print(f"FAIL: Component 3 - Sorting is NOT allowed (sort={prot.sort})")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
