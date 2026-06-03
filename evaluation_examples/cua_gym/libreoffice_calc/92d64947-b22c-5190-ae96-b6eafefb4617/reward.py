"""
Reward Script: Save and organize email attachments from Thunderbird, then create analytics_index.ods
Task ID: osworld_multi_apps_email_file_convert_006
Domain: multi_apps (OS + LibreOffice Calc)
Scoring:
  Component 1: Directory structure exists (pdfs/ and sheets/ subdirs) — 0.10 pts
  Component 2: 3 PDFs correctly saved and renamed in pdfs/ — 0.30 pts
  Component 3: 2 ODS sheets correctly saved and renamed in sheets/ — 0.20 pts
  Component 4: analytics_index.ods exists and has 5 data rows — 0.20 pts
  Component 5: analytics_index.ods content accuracy (columns + correct category/date values) — 0.20 pts
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_file_convert_006'

# Expected files in each subdirectory (derived from task context)
EXPECTED_PDFS = {
    'reports_analytics_com_20260210_q4_2025_revenue_summary.pdf',
    'reports_analytics_com_20260219_feb_2026_marketing_campaign.pdf',
    'reports_analytics_com_20260304_march_2026_executive_dashboard.pdf',
}

EXPECTED_SHEETS = {
    'reports_analytics_com_20260217_jan_2026_web_traffic.ods',
    'reports_analytics_com_20260228_customer_retention_q1_2026.ods',
}

# Expected rows in analytics_index.ods: (original_name, new_name, category, date_received)
EXPECTED_ROWS = [
    ('q4_2025_revenue_summary.pdf', 'reports_analytics_com_20260210_q4_2025_revenue_summary.pdf', 'PDF', '2026-02-10'),
    ('jan_2026_web_traffic.ods', 'reports_analytics_com_20260217_jan_2026_web_traffic.ods', 'Sheet', '2026-02-17'),
    ('feb_2026_marketing_campaign.pdf', 'reports_analytics_com_20260219_feb_2026_marketing_campaign.pdf', 'PDF', '2026-02-19'),
    ('customer_retention_q1_2026.ods', 'reports_analytics_com_20260228_customer_retention_q1_2026.ods', 'Sheet', '2026-02-28'),
    ('march_2026_executive_dashboard.pdf', 'reports_analytics_com_20260304_march_2026_executive_dashboard.pdf', 'PDF', '2026-03-04'),
]

ANALYTICS_DIR = os.path.join(WORKDIR, 'analytics_files')
PDFS_DIR = os.path.join(ANALYTICS_DIR, 'pdfs')
SHEETS_DIR = os.path.join(ANALYTICS_DIR, 'sheets')
INDEX_FILE = os.path.join(WORKDIR, 'analytics_index.ods')


def parse_ods_rows(ods_path):
    """
    Parse an ODS file and return a list of rows, each row is a list of cell text values.
    Uses xml.etree.ElementTree to parse the content.xml inside the ODS zip.
    """
    ns = {
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    }
    rows_data = []
    with zipfile.ZipFile(ods_path, 'r') as z:
        with z.open('content.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

    # Find all table-row elements
    for table in root.iter('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table'):
        for row_elem in table.findall('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-row'):
            row_cells = []
            for cell in row_elem.findall('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}table-cell'):
                # Get text content
                texts = cell.findall('.//{urn:oasis:names:tc:opendocument:xmlns:text:1.0}p')
                cell_text = ' '.join(t.text or '' for t in texts).strip()
                row_cells.append(cell_text)
            # Only keep non-empty rows (filter out rows that are all empty)
            if any(c for c in row_cells):
                rows_data.append(row_cells)
    return rows_data


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Directory structure exists (0.10 points)
    # analytics_files/, analytics_files/pdfs/, analytics_files/sheets/ must all exist
    try:
        dirs_ok = (
            os.path.isdir(ANALYTICS_DIR) and
            os.path.isdir(PDFS_DIR) and
            os.path.isdir(SHEETS_DIR)
        )
        if dirs_ok:
            print(f"PASS: Component 1 — all three directories exist (0.10 pts)")
            total_score += 0.10
        else:
            missing = []
            if not os.path.isdir(ANALYTICS_DIR):
                missing.append(ANALYTICS_DIR)
            if not os.path.isdir(PDFS_DIR):
                missing.append(PDFS_DIR)
            if not os.path.isdir(SHEETS_DIR):
                missing.append(SHEETS_DIR)
            print(f"FAIL: Component 1 — missing directories: {missing}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 3 PDFs correctly saved and renamed in pdfs/ (0.30 points)
    # Each PDF must exist with correct renamed pattern
    try:
        if not os.path.isdir(PDFS_DIR):
            print(f"FAIL: Component 2 — pdfs/ directory missing, cannot check PDFs")
        else:
            actual_pdfs = set(os.listdir(PDFS_DIR))
            found_pdfs = EXPECTED_PDFS & actual_pdfs
            missing_pdfs = EXPECTED_PDFS - actual_pdfs
            extra_pdfs = actual_pdfs - EXPECTED_PDFS

            if found_pdfs == EXPECTED_PDFS:
                print(f"PASS: Component 2 — all 3 PDFs correctly renamed and placed in pdfs/ (0.30 pts)")
                total_score += 0.30
            else:
                # Partial credit: 0.10 per correctly placed PDF
                partial = len(found_pdfs) * 0.10
                if partial > 0:
                    print(f"PARTIAL: Component 2 — {len(found_pdfs)}/3 PDFs found in pdfs/ ({partial:.2f} pts)")
                    print(f"  Found: {sorted(found_pdfs)}")
                    print(f"  Missing: {sorted(missing_pdfs)}")
                    total_score += partial
                else:
                    print(f"FAIL: Component 2 — no expected PDFs found in pdfs/")
                    print(f"  Expected: {sorted(EXPECTED_PDFS)}")
                    print(f"  Actual: {sorted(actual_pdfs)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 2 ODS sheets correctly saved and renamed in sheets/ (0.20 points)
    try:
        if not os.path.isdir(SHEETS_DIR):
            print(f"FAIL: Component 3 — sheets/ directory missing, cannot check sheets")
        else:
            actual_sheets = set(os.listdir(SHEETS_DIR))
            found_sheets = EXPECTED_SHEETS & actual_sheets
            missing_sheets = EXPECTED_SHEETS - actual_sheets

            if found_sheets == EXPECTED_SHEETS:
                print(f"PASS: Component 3 — all 2 ODS sheets correctly renamed and placed in sheets/ (0.20 pts)")
                total_score += 0.20
            else:
                # Partial credit: 0.10 per correct sheet
                partial = len(found_sheets) * 0.10
                if partial > 0:
                    print(f"PARTIAL: Component 3 — {len(found_sheets)}/2 sheets found in sheets/ ({partial:.2f} pts)")
                    print(f"  Found: {sorted(found_sheets)}")
                    print(f"  Missing: {sorted(missing_sheets)}")
                    total_score += partial
                else:
                    print(f"FAIL: Component 3 — no expected ODS files found in sheets/")
                    print(f"  Expected: {sorted(EXPECTED_SHEETS)}")
                    print(f"  Actual: {sorted(actual_sheets)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: analytics_index.ods exists and has exactly 5 data rows (0.20 points)
    try:
        if not os.path.isfile(INDEX_FILE):
            print(f"FAIL: Component 4 — analytics_index.ods not found at {INDEX_FILE}")
        else:
            rows = parse_ods_rows(INDEX_FILE)
            # First row should be header; data rows follow
            # Count non-header data rows (exclude header row)
            if len(rows) >= 1:
                # Detect header row by checking if first row contains 'original_name'
                header_row = rows[0]
                header_lower = [c.lower() for c in header_row]
                if 'original_name' in header_lower or 'original' in ' '.join(header_lower):
                    data_rows = rows[1:]
                else:
                    data_rows = rows
                print(f"  Header row: {header_row}")
                print(f"  Data rows count: {len(data_rows)}")
                if len(data_rows) == 5:
                    print(f"PASS: Component 4 — analytics_index.ods exists with 5 data rows (0.20 pts)")
                    total_score += 0.20
                else:
                    print(f"FAIL: Component 4 — analytics_index.ods has {len(data_rows)} data rows, expected 5")
            else:
                print(f"FAIL: Component 4 — analytics_index.ods is empty")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: analytics_index.ods content accuracy (0.20 points)
    # Check that each row has correct original_name, new_name, category, date_received
    try:
        if not os.path.isfile(INDEX_FILE):
            print(f"FAIL: Component 5 — analytics_index.ods not found, skipping content check")
        else:
            rows = parse_ods_rows(INDEX_FILE)
            # Identify data rows
            if len(rows) >= 1:
                header_row = rows[0]
                header_lower = [c.lower() for c in header_row]
                if 'original_name' in header_lower or 'original' in ' '.join(header_lower):
                    data_rows = rows[1:]
                else:
                    data_rows = rows

                if len(data_rows) >= 5:
                    correct_rows = 0
                    # Build a lookup by new_name for flexible comparison
                    actual_by_newname = {}
                    for row in data_rows:
                        if len(row) >= 2:
                            actual_by_newname[row[1].strip()] = row

                    for exp_orig, exp_new, exp_cat, exp_date in EXPECTED_ROWS:
                        # Try to find this row by new_name
                        if exp_new in actual_by_newname:
                            row = actual_by_newname[exp_new]
                            row_orig = row[0].strip() if len(row) > 0 else ''
                            row_cat = row[2].strip() if len(row) > 2 else ''
                            row_date = row[3].strip() if len(row) > 3 else ''
                            # Check all 4 fields
                            orig_ok = (row_orig == exp_orig)
                            cat_ok = (row_cat.upper() == exp_cat.upper())
                            date_ok = (row_date == exp_date)
                            if orig_ok and cat_ok and date_ok:
                                correct_rows += 1
                                print(f"  ROW OK: {exp_new}")
                            else:
                                issues = []
                                if not orig_ok:
                                    issues.append(f"original_name: got '{row_orig}' expected '{exp_orig}'")
                                if not cat_ok:
                                    issues.append(f"category: got '{row_cat}' expected '{exp_cat}'")
                                if not date_ok:
                                    issues.append(f"date_received: got '{row_date}' expected '{exp_date}'")
                                print(f"  ROW PARTIAL: {exp_new} — {'; '.join(issues)}")
                        else:
                            print(f"  ROW MISSING: new_name='{exp_new}' not found in index")

                    if correct_rows == 5:
                        print(f"PASS: Component 5 — all 5 rows have correct content (0.20 pts)")
                        total_score += 0.20
                    elif correct_rows >= 3:
                        partial = 0.10
                        print(f"PARTIAL: Component 5 — {correct_rows}/5 rows correct ({partial:.2f} pts)")
                        total_score += partial
                    else:
                        print(f"FAIL: Component 5 — only {correct_rows}/5 rows have correct content")
                else:
                    print(f"FAIL: Component 5 — not enough data rows to check content")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
