"""
Reward Script: Protect workbook structure and windows with a password
Task ID: calc_gsi_042
Domain: libreoffice_calc
Scoring:
  Component 1 — lockStructure is True (0.35 pts)
  Component 2 — lockWindows is True (0.30 pts)
  Component 3 — workbookPassword is set (0.35 pts)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_042'


def persist_app_state(domain: str):
    """Attempt to save any unsaved GUI state via Ctrl+S."""
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
    Verify workbook-level protection with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sec = wb.security

    # Component 1: lockStructure is True (0.35 points)
    # This is the core protection that prevents adding/removing/renaming sheets.
    try:
        if sec is not None and sec.lockStructure is True:
            print(f"PASS: Component 1 — lockStructure is True (0.35 pts)")
            total_score += 0.35
        else:
            lock_val = sec.lockStructure if sec is not None else None
            print(f"FAIL: Component 1 — expected lockStructure=True, found: {lock_val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: lockWindows is True (0.30 points)
    # The task explicitly asks to protect windows as well.
    try:
        if sec is not None and sec.lockWindows is True:
            print(f"PASS: Component 2 — lockWindows is True (0.30 pts)")
            total_score += 0.30
        else:
            lock_val = sec.lockWindows if sec is not None else None
            print(f"FAIL: Component 2 — expected lockWindows=True, found: {lock_val}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: workbookPassword is set (0.35 points)
    # The task requires a password. We check that a non-empty hash is present.
    try:
        if sec is not None and sec.workbookPassword is not None and len(str(sec.workbookPassword)) > 0:
            print(f"PASS: Component 3 — workbookPassword is set (hash: {sec.workbookPassword}) (0.35 pts)")
            total_score += 0.35
        else:
            pw_val = sec.workbookPassword if sec is not None else None
            print(f"FAIL: Component 3 — expected workbookPassword to be set, found: {pw_val}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before verifying
persist_app_state("libreoffice_calc")

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
