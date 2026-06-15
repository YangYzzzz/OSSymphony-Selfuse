"""
Reward Script: Read PDF inventory data, add Current Stock and Reorder Needed columns,
               filter items below reorder threshold into a new 'Reorder List' sheet.
Task ID: pdf_cross_045
Domain: libreoffice_calc (cross-domain: PDF + ODS)

Scoring Rubric:
  Component 1: 'Current Stock' column added to main 'Reorder Levels' sheet     (0.25 pts)
  Component 2: 'Reorder Needed' column with correct TRUE/FALSE values           (0.30 pts)
  Component 3: 'Reorder List' sheet exists with 12 items needing reorder        (0.25 pts)
  Component 4: Reorder List contains the correct 12 item codes                  (0.20 pts)
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user/Documents'
TASK_FILE = 'reorder_levels.ods'
FILE_PATH = os.path.join(WORKDIR, TASK_FILE)

# Expected 12 items that need reordering (current stock < reorder level)
EXPECTED_REORDER_ITEMS = {
    'ITM-001', 'ITM-003', 'ITM-005', 'ITM-007', 'ITM-009',
    'ITM-011', 'ITM-014', 'ITM-016', 'ITM-018', 'ITM-020',
    'ITM-024', 'ITM-027'
}
EXPECTED_REORDER_COUNT = 12


def get_sheet_data(doc, sheet):
    """Extract all rows from an ODF sheet as a list of lists of strings."""
    from odf.table import TableRow, TableCell
    from odf.text import P

    rows_data = []
    rows = sheet.getElementsByType(TableRow)
    for row in rows:
        cells = row.getElementsByType(TableCell)
        cell_vals = []
        for cell in cells:
            val = ''
            paragraphs = cell.getElementsByType(P)
            if paragraphs:
                for p in paragraphs:
                    val += str(p)
            cell_vals.append(val.strip())
        rows_data.append(cell_vals)
    return rows_data


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        from odf.opendocument import load
        from odf.table import Table
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get all sheets
    try:
        sheets = doc.spreadsheet.getElementsByType(Table)
        sheet_names = [s.getAttribute('name') for s in sheets]
        print(f"INFO: Found {len(sheets)} sheet(s): {sheet_names}")
    except Exception as e:
        print(f"CRITICAL: Cannot read sheets: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the main sheet 'Reorder Levels'
    main_sheet = None
    for s in sheets:
        if s.getAttribute('name') == 'Reorder Levels':
            main_sheet = s
            break
    if main_sheet is None:
        print("FAIL: 'Reorder Levels' sheet not found (precondition)")
        print("REWARD: 0.0")
        return 0.0

    main_rows = get_sheet_data(doc, main_sheet)
    if not main_rows:
        print("FAIL: 'Reorder Levels' sheet is empty")
        print("REWARD: 0.0")
        return 0.0

    header = [h.strip() for h in main_rows[0]]
    print(f"INFO: Main sheet header: {header}")
    print(f"INFO: Main sheet has {len(main_rows)} rows (including header)")

    # ----------------------------------------------------------------
    # Component 1: 'Current Stock' column added (0.25 points)
    # This FAILS on initial (only 3 columns) and PASSES on golden (5 columns)
    # ----------------------------------------------------------------
    try:
        # Check 'Current Stock' column exists in header
        current_stock_idx = None
        for i, h in enumerate(header):
            if 'current' in h.lower() and 'stock' in h.lower():
                current_stock_idx = i
                break

        if current_stock_idx is not None:
            # Verify it has actual data in data rows (not empty)
            non_empty_count = 0
            for row in main_rows[1:]:
                if current_stock_idx < len(row) and row[current_stock_idx] != '':
                    non_empty_count += 1

            if non_empty_count >= 25:  # At least 25 of 30 rows have stock data
                print(f"PASS: Component 1 — 'Current Stock' column found at index {current_stock_idx} "
                      f"with data in {non_empty_count} rows (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 1 — 'Current Stock' column exists but only {non_empty_count}/30 "
                      f"rows have data (expected >=25)")
        else:
            print(f"FAIL: Component 1 — No 'Current Stock' column found in header: {header}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: 'Reorder Needed' column with correct TRUE/FALSE (0.30 points)
    # This FAILS on initial (no such column) and PASSES on golden
    # ----------------------------------------------------------------
    try:
        reorder_needed_idx = None
        for i, h in enumerate(header):
            if 'reorder' in h.lower() and 'needed' in h.lower():
                reorder_needed_idx = i
                break

        if reorder_needed_idx is None:
            print(f"FAIL: Component 2 — No 'Reorder Needed' column found in header: {header}")
        else:
            # Verify at least some TRUE and FALSE values exist
            true_count = 0
            false_count = 0
            valid_count = 0

            for row in main_rows[1:]:
                if reorder_needed_idx < len(row):
                    val = row[reorder_needed_idx].strip().upper()
                    if val == 'TRUE':
                        true_count += 1
                        valid_count += 1
                    elif val == 'FALSE':
                        false_count += 1
                        valid_count += 1

            print(f"INFO: Reorder Needed values — TRUE: {true_count}, FALSE: {false_count}, valid: {valid_count}")

            # Ground truth: exactly 12 TRUE and 18 FALSE for 30 items
            if true_count == EXPECTED_REORDER_COUNT and false_count == (30 - EXPECTED_REORDER_COUNT):
                print(f"PASS: Component 2 — 'Reorder Needed' column has correct values: "
                      f"{true_count} TRUE, {false_count} FALSE (0.30 pts)")
                total_score += 0.30
            elif valid_count >= 25:
                # Partial: column exists with many values but count may be slightly off
                print(f"FAIL: Component 2 — 'Reorder Needed' column exists but counts are wrong: "
                      f"{true_count} TRUE (expected {EXPECTED_REORDER_COUNT}), "
                      f"{false_count} FALSE (expected {30 - EXPECTED_REORDER_COUNT})")
            else:
                print(f"FAIL: Component 2 — 'Reorder Needed' column found but mostly empty "
                      f"(only {valid_count} valid values)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: 'Reorder List' sheet with exactly 12 data rows (0.25 points)
    # This FAILS on initial (no such sheet) and PASSES on golden
    # ----------------------------------------------------------------
    try:
        reorder_list_sheet = None
        for s in sheets:
            if s.getAttribute('name') == 'Reorder List':
                reorder_list_sheet = s
                break

        if reorder_list_sheet is None:
            print("FAIL: Component 3 — 'Reorder List' sheet not found")
        else:
            reorder_rows = get_sheet_data(doc, reorder_list_sheet)
            # Count data rows (exclude header)
            data_rows = [r for r in reorder_rows if any(c != '' for c in r)]
            # Remove header row
            data_row_count = len(data_rows) - 1 if len(data_rows) > 0 else 0

            print(f"INFO: 'Reorder List' sheet has {data_row_count} data rows "
                  f"(excluding header), expected {EXPECTED_REORDER_COUNT}")

            if data_row_count == EXPECTED_REORDER_COUNT:
                print(f"PASS: Component 3 — 'Reorder List' sheet exists with {data_row_count} "
                      f"items (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — 'Reorder List' sheet has {data_row_count} rows, "
                      f"expected {EXPECTED_REORDER_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: Reorder List contains exactly the correct 12 items (0.20 points)
    # This FAILS on initial (no Reorder List sheet) and PASSES on golden
    # ----------------------------------------------------------------
    try:
        if reorder_list_sheet is None:
            print("FAIL: Component 4 — 'Reorder List' sheet not found, cannot check item codes")
        else:
            reorder_rows = get_sheet_data(doc, reorder_list_sheet)
            if not reorder_rows:
                print("FAIL: Component 4 — 'Reorder List' sheet is empty")
            else:
                # Find item code column (first column = Item Code based on golden)
                rl_header = [h.strip() for h in reorder_rows[0]] if reorder_rows else []
                item_code_idx = 0  # Default: first column
                for i, h in enumerate(rl_header):
                    if 'item' in h.lower() and 'code' in h.lower():
                        item_code_idx = i
                        break

                # Collect item codes from data rows (skip header)
                found_codes = set()
                for row in reorder_rows[1:]:
                    if item_code_idx < len(row) and row[item_code_idx].strip() != '':
                        found_codes.add(row[item_code_idx].strip())

                print(f"INFO: Found item codes in Reorder List: {sorted(found_codes)}")
                print(f"INFO: Expected item codes: {sorted(EXPECTED_REORDER_ITEMS)}")

                missing = EXPECTED_REORDER_ITEMS - found_codes
                extra = found_codes - EXPECTED_REORDER_ITEMS

                if found_codes == EXPECTED_REORDER_ITEMS:
                    print(f"PASS: Component 4 — Reorder List contains exactly the correct "
                          f"{len(found_codes)} items (0.20 pts)")
                    total_score += 0.20
                else:
                    if missing:
                        print(f"FAIL: Component 4 — Missing items: {sorted(missing)}")
                    if extra:
                        print(f"FAIL: Component 4 — Extra items: {sorted(extra)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
