"""
Reward Script: Convert PDF table to CSV
Task ID: pdf_cf_045
Domain: pdf (libreoffice_calc)
Scoring:
  Component 1: CSV file exists and is parseable (0.15)
  Component 2: Correct row count (21 lines: 1 header + 20 data) (0.20)
  Component 3: Correct column count (5 columns) (0.15)
  Component 4: Header row matches expected columns (0.20)
  Component 5: Data content accuracy - spot-check specific rows (0.30)
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'pdf_cf_045'

CSV_PATH = os.path.join(WORKDIR, 'Documents', 'spreadsheet_export.csv')

EXPECTED_HEADERS = ['Region', 'Product', 'Units Sold', 'Revenue', 'Margin %']

# Known data rows from the PDF (all 20 rows for thorough verification)
EXPECTED_DATA = [
    ['Northeast', 'Widget A', '1245', '62250.00', '18.5'],
    ['Northeast', 'Widget B', '873', '52380.00', '22.1'],
    ['Southeast', 'Widget A', '1102', '55100.00', '17.8'],
    ['Southeast', 'Widget C', '654', '45780.00', '25.3'],
    ['Midwest', 'Widget A', '987', '49350.00', '19.2'],
    ['Midwest', 'Widget B', '1320', '79200.00', '21.7'],
    ['Midwest', 'Widget D', '445', '35600.00', '28.4'],
    ['West Coast', 'Widget A', '1578', '78900.00', '16.9'],
    ['West Coast', 'Widget B', '1034', '62040.00', '20.5'],
    ['West Coast', 'Widget C', '762', '53340.00', '24.8'],
    ['Southwest', 'Widget D', '523', '41840.00', '27.6'],
    ['Southwest', 'Widget A', '891', '44550.00', '18.1'],
    ['Northwest', 'Widget B', '1156', '69360.00', '22.9'],
    ['Northwest', 'Widget C', '698', '48860.00', '26.1'],
    ['Central', 'Widget A', '1045', '52250.00', '17.4'],
    ['Central', 'Widget D', '387', '30960.00', '29.8'],
    ['Northeast', 'Widget D', '612', '48960.00', '26.7'],
    ['Southeast', 'Widget B', '945', '56700.00', '21.3'],
    ['West Coast', 'Widget D', '489', '39120.00', '28.0'],
    ['Midwest', 'Widget C', '718', '50260.00', '25.0'],
]


def normalize_cell(val):
    """Normalize a cell value for comparison: strip whitespace, handle numeric variants."""
    if val is None:
        return ''
    val = str(val).strip()
    # Try to normalize numeric values (e.g., "62250" vs "62250.00")
    try:
        f = float(val)
        # If it's an integer value, compare as int string too
        return val
    except ValueError:
        return val


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: CSV file exists and is parseable (0.15 points)
    try:
        if not os.path.exists(CSV_PATH):
            print(f"FAIL: Component 1 — CSV file not found at {CSV_PATH}")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        with open(CSV_PATH, 'r', newline='') as f:
            reader = csv.reader(f)
            rows = list(reader)

        # Filter out completely empty rows
        rows = [r for r in rows if any(cell.strip() for cell in r)]

        if len(rows) < 2:
            print(f"FAIL: Component 1 — CSV has fewer than 2 rows (found {len(rows)}), not a valid table")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        print(f"PASS: Component 1 — CSV file exists and is parseable with {len(rows)} rows (0.15 pts)")
        total_score += 0.15
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Correct row count — 21 total (1 header + 20 data) (0.20 points)
    try:
        if len(rows) == 21:
            print(f"PASS: Component 2 — Row count is 21 (1 header + 20 data) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected 21 rows, found {len(rows)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Correct column count — 5 columns (0.15 points)
    try:
        header = rows[0]
        num_cols = len(header)
        if num_cols == 5:
            print(f"PASS: Component 3 — Column count is 5 (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 — Expected 5 columns, found {num_cols}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Header row matches expected columns (0.20 points)
    try:
        header_stripped = [h.strip() for h in rows[0]]
        if header_stripped == EXPECTED_HEADERS:
            print(f"PASS: Component 4 — Header matches exactly: {header_stripped} (0.20 pts)")
            total_score += 0.20
        else:
            # Try case-insensitive match
            if [h.lower() for h in header_stripped] == [h.lower() for h in EXPECTED_HEADERS]:
                print(f"PARTIAL: Component 4 — Header matches case-insensitively (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 4 — Expected headers {EXPECTED_HEADERS}, found {header_stripped}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Data content accuracy (0.30 points)
    # Check all 20 data rows; each correct row contributes proportionally
    try:
        data_rows = rows[1:]  # skip header
        if len(data_rows) == 0:
            print(f"FAIL: Component 5 — No data rows found")
        else:
            matched_rows = 0
            total_expected = len(EXPECTED_DATA)

            for i, expected_row in enumerate(EXPECTED_DATA):
                if i >= len(data_rows):
                    break
                actual_row = [normalize_cell(c) for c in data_rows[i]]
                expected_norm = [normalize_cell(c) for c in expected_row]

                # Compare each cell with some tolerance for numeric values
                row_match = True
                for j, (actual, expected) in enumerate(zip(actual_row, expected_norm)):
                    if actual == expected:
                        continue
                    # Try numeric comparison
                    try:
                        if abs(float(actual) - float(expected)) < 0.01:
                            continue
                    except (ValueError, TypeError):
                        pass
                    row_match = False
                    break

                if row_match and len(actual_row) == len(expected_row):
                    matched_rows += 1

            fraction = matched_rows / total_expected
            data_score = round(0.30 * fraction, 4)
            if matched_rows == total_expected:
                print(f"PASS: Component 5 — All {total_expected} data rows match ({data_score} pts)")
            else:
                print(f"PARTIAL: Component 5 — {matched_rows}/{total_expected} data rows match ({data_score} pts)")
            total_score += data_score
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
