"""
Reward Script: Convert spreadsheets to CSV and concatenate into combined.csv
Task ID: osworld_multi_apps_terminal_calc_001
Domain: os / libreoffice_calc (multi-app terminal task)
Scoring:
  - Component 1: combined.csv has correct row count (22 rows = 12 from data_a + 10 from data_b) — 0.4 pts
  - Component 2: All values in combined.csv are numeric (float-parseable, no header rows) — 0.3 pts
  - Component 3: Combined values match expected set from both source files — 0.3 pts
"""

import os
import csv

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_terminal_calc_001'
COMBINED_CSV_PATH = os.path.join(WORKDIR, 'combined.csv')

# Expected data from source files (verified from task setup):
# data_a.xlsx: 12 numeric values (rows 2-13, header in row 1)
# data_b.ods: 10 numeric values (rows 2-11, header in row 1)
EXPECTED_ROW_COUNT = 22  # 12 + 10

# Expected values from data_a.xlsx (excluding header)
EXPECTED_DATA_A_VALUES = {142.5, 238.0, 195.75, 307.25, 412.0, 289.5,
                          358.0, 475.25, 521.5, 399.75, 463.0, 512.25}
# Expected values from data_b.ods (excluding header)
EXPECTED_DATA_B_VALUES = {88.4, 117.6, 205.3, 156.8, 93.2, 178.5,
                          243.7, 132.45, 189.9, 211.15}
EXPECTED_ALL_VALUES = EXPECTED_DATA_A_VALUES | EXPECTED_DATA_B_VALUES


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: combined.csv must exist
    if not os.path.isfile(file_path):
        print(f"FAIL: combined.csv not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Read the CSV file
    try:
        with open(file_path, 'r', newline='') as f:
            content = f.read()
        lines = [line.strip() for line in content.strip().splitlines() if line.strip()]
    except Exception as e:
        print(f"CRITICAL: Cannot read file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Row count is exactly 22 (12 from data_a + 10 from data_b) — 0.4 points
    # This FAILS on initial_env (no combined.csv → already returned 0.0) and
    # PASSES on golden_env (combined.csv with 22 rows)
    try:
        row_count = len(lines)
        if row_count == EXPECTED_ROW_COUNT:
            print(f"PASS: Component 1 — combined.csv has {row_count} rows (expected {EXPECTED_ROW_COUNT}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected {EXPECTED_ROW_COUNT} rows, found {row_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All values are numeric (float-parseable, no header row) — 0.3 points
    # This verifies that the CSV was generated correctly without headers being carried over
    try:
        numeric_values = []
        non_numeric = []
        for line in lines:
            try:
                val = float(line)
                numeric_values.append(val)
            except ValueError:
                non_numeric.append(line)

        if len(non_numeric) == 0 and len(numeric_values) == len(lines):
            print(f"PASS: Component 2 — all {len(numeric_values)} values are numeric (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — found {len(non_numeric)} non-numeric values: {non_numeric[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The combined values match the expected set from both source files — 0.3 points
    # This verifies that values from BOTH data_a.xlsx and data_b.ods are present
    try:
        # Parse float values (component 2 may have already done this, but be safe)
        parsed_vals = []
        for line in lines:
            try:
                parsed_vals.append(float(line))
            except ValueError:
                pass

        parsed_set = set(parsed_vals)

        data_a_present = EXPECTED_DATA_A_VALUES.issubset(parsed_set)
        data_b_present = EXPECTED_DATA_B_VALUES.issubset(parsed_set)

        if data_a_present and data_b_present:
            print(f"PASS: Component 3 — values from both data_a.xlsx and data_b.ods are present (0.3 pts)")
            total_score += 0.3
        else:
            if not data_a_present:
                missing_a = EXPECTED_DATA_A_VALUES - parsed_set
                print(f"FAIL: Component 3 — missing values from data_a.xlsx: {missing_a}")
            if not data_b_present:
                missing_b = EXPECTED_DATA_B_VALUES - parsed_set
                print(f"FAIL: Component 3 — missing values from data_b.ods: {missing_b}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path on VM
if not os.path.exists(COMBINED_CSV_PATH):
    print(f"File not found: {COMBINED_CSV_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(COMBINED_CSV_PATH)
