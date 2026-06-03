"""
Reward Script: Export temperatures.xlsx to CSV, write Python script that fills blanks
with column median and writes overall median to median_temp.txt.
Task ID: osworld_multi_apps_calc_vscode_004
Domain: libreoffice_calc + vscode (multi-app)
Scoring:
  Component 1 (0.30): temperatures.csv exists on Desktop with correct structure
                       (Date+Temperature columns, 20 data rows, blank entries preserved)
  Component 2 (0.20): A Python script (.py) exists on Desktop implementing median-fill
                       logic that loads CSV, fills blanks, computes median, writes output
  Component 3 (0.50): median_temp.txt exists on Desktop with the correct median value (21.25)
"""

import os
import csv

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_calc_vscode_004'

# Expected values derived from task data (verified from xlsx inspection)
EXPECTED_MEDIAN = 21.25
MEDIAN_TOLERANCE = 0.01

# Expected CSV structure from temperatures.xlsx
EXPECTED_TOTAL_ROWS = 20
EXPECTED_BLANK_ROWS = 4
EXPECTED_COLUMNS = {'Date', 'Temperature'}


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # ------------------------------------------------------------
    # Component 1: temperatures.csv exists with correct structure (0.30 points)
    # The agent must export temperatures.xlsx to temperatures.csv on the Desktop.
    # The CSV should have Date and Temperature columns, 20 data rows, and
    # preserve blank temperature entries (4 blank temperature cells in source).
    # This FAILS on initial_env (no csv exists) → PASSES on golden_env ✅
    # ------------------------------------------------------------
    csv_path = os.path.join(DESKTOP, 'temperatures.csv')
    try:
        if not os.path.exists(csv_path):
            print("FAIL: Component 1 — temperatures.csv not found on Desktop")
        else:
            with open(csv_path, newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                fieldnames = reader.fieldnames or []

            actual_cols = set(fieldnames)
            has_correct_cols = EXPECTED_COLUMNS.issubset(actual_cols)
            has_correct_rows = len(rows) == EXPECTED_TOTAL_ROWS
            blank_count = sum(1 for r in rows if r.get('Temperature', '').strip() == '')
            has_correct_blanks = blank_count == EXPECTED_BLANK_ROWS

            if has_correct_cols and has_correct_rows and has_correct_blanks:
                print(f"PASS: Component 1 — temperatures.csv: {len(rows)} rows, cols={list(actual_cols)}, {blank_count} blanks (0.30 pts)")
                total_score += 0.30
            elif has_correct_cols and has_correct_rows:
                print(f"PASS: Component 1 (partial) — temperatures.csv: {len(rows)} rows, {blank_count}/{EXPECTED_BLANK_ROWS} blank entries (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 — temperatures.csv: cols_ok={has_correct_cols}, rows_ok={has_correct_rows} ({len(rows)} rows), blanks_ok={has_correct_blanks}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ------------------------------------------------------------
    # Component 2: A Python script exists implementing median-fill logic (0.20 points)
    # The agent must write a .py file (in VSCode) on the Desktop that:
    #   - Loads temperatures.csv
    #   - Fills blank temperature entries with the column median
    #   - Computes overall median after filling
    #   - Writes result to median_temp.txt
    # This FAILS on initial_env (no .py script on Desktop) → PASSES on golden_env ✅
    # ------------------------------------------------------------
    try:
        py_files = [f for f in os.listdir(DESKTOP) if f.endswith('.py')]
        if not py_files:
            print("FAIL: Component 2 — no .py script found on Desktop")
        else:
            script_score = 0.0
            best_info = ""
            for py_file in py_files:
                py_path = os.path.join(DESKTOP, py_file)
                try:
                    with open(py_path, 'r') as f:
                        code = f.read()
                    checks = {
                        'loads_csv': ('temperatures.csv' in code
                                      or ('csv' in code.lower() and 'open' in code)),
                        'uses_median': 'median' in code.lower(),
                        'writes_output': ('median_temp.txt' in code
                                          or ('median_temp' in code and 'write' in code.lower())),
                        'handles_blanks': (
                            'fill' in code.lower() or 'blank' in code.lower()
                            or 'nan' in code.lower() or '.strip()' in code
                            or 'replace' in code or '""' in code or "''" in code
                        ),
                    }
                    passed = sum(checks.values())
                    candidate = (passed / 4) * 0.20
                    if candidate > script_score:
                        script_score = candidate
                        best_info = f"{py_file}: {passed}/4 checks passed {checks}"
                        if passed == 4:
                            break
                except Exception as inner_e:
                    print(f"  WARN: Could not read {py_file}: {inner_e}")

            if script_score >= 0.20:
                print(f"PASS: Component 2 — Python script with all required elements: {best_info} (0.20 pts)")
                total_score += 0.20
            elif script_score > 0:
                print(f"PASS: Component 2 (partial) — {best_info} ({script_score:.2f} pts)")
                total_score += script_score
            else:
                print(f"FAIL: Component 2 — no qualifying Python script found. Best: {best_info}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ------------------------------------------------------------
    # Component 3: median_temp.txt contains the correct median value (0.50 points)
    # After running the script, median_temp.txt must contain 21.25 (the overall
    # median after filling 4 blank rows with the column median 21.25).
    # This FAILS on initial_env (no median_temp.txt) → PASSES on golden_env ✅
    # ------------------------------------------------------------
    median_path = os.path.join(DESKTOP, 'median_temp.txt')
    try:
        if not os.path.exists(median_path):
            print("FAIL: Component 3 — median_temp.txt not found on Desktop")
        else:
            with open(median_path, 'r') as f:
                content = f.read().strip()
            if not content:
                print("FAIL: Component 3 — median_temp.txt is empty")
            else:
                try:
                    actual_median = float(content)
                    if abs(actual_median - EXPECTED_MEDIAN) <= MEDIAN_TOLERANCE:
                        print(f"PASS: Component 3 — median_temp.txt = {actual_median} (expected {EXPECTED_MEDIAN}) (0.50 pts)")
                        total_score += 0.50
                    else:
                        print(f"FAIL: Component 3 — median_temp.txt = {actual_median}, expected {EXPECTED_MEDIAN} (tolerance ±{MEDIAN_TOLERANCE})")
                except ValueError:
                    print(f"FAIL: Component 3 — median_temp.txt not a valid number: '{content}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
