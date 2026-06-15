"""
Reward Script: Save workbook as ODS to Documents folder
Task ID: calc_gg1_040
Domain: libreoffice_calc
Scoring:
  Component 1 (0.3): ODS file exists at /home/user/Documents/budget_final.ods
  Component 2 (0.4): ODS is valid with 3 correctly-named sheets
  Component 3 (0.3): ODS has real data content AND original XLSX is still intact
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'calc_gg1_040'

ODS_PATH = os.path.join(WORKDIR, 'Documents', 'budget_final.ods')
XLSX_PATH = os.path.join(WORKDIR, f'{TASK_ID}.xlsx')

EXPECTED_SHEETS = ['Budget Overview', 'Department Breakdown', 'Quarterly Summary']

ODS_NS = {
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
}


def parse_ods_sheets(ods_path):
    """Parse ODS file and return list of (sheet_name, rows_with_data) tuples."""
    z = zipfile.ZipFile(ods_path)
    content = z.read('content.xml')
    root = ET.fromstring(content)
    tables = root.findall('.//table:table', ODS_NS)
    results = []
    for t in tables:
        name = t.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}name')
        rows = t.findall('.//table:table-row', ODS_NS)
        rows_with_data = 0
        for row in rows:
            cells = row.findall('.//table:table-cell', ODS_NS)
            for cell in cells:
                texts = cell.findall('.//text:p', ODS_NS)
                if any(tp.text for tp in texts if tp.text):
                    rows_with_data += 1
                    break
        results.append((name, rows_with_data))
    z.close()
    return results


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: ODS file exists at the correct path (0.3 points)
    # This is the primary task-introduced change: the ODS file must be created.
    try:
        if os.path.isfile(ODS_PATH):
            file_size = os.path.getsize(ODS_PATH)
            if file_size > 1000:  # a real ODS should be more than 1KB
                print(f"PASS: Component 1 — budget_final.ods exists at {ODS_PATH} (size: {file_size} bytes) (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — budget_final.ods exists but is too small ({file_size} bytes), likely corrupted")
        else:
            print(f"FAIL: Component 1 — budget_final.ods not found at {ODS_PATH}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: ODS is a valid ODS file with 3 correctly-named sheets (0.4 points)
    # Verifies the conversion produced a structurally correct ODS matching the source XLSX.
    try:
        if not os.path.isfile(ODS_PATH):
            print(f"FAIL: Component 2 — ODS file does not exist, cannot check structure")
        else:
            # Verify it's a valid zip/ODS
            if not zipfile.is_zipfile(ODS_PATH):
                print(f"FAIL: Component 2 — {ODS_PATH} is not a valid ZIP/ODS file")
            else:
                z = zipfile.ZipFile(ODS_PATH)
                entries = z.namelist()
                z.close()
                if 'content.xml' not in entries:
                    print(f"FAIL: Component 2 — ODS missing content.xml, not a valid ODS")
                else:
                    sheets = parse_ods_sheets(ODS_PATH)
                    sheet_names = [s[0] for s in sheets]
                    if len(sheet_names) == len(EXPECTED_SHEETS) and sheet_names == EXPECTED_SHEETS:
                        print(f"PASS: Component 2 — ODS has 3 sheets with correct names: {sheet_names} (0.4 pts)")
                        total_score += 0.4
                    else:
                        print(f"FAIL: Component 2 — Expected sheets {EXPECTED_SHEETS}, found {sheet_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: ODS has real data AND original XLSX is intact (0.3 points)
    # Both sub-conditions must pass. The ODS must contain actual data (not empty sheets),
    # and the original XLSX must still be present with 3 sheets.
    try:
        if not os.path.isfile(ODS_PATH):
            print(f"FAIL: Component 3 — ODS file does not exist, cannot check data")
        else:
            # Sub-check A: ODS has data rows in all 3 sheets
            sheets = parse_ods_sheets(ODS_PATH)
            all_have_data = all(data_rows >= 4 for _, data_rows in sheets)

            if not all_have_data:
                for name, count in sheets:
                    print(f"  Sheet '{name}': {count} rows with data")
                print(f"FAIL: Component 3 — ODS sheets are missing data (expected >= 4 rows each)")
            else:
                # Sub-check B: Original XLSX still exists with correct structure
                if not os.path.isfile(XLSX_PATH):
                    print(f"FAIL: Component 3 — Original XLSX not found at {XLSX_PATH}")
                else:
                    import openpyxl
                    wb = openpyxl.load_workbook(XLSX_PATH)
                    xlsx_sheets = wb.sheetnames
                    wb.close()
                    if xlsx_sheets == EXPECTED_SHEETS:
                        print(f"PASS: Component 3 — ODS has data in all sheets AND XLSX intact with sheets {xlsx_sheets} (0.3 pts)")
                        total_score += 0.3
                    else:
                        print(f"FAIL: Component 3 — XLSX sheets changed: expected {EXPECTED_SHEETS}, found {xlsx_sheets}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
