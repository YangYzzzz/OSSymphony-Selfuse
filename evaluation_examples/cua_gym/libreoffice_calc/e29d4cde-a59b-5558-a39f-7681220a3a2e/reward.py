"""
Reward Script: Build supplier comparison database from PDF quotes
Task ID: osworld_multi_apps_doc_pdf_calc_012
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.30): 5 product data rows populated with price data from all 3 suppliers
  Component 2 (0.40): Cheapest_Supplier column correctly identifies the lowest-price supplier per product
  Component 3 (0.30): Cheapest_Supplier column cells have green (#00ff00) background highlight
"""

import os
import re
import zipfile

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_doc_pdf_calc_012'
FILE_PATH = f'{WORKDIR}/quote_comparison.ods'

# Ground truth values extracted from task context:
# PRD-001: Apex=12.5, Bolt=11.9, Crest=13.2 -> Bolt Industries, 11.9
# PRD-002: Apex=34.8, Bolt=36.5, Crest=33.6 -> Crest Wholesale, 33.6
# PRD-003: Apex=8.75, Bolt=9.2,  Crest=8.5  -> Crest Wholesale, 8.5
# PRD-004: Apex=67.2, Bolt=63.8, Crest=65.5 -> Bolt Industries, 63.8
# PRD-005: Apex=15.4, Bolt=16.1, Crest=14.9 -> Crest Wholesale, 14.9

EXPECTED_DATA = [
    {
        'product_code': 'PRD-001',
        'product_name': 'Industrial Bearing 6205',
        'apex': 12.5, 'bolt': 11.9, 'crest': 13.2,
        'cheapest_supplier': 'Bolt Industries',
        'best_price': 11.9,
    },
    {
        'product_code': 'PRD-002',
        'product_name': 'Hydraulic Seal Kit HS-300',
        'apex': 34.8, 'bolt': 36.5, 'crest': 33.6,
        'cheapest_supplier': 'Crest Wholesale',
        'best_price': 33.6,
    },
    {
        'product_code': 'PRD-003',
        'product_name': 'Steel Coupling SC-150',
        'apex': 8.75, 'bolt': 9.2, 'crest': 8.5,
        'cheapest_supplier': 'Crest Wholesale',
        'best_price': 8.5,
    },
    {
        'product_code': 'PRD-004',
        'product_name': 'Pneumatic Valve PV-80',
        'apex': 67.2, 'bolt': 63.8, 'crest': 65.5,
        'cheapest_supplier': 'Bolt Industries',
        'best_price': 63.8,
    },
    {
        'product_code': 'PRD-005',
        'product_name': 'Electrical Relay ER-24V',
        'apex': 15.4, 'bolt': 16.1, 'crest': 14.9,
        'cheapest_supplier': 'Crest Wholesale',
        'best_price': 14.9,
    },
]

GREEN_BACKGROUND = '#00ff00'


def parse_ods(file_path):
    """
    Parse ODS file using zipfile + XML to extract:
    - rows: list of dicts {col_idx: (value, style_name)}
    - green_styles: set of style names that have green (#00ff00) background
    Returns (rows, green_styles) or raises Exception.
    """
    with zipfile.ZipFile(file_path) as z:
        content = z.read('content.xml').decode('utf-8')

    # Find styles with green background
    style_pattern = r'<style:style\s+style:name="([^"]+)"[^>]*>(.*?)</style:style>'
    all_styles = re.findall(style_pattern, content, re.DOTALL)
    green_styles = set()
    for name, body in all_styles:
        if GREEN_BACKGROUND in body or 'green' in body.lower():
            green_styles.add(name)

    # Parse table rows
    table_match = re.search(r'<table:table[^>]*>(.*?)</table:table>', content, re.DOTALL)
    if not table_match:
        raise ValueError("No table found in ODS content.xml")
    table_content = table_match.group(1)

    row_pattern = r'<table:table-row[^>]*>(.*?)</table:table-row>'
    all_rows_raw = re.findall(row_pattern, table_content, re.DOTALL)

    rows = []
    for row_raw in all_rows_raw:
        cell_pattern = r'<table:table-cell([^>]*)>(.*?)</table:table-cell>'
        cells_raw = re.findall(cell_pattern, row_raw, re.DOTALL)
        row_dict = {}
        col_idx = 0
        for attrs, body in cells_raw:
            val_match = re.search(r'<text:p[^>]*>(.*?)</text:p>', body, re.DOTALL)
            value = val_match.group(1).strip() if val_match else ''
            style_match = re.search(r'table:style-name="([^"]+)"', attrs)
            style = style_match.group(1) if style_match else ''
            # Handle repeated cells
            repeat_match = re.search(r'table:number-columns-repeated="(\d+)"', attrs)
            repeat = int(repeat_match.group(1)) if repeat_match else 1
            for _ in range(repeat):
                row_dict[col_idx] = (value, style)
                col_idx += 1
        rows.append(row_dict)

    return rows, green_styles


def float_close(a, b, tol=0.01):
    """Check if two floats are approximately equal."""
    try:
        return abs(float(a) - float(b)) <= tol
    except (TypeError, ValueError):
        return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be readable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        rows, green_styles = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Skip header row (row 0)
    data_rows = [rows[i] for i in range(1, len(rows)) if rows[i]]

    print(f"INFO: Found {len(data_rows)} data rows (expected 5)")
    print(f"INFO: Green styles detected: {green_styles}")

    # -----------------------------------------------------------------------
    # Component 1: 5 data rows populated with price data from all 3 suppliers (0.30 pts)
    # This checks that the agent has extracted and entered data for all products.
    # The initial_env only has headers — no data rows — so this FAILS on initial.
    # -----------------------------------------------------------------------
    try:
        rows_with_prices = 0
        for row in data_rows:
            # Each data row should have values in cols 0-6: code, name, apex, bolt, crest, supplier, best_price
            code = row.get(0, ('', ''))[0]
            apex_val = row.get(2, ('', ''))[0]
            bolt_val = row.get(3, ('', ''))[0]
            crest_val = row.get(4, ('', ''))[0]
            supplier_val = row.get(5, ('', ''))[0]
            best_price_val = row.get(6, ('', ''))[0]

            # Check that price columns and supplier/best_price are populated
            has_all = (
                code.startswith('PRD-') and
                apex_val not in ('', None) and
                bolt_val not in ('', None) and
                crest_val not in ('', None) and
                supplier_val not in ('', None) and
                best_price_val not in ('', None)
            )
            if has_all:
                rows_with_prices += 1
                print(f"PASS (comp1): Row has full price data: {code}")
            else:
                print(f"FAIL (comp1): Row missing data: code={code}, apex={apex_val}, bolt={bolt_val}, crest={crest_val}, supplier={supplier_val}, best_price={best_price_val}")

        if rows_with_prices == 5:
            print(f"PASS: Component 1 — All 5 data rows populated with prices (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Only {rows_with_prices}/5 rows fully populated")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Cheapest_Supplier column correctly identifies lowest-price supplier (0.40 pts)
    # We match each product row to expected data and check correctness.
    # The initial_env has no data rows so this FAILS on initial.
    # -----------------------------------------------------------------------
    try:
        correct_supplier_count = 0
        correct_best_price_count = 0

        # Build lookup from product code to row data
        row_by_code = {}
        for row in data_rows:
            code = row.get(0, ('', ''))[0]
            if code:
                row_by_code[code] = row

        for expected in EXPECTED_DATA:
            code = expected['product_code']
            row = row_by_code.get(code)
            if row is None:
                print(f"FAIL (comp2): Product {code} not found in table")
                continue

            actual_supplier = row.get(5, ('', ''))[0].strip()
            actual_best_price = row.get(6, ('', ''))[0]

            # Check Cheapest_Supplier
            if actual_supplier == expected['cheapest_supplier']:
                correct_supplier_count += 1
                print(f"PASS (comp2): {code} cheapest supplier = {actual_supplier}")
            else:
                print(f"FAIL (comp2): {code} cheapest supplier expected={expected['cheapest_supplier']}, got={actual_supplier}")

            # Check Best_Price value
            if float_close(actual_best_price, expected['best_price']):
                correct_best_price_count += 1
                print(f"PASS (comp2): {code} best price = {actual_best_price} (expected {expected['best_price']})")
            else:
                print(f"FAIL (comp2): {code} best price expected={expected['best_price']}, got={actual_best_price}")

        # Score proportionally: need both supplier name AND best price correct for all 5
        # Award 0.40 if all 5 cheapest suppliers are correct and all 5 best prices are correct
        # Award partial credit based on correct count
        supplier_fraction = correct_supplier_count / 5.0
        best_price_fraction = correct_best_price_count / 5.0
        comp2_score = 0.20 * supplier_fraction + 0.20 * best_price_fraction

        if comp2_score > 0:
            print(f"PASS: Component 2 — {correct_supplier_count}/5 suppliers correct, {correct_best_price_count}/5 best prices correct ({comp2_score:.2f} pts)")
            total_score += comp2_score
        else:
            print(f"FAIL: Component 2 — No correct cheapest supplier identifications")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Cheapest_Supplier cells (column F / index 5) are highlighted green (0.30 pts)
    # The initial_env has no data and no green cells, so this FAILS on initial.
    # -----------------------------------------------------------------------
    try:
        green_supplier_cells = 0
        total_data_rows = len(data_rows)

        for row in data_rows:
            supplier_cell = row.get(5, ('', ''))
            cell_style = supplier_cell[1]
            cell_value = supplier_cell[0]
            if cell_style in green_styles:
                green_supplier_cells += 1
                print(f"PASS (comp3): Supplier cell '{cell_value}' has green background (style={cell_style})")
            else:
                print(f"FAIL (comp3): Supplier cell '{cell_value}' missing green background (style={cell_style})")

        if total_data_rows > 0 and green_supplier_cells == total_data_rows:
            print(f"PASS: Component 3 — All {green_supplier_cells}/{total_data_rows} cheapest-supplier cells highlighted green (0.30 pts)")
            total_score += 0.30
        elif green_supplier_cells > 0:
            partial = 0.30 * (green_supplier_cells / total_data_rows) if total_data_rows > 0 else 0.0
            print(f"PARTIAL: Component 3 — {green_supplier_cells}/{total_data_rows} supplier cells highlighted green ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No green highlighting found on Cheapest_Supplier cells")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score:.4f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
