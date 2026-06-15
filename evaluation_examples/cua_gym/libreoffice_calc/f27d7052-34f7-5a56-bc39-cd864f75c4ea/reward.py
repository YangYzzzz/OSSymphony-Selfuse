"""
Reward Script: Look up MIT CSAIL LIS group researchers and record in Calc file
Task ID: osworld_multi_apps_web_faculty_007
Domain: libreoffice_calc
Scoring:
  Component 1 (0.30): ODS file exists on Desktop with correct name
  Component 2 (0.30): File has all 5 required columns (Name, Title, Research_Areas, DBLP_URL, Papers_Last_3_Years)
  Component 3 (0.20): File has at least 3 researcher data rows
  Component 4 (0.20): DBLP_URL column has valid DBLP URLs AND Papers_Last_3_Years column has numeric values
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_007'
FILE_PATH = '/home/user/Desktop/mit_lis_researchers.ods'

REQUIRED_COLUMNS = ['Name', 'Title', 'Research_Areas', 'DBLP_URL', 'Papers_Last_3_Years']


def parse_ods_rows(file_path):
    """
    Parse an ODS file and return (header_row, data_rows).
    Each row is a list of cell values (strings or None).
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        with z.open('content.xml') as f:
            content = f.read().decode('utf-8')

    root = ET.fromstring(content)
    ns = {
        'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
        'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
        'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    }

    spreadsheet = root.find('.//office:spreadsheet', ns)
    tables = spreadsheet.findall('table:table', ns)
    if not tables:
        return None, []

    # Use first table/sheet
    table = tables[0]
    rows = table.findall('table:table-row', ns)

    parsed_rows = []
    for row in rows:
        cells = row.findall('table:table-cell', ns)
        cell_vals = []
        for c in cells:
            str_val = c.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}string-value')
            num_val = c.get('{urn:oasis:names:tc:opendocument:xmlns:office:1.0}value')
            if str_val is not None:
                cell_vals.append(str_val)
            elif num_val is not None:
                cell_vals.append(num_val)
            else:
                cell_vals.append(None)
        # Remove trailing None values
        while cell_vals and cell_vals[-1] is None:
            cell_vals.pop()
        if cell_vals:
            parsed_rows.append(cell_vals)

    if not parsed_rows:
        return None, []

    header = parsed_rows[0]
    data = parsed_rows[1:]
    return header, data


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Component 1: ODS file exists on Desktop with correct name (0.30 points)
    # This FAILS on initial (no file) -> PASSES on golden (file present)
    try:
        if os.path.exists(FILE_PATH) and os.path.getsize(FILE_PATH) > 0:
            print(f"PASS: Component 1 — mit_lis_researchers.ods exists on Desktop (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — mit_lis_researchers.ods not found at {FILE_PATH}")
            print(f"Score: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"Score: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load and parse ODS file
    try:
        header, data_rows = parse_ods_rows(FILE_PATH)
        if header is None:
            print("CRITICAL: Could not parse ODS file — no sheets found")
            print(f"Score: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
        print(f"INFO: Parsed ODS — header={header}, data rows={len(data_rows)}")
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {FILE_PATH}: {e}")
        print(f"Score: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: File has all 5 required columns (0.30 points)
    # This FAILS on initial (no file) -> PASSES on golden (correct headers)
    try:
        # Normalize headers for comparison (strip whitespace, case-insensitive)
        header_normalized = [str(h).strip() if h else '' for h in header]
        required_cols_normalized = [c.strip() for c in REQUIRED_COLUMNS]

        missing_cols = []
        for col in required_cols_normalized:
            # Case-insensitive match
            if not any(col.lower() == h.lower() for h in header_normalized):
                missing_cols.append(col)

        if not missing_cols:
            print(f"PASS: Component 2 — All 5 required columns present: {header_normalized} (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — Missing columns: {missing_cols}. Found columns: {header_normalized}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: File has at least 3 researcher data rows (0.20 points)
    # This FAILS on initial (no file) -> PASSES on golden (10 rows of data)
    try:
        num_rows = len(data_rows)
        if num_rows >= 3:
            print(f"PASS: Component 3 — {num_rows} researcher rows found (>= 3 required) (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 — Only {num_rows} data rows found, need at least 3")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: DBLP_URL column has valid DBLP URLs AND Papers_Last_3_Years has numeric values (0.20 points)
    # This FAILS on initial (no file) -> PASSES on golden (valid DBLP URLs and paper counts)
    try:
        # Find column indices for DBLP_URL and Papers_Last_3_Years
        dblp_col_idx = None
        papers_col_idx = None
        for i, h in enumerate(header_normalized):
            if h.lower() == 'dblp_url':
                dblp_col_idx = i
            elif h.lower() == 'papers_last_3_years':
                papers_col_idx = i

        if dblp_col_idx is None or papers_col_idx is None:
            print(f"FAIL: Component 4 — Could not find DBLP_URL or Papers_Last_3_Years columns. Header: {header_normalized}")
        else:
            # Check DBLP URLs and paper counts for data rows
            valid_dblp = 0
            valid_papers = 0
            rows_checked = 0

            for row in data_rows:
                rows_checked += 1
                # Check DBLP URL
                if len(row) > dblp_col_idx and row[dblp_col_idx]:
                    url = str(row[dblp_col_idx]).strip()
                    if 'dblp.org' in url.lower():
                        valid_dblp += 1

                # Check Papers_Last_3_Years is numeric
                if len(row) > papers_col_idx and row[papers_col_idx] is not None:
                    try:
                        val = float(str(row[papers_col_idx]))
                        if val >= 0:
                            valid_papers += 1
                    except (ValueError, TypeError):
                        pass

            # Both conditions: majority of rows have valid DBLP URLs and numeric paper counts
            dblp_pass = rows_checked > 0 and (valid_dblp / rows_checked) >= 0.5
            papers_pass = rows_checked > 0 and (valid_papers / rows_checked) >= 0.5

            if dblp_pass and papers_pass:
                print(f"PASS: Component 4 — {valid_dblp}/{rows_checked} rows have valid DBLP URLs, "
                      f"{valid_papers}/{rows_checked} rows have numeric paper counts (0.20 pts)")
                total_score += 0.20
            else:
                if not dblp_pass:
                    print(f"FAIL: Component 4 — Only {valid_dblp}/{rows_checked} rows have valid DBLP URLs (dblp.org)")
                if not papers_pass:
                    print(f"FAIL: Component 4 — Only {valid_papers}/{rows_checked} rows have numeric Papers_Last_3_Years")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == '__main__':
    verify_task()
