"""
Reward Script: Convert PDF table data to CSV
Task ID: pdf_mbc_078
Domain: pdf (libreoffice_calc)
Scoring:
  Component 1 (0.20): CSV file exists and is parseable
  Component 2 (0.25): Correct header row
  Component 3 (0.25): Correct number of data rows (100)
  Component 4 (0.15): All rows have exactly 5 columns
  Component 5 (0.15): Data integrity - first/last row IDs and sample values
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_078'
CSV_PATH = os.path.join(WORKDIR, 'Documents', 'full_data.csv')

EXPECTED_HEADERS = ['ID', 'Name', 'Department', 'Salary', 'Start Date']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: CSV file not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Try to parse the CSV
    try:
        with open(file_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot parse CSV file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Filter out completely empty rows (common CSV artifact)
    rows = [r for r in rows if any(cell.strip() for cell in r)]

    if len(rows) < 2:
        print(f"CRITICAL: CSV has fewer than 2 rows ({len(rows)}), cannot verify")
        print("REWARD: 0.0")
        return 0.0

    header = rows[0]
    data_rows = rows[1:]

    # Component 1: CSV file exists and is parseable as valid CSV (0.20 points)
    # This fails on initial_env because the file does not exist (early return above)
    try:
        if len(rows) >= 2 and len(header) >= 3:
            print(f"PASS: Component 1 — CSV file exists and is parseable with {len(rows)} rows (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — CSV file has insufficient content: {len(rows)} rows, {len(header)} cols")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Correct header row (0.25 points)
    # Headers should be exactly: ID, Name, Department, Salary, Start Date
    try:
        # Normalize headers (strip whitespace)
        normalized_header = [h.strip() for h in header]
        if normalized_header == EXPECTED_HEADERS:
            print(f"PASS: Component 2 — Header matches exactly: {normalized_header} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Expected headers {EXPECTED_HEADERS}, found {normalized_header}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct number of data rows - should be 100 (0.25 points)
    # Task says 100 data rows (20 on page 1 + 20 each on pages 2-5 = 100 total)
    try:
        # Also check that headers don't appear as duplicate data rows
        duplicate_headers = sum(1 for r in data_rows if [c.strip() for c in r] == EXPECTED_HEADERS)
        effective_data_rows = len(data_rows) - duplicate_headers

        if effective_data_rows == 100:
            print(f"PASS: Component 3 — Exactly 100 data rows found (0.25 pts)")
            total_score += 0.25
        elif 90 <= effective_data_rows <= 110:
            # Partial credit for close row count
            if effective_data_rows != 100:
                partial = 0.15
                print(f"PARTIAL: Component 3 — {effective_data_rows} data rows (expected 100), awarding {partial} pts")
                total_score += partial
        else:
            print(f"FAIL: Component 3 — Expected 100 data rows, found {effective_data_rows} (duplicate headers removed: {duplicate_headers})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All rows have exactly 5 columns (proper comma separation) (0.15 points)
    try:
        correct_col_count = sum(1 for r in data_rows if len(r) == 5)
        total_data = len(data_rows)
        if total_data > 0 and correct_col_count == total_data:
            print(f"PASS: Component 4 — All {total_data} data rows have exactly 5 columns (0.15 pts)")
            total_score += 0.15
        elif total_data > 0 and correct_col_count / total_data >= 0.9:
            if correct_col_count < total_data:
                partial = 0.08
                print(f"PARTIAL: Component 4 — {correct_col_count}/{total_data} rows have 5 columns, awarding {partial} pts")
                total_score += partial
        else:
            print(f"FAIL: Component 4 — Only {correct_col_count}/{total_data} data rows have 5 columns")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Data integrity checks (0.15 points)
    # First row should have ID=1, last row ID=100
    # Also verify some known values from the golden state
    try:
        checks_passed = 0
        total_checks = 3

        # Check 1: First data row ID is 1
        first_id = data_rows[0][0].strip() if len(data_rows[0]) > 0 else ''
        if first_id == '1':
            checks_passed += 1
            print(f"  PASS: First row ID is '1'")
        else:
            print(f"  FAIL: First row ID expected '1', found '{first_id}'")

        # Check 2: Last data row ID is 100
        last_id = data_rows[-1][0].strip() if len(data_rows[-1]) > 0 else ''
        if last_id == '100':
            checks_passed += 1
            print(f"  PASS: Last row ID is '100'")
        else:
            print(f"  FAIL: Last row ID expected '100', found '{last_id}'")

        # Check 3: First row name is 'Sarah Chen' (from golden exploration)
        first_name = data_rows[0][1].strip() if len(data_rows[0]) > 1 else ''
        if first_name == 'Sarah Chen':
            checks_passed += 1
            print(f"  PASS: First row name is 'Sarah Chen'")
        else:
            print(f"  FAIL: First row name expected 'Sarah Chen', found '{first_name}'")

        if checks_passed == total_checks:
            print(f"PASS: Component 5 — All {total_checks} data integrity checks passed (0.15 pts)")
            total_score += 0.15
        elif checks_passed > 0:
            if checks_passed < total_checks:
                partial = round(0.15 * checks_passed / total_checks, 2)
                print(f"PARTIAL: Component 5 — {checks_passed}/{total_checks} integrity checks passed, awarding {partial} pts")
                total_score += partial
        else:
            print(f"FAIL: Component 5 — No data integrity checks passed")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(CSV_PATH):
    print(f"File not found: {CSV_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(CSV_PATH)
