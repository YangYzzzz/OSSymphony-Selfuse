"""
Reward Script: Protect 'Weekly Plan' sheet with password and allow formatting
Task ID: calc_ps_036
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Sheet protection is enabled
  Component 2 (0.30): Password is set (non-empty)
  Component 3 (0.20): formatCells is allowed (False when protection on)
  Component 4 (0.15): formatColumns is allowed (False when protection on)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_ps_036'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    In openpyxl's SheetProtection model:
    - ws.protection.sheet = True means protection IS enabled
    - ws.protection.formatCells = False means formatting cells IS allowed
    - ws.protection.formatCells = True means formatting cells IS blocked
    So when protection is on, False = allowed, True = blocked.
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Weekly Plan' sheet must exist
    if 'Weekly Plan' not in wb.sheetnames:
        print("FAIL: 'Weekly Plan' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Weekly Plan']
    prot = ws.protection

    # Component 1: Sheet protection is enabled (0.35 points)
    # Initial: sheet=False, Golden: sheet=True
    try:
        if prot.sheet is True:
            print(f"PASS: Component 1 — Sheet protection is enabled (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Sheet protection not enabled (sheet={prot.sheet})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Password is set (0.30 points)
    # Initial: password=None, Golden: password is a non-empty hash string
    # We check that a password hash exists (non-None, non-empty).
    # openpyxl stores legacy hash in .password attribute.
    try:
        pwd = prot.password
        if pwd is not None and str(pwd).strip() != '':
            print(f"PASS: Component 2 — Password is set (hash present) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — No password set (password={pwd})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: formatCells is allowed (0.20 points)
    # When protection is on, formatCells=False means formatting cells IS allowed.
    # Initial: formatCells=True (default, blocked), Golden: formatCells=False (allowed)
    # This check only awards points if protection is also enabled (otherwise meaningless).
    try:
        if prot.sheet is True and prot.formatCells is False:
            print(f"PASS: Component 3 — formatCells is allowed (formatCells={prot.formatCells}) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — formatCells not properly set (sheet={prot.sheet}, formatCells={prot.formatCells})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: formatColumns is allowed (0.15 points)
    # When protection is on, formatColumns=False means formatting columns IS allowed.
    # Initial: formatColumns=True (default, blocked), Golden: formatColumns=False (allowed)
    # This check only awards points if protection is also enabled.
    try:
        if prot.sheet is True and prot.formatColumns is False:
            print(f"PASS: Component 4 — formatColumns is allowed (formatColumns={prot.formatColumns}) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 — formatColumns not properly set (sheet={prot.sheet}, formatColumns={prot.formatColumns})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist any unsaved GUI state
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
