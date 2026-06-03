"""
Reward Script: Process 3 PDF receipts and add to expense tracker with SUM formula
Task ID: osworld_multi_apps_doc_pdf_calc_004
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.5): 3 new receipt rows added (rows 7-9) with correct vendor/date/amount
  Component 2 (0.2): Row 10 Date column contains 'TOTAL' label
  Component 3 (0.3): Row 10 Amount column contains a SUM formula covering C2:C9
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_pdf_calc_004'

# ODS namespace map
ODS_NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'of':     'urn:oasis:names:tc:opendocument:xmlns:of:1.0',
}

# Expected receipt data from task context (ground truth)
EXPECTED_RECEIPTS = [
    {'date': '2025-03-01', 'vendor': 'Blue Bottle Coffee',     'amount': 12.50},
    {'date': '2025-03-02', 'vendor': 'Uber Technologies',      'amount': 28.75},
    {'date': '2025-03-03', 'vendor': 'The Sandwich Collective', 'amount': 18.90},
]


def parse_ods_rows(file_path):
    """
    Parse an ODS file and return a list of rows.
    Each row is a list of (value_type, value, formula, text) tuples.
    Returns None if the file cannot be parsed.
    """
    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            content = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content)
        tables = root.findall('.//table:table', ODS_NS)
        if not tables:
            return None
        # Use first table (the Expenses sheet)
        t = tables[0]
        rows_out = []
        for row_el in t.findall('table:table-row', ODS_NS):
            cells = row_el.findall('table:table-cell', ODS_NS)
            row_data = []
            for cell in cells:
                vt      = cell.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value-type')
                val     = cell.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value')
                formula = cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}formula', '')
                texts   = cell.findall('.//text:p', ODS_NS)
                text_val = ' '.join(t.text or '' for t in texts if t.text)
                # handle column-repeated empty cells
                repeat = cell.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated')
                row_data.append((vt, val, formula, text_val, repeat))
            rows_out.append(row_data)
        return rows_out
    except Exception as e:
        print(f"ERROR: Could not parse ODS file: {e}")
        return None


def get_cell_text(row_data, col_index):
    """
    Get the text value for a given 0-based column index in a parsed row.
    Non-repeated cells map directly. Repeated empty cells are collapsed.
    """
    # We walk the row data expanding repeated cells to find col_index
    current_col = 0
    for (vt, val, formula, text_val, repeat) in row_data:
        repeat_count = int(repeat) if repeat else 1
        if current_col + repeat_count > col_index:
            return (vt, val, formula, text_val)
        current_col += repeat_count
    return (None, None, '', '')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # --- Precondition: file must exist ---
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    rows = parse_ods_rows(file_path)
    if rows is None:
        print("CRITICAL: Could not parse ODS file.")
        print("REWARD: 0.0")
        return 0.0

    # We expect at least 10 rows (1 header + 5 existing + 3 new + 1 total)
    print(f"INFO: Parsed {len(rows)} rows from ODS file.")

    # -------------------------------------------------------------------------
    # Component 1: 3 receipt rows added with correct data (0.5 points)
    #   Row 7 → Blue Bottle Coffee  / 2025-03-01 / 12.50
    #   Row 8 → Uber Technologies   / 2025-03-02 / 28.75
    #   Row 9 → The Sandwich Collective / 2025-03-03 / 18.90
    #   Rows are 0-indexed as rows[6], rows[7], rows[8]
    # -------------------------------------------------------------------------
    try:
        receipt_rows_correct = 0

        for i, expected in enumerate(EXPECTED_RECEIPTS):
            row_idx = 6 + i   # 0-indexed; row 7 is index 6
            if row_idx >= len(rows):
                print(f"FAIL: Row {row_idx + 1} is missing from the file.")
                continue

            row = rows[row_idx]
            date_vt,   date_val,   date_formula,   date_text   = get_cell_text(row, 0)
            vendor_vt, vendor_val, vendor_formula, vendor_text = get_cell_text(row, 1)
            amt_vt,    amt_val,    amt_formula,    amt_text    = get_cell_text(row, 2)

            # Check date
            date_match = (date_text.strip() == expected['date'])
            # Check vendor (case-insensitive strip)
            vendor_match = (vendor_text.strip().lower() == expected['vendor'].lower())
            # Check amount (numeric tolerance 0.01)
            try:
                amount_found = float(amt_val) if amt_val else float(amt_text.replace(',', ''))
                amount_match = abs(amount_found - expected['amount']) <= 0.01
            except (ValueError, TypeError):
                amount_match = False

            if date_match and vendor_match and amount_match:
                print(f"PASS: Row {row_idx + 1} — {expected['vendor']} / {expected['date']} / {expected['amount']}")
                receipt_rows_correct += 1
            else:
                print(f"FAIL: Row {row_idx + 1} — expected {expected}, "
                      f"found date='{date_text}' vendor='{vendor_text}' amount='{amt_val}'")

        if receipt_rows_correct == 3:
            print(f"PASS: Component 1 — all 3 receipt rows present and correct (0.5 pts)")
            total_score += 0.5
        elif receipt_rows_correct > 0:
            partial = round(receipt_rows_correct / 3 * 0.5, 4)
            print(f"PARTIAL: Component 1 — {receipt_rows_correct}/3 receipt rows correct ({partial} pts)")
            total_score += partial
        else:
            print("FAIL: Component 1 — no receipt rows found or all incorrect (0.0 pts)")

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Row 10 Date column contains 'TOTAL' label (0.2 points)
    #   Row 10 is 0-indexed as rows[9]
    # -------------------------------------------------------------------------
    try:
        total_row_idx = 9  # 0-indexed for row 10
        if total_row_idx >= len(rows):
            print(f"FAIL: Component 2 — Row 10 is missing (only {len(rows)} rows found)")
        else:
            row_10 = rows[total_row_idx]
            date_vt, date_val, date_formula, date_text = get_cell_text(row_10, 0)
            if date_text.strip().upper() == 'TOTAL':
                print(f"PASS: Component 2 — Row 10 Date column contains 'TOTAL' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — Expected 'TOTAL' in Row 10 Date column, found: '{date_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Row 10 Amount column contains a SUM formula covering C2:C9 (0.3 points)
    #   Formula expected: =SUM(C2:C9) or equivalent ODS: of:=SUM([.C2:.C9])
    # -------------------------------------------------------------------------
    try:
        total_row_idx = 9  # 0-indexed for row 10
        if total_row_idx >= len(rows):
            print(f"FAIL: Component 3 — Row 10 is missing")
        else:
            row_10 = rows[total_row_idx]
            amt_vt, amt_val, amt_formula, amt_text = get_cell_text(row_10, 2)
            formula_str = amt_formula.upper().replace(' ', '')
            # Accept various valid ODS/formula representations of SUM(C2:C9)
            sum_patterns = [
                'OF:=SUM([.C2:.C9])',
                '=SUM(C2:C9)',
                'OF:=SUM(.C2:.C9)',
            ]
            # Also accept any formula containing 'SUM' referencing rows 2-9
            formula_ok = any(p in formula_str for p in sum_patterns) or (
                'SUM' in formula_str and 'C2' in formula_str and 'C9' in formula_str
            )

            if formula_ok:
                print(f"PASS: Component 3 — SUM formula covering C2:C9 found in Row 10 Amount: '{amt_formula}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 — Expected SUM(C2:C9) formula in Row 10 Amount, found: '{amt_formula}' (value='{amt_val}')")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/expense_log.ods'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
