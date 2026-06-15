"""
Reward Script: Split the current view horizontally at row 20
Task ID: calc_gsi_019
Domain: libreoffice_calc
Scoring:
  Component 1 (0.35): Pane exists with state='split' (horizontal split is active)
  Component 2 (0.35): ySplit value corresponds to ~row 20 (between rows 15-25 range)
  Component 3 (0.30): topLeftCell of bottom pane starts at row 21 (A21)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_019'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
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
    Verify that the spreadsheet has a horizontal split at approximately row 20.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Precondition: sheet view must exist
    sv = ws.sheet_view
    pane = sv.pane

    if pane is None:
        print("FAIL: No pane/split defined on the active sheet")
        print("\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Pane state is 'split' (not 'frozen' or 'frozenSplit') (0.35 points)
    try:
        pane_state = pane.state
        if pane_state == 'split':
            print(f"PASS: Component 1 — Pane state is 'split' (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — Expected pane state 'split', found '{pane_state}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ySplit is set and corresponds to approximately row 20 (0.35 points)
    # In OOXML, ySplit for split (not freeze) is in twips (1/20 of a point).
    # Default row height is 15 points = 300 twips. So 20 rows ~ 6000 twips.
    # We accept a range: 3000-9000 twips (~10-30 rows at default height)
    # to accommodate slight variations in row heights.
    # Also xSplit should be None or 0 (horizontal split only, not vertical).
    try:
        y_split = pane.ySplit
        x_split = pane.xSplit

        is_horizontal_only = (x_split is None or x_split == 0 or x_split == 0.0)
        # Check ySplit is in a reasonable range around row 20
        # 6000 twips = 20 rows at default 300 twips/row
        # Allow 3000-9000 (roughly rows 10-30)
        if y_split is not None and 3000 <= float(y_split) <= 9000 and is_horizontal_only:
            print(f"PASS: Component 2 — ySplit={y_split} (horizontal split near row 20), xSplit={x_split} (0.35 pts)")
            total_score += 0.35
        elif y_split is not None and float(y_split) > 0 and is_horizontal_only:
            # Partial credit: it's a horizontal split but not near row 20
            print(f"PARTIAL: Component 2 — ySplit={y_split} exists but outside expected range 3000-9000 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — ySplit={y_split}, xSplit={x_split}; expected horizontal split near row 20")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: topLeftCell of bottom pane is A21 (row 21 = just below the split at row 20) (0.30 points)
    try:
        top_left = pane.topLeftCell
        if top_left is not None:
            # Extract row number from cell reference like 'A21'
            import re
            match = re.match(r'[A-Z]+(\d+)', str(top_left))
            if match:
                row_num = int(match.group(1))
                if row_num == 21:
                    print(f"PASS: Component 3 — topLeftCell={top_left}, bottom pane starts at row 21 (0.30 pts)")
                    total_score += 0.30
                elif 16 <= row_num <= 26:
                    # Close but not exact
                    print(f"PARTIAL: Component 3 — topLeftCell={top_left}, row {row_num} is close to expected 21 (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — topLeftCell={top_left}, row {row_num} far from expected 21")
            else:
                print(f"FAIL: Component 3 — Could not parse topLeftCell: {top_left}")
        else:
            print(f"FAIL: Component 3 — topLeftCell is None")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(round(total_score, 2), 1.0)
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
