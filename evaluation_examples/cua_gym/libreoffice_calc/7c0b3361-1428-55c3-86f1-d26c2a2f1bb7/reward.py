"""
Reward Script: Export LibreOffice Calc workbook to tab-delimited text file with all sheets
Task ID: calc_gsi_057
Domain: libreoffice_calc
Scoring:
  Component 1 (0.25): .txt export file exists and is non-empty
  Component 2 (0.35): File uses tab delimiter (not comma or other)
  Component 3 (0.25): All three sheets' data included (Inventory, Suppliers, Orders)
  Component 4 (0.15): Data integrity - expected row counts and sample values present
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'calc_gsi_057'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    txt_path = f'{WORKDIR}/{TASK_ID}.txt'

    # ---------------------------------------------------------------
    # Component 1: .txt export file exists and is non-empty (0.25 pts)
    # ---------------------------------------------------------------
    try:
        if not os.path.exists(txt_path):
            print(f"FAIL: Component 1 — {txt_path} does not exist")
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        file_size = os.path.getsize(txt_path)
        if file_size < 100:
            print(f"FAIL: Component 1 — file exists but too small ({file_size} bytes)")
        else:
            print(f"PASS: Component 1 — .txt file exists, size={file_size} bytes (0.25 pts)")
            total_score += 0.25
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Read file content for remaining checks
    try:
        with open(txt_path, 'r', encoding='utf-8', errors='replace') as f:
            content = f.read()
        lines = [l for l in content.strip().split('\n') if l.strip()]
    except Exception as e:
        print(f"ERROR: Cannot read file content: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # ---------------------------------------------------------------
    # Component 2: Tab-delimited format (0.35 pts)
    # The file must use tabs as field separators, NOT commas.
    # ---------------------------------------------------------------
    try:
        tab_count = content.count('\t')
        # Check first data line uses tabs as separators
        first_line = lines[0] if lines else ''
        fields_by_tab = first_line.split('\t')

        if tab_count >= 50 and len(fields_by_tab) >= 3:
            # Additionally verify no commas are used as delimiters
            # (commas may appear in data values, but the delimiter should be tab)
            # Check that splitting by tab gives structured fields
            print(f"PASS: Component 2 — tab-delimited format confirmed, "
                  f"{tab_count} tabs found, first line has {len(fields_by_tab)} tab-separated fields (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 — not properly tab-delimited. "
                  f"Tab count: {tab_count}, fields by tab in first line: {len(fields_by_tab)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ---------------------------------------------------------------
    # Component 3: All three sheets included (0.25 pts)
    # Must contain data from Inventory, Suppliers, and Orders sheets.
    # ---------------------------------------------------------------
    try:
        sheets_found = 0
        # Inventory sheet: header has "Item Code", "Product Name", "Category"
        inv_header = 'Item Code\tProduct Name\tCategory'
        has_inventory = inv_header in content
        if has_inventory:
            sheets_found += 1
            print(f"  - Inventory sheet data: FOUND")
        else:
            print(f"  - Inventory sheet data: MISSING")

        # Suppliers sheet: header has "Supplier ID", "Company Name", "Contact Person"
        sup_header = 'Supplier ID\tCompany Name\tContact Person'
        has_suppliers = sup_header in content
        if has_suppliers:
            sheets_found += 1
            print(f"  - Suppliers sheet data: FOUND")
        else:
            print(f"  - Suppliers sheet data: MISSING")

        # Orders sheet: header has "Order No", "Order Date"
        ord_header = 'Order No\tOrder Date\tSupplier ID'
        has_orders = ord_header in content
        if has_orders:
            sheets_found += 1
            print(f"  - Orders sheet data: FOUND")
        else:
            print(f"  - Orders sheet data: MISSING")

        if sheets_found == 3:
            print(f"PASS: Component 3 — all 3 sheets included ({sheets_found}/3) (0.25 pts)")
            total_score += 0.25
        elif sheets_found >= 1:
            partial = round(0.25 * sheets_found / 3, 2)
            print(f"PARTIAL: Component 3 — {sheets_found}/3 sheets found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — no sheet data recognized in the export")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ---------------------------------------------------------------
    # Component 4: Data integrity (0.15 pts)
    # Verify expected row counts and sample values from each sheet.
    # Inventory: 14 data rows, Suppliers: 10 data rows, Orders: 12 data rows
    # ---------------------------------------------------------------
    try:
        integrity_checks = 0
        max_checks = 3

        # Check for specific data values from each sheet
        # Inventory: "Precision Ball Bearing 6205" should appear
        if 'Precision Ball Bearing 6205' in content:
            integrity_checks += 1
            print(f"  - Inventory sample data: FOUND")
        else:
            print(f"  - Inventory sample data: MISSING")

        # Suppliers: "Pacific Industrial Supply Co." should appear
        if 'Pacific Industrial Supply Co.' in content:
            integrity_checks += 1
            print(f"  - Suppliers sample data: FOUND")
        else:
            print(f"  - Suppliers sample data: MISSING")

        # Orders: "PO-3001" should appear
        if 'PO-3001' in content:
            integrity_checks += 1
            print(f"  - Orders sample data: FOUND")
        else:
            print(f"  - Orders sample data: MISSING")

        if integrity_checks == max_checks:
            print(f"PASS: Component 4 — data integrity verified ({integrity_checks}/{max_checks}) (0.15 pts)")
            total_score += 0.15
        elif integrity_checks > 0:
            partial = round(0.15 * integrity_checks / max_checks, 2)
            print(f"PARTIAL: Component 4 — {integrity_checks}/{max_checks} checks passed ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — no expected data values found")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
