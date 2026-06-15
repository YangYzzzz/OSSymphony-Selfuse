"""
Reward Script: Group rows 5-12 to create a collapsible section for Q1 detail rows
Task ID: calc_gfl_053
Domain: libreoffice_calc
Scoring:
  Component 1 (0.5): Rows 5-12 all have outline_level >= 1
  Component 2 (0.3): Only rows 5-12 are grouped (no other rows have outline_level > 0)
  Component 3 (0.2): Sheet 'P&L' exists and data integrity (rows not hidden)
"""

import os
import openpyxl

WORKDIR = '/home/user'
TASK_ID = 'calc_gfl_053'


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
    """
    total_score = 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: Sheet 'P&L' must exist
    if 'P&L' not in wb.sheetnames:
        print("FAIL: Sheet 'P&L' not found")
        print("REWARD: 0.0")
        return 0.0

    ws = wb['P&L']

    # Component 1: All rows 5-12 have outline_level >= 1 (0.5 points)
    try:
        grouped_rows = []
        ungrouped_rows = []
        for r in range(5, 13):
            rd = ws.row_dimensions.get(r)
            if rd and rd.outline_level >= 1:
                grouped_rows.append(r)
            else:
                ungrouped_rows.append(r)

        if len(grouped_rows) == 8:
            print(f"PASS: Component 1 — All rows 5-12 are grouped (outline_level >= 1) (0.5 pts)")
            total_score += 0.5
        elif len(grouped_rows) > 0:
            # Partial credit: proportional to how many target rows are grouped
            partial = 0.5 * (len(grouped_rows) / 8)
            print(f"PARTIAL: Component 1 — {len(grouped_rows)}/8 target rows grouped: {grouped_rows}, missing: {ungrouped_rows} ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No rows 5-12 are grouped. ungrouped: {ungrouped_rows}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Rows 5-12 are grouped AND no other rows have outline_level > 0 (0.3 points)
    # Both conditions must be true — this ensures initial_env (no grouping) scores 0.
    try:
        extra_grouped = []
        for r in range(1, 100):
            if 5 <= r <= 12:
                continue  # skip target rows
            rd = ws.row_dimensions.get(r)
            if rd and rd.outline_level > 0:
                extra_grouped.append(r)

        if len(grouped_rows) == 8 and len(extra_grouped) == 0:
            print(f"PASS: Component 2 — All 8 target rows grouped AND no extra rows grouped (0.3 pts)")
            total_score += 0.3
        elif len(grouped_rows) < 8:
            print(f"FAIL: Component 2 — Not all target rows grouped ({len(grouped_rows)}/8)")
        else:
            print(f"FAIL: Component 2 — Extra rows grouped outside 5-12: {extra_grouped}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Grouped rows 5-12 are NOT hidden (they should be visible/expanded) (0.2 points)
    # This verifies the group is in expanded state (rows visible), which is the expected default
    # after grouping. This check differentiates from initial state because it's combined with
    # outline_level check — we verify rows are grouped AND visible.
    try:
        any_target_grouped = any(
            ws.row_dimensions.get(r) and ws.row_dimensions[r].outline_level >= 1
            for r in range(5, 13)
        )
        all_visible = True
        for r in range(5, 13):
            rd = ws.row_dimensions.get(r)
            if rd and rd.hidden:
                all_visible = False
                break

        if any_target_grouped and all_visible:
            print(f"PASS: Component 3 — Grouped rows 5-12 are visible (expanded state) (0.2 pts)")
            total_score += 0.2
        elif not any_target_grouped:
            print(f"FAIL: Component 3 — No target rows are grouped, cannot award visibility points")
        else:
            print(f"FAIL: Component 3 — Some grouped rows are hidden (collapsed state)")
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
