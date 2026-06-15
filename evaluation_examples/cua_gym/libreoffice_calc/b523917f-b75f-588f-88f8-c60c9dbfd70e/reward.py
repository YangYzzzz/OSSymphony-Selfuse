"""
Reward Script: Configure print settings for Inventory sheet
Task ID: calc_gg3_015
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): Rows 1-2 set as repeating print title rows
  Component 2 (0.3): Page orientation set to landscape
  Component 3 (0.3): Centered header with 'Inventory Report — Confidential'
"""

import os

import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gg3_015'


def persist_app_state(domain: str):
    """Attempt to save any unsaved edits in LibreOffice."""
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
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check that 'Inventory' sheet exists (precondition gate)
    if 'Inventory' not in wb.sheetnames:
        print("CRITICAL: 'Inventory' sheet not found in workbook")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Inventory']

    # Component 1: Rows 1-2 set as repeating print title rows (0.4 points)
    # Task requires rows 1 and 2 to repeat at the top of every printed page.
    # openpyxl stores this as print_title_rows, e.g. '$1:$2'
    try:
        title_rows = ws.print_title_rows
        if title_rows is not None:
            # Normalize and check: should cover rows 1 through 2
            # Expected: '$1:$2' or '1:2'
            cleaned = title_rows.replace('$', '').strip()
            if cleaned == '1:2':
                print(f"PASS: Component 1 — print_title_rows is '{title_rows}' (rows 1-2 repeat) (0.4 pts)")
                total_score += 0.4
            else:
                print(f"FAIL: Component 1 — print_title_rows is '{title_rows}', expected '$1:$2'")
        else:
            print("FAIL: Component 1 — print_title_rows is None (no repeating rows set)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page orientation set to landscape (0.3 points)
    # Task requires landscape orientation for the page style.
    try:
        orientation = ws.page_setup.orientation
        if orientation is not None and orientation.lower() == 'landscape':
            print(f"PASS: Component 2 — orientation is '{orientation}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — orientation is '{orientation}', expected 'landscape'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Centered header with 'Inventory Report — Confidential' (0.3 points)
    # Task requires a center header section showing this exact text.
    try:
        hf = ws.oddHeader
        center_text = None
        if hf and hf.center:
            center_text = hf.center.text

        if center_text is not None:
            # Check for the expected text (allow minor whitespace variation)
            expected = 'Inventory Report — Confidential'
            if center_text.strip() == expected:
                print(f"PASS: Component 3 — center header is '{center_text}' (0.3 pts)")
                total_score += 0.3
            else:
                # Also check with regular dash in case em-dash was substituted
                alt_expected = 'Inventory Report - Confidential'
                if center_text.strip() == alt_expected:
                    print(f"PASS: Component 3 — center header is '{center_text}' (dash variant accepted) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — center header is '{center_text}', expected '{expected}'")
        else:
            print("FAIL: Component 3 — no center header text found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved GUI state before verification
persist_app_state("libreoffice_calc")

# Run verification
file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
