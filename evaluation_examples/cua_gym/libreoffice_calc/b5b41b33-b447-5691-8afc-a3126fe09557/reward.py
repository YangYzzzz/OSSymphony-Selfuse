"""
Reward Script: Process 4 PDF invoices and add them to accounts_payable.ods
Task ID: osworld_multi_apps_doc_pdf_calc_005
Domain: libreoffice_calc (ODS format)

Scoring Rubric:
  Component 1 (0.5): All 4 invoice rows added with correct Invoice_No, Vendor, Date, Amount
  Component 2 (0.3): All 4 new rows have Status = 'Pending'
  Component 3 (0.2): Running_Total column has cumulative SUM formulas in new rows
  Total: 1.0

Initial state: 4 rows (header + 3 pre-existing data rows)
Golden state: 8 rows (header + 3 pre-existing + 4 new invoice rows)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
FILE_PATH = '/home/user/Desktop/accounts_payable.ods'

# Expected new invoice rows extracted from PDF context (ground truth from task_config.json)
EXPECTED_INVOICES = [
    {'invoice_no': 'INV-2025-001', 'vendor': 'Adobe Systems',       'date': '2025-01-10', 'amount': 599.88},
    {'invoice_no': 'INV-2025-002', 'vendor': 'AWS',                 'date': '2025-01-15', 'amount': 234.56},
    {'invoice_no': 'INV-2025-003', 'vendor': 'Slack Technologies',   'date': '2025-01-20', 'amount': 87.50},
    {'invoice_no': 'INV-2025-004', 'vendor': 'Zoom Video',          'date': '2025-01-22', 'amount': 149.90},
]


def parse_ods_rows(filepath):
    """
    Parse ODS file and return list of data rows (excluding header row 0).
    Each row is a dict with keys: invoice_no, vendor, date, amount_str, status, running_total_str, formula
    Returns (header_row, data_rows, error_message)
    """
    NS = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    }
    TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'

    try:
        with zipfile.ZipFile(filepath) as z:
            content = z.read('content.xml').decode('utf-8')
    except Exception as e:
        return None, None, f"Cannot open ODS file: {e}"

    try:
        root = ET.fromstring(content)
        body = root.find('.//office:spreadsheet', NS)
        if body is None:
            return None, None, "No spreadsheet body found in ODS"

        tables = body.findall('table:table', NS)
        if not tables:
            return None, None, "No tables found in ODS"

        # Use first sheet
        t = tables[0]
        rows_raw = t.findall('table:table-row', NS)

        all_rows = []
        for row_el in rows_raw:
            cells = []
            for cell in row_el.findall('table:table-cell', NS):
                p_els = cell.findall('.//text:p', NS)
                val = ' '.join((p.text or '') for p in p_els).strip()
                formula = cell.get(f'{{{TABLE_NS}}}formula')
                num_repeated = cell.get(f'{{{TABLE_NS}}}number-columns-repeated')
                if num_repeated and int(num_repeated) > 5:
                    # Padding/empty cells, stop here
                    break
                cells.append({'value': val, 'formula': formula})
            if any(c['value'] for c in cells):
                all_rows.append(cells)

        return all_rows, None, None
    except Exception as e:
        return None, None, f"Error parsing ODS XML: {e}"


def parse_currency(s):
    """Parse '$1,234.56' or '234.56' to float. Returns None on failure."""
    if s is None:
        return None
    s = str(s).strip().replace('$', '').replace(',', '')
    try:
        return float(s)
    except (ValueError, TypeError):
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be parseable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    all_rows, _, err = parse_ods_rows(file_path)
    if err or all_rows is None:
        print(f"CRITICAL: Cannot parse ODS file: {err}")
        print("REWARD: 0.0")
        return 0.0

    # Row 0 is header; data rows start at index 1
    # Initial state has rows 1-3 (3 pre-existing data rows)
    # Golden state has rows 1-7 (3 pre-existing + 4 new invoice rows)
    # New invoice rows are at index 4-7 (0-indexed) = rows 4-7 in all_rows list
    data_rows = all_rows[1:]  # Skip header

    print(f"INFO: Total data rows found: {len(data_rows)}")

    # Component 1 (0.5 pts): All 4 invoice rows added with correct Invoice_No, Vendor, Date, Amount
    # Each verified invoice earns 0.125 pts (4 invoices * 0.125 = 0.5)
    try:
        # The 4 new invoice rows should be at positions 3,4,5,6 in data_rows (0-indexed)
        # i.e., after the 3 pre-existing rows
        new_rows = data_rows[3:7] if len(data_rows) >= 7 else data_rows[3:]

        invoice_matches = 0
        for expected in EXPECTED_INVOICES:
            # Search for this invoice in new_rows
            found = False
            for row in new_rows:
                # Need at least 6 cells: Invoice_No, Vendor, Date, Amount, Status, Running_Total
                if len(row) < 4:
                    continue
                row_invoice = row[0]['value']
                row_vendor = row[1]['value']
                row_date = row[2]['value']
                row_amount = parse_currency(row[3]['value'])

                # Check invoice number
                inv_match = row_invoice.strip().upper() == expected['invoice_no'].upper()
                # Check vendor (case-insensitive)
                vendor_match = row_vendor.strip().lower() == expected['vendor'].lower()
                # Check date (string comparison)
                date_match = row_date.strip() == expected['date']
                # Check amount (numeric with tolerance)
                amount_match = row_amount is not None and abs(row_amount - expected['amount']) < 0.02

                if inv_match and vendor_match and date_match and amount_match:
                    found = True
                    print(f"PASS: Invoice {expected['invoice_no']} - {expected['vendor']} found correctly")
                    break
                elif inv_match:
                    # Partial match on invoice number; check other fields
                    if not vendor_match:
                        print(f"FAIL: Invoice {expected['invoice_no']} vendor mismatch: expected '{expected['vendor']}', found '{row_vendor}'")
                    if not date_match:
                        print(f"FAIL: Invoice {expected['invoice_no']} date mismatch: expected '{expected['date']}', found '{row_date}'")
                    if not amount_match:
                        print(f"FAIL: Invoice {expected['invoice_no']} amount mismatch: expected {expected['amount']}, found {row_amount}")

            if found:
                invoice_matches += 1
            else:
                print(f"FAIL: Invoice {expected['invoice_no']} ({expected['vendor']}) NOT found in new rows")

        comp1_score = invoice_matches * 0.125
        if invoice_matches == 4:
            print(f"PASS: Component 1 — All 4 invoices added correctly ({comp1_score} pts)")
        else:
            print(f"PARTIAL: Component 1 — {invoice_matches}/4 invoices added correctly ({comp1_score} pts)")
        total_score += comp1_score

    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2 (0.3 pts): All 4 new rows have Status = 'Pending'
    # Each correct status earns 0.075 pts
    try:
        new_rows_for_status = data_rows[3:7] if len(data_rows) >= 7 else data_rows[3:]
        status_matches = 0

        for expected in EXPECTED_INVOICES:
            # Find corresponding row
            for row in new_rows_for_status:
                if len(row) < 5:
                    continue
                row_invoice = row[0]['value']
                if row_invoice.strip().upper() == expected['invoice_no'].upper():
                    row_status = row[4]['value'] if len(row) > 4 else ''
                    if row_status.strip().lower() == 'pending':
                        status_matches += 1
                        print(f"PASS: Invoice {expected['invoice_no']} has Status='Pending'")
                    else:
                        print(f"FAIL: Invoice {expected['invoice_no']} Status expected 'Pending', found '{row_status}'")
                    break

        comp2_score = status_matches * 0.075
        if status_matches == 4:
            print(f"PASS: Component 2 — All 4 new rows have Status='Pending' ({comp2_score} pts)")
        else:
            print(f"PARTIAL: Component 2 — {status_matches}/4 rows have Status='Pending' ({comp2_score} pts)")
        total_score += comp2_score

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3 (0.2 pts): Running_Total column has cumulative SUM formulas in new rows
    # Cumulative SUM formulas expected like: of:=SUM([.$D$2:.D5]) (OpenDocument formula)
    # OR the running total values can be verified numerically as a fallback
    try:
        new_rows_for_formula = data_rows[3:7] if len(data_rows) >= 7 else data_rows[3:]

        formula_or_value_ok = 0
        expected_running_totals = [1266.38, 1500.94, 1588.44, 1738.34]

        for i, (expected_inv, expected_rt) in enumerate(zip(EXPECTED_INVOICES, expected_running_totals)):
            # Find corresponding row
            for row in new_rows_for_formula:
                if len(row) < 1:
                    continue
                row_invoice = row[0]['value']
                if row_invoice.strip().upper() == expected_inv['invoice_no'].upper():
                    if len(row) >= 6:
                        rt_formula = row[5]['formula']
                        rt_value_str = row[5]['value']
                        rt_value = parse_currency(rt_value_str)

                        # Check if formula is a cumulative SUM (either formula or correct value)
                        has_sum_formula = (rt_formula is not None and 'SUM' in rt_formula.upper())
                        has_correct_value = (rt_value is not None and abs(rt_value - expected_rt) < 0.05)

                        if has_sum_formula and has_correct_value:
                            formula_or_value_ok += 1
                            print(f"PASS: Invoice {expected_inv['invoice_no']} has cumulative SUM formula and value {rt_value}")
                        elif has_sum_formula:
                            formula_or_value_ok += 1
                            print(f"PASS: Invoice {expected_inv['invoice_no']} has cumulative SUM formula (formula: {rt_formula})")
                        elif has_correct_value:
                            formula_or_value_ok += 1
                            print(f"PASS: Invoice {expected_inv['invoice_no']} Running_Total value correct: {rt_value} (no formula, but value ok)")
                        else:
                            print(f"FAIL: Invoice {expected_inv['invoice_no']} Running_Total: formula={rt_formula}, value={rt_value_str} (expected ~{expected_rt})")
                    else:
                        print(f"FAIL: Invoice {expected_inv['invoice_no']} row has fewer than 6 columns (no Running_Total)")
                    break

        comp3_score = (formula_or_value_ok / 4) * 0.2
        if formula_or_value_ok == 4:
            print(f"PASS: Component 3 — All 4 new rows have cumulative Running_Total ({comp3_score} pts)")
        else:
            print(f"PARTIAL: Component 3 — {formula_or_value_ok}/4 rows have cumulative Running_Total ({comp3_score} pts)")
        total_score += comp3_score

    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
