"""
Reward Script: Set all page margins to 1.5cm
Task ID: calc_gfl_049
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): Top margin == 1.5cm
  Component 2 (0.25): Bottom margin == 1.5cm
  Component 3 (0.25): Left margin == 1.5cm
  Component 4 (0.25): Right margin == 1.5cm
"""

import os
import math

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_049'

# 1.5 cm in inches (openpyxl stores margins in inches)
TARGET_MARGIN_INCHES = 1.5 / 2.54  # ~0.5905511811023622
TOLERANCE = 0.02  # ~0.5mm tolerance in inches


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for libreoffice_calc")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that all four page margins are set to 1.5cm.
    Returns: float between 0.0 and 1.0
    """
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Summary']
    pm = ws.page_margins

    # Component 1: Top margin == 1.5cm (0.25 points)
    try:
        top = pm.top
        if top is not None and math.isclose(top, TARGET_MARGIN_INCHES, abs_tol=TOLERANCE):
            print(f"PASS: Component 1 — Top margin is {top:.4f} in (~{top*2.54:.2f} cm) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Top margin is {top} in (~{top*2.54:.2f} cm), expected ~0.5906 in (1.5 cm)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Bottom margin == 1.5cm (0.25 points)
    try:
        bottom = pm.bottom
        if bottom is not None and math.isclose(bottom, TARGET_MARGIN_INCHES, abs_tol=TOLERANCE):
            print(f"PASS: Component 2 — Bottom margin is {bottom:.4f} in (~{bottom*2.54:.2f} cm) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Bottom margin is {bottom} in (~{bottom*2.54:.2f} cm), expected ~0.5906 in (1.5 cm)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Left margin == 1.5cm (0.25 points)
    try:
        left = pm.left
        if left is not None and math.isclose(left, TARGET_MARGIN_INCHES, abs_tol=TOLERANCE):
            print(f"PASS: Component 3 — Left margin is {left:.4f} in (~{left*2.54:.2f} cm) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Left margin is {left} in (~{left*2.54:.2f} cm), expected ~0.5906 in (1.5 cm)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Right margin == 1.5cm (0.25 points)
    try:
        right = pm.right
        if right is not None and math.isclose(right, TARGET_MARGIN_INCHES, abs_tol=TOLERANCE):
            print(f"PASS: Component 4 — Right margin is {right:.4f} in (~{right*2.54:.2f} cm) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 — Right margin is {right} in (~{right*2.54:.2f} cm), expected ~0.5906 in (1.5 cm)")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
