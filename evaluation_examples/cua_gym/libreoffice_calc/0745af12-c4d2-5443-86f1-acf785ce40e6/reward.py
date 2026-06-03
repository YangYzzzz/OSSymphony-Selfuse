"""
Reward Script: Unmerge cells in column A, fill down category names, apply AutoFilter
Task ID: calc_tbl_022
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): No merged cells remain in column A
  Component 2 (0.4): Category names filled down correctly in all data rows
  Component 3 (0.3): AutoFilter applied to the header row
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'calc_tbl_022'

# Expected category fill-down mapping: row -> category name
EXPECTED_CATEGORIES = {
    2: 'Electronics',
    3: 'Electronics',
    4: 'Electronics',
    5: 'Electronics',
    6: 'Clothing',
    7: 'Clothing',
    8: 'Clothing',
    9: 'Clothing',
    10: 'Home & Garden',
    11: 'Home & Garden',
    12: 'Home & Garden',
    13: 'Home & Garden',
    14: 'Sports & Outdoors',
    15: 'Sports & Outdoors',
    16: 'Sports & Outdoors',
    17: 'Sports & Outdoors',
}


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
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import openpyxl
        from openpyxl.cell.cell import MergedCell
    except ImportError as e:
        print(f"CRITICAL: Cannot import openpyxl: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Component 1: No merged cells in column A (0.3 points)
    # Initial has 4 merged ranges in column A; golden has none.
    try:
        col_a_merges = []
        for mr in list(ws.merged_cells.ranges):
            # Check if merge range involves column A (column 1)
            if mr.min_col <= 1 <= mr.max_col:
                col_a_merges.append(str(mr))

        if len(col_a_merges) == 0:
            print(f"PASS: Component 1 — No merged cells in column A (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Found {len(col_a_merges)} merged ranges in column A: {col_a_merges}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Category names filled down correctly (0.4 points)
    # Each row in A2:A17 must have its correct category name.
    # Award partial credit proportional to correctly filled rows.
    try:
        correct_count = 0
        total_rows = len(EXPECTED_CATEGORIES)  # 16 data rows

        for row_num, expected_cat in EXPECTED_CATEGORIES.items():
            cell = ws.cell(row=row_num, column=1)
            actual_val = cell.value
            # Skip MergedCell objects (they have value=None) — those are NOT filled
            if isinstance(cell, MergedCell):
                print(f"  Row {row_num}: still a MergedCell (not filled)")
                continue
            if actual_val is not None and str(actual_val).strip() == expected_cat:
                correct_count += 1
            else:
                print(f"  Row {row_num}: expected '{expected_cat}', found {actual_val!r}")

        # Only the rows that were previously blank (in merged regions) matter.
        # Initial has 4 correct (top-left of each merge) and 12 blank/merged.
        # We only award points if ALL 16 rows are correct (meaning 12 were filled).
        # But for partial credit: score proportional, but subtract the 4 that are
        # already correct in initial (they are preconditions).
        # Initial correct = 4 (A2, A6, A10, A14 — the merge anchors).
        # So we need correct_count > 4 to show progress.
        # Points = 0.4 * (correct_count - 4) / 12, clamped to [0, 0.4]
        newly_filled = max(0, correct_count - 4)
        fill_score = 0.4 * (newly_filled / 12.0)
        if fill_score > 0:
            print(f"PASS: Component 2 — {correct_count}/16 rows correct ({newly_filled} newly filled) ({fill_score:.3f} pts)")
            total_score += fill_score
        else:
            print(f"FAIL: Component 2 — Only {correct_count}/16 rows correct, no new fills detected")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: AutoFilter applied to header row (0.3 points)
    # Initial has no auto_filter; golden has auto_filter on A1:F17.
    try:
        af_ref = ws.auto_filter.ref
        if af_ref is not None and af_ref != '':
            # Verify it covers at least the header row and column A
            print(f"PASS: Component 3 — AutoFilter set to '{af_ref}' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — AutoFilter not set (ref={af_ref!r})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
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
