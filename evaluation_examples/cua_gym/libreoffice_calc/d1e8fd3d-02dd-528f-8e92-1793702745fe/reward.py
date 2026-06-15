"""
Reward Script: Convert PDF spreadsheet to CSV
Task ID: pdf_gf1_045
Domain: libreoffice_calc (PDF extraction task)
Scoring:
  Component 1: CSV file exists and is readable as UTF-8 (0.15)
  Component 2: Header line matches expected columns exactly (0.25)
  Component 3: File has exactly 21 lines (1 header + 20 data rows) (0.25)
  Component 4: Every data row has exactly 5 comma-separated fields (0.20)
  Component 5: Data content integrity - spot check values from known rows (0.15)
"""

import os
import csv

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_gf1_045'
CSV_PATH = os.path.join(WORKDIR, 'spreadsheet_data.csv')

EXPECTED_HEADER = ['Date', 'Item', 'Quantity', 'Unit Price', 'Total']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Gate: file must exist — if not, nothing to verify
    if not os.path.exists(file_path):
        print(f"CRITICAL: CSV file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: CSV file exists and is readable as valid UTF-8 (0.15 points)
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        if len(content.strip()) > 0:
            print(f"PASS: Component 1 — CSV file exists and is valid UTF-8 ({len(content)} bytes) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — CSV file is empty")
    except UnicodeDecodeError as e:
        print(f"FAIL: Component 1 — File is not valid UTF-8: {e}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Read all lines for subsequent checks
    try:
        with open(file_path, 'r', encoding='utf-8', errors='strict') as f:
            lines = f.read().strip().split('\n')
    except Exception as e:
        print(f"ERROR: Could not read file for further checks: {e}")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Header line matches exactly (0.25 points)
    try:
        if len(lines) > 0:
            header_line = lines[0].strip()
            expected_header_line = ','.join(EXPECTED_HEADER)
            if header_line == expected_header_line:
                print(f"PASS: Component 2 — Header is '{header_line}' (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Expected header '{expected_header_line}', found '{header_line}'")
        else:
            print(f"FAIL: Component 2 — File has no lines")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File has exactly 21 lines (1 header + 20 data rows) (0.25 points)
    try:
        num_lines = len(lines)
        if num_lines == 21:
            print(f"PASS: Component 3 — File has exactly 21 lines (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 — Expected 21 lines, found {num_lines}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Every data row has exactly 5 comma-separated fields (0.20 points)
    try:
        if len(lines) > 1:
            data_lines = lines[1:]
            reader = csv.reader(data_lines)
            bad_rows = []
            for i, row in enumerate(reader, start=2):
                if len(row) != 5:
                    bad_rows.append((i, len(row)))
            if len(bad_rows) == 0 and len(data_lines) > 0:
                print(f"PASS: Component 4 — All {len(data_lines)} data rows have exactly 5 fields (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Rows with wrong field count: {bad_rows[:5]}")
        else:
            print(f"FAIL: Component 4 — No data rows found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Data content integrity - spot check specific known values (0.15 points)
    # Verify a few known data points that should be in the extracted table
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)

        checks_passed = 0
        total_checks = 3

        # Check row 2 (first data row): should be 2025-01-03,Wireless Mouse,12,24.99,299.88
        if len(rows) > 1:
            r = rows[1]
            if len(r) == 5 and 'Wireless Mouse' in r[1] and '12' in r[2]:
                checks_passed += 1
            else:
                print(f"  DETAIL: Row 2 mismatch: {r}")

        # Check a middle row (row 11, index 10): 2025-02-28,Ergonomic Chair Pad,6,55.00,330.00
        if len(rows) > 10:
            r = rows[10]
            if len(r) == 5 and 'Ergonomic' in r[1] and '6' in r[2]:
                checks_passed += 1
            else:
                print(f"  DETAIL: Row 11 mismatch: {r}")

        # Check last data row (row 21, index 20): 2025-04-30,Ethernet Patch Cable,35,4.50,157.50
        if len(rows) > 20:
            r = rows[20]
            if len(r) == 5 and 'Ethernet' in r[1] and '35' in r[2]:
                checks_passed += 1
            else:
                print(f"  DETAIL: Row 21 mismatch: {r}")

        if checks_passed == total_checks:
            print(f"PASS: Component 5 — All {total_checks} spot checks passed (0.15 pts)")
            total_score += 0.15
        elif checks_passed > 0:
            partial = round(0.15 * checks_passed / total_checks, 2)
            print(f"PARTIAL: Component 5 — {checks_passed}/{total_checks} spot checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — No spot checks passed (0/{total_checks})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(CSV_PATH):
    print(f"File not found: {CSV_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CSV_PATH)
