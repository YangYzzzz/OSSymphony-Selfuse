"""
Reward Script: Add page header with 'Acme Corp' on left and current date on right
Task ID: calc_gsi_024
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Left header contains 'Acme Corp'
  Component 2 (0.5): Right header contains date field code '&D'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_024'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print("PERSIST: ctrl+s sent for", domain)
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that the active sheet's page header has:
      - Left section: 'Acme Corp'
      - Right section: current date field code '&D'
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

    # The task says "current sheet" — the active sheet is 'Q3 Financial Summary'
    ws = wb.active
    print(f"INFO: Active sheet: '{ws.title}'")

    # Get header/footer object
    hf = ws.HeaderFooter
    oh = hf.oddHeader

    # Component 1: Left header contains 'Acme Corp' (0.5 points)
    try:
        left_text = oh.left.text if oh and oh.left else None
        if left_text and 'Acme Corp' in left_text:
            print(f"PASS: Component 1 — Left header contains 'Acme Corp' (found: '{left_text}') (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Expected 'Acme Corp' in left header, found: {repr(left_text)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Right header contains date field '&D' (0.5 points)
    # In xlsx page headers, '&D' is the date placeholder code
    try:
        right_text = oh.right.text if oh and oh.right else None
        if right_text and '&D' in right_text:
            print(f"PASS: Component 2 — Right header contains date field '&D' (found: '{right_text}') (0.5 pts)")
            total_score += 0.5
        else:
            # Also accept other date patterns: explicit date strings like '2024-01-15',
            # or alternative date codes like '&[Date]'
            if right_text and ('&[Date]' in right_text):
                print(f"PASS: Component 2 — Right header contains date field (found: '{right_text}') (0.5 pts)")
                total_score += 0.5
            else:
                print(f"FAIL: Component 2 — Expected date field '&D' in right header, found: {repr(right_text)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state("libreoffice_calc")
    verify_task(file_path)
