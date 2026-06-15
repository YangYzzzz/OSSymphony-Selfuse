"""
Reward Script: Create loan amortization schedule in LibreOffice Calc
Task ID: pdf_cross_042
Domain: libreoffice_calc
Scoring:
  - Component 1: amortization.ods exists (precondition gate)
  - Component 2: PMT function present in the ODS file (0.3 pts)
  - Component 3: Amortization table has 12 data rows with correct headers (0.3 pts)
  - Component 4: Month 1 values are correct (Interest ~1093.75, Principal ~286.77, Balance ~249713.23) (0.2 pts)
  - Component 5: amortization.pdf exists (0.2 pts)
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user/Documents'
ODS_PATH = '/home/user/Documents/amortization.ods'
PDF_PATH = '/home/user/Documents/amortization.pdf'

TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def parse_ods(file_path):
    """Parse ODS file and return list of rows, each row is list of (text, formula, numeric_value)."""
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read().decode('utf-8')

    root = ET.fromstring(content)
    sheets = root.findall('.//{%s}table' % TABLE_NS)
    if not sheets:
        return None, []

    sheet = sheets[0]
    sheet_name = sheet.attrib.get('{%s}name' % TABLE_NS, '')
    rows = sheet.findall('{%s}table-row' % TABLE_NS)

    all_rows = []
    for row in rows:
        cells = row.findall('{%s}table-cell' % TABLE_NS)
        row_data = []
        for cell in cells:
            text_val = cell.findtext('{%s}p' % TEXT_NS)
            formula = cell.attrib.get('{%s}formula' % TABLE_NS, '')
            num_val = cell.attrib.get('{%s}value' % OFFICE_NS, '')
            row_data.append((text_val, formula, num_val))
        all_rows.append(row_data)

    return sheet_name, all_rows


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: amortization.ods must exist
    if not os.path.exists(ODS_PATH):
        print("CRITICAL: amortization.ods not found at %s" % ODS_PATH)
        print("REWARD: 0.0")
        return 0.0

    # Parse the ODS file
    try:
        sheet_name, all_rows = parse_ods(ODS_PATH)
        if not all_rows:
            print("CRITICAL: Could not parse amortization.ods — no rows found")
            print("REWARD: 0.0")
            return 0.0
        print("INFO: Parsed ODS file, sheet='%s', rows=%d" % (sheet_name, len(all_rows)))
    except Exception as e:
        print("CRITICAL: Cannot parse ODS file: %s" % e)
        print("REWARD: 0.0")
        return 0.0

    # Component 1: PMT function present in the ODS file (0.3 points)
    # The PMT formula is the core task requirement — calculating monthly payment from PDF terms
    try:
        pmt_formula_text = ''
        pmt_num_val = ''
        for row in all_rows:
            for (text_val, formula, num_val) in row:
                if formula and 'PMT' in formula.upper():
                    pmt_formula_text = formula
                    pmt_num_val = num_val
                    break
            if pmt_formula_text:
                break

        if not pmt_formula_text:
            print("FAIL: Component 1 — No PMT function found in amortization.ods")
        else:
            # PMT formula found — verify the computed value is approximately correct (~1380.51)
            pmt_score = 0.0
            try:
                pmt_value = float(pmt_num_val)
                expected_pmt = 1380.51
                if abs(pmt_value - expected_pmt) <= 1.0:
                    pmt_score = 0.3
                    print("PASS: Component 1 — PMT function with correct value %.2f (formula: %s)" % (pmt_value, pmt_formula_text[:60]))
                else:
                    print("FAIL: Component 1 — PMT found but value %.2f deviates from expected ~%.2f" % (pmt_value, expected_pmt))
            except (ValueError, TypeError):
                # Numeric cache not available — formula presence alone earns partial credit
                pmt_score = 0.2
                print("PASS: Component 1 — PMT function found (formula: %s), value not cached" % pmt_formula_text[:60])
            if pmt_score > 0:
                total_score += pmt_score
    except Exception as e:
        print("ERROR: Component 1 — PMT check failed: %s" % e)

    # Component 2: Amortization table has 12 data rows with correct headers (0.3 points)
    # Headers: Month, Payment, Principal, Interest, Balance
    try:
        # Find the header row: contains 'Month', 'Payment', 'Principal', 'Interest', 'Balance'
        header_row_idx = -1
        data_start_idx = -1
        for i, row in enumerate(all_rows):
            row_texts = [cell[0] for cell in row if cell[0] is not None]
            row_texts_lower = [t.lower() for t in row_texts]
            if ('month' in row_texts_lower and 'payment' in row_texts_lower
                    and 'principal' in row_texts_lower and 'interest' in row_texts_lower
                    and 'balance' in row_texts_lower):
                header_row_idx = i
                data_start_idx = i + 1
                break

        if header_row_idx == -1:
            print("FAIL: Component 2 — Amortization table headers not found (Month, Payment, Principal, Interest, Balance)")
        else:
            # Count data rows (rows with month numbers 1-12)
            data_rows = []
            for i in range(data_start_idx, len(all_rows)):
                row = all_rows[i]
                if not row:
                    continue
                # Check if first cell is a number (month number)
                first_cell_text = row[0][0] if row[0][0] is not None else ''
                first_cell_num = row[0][2] if row[0][2] else ''
                try:
                    month_num = int(float(first_cell_num)) if first_cell_num else int(first_cell_text)
                    if 1 <= month_num <= 12:
                        data_rows.append((month_num, row))
                except (ValueError, TypeError):
                    pass

            unique_months = set(m for m, _ in data_rows)
            if len(unique_months) >= 12:
                print("PASS: Component 2 — Amortization table has %d months of data (months: %s)" % (len(unique_months), sorted(unique_months)))
                total_score += 0.3
            elif len(unique_months) >= 6:
                print("PARTIAL: Component 2 — Amortization table has only %d months (expected 12)" % len(unique_months))
                total_score += 0.15
            else:
                print("FAIL: Component 2 — Amortization table has only %d months (expected 12)" % len(unique_months))
    except Exception as e:
        print("ERROR: Component 2 — Table structure check failed: %s" % e)

    # Component 3: Month 1 values are correct (0.2 points)
    # Month 1: Interest = 1093.75, Principal = 286.77, Balance = 249713.23
    try:
        month1_row = None
        for row in all_rows:
            if not row:
                continue
            first_cell_num = row[0][2] if row[0][2] else ''
            first_cell_text = row[0][0] if row[0][0] is not None else ''
            try:
                month_num = int(float(first_cell_num)) if first_cell_num else int(first_cell_text)
                if month_num == 1 and len(row) >= 5:
                    month1_row = row
                    break
            except (ValueError, TypeError):
                pass

        if month1_row is None:
            print("FAIL: Component 3 — Month 1 data row not found")
        else:
            # Extract numeric values: Payment(col1), Principal(col2), Interest(col3), Balance(col4)
            def get_num(cell):
                num = cell[2]  # numeric value attribute
                if num:
                    return float(num)
                text = cell[0]
                if text:
                    return float(text.replace(',', ''))
                return None

            try:
                payment_val = get_num(month1_row[1]) if len(month1_row) > 1 else None
                principal_val = get_num(month1_row[2]) if len(month1_row) > 2 else None
                interest_val = get_num(month1_row[3]) if len(month1_row) > 3 else None
                balance_val = get_num(month1_row[4]) if len(month1_row) > 4 else None

                expected_interest = 1093.75
                expected_principal = 286.77
                expected_balance = 249713.23

                checks_passed = 0
                total_checks = 3

                if interest_val is not None and abs(interest_val - expected_interest) <= 0.1:
                    checks_passed += 1
                    print("PASS: Month 1 Interest = %.2f (expected ~%.2f)" % (interest_val, expected_interest))
                else:
                    print("FAIL: Month 1 Interest = %s (expected ~%.2f)" % (interest_val, expected_interest))

                if principal_val is not None and abs(principal_val - expected_principal) <= 0.1:
                    checks_passed += 1
                    print("PASS: Month 1 Principal = %.2f (expected ~%.2f)" % (principal_val, expected_principal))
                else:
                    print("FAIL: Month 1 Principal = %s (expected ~%.2f)" % (principal_val, expected_principal))

                if balance_val is not None and abs(balance_val - expected_balance) <= 0.1:
                    checks_passed += 1
                    print("PASS: Month 1 Balance = %.2f (expected ~%.2f)" % (balance_val, expected_balance))
                else:
                    print("FAIL: Month 1 Balance = %s (expected ~%.2f)" % (balance_val, expected_balance))

                if checks_passed == total_checks:
                    print("PASS: Component 3 — Month 1 values correct (Interest=%.2f, Principal=%.2f, Balance=%.2f)" % (interest_val, principal_val, balance_val))
                    total_score += 0.2
                elif checks_passed >= 2:
                    print("PARTIAL: Component 3 — Month 1 values mostly correct (%d/3 checks passed)" % checks_passed)
                    total_score += 0.1
                else:
                    print("FAIL: Component 3 — Month 1 values incorrect (%d/3 checks passed)" % checks_passed)
            except (ValueError, TypeError) as e:
                print("ERROR: Component 3 — Could not parse Month 1 values: %s" % e)
    except Exception as e:
        print("ERROR: Component 3 — Month 1 check failed: %s" % e)

    # Component 4: amortization.pdf exists (0.2 points)
    # The task requires exporting the spreadsheet as a PDF
    try:
        if os.path.exists(PDF_PATH):
            pdf_size = os.path.getsize(PDF_PATH)
            if pdf_size > 1000:  # must be a real PDF (> 1KB)
                print("PASS: Component 4 — amortization.pdf exists (size: %d bytes)" % pdf_size)
                total_score += 0.2
            else:
                print("FAIL: Component 4 — amortization.pdf exists but is too small (%d bytes) — may be empty" % pdf_size)
        else:
            print("FAIL: Component 4 — amortization.pdf not found at %s" % PDF_PATH)
    except Exception as e:
        print("ERROR: Component 4 — PDF check failed: %s" % e)

    final_score = min(total_score, 1.0)
    print("\nScore: %.1f/1.0" % total_score)
    print("REWARD: %.1f" % final_score)
    return final_score


verify_task()
