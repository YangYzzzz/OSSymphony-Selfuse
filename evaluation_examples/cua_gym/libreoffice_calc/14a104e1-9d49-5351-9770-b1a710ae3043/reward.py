"""
Reward Script: Configure print scaling to fit 2 pages wide x 1 page tall
Task ID: calc_mcp_081
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): fitToPage enabled in sheet properties
  Component 2 (0.4): fitToWidth == 2
  Component 3 (0.3): fitToHeight == 1
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_mcp_081'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: 'Ledger' sheet must exist
    if 'Ledger' not in wb.sheetnames:
        print("CRITICAL: 'Ledger' sheet not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['Ledger']

    # Component 1: fitToPage enabled in sheet properties (0.3 points)
    # This must be True for fit-to-page scaling to take effect.
    try:
        sp = ws.sheet_properties
        fit_to_page = False
        if sp.pageSetUpPr is not None:
            fit_to_page = sp.pageSetUpPr.fitToPage is True
        if fit_to_page:
            print(f"PASS: Component 1 — fitToPage is True (0.3 pts)")
            total_score += 0.3
        else:
            val = sp.pageSetUpPr.fitToPage if sp.pageSetUpPr else None
            print(f"FAIL: Component 1 — fitToPage expected True, found {val}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: fitToWidth == 2 (0.4 points)
    # The task says "2 pages wide", so fitToWidth must be 2.
    try:
        ps = ws.page_setup
        fit_w = ps.fitToWidth
        if fit_w is not None and int(fit_w) == 2:
            print(f"PASS: Component 2 — fitToWidth is {fit_w} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — fitToWidth expected 2, found {fit_w}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: fitToHeight == 1 AND fitToPage enabled (0.3 points)
    # fitToHeight=1 alone is a default; it only matters when fitToPage is active.
    # This compound check ensures the full scaling config is in effect.
    try:
        ps = ws.page_setup
        sp = ws.sheet_properties
        fit_h = ps.fitToHeight
        ftp = sp.pageSetUpPr is not None and sp.pageSetUpPr.fitToPage is True
        if fit_h is not None and int(fit_h) == 1 and ftp:
            print(f"PASS: Component 3 — fitToHeight is {fit_h} with fitToPage active (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — fitToHeight={fit_h}, fitToPage={ftp}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {final_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_calc")

file_path = f'{WORKDIR}/{TASK_ID}.xlsx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
