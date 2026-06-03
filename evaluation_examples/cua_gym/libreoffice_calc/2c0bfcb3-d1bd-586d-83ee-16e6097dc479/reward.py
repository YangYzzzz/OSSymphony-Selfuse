"""
Reward Script: Protect 'Feedback' sheet with password, allowing format rows and AutoFilter
Task ID: calc_ps_040
Domain: libreoffice_calc
Scoring:
  Component 1: Sheet protection enabled (0.4)
  Component 2: Password is set (0.2)
  Component 3: Format rows allowed (0.2)
  Component 4: AutoFilter allowed (0.2)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_040'


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

    # Precondition: 'Feedback' sheet must exist
    if 'Feedback' not in wb.sheetnames:
        print("FAIL: 'Feedback' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Feedback']
    prot = ws.protection

    # Component 1: Sheet protection is enabled (0.4 points)
    # In openpyxl, protection.sheet == True means the sheet is protected.
    # Initial state: sheet=False. Golden state: sheet=True.
    try:
        if prot.sheet is True:
            print(f"PASS: Component 1 -- Sheet protection enabled (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Sheet protection not enabled (sheet={prot.sheet})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Password is set (0.2 points)
    # Initial state: password=None. Golden state: password is a hash string.
    # We check that a password hash exists (openpyxl stores it as a hash, not plaintext).
    try:
        has_password = (prot.password is not None and len(str(prot.password)) > 0)
        if has_password:
            print(f"PASS: Component 2 -- Password is set (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 -- No password set (password={prot.password})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Format rows is allowed (0.2 points)
    # In openpyxl SheetProtection, formatRows=False means formatting rows IS allowed.
    # Initial state: formatRows=True (forbidden by default template, but sheet not protected).
    # Golden state: formatRows=False (allowed).
    # We only award points if the sheet IS protected AND formatRows is allowed.
    try:
        if prot.sheet is True and prot.formatRows is False:
            print(f"PASS: Component 3 -- Format rows allowed while protected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Format rows not properly configured (sheet={prot.sheet}, formatRows={prot.formatRows})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: AutoFilter is allowed (0.2 points)
    # In openpyxl SheetProtection, autoFilter=False means AutoFilter IS allowed.
    # Initial state: autoFilter=True (forbidden by default). Golden: autoFilter=False (allowed).
    # We only award points if the sheet IS protected AND autoFilter is allowed.
    try:
        if prot.sheet is True and prot.autoFilter is False:
            print(f"PASS: Component 4 -- AutoFilter allowed while protected (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 -- AutoFilter not properly configured (sheet={prot.sheet}, autoFilter={prot.autoFilter})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
