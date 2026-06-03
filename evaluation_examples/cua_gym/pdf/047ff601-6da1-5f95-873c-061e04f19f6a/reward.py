"""
Reward Script: Extract table from page 3 of financial_data.pdf and save as CSV
Task ID: pdf_mbc_071
Domain: pdf
Scoring:
  Component 1 (0.25): CSV file exists at expected path
  Component 2 (0.25): CSV header row matches expected columns
  Component 3 (0.30): CSV has 4 data rows with correct quarter labels Q1-Q4
  Component 4 (0.20): CSV data values match expected financial figures
"""

import os
import csv
import io

WORKDIR = '/home/user'
TASK_ID = 'pdf_mbc_071'
CSV_PATH = os.path.join(WORKDIR, 'Documents', 'table_page3.csv')

# Expected data extracted from the PDF table on page 3
EXPECTED_HEADERS = ['Quarter', 'Revenue', 'Expenses', 'Profit']
EXPECTED_ROWS = [
    ['Q1', '$780,000', '$540,000', '$240,000'],
    ['Q2', '$820,000', '$575,000', '$245,000'],
    ['Q3', '$790,000', '$560,000', '$230,000'],
    ['Q4', '$860,000', '$590,000', '$270,000'],
]


def normalize_cell(val):
    """Normalize a cell value for comparison: strip whitespace, quotes."""
    if val is None:
        return ''
    return str(val).strip().strip('"').strip("'").strip()


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: CSV file exists at ~/Documents/table_page3.csv (0.25 points)
    # This is the primary task output — it does NOT exist in initial_env.
    try:
        if os.path.isfile(CSV_PATH):
            print(f"PASS: Component 1 — CSV file exists at {CSV_PATH} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — CSV file not found at {CSV_PATH}")
            # No file means nothing else to check
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Read and parse the CSV file
    try:
        with open(CSV_PATH, 'r', newline='', encoding='utf-8') as f:
            content = f.read()
        # Parse CSV
        reader = csv.reader(io.StringIO(content))
        rows = list(reader)
        # Filter out empty rows
        rows = [r for r in rows if any(cell.strip() for cell in r)]
        print(f"INFO: CSV has {len(rows)} non-empty rows")
    except Exception as e:
        print(f"ERROR: Could not read/parse CSV file: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: Header row matches expected columns (0.25 points)
    try:
        if len(rows) >= 1:
            actual_headers = [normalize_cell(h) for h in rows[0]]
            if actual_headers == EXPECTED_HEADERS:
                print(f"PASS: Component 2 — Header row matches: {actual_headers} (0.25 pts)")
                total_score += 0.25
            else:
                # Try case-insensitive match
                if [h.lower() for h in actual_headers] == [h.lower() for h in EXPECTED_HEADERS]:
                    print(f"PASS: Component 2 — Header row matches (case-insensitive): {actual_headers} (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 2 — Expected headers {EXPECTED_HEADERS}, found {actual_headers}")
        else:
            print(f"FAIL: Component 2 — CSV file is empty (no rows)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: CSV has 4 data rows with correct quarter labels Q1-Q4 (0.30 points)
    try:
        data_rows = rows[1:] if len(rows) > 1 else []
        if len(data_rows) >= 4:
            actual_quarters = [normalize_cell(r[0]) for r in data_rows[:4]]
            expected_quarters = ['Q1', 'Q2', 'Q3', 'Q4']
            if actual_quarters == expected_quarters:
                print(f"PASS: Component 3 — 4 data rows with quarters {actual_quarters} (0.30 pts)")
                total_score += 0.30
            else:
                print(f"FAIL: Component 3 — Expected quarters {expected_quarters}, found {actual_quarters}")
        else:
            print(f"FAIL: Component 3 — Expected 4 data rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data values match expected financial figures (0.20 points)
    try:
        data_rows = rows[1:] if len(rows) > 1 else []
        if len(data_rows) >= 4:
            matches = 0
            total_cells = 0
            for row_idx in range(4):
                actual_row = [normalize_cell(c) for c in data_rows[row_idx]]
                expected_row = EXPECTED_ROWS[row_idx]
                # Compare each cell (skip Quarter column, already checked)
                for col_idx in range(1, min(len(actual_row), len(expected_row))):
                    total_cells += 1
                    actual_val = actual_row[col_idx]
                    expected_val = expected_row[col_idx]
                    # Normalize: remove $ and , for numeric comparison
                    actual_num = actual_val.replace('$', '').replace(',', '').strip()
                    expected_num = expected_val.replace('$', '').replace(',', '').strip()
                    if actual_num == expected_num:
                        matches += 1
                    else:
                        print(f"  MISMATCH: Row {row_idx+1}, Col {col_idx}: "
                              f"expected '{expected_val}', found '{actual_val}'")

            if total_cells > 0 and matches == total_cells:
                print(f"PASS: Component 4 — All {total_cells} data values match (0.20 pts)")
                total_score += 0.20
            elif total_cells > 0:
                # Partial credit proportional to matching cells
                partial = 0.20 * (matches / total_cells)
                print(f"PARTIAL: Component 4 — {matches}/{total_cells} values match ({partial:.2f} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — No data cells to compare")
        else:
            print(f"FAIL: Component 4 — Not enough data rows ({len(data_rows)})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
