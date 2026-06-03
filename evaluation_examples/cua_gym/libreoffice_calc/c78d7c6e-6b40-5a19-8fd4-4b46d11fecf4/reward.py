"""
Reward Script: Export sales.xlsx to CSV, compute mean revenue, save to result.txt
Task ID: osworld_multi_apps_calc_vscode_001
Domain: multi_apps (libreoffice_calc + vscode + os)

Scoring Rubric:
  Component 1: sales.csv exists on Desktop with correct header and 12 data rows (0.35 pts)
  Component 2: result.txt exists on Desktop containing correct mean revenue (0.40 pts)
  Component 3: A Python script exists that reads sales.csv, computes mean treating blanks
               as zero, and writes result to result.txt (0.25 pts)
  Total: 1.0
"""

import os
import csv

DESKTOP = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_calc_vscode_001'

# Expected ground-truth values derived from task analysis:
# 12 quarters, 2 blank cells (Q4 2023, Q3 2024) treated as 0
# Sum of all 12 entries (blanks=0): 1,702,323.5
# Mean = 1,702,323.5 / 12 = 141860.29166666666
EXPECTED_MEAN = 141860.29166666666
MEAN_TOLERANCE = 0.01  # allow small floating-point rounding differences
EXPECTED_ROW_COUNT = 12  # 12 data rows after header
EXPECTED_HEADER = ['Quarter', 'Revenue']


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # -------------------------------------------------------------------------
    # Component 1: sales.csv exists with correct structure and data (0.35 pts)
    # The agent must have exported sales.xlsx to sales.csv with matching data.
    # This FAILS on initial_env (no sales.csv) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    csv_path = os.path.join(DESKTOP, 'sales.csv')
    csv_ok = False
    try:
        if not os.path.isfile(csv_path):
            print(f"FAIL: Component 1 — sales.csv not found at {csv_path}")
        else:
            with open(csv_path, newline='', encoding='utf-8') as f:
                reader = csv.reader(f)
                rows = list(reader)

            if len(rows) == 0:
                print(f"FAIL: Component 1 — sales.csv is empty")
            else:
                # Check header
                header = [h.strip() for h in rows[0]]
                if len(header) < 2 or header[0].strip().lower() != 'quarter' or header[1].strip().lower() != 'revenue':
                    print(f"FAIL: Component 1 — unexpected header: {rows[0]}, expected: {EXPECTED_HEADER}")
                else:
                    data_rows = rows[1:]  # exclude header
                    if len(data_rows) != EXPECTED_ROW_COUNT:
                        print(f"FAIL: Component 1 — expected {EXPECTED_ROW_COUNT} data rows, found {len(data_rows)}")
                    else:
                        # Verify at least first and last quarter labels match expectations
                        first_quarter = data_rows[0][0].strip()
                        last_quarter = data_rows[-1][0].strip()
                        if 'Q1' in first_quarter and '2023' in first_quarter and \
                           'Q4' in last_quarter and '2025' in last_quarter:
                            total_score += 0.35
                            print(f"PASS: Component 1 — sales.csv found with correct header and {len(data_rows)} data rows "
                                  f"(first: '{first_quarter}', last: '{last_quarter}') (0.35 pts)")
                        else:
                            print(f"FAIL: Component 1 — quarter labels mismatch: "
                                  f"first='{first_quarter}', last='{last_quarter}'")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: result.txt exists with the correct mean revenue value (0.40 pts)
    # The agent must have computed mean(revenues, blank=0) and saved to result.txt.
    # This FAILS on initial_env (no result.txt) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    result_path = os.path.join(DESKTOP, 'result.txt')
    try:
        if not os.path.isfile(result_path):
            print(f"FAIL: Component 2 — result.txt not found at {result_path}")
        else:
            with open(result_path, 'r', encoding='utf-8') as f:
                content = f.read().strip()

            if not content:
                print(f"FAIL: Component 2 — result.txt is empty")
            else:
                try:
                    actual_mean = float(content)
                    if abs(actual_mean - EXPECTED_MEAN) <= MEAN_TOLERANCE:
                        print(f"PASS: Component 2 — result.txt contains correct mean revenue "
                              f"{actual_mean} (expected {EXPECTED_MEAN}, tolerance {MEAN_TOLERANCE}) (0.40 pts)")
                        total_score += 0.40
                    else:
                        print(f"FAIL: Component 2 — result.txt has mean={actual_mean}, "
                              f"expected {EXPECTED_MEAN} (diff={abs(actual_mean - EXPECTED_MEAN):.6f})")
                except ValueError:
                    print(f"FAIL: Component 2 — result.txt content is not a number: '{content}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: A Python script exists that reads sales.csv, computes mean
    # treating blank cells as zero, and writes to result.txt (0.25 pts)
    # The agent should have written this script in VSCode.
    # This FAILS on initial_env (no .py file) and PASSES on golden_env.
    # -------------------------------------------------------------------------
    try:
        # Search for any Python script on the Desktop that performs the computation
        py_files = [f for f in os.listdir(DESKTOP) if f.endswith('.py')]
        if not py_files:
            print(f"FAIL: Component 3 — no Python script found on Desktop")
        else:
            # Check that at least one .py file references: csv reading, blank handling, mean, result.txt
            matching_script = None
            for py_file in py_files:
                py_path = os.path.join(DESKTOP, py_file)
                with open(py_path, 'r', encoding='utf-8') as f:
                    py_code = f.read()
                py_lower = py_code.lower()
                # Must read sales.csv (or csv), compute some mean/average, write to result.txt
                reads_csv = 'sales.csv' in py_code or ('csv' in py_lower and 'reader' in py_lower)
                handles_blanks = (
                    "== ''" in py_code or '== ""' in py_code or
                    'blank' in py_lower or 'strip' in py_lower or
                    'replace' in py_lower or 'fillna' in py_lower or
                    'nan' in py_lower
                )
                computes_mean = (
                    'mean' in py_lower or 'sum' in py_lower or 'average' in py_lower or
                    'len(' in py_code
                )
                writes_result = 'result.txt' in py_code
                if reads_csv and computes_mean and writes_result:
                    blank_note = " (with blank handling)" if handles_blanks else " (blank handling not confirmed)"
                    matching_script = (py_file, blank_note)
                    break
            if matching_script is not None:
                py_file, blank_note = matching_script
                total_score += 0.25
                print(f"PASS: Component 3 — Python script '{py_file}' found: "
                      f"reads CSV, computes mean, writes result.txt{blank_note} (0.25 pts)")
            else:
                found_scripts = ', '.join(py_files)
                print(f"FAIL: Component 3 — Python scripts found ({found_scripts}) but none satisfy "
                      f"all requirements (read sales.csv + compute mean + write result.txt)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
