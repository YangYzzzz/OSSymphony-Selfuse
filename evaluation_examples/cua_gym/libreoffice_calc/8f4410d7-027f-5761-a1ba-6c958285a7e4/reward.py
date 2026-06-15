"""
Reward Script: NeurIPS Awards Research & LibreOffice Calc Entry Task
Task ID: osworld_multi_apps_acl_awards_calc_007
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: At least 4 data rows present (0.30)
  - Component 2: At least 2 rows from NeurIPS 2022 (0.20)
  - Component 3: At least 2 rows from NeurIPS 2021 (0.20)
  - Component 4: Rows sorted by Year descending (2022 before 2021) (0.20)
  - Component 5: All 4 columns (Year, Paper Title, Authors, Award Category) filled (0.10)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_007'


def parse_ods_rows(file_path):
    """
    Parse ODS file using zipfile + XML parsing.
    Returns list of rows, each row is a list of string values.
    Row 0 is the header row.
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            tree = ET.parse(f)

    root = tree.getroot()
    ns = {
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    }

    all_rows = []
    sheets = root.findall('.//table:table', ns)
    if not sheets:
        return []

    # Use the first (active) sheet
    sheet = sheets[0]
    rows = sheet.findall('table:table-row', ns)

    for row in rows:
        cells = row.findall('table:table-cell', ns)
        row_data = []
        for cell in cells:
            repeat = cell.get(
                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}number-columns-repeated'
            )
            text_elems = cell.findall('.//text:p', ns)
            val = ' '.join(t.text or '' for t in text_elems).strip()
            if repeat:
                repeat = int(repeat)
                if val:
                    for _ in range(repeat):
                        row_data.append(val)
                else:
                    row_data.extend([''] * repeat)
            else:
                row_data.append(val)
        # Trim trailing empty cells
        while row_data and row_data[-1] == '':
            row_data.pop()
        if row_data:
            all_rows.append(row_data)

    return all_rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Task: Research NeurIPS 2021 and 2022 outstanding papers and add them to
    neurips_awards.ods, sorted by Year descending.
    """
    total_score = 0.0

    # Precondition: Load the file
    try:
        all_rows = parse_ods_rows(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify header row exists (precondition gate, not scored)
    if not all_rows:
        print("CRITICAL: File is empty (no rows found)")
        print("REWARD: 0.0")
        return 0.0

    header = all_rows[0]
    expected_headers = ['Year', 'Paper Title', 'Authors', 'Award Category']
    header_ok = all(h in header for h in expected_headers)
    if not header_ok:
        print(f"CRITICAL: Header row does not match expected: {header}")
        print("REWARD: 0.0")
        return 0.0

    print(f"Header OK: {header}")

    # Extract data rows (skip header)
    data_rows = all_rows[1:]
    print(f"Data rows found: {len(data_rows)}")

    # Get column indices from header
    try:
        year_col = header.index('Year')
        title_col = header.index('Paper Title')
        authors_col = header.index('Authors')
        award_col = header.index('Award Category')
    except ValueError as e:
        print(f"CRITICAL: Missing expected column: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: At least 4 data rows present (0.30 points)
    # Initial has 0 data rows; golden has 4 — this only passes on golden.
    # -----------------------------------------------------------------------
    try:
        if len(data_rows) >= 4:
            print(f"PASS: Component 1 — At least 4 data rows found ({len(data_rows)} rows) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Expected >= 4 data rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: At least 2 rows from NeurIPS 2022 (0.20 points)
    # Initial has 0 rows from any year; golden has 2 from 2022.
    # -----------------------------------------------------------------------
    try:
        rows_2022 = []
        for row in data_rows:
            if len(row) > year_col:
                year_val = str(row[year_col]).strip()
                if year_val == '2022':
                    rows_2022.append(row)

        if len(rows_2022) >= 2:
            print(f"PASS: Component 2 — At least 2 rows from 2022 found ({len(rows_2022)} rows) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Expected >= 2 rows from 2022, found {len(rows_2022)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: At least 2 rows from NeurIPS 2021 (0.20 points)
    # Initial has 0 rows from any year; golden has 2 from 2021.
    # -----------------------------------------------------------------------
    try:
        rows_2021 = []
        for row in data_rows:
            if len(row) > year_col:
                year_val = str(row[year_col]).strip()
                if year_val == '2021':
                    rows_2021.append(row)

        if len(rows_2021) >= 2:
            print(f"PASS: Component 3 — At least 2 rows from 2021 found ({len(rows_2021)} rows) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Expected >= 2 rows from 2021, found {len(rows_2021)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -----------------------------------------------------------------------
    # Component 4: Rows sorted by Year descending (2022 rows first) (0.20 points)
    # Initial has no data rows so this trivially fails (len check ensures >= 4 rows needed).
    # Golden has 2022 rows before 2021 rows.
    # -----------------------------------------------------------------------
    try:
        if len(data_rows) >= 4:
            # Extract year values for all data rows
            year_vals = []
            for row in data_rows:
                if len(row) > year_col:
                    try:
                        year_vals.append(int(str(row[year_col]).strip()))
                    except ValueError:
                        year_vals.append(0)
                else:
                    year_vals.append(0)

            # Check sorted descending
            is_sorted_desc = all(year_vals[i] >= year_vals[i + 1] for i in range(len(year_vals) - 1))
            if is_sorted_desc:
                print(f"PASS: Component 4 — Rows sorted by Year descending: {year_vals} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Rows NOT sorted by Year descending: {year_vals}")
        else:
            print(f"FAIL: Component 4 — Cannot check sort order, fewer than 4 data rows ({len(data_rows)})")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # -----------------------------------------------------------------------
    # Component 5: All 4 columns filled for every data row (0.10 points)
    # Initial has no data rows so nothing to fill; golden has all 4 cols filled.
    # -----------------------------------------------------------------------
    try:
        if len(data_rows) >= 4:
            empty_details = []
            for r_idx, row in enumerate(data_rows):
                for col_idx, col_name in [(year_col, 'Year'), (title_col, 'Paper Title'),
                                           (authors_col, 'Authors'), (award_col, 'Award Category')]:
                    if len(row) <= col_idx or not str(row[col_idx]).strip():
                        empty_details.append(f"Row {r_idx + 2} col '{col_name}' is empty")

            if len(empty_details) == 0:
                print(f"PASS: Component 5 — All 4 columns filled for all {len(data_rows)} data rows (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 5 — Some columns are empty: {empty_details[:5]}")
        else:
            print(f"FAIL: Component 5 — Cannot check column fill, fewer than 4 data rows ({len(data_rows)})")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/neurips_awards.ods'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
