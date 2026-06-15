"""
Reward Script: Row grouping and collapsing in LibreOffice Calc
Task ID: calc_gsi_052
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Rows 10-25 have outline_level >= 1 (grouped)
  Component 2 (0.5): Rows 10-25 are hidden (group collapsed)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_052'


def persist_app_state(domain: str):
    """Save any unsaved LibreOffice changes before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(1.0)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that rows 10-25 are grouped (outline_level >= 1) and collapsed (hidden).
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

    ws = wb.active

    # Component 1: Rows 10-25 are grouped (outline_level >= 1) — 0.5 points
    # This checks that the user applied Data > Group on rows 10-25.
    # In the initial file, these rows have no outline_level set (default 0).
    try:
        grouped_count = 0
        target_rows = list(range(10, 26))  # rows 10 through 25 inclusive
        for r in target_rows:
            rd = ws.row_dimensions.get(r)
            if rd and rd.outline_level and rd.outline_level >= 1:
                grouped_count += 1

        ratio = grouped_count / len(target_rows)
        if ratio >= 0.9:
            # At least 90% of target rows are grouped — full credit
            print(f"PASS: Component 1 — {grouped_count}/{len(target_rows)} rows grouped (outline_level >= 1) (0.5 pts)")
            total_score += 0.5
        elif ratio >= 0.5:
            # Partial grouping — partial credit
            partial = round(0.5 * ratio, 2)
            print(f"PARTIAL: Component 1 — {grouped_count}/{len(target_rows)} rows grouped ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — Only {grouped_count}/{len(target_rows)} rows have outline_level >= 1")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rows 10-25 are hidden (group is collapsed) — 0.5 points
    # This checks that the group was collapsed (minus button clicked).
    # In the initial file, rows are not hidden.
    try:
        hidden_count = 0
        for r in target_rows:
            rd = ws.row_dimensions.get(r)
            if rd and rd.hidden:
                hidden_count += 1

        ratio = hidden_count / len(target_rows)
        if ratio >= 0.9:
            print(f"PASS: Component 2 — {hidden_count}/{len(target_rows)} rows hidden (collapsed) (0.5 pts)")
            total_score += 0.5
        elif ratio >= 0.5:
            partial = round(0.5 * ratio, 2)
            print(f"PARTIAL: Component 2 — {hidden_count}/{len(target_rows)} rows hidden ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Only {hidden_count}/{len(target_rows)} rows are hidden (expected all 16)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

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
