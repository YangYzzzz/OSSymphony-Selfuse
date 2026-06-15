"""
Reward Script: Extract table data from PDF pages 3-4 and save as CSV
Task ID: pdf_gf2_038
Domain: pdf
Scoring:
  - Component 1 (0.25): CSV row count = 16 (1 header + 15 data rows)
  - Component 2 (0.25): CSV has 5 columns with correct header names
  - Component 3 (0.25): Department names (column 1) match expected values
  - Component 4 (0.25): Revenue values in spot-checked cells match expected
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf2_038'

# Expected ground truth from task context
EXPECTED_HEADERS = ['Department', 'Q1 Revenue ($)', 'Q2 Revenue ($)', 'Q3 Revenue ($)', 'Q4 Revenue ($)']

EXPECTED_DEPARTMENTS = [
    'Engineering', 'Marketing', 'Sales', 'Human Resources', 'Finance',
    'Operations', 'Research & Dev', 'Customer Support', 'Legal',
    'IT Infrastructure', 'Product Design', 'Quality Assurance',
    'Supply Chain', 'Business Dev', 'Data Analytics'
]

# Spot-check values: (row_index_0based_in_data, col_index, expected_value)
SPOT_CHECKS = [
    (0, 1, '245,800'),   # Engineering Q1
    (2, 3, '589,100'),   # Sales Q3
    (5, 2, '328,400'),   # Operations Q2
    (8, 4, '83,100'),    # Legal Q4
    (11, 1, '89,300'),   # Quality Assurance Q1
    (14, 3, '150,100'),  # Data Analytics Q3
]


def verify_task(csv_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: CSV file must exist (gate, not scored)
    if not os.path.exists(csv_path):
        print(f"CRITICAL: CSV file not found at {csv_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot read CSV file {csv_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if len(rows) == 0:
        print("CRITICAL: CSV file is empty")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Row count = 16 (1 header + 15 data rows) (0.25 points)
    try:
        row_count = len(rows)
        if row_count == 16:
            print(f"PASS: Component 1 — Row count is 16 (1 header + 15 data) (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Row count is {row_count}, expected 16")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 5 columns with correct header names (0.25 points)
    try:
        header = rows[0]
        col_count = len(header)
        # Normalize headers for comparison (strip whitespace)
        header_stripped = [h.strip() for h in header]

        if col_count == 5:
            # Check header names match by counting mismatches
            header_mismatches = 0
            for i, expected_h in enumerate(EXPECTED_HEADERS):
                if i < len(header_stripped):
                    if header_stripped[i] != expected_h:
                        header_mismatches += 1
                        print(f"  Header mismatch at col {i}: got '{header_stripped[i]}', expected '{expected_h}'")
                else:
                    header_mismatches += 1

            if header_mismatches == 0:
                print(f"PASS: Component 2 — 5 columns with correct headers (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — 5 columns but {header_mismatches} header name(s) don't match")
        else:
            print(f"FAIL: Component 2 — Column count is {col_count}, expected 5. Headers: {header_stripped[:6]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Department names match (0.25 points)
    try:
        if len(rows) < 2:
            print("FAIL: Component 3 — No data rows to check departments")
        else:
            data_rows = rows[1:]  # skip header
            matched = 0
            total_depts = len(EXPECTED_DEPARTMENTS)

            for i, expected_dept in enumerate(EXPECTED_DEPARTMENTS):
                if i < len(data_rows):
                    actual_dept = data_rows[i][0].strip() if data_rows[i] else ''
                    if actual_dept == expected_dept:
                        matched += 1
                    else:
                        print(f"  Dept mismatch row {i+1}: got '{actual_dept}', expected '{expected_dept}'")

            ratio = matched / total_depts if total_depts > 0 else 0
            if ratio == 1.0:
                print(f"PASS: Component 3 — All 15 department names match (0.25 pts)")
                total_score += 0.25
            elif ratio >= 0.8:
                partial = round(0.25 * ratio, 3)
                print(f"PARTIAL: Component 3 — {matched}/{total_depts} departments match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — Only {matched}/{total_depts} departments match")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Revenue values spot-check (0.25 points)
    try:
        if len(rows) < 2:
            print("FAIL: Component 4 — No data rows to check values")
        else:
            data_rows = rows[1:]
            passed_checks = 0
            total_checks = len(SPOT_CHECKS)

            for row_idx, col_idx, expected_val in SPOT_CHECKS:
                if row_idx < len(data_rows) and col_idx < len(data_rows[row_idx]):
                    actual_val = data_rows[row_idx][col_idx].strip().strip('"')
                    if actual_val == expected_val:
                        passed_checks += 1
                    else:
                        print(f"  Value mismatch at data row {row_idx}, col {col_idx}: got '{actual_val}', expected '{expected_val}'")
                else:
                    print(f"  Cannot access data row {row_idx}, col {col_idx} (rows={len(data_rows)})")

            ratio = passed_checks / total_checks if total_checks > 0 else 0
            if ratio == 1.0:
                print(f"PASS: Component 4 — All {total_checks} spot-check values match (0.25 pts)")
                total_score += 0.25
            elif ratio >= 0.5:
                partial = round(0.25 * ratio, 3)
                print(f"PARTIAL: Component 4 — {passed_checks}/{total_checks} values match ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Only {passed_checks}/{total_checks} values match")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
csv_path = f'{WORKDIR}/Documents/report_tables.csv'
if not os.path.exists(csv_path):
    print(f"File not found: {csv_path}")
    print("REWARD: 0.0")
else:
    verify_task(csv_path)
