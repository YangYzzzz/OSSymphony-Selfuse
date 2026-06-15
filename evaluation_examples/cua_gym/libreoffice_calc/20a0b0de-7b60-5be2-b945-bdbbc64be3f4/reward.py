"""
Reward Script: Insert 'Pivot Analysis' sheet, move 'Raw' before it, green tab color
Task ID: calc_ggf_021
Domain: libreoffice_calc
Scoring:
  C1 (0.30): 'Pivot Analysis' sheet exists
  C2 (0.40): Sheet order is Dashboard, Summary, Charts, Raw, Pivot Analysis
  C3 (0.30): 'Pivot Analysis' tab color is green
  Precondition gate: All 4 original sheets must still be present
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_ggf_021'


def persist_app_state(domain: str):
    """Best-effort save of any open LibreOffice document."""
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
    import openpyxl

    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    sheet_names = wb.sheetnames

    # Precondition gate: All 4 original sheets must still be present
    original_sheets = ['Dashboard', 'Summary', 'Raw', 'Charts']
    missing = [s for s in original_sheets if s not in sheet_names]
    if missing:
        print(f"PRECONDITION FAIL: Missing original sheets: {missing}. Returning 0.0.")
        print("REWARD: 0.0")
        return 0.0
    print(f"PRECONDITION OK: All original sheets present: {original_sheets}")

    # Component 1: 'Pivot Analysis' sheet exists (0.30 points)
    try:
        if 'Pivot Analysis' in sheet_names:
            print(f"PASS: Component 1 — 'Pivot Analysis' sheet exists (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — 'Pivot Analysis' sheet not found. Sheets: {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Sheet order is exactly [Dashboard, Summary, Charts, Raw, Pivot Analysis] (0.40 points)
    try:
        expected_order = ['Dashboard', 'Summary', 'Charts', 'Raw', 'Pivot Analysis']
        if sheet_names == expected_order:
            print(f"PASS: Component 2 — Sheet order is correct: {sheet_names} (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 2 — Expected order {expected_order}, found {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Pivot Analysis' tab color is green (0.30 points)
    # Green in the golden file is FF00B050. We accept any green-ish color where
    # the green channel dominates (G > R and G > B).
    try:
        if 'Pivot Analysis' in sheet_names:
            ws_pivot = wb['Pivot Analysis']
            tab_color = ws_pivot.sheet_properties.tabColor
            if tab_color is not None:
                rgb_str = tab_color.rgb  # 8-char ARGB e.g. FF00B050
                if rgb_str and len(rgb_str) == 8:
                    r = int(rgb_str[2:4], 16)
                    g = int(rgb_str[4:6], 16)
                    b = int(rgb_str[6:8], 16)
                    if g > r and g > b and g >= 128:
                        print(f"PASS: Component 3 — 'Pivot Analysis' tab color is green (RGB: {rgb_str}) (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 3 — Tab color {rgb_str} is not green (R={r}, G={g}, B={b})")
                else:
                    print(f"FAIL: Component 3 — Tab color RGB unexpected format: {rgb_str}")
            else:
                print(f"FAIL: Component 3 — 'Pivot Analysis' has no tab color set")
        else:
            print(f"FAIL: Component 3 — 'Pivot Analysis' sheet not found, cannot check tab color")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
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
