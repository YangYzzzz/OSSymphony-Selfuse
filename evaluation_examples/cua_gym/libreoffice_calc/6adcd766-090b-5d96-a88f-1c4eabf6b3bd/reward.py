"""
FINAL REWARD SCRIPT - SUCCESS
Task: I've got two tables showing the monthly expenses for Department A and Department B. Please create two column bar charts displaying per-month total expenses for each department.
Generated: 2025-11-24 07:41:15
Status: success
Model: o3
Total Steps: 4
"""

import os
import openpyxl

"""
Reward Script: verify_expense_charts.py
--------------------------------------
This script verifies completion of the task:
"I've got two tables showing the monthly expenses for Department A and Department B. Please create two column bar charts displaying per-month total expenses for each department."

Scoring Breakdown (progressive – sums to 1.0):
• 0.30 – At least two charts exist
• 0.20 – Exactly two charts (no extras)
• 0.20 – Each chart is a *column* BarChart (0.10 per chart)
• 0.30 – Each chart’s data range matches the expected table ranges
            Dept A → categories A3:A14, values B3:B14
            Dept B → categories D3:D14, values E3:E14
            (0.15 per correct pairing)
The script loads the workbook, detects charts via openpyxl, inspects their types, and extracts category/value
cell ranges from the first series of each chart to validate correctness.
Returns a float between 0.0-1.0 and prints "REWARD: X.X".
"""

def clean_range(ref: str):
    """Normalise a cell reference (strip sheet name/quotes/$, upper-case)."""
    if not ref:
        return None
    ref = ref.split('!')[-1]           # after !
    return ref.replace("'", "").replace("$", "").upper()


def extract_series_ranges(chart):
    """Return (categories_range, values_range) from the chart’s first series."""
    if not chart.series:
        return None, None

    ser = chart.series[0]

    # Category reference
    cat_ref = None
    if hasattr(ser, 'cat') and ser.cat is not None:
        if getattr(ser.cat, 'strRef', None):
            cat_ref = ser.cat.strRef.f
        elif getattr(ser.cat, 'numRef', None):
            cat_ref = ser.cat.numRef.f

    # Value reference
    val_ref = None
    if hasattr(ser, 'val') and ser.val is not None:
        if getattr(ser.val, 'numRef', None):
            val_ref = ser.val.numRef.f
        elif getattr(ser.val, 'strRef', None):
            val_ref = ser.val.strRef.f

    return clean_range(cat_ref), clean_range(val_ref)


def verify_expense_charts(file_path: str) -> float:
    max_score = 1.0
    score = 0.0

    # --- Load workbook -----------------------------------------------------
    try:
        wb = openpyxl.load_workbook(file_path)
        print(f"Workbook '{file_path}' loaded.")
    except Exception as e:
        print(f"✗ Failed to load workbook: {e}")
        return 0.0

    # --- Collect all charts ------------------------------------------------
    charts = []  # list of (sheet_name, chart)
    for sh in wb.worksheets:
        local = []
        if getattr(sh, '_charts', []):
            local = sh._charts
        elif getattr(sh, 'charts', []):
            local = sh.charts
        for ch in local:
            charts.append((sh.title, ch))

    print(f"Total charts found: {len(charts)}")

    # --- Requirement 1: at least 2 charts (0.30) & exactly 2 (extra 0.20) --
    if len(charts) >= 2:
        score += 0.30
        print("✓ Found at least 2 charts (0.30)")
        if len(charts) == 2:
            score += 0.20
            print("✓ Found exactly 2 charts (0.20)")
        else:
            print("⚠️ More than two charts – no exact-count bonus")
    else:
        print("✗ Less than 2 charts – no points for chart presence")

    # --- Requirement 2: correct chart type (0.10 each) ---------------------
    type_points = 0.0
    for sheet, ch in charts[:2]:  # evaluate first two charts only
        if isinstance(ch, openpyxl.chart.BarChart) and getattr(ch, 'type', getattr(ch, 'barDir', None)) == 'col':
            type_points += 0.10
            print(f"✓ Chart on sheet '{sheet}' is a column BarChart (+0.10)")
        else:
            print(f"✗ Chart on sheet '{sheet}' is not a column BarChart")
    score += type_points

    # --- Requirement 3: correct data ranges (0.15 each) --------------------
    expected = {('A3:A14', 'B3:B14'), ('D3:D14', 'E3:E14')}
    data_points = 0.0
    matched = set()
    for sheet, ch in charts[:2]:
        cat, val = extract_series_ranges(ch)
        print(f"Chart ranges → Categories: {cat}, Values: {val}")
        if (cat, val) in expected and (cat, val) not in matched:
            matched.add((cat, val))
            data_points += 0.15
            print("✓ Data range matches expected table (+0.15)")
        else:
            print("✗ Data range does not match expected table")
    score += data_points

    # --- Final score -------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Total Score: {final_score} / {max_score}")
    return final_score


if __name__ == "__main__":
    default_path = "/home/user/ive_got_two_tables_showing_the_monthly_expenses_for_department_a_and_department_b_please_create_two_.xlsx"
    if not os.path.exists(default_path):
        print("✗ Expected workbook not found.")
        reward = 0.0
    else:
        reward = verify_expense_charts(default_path)
    print(f"REWARD: {reward}")
