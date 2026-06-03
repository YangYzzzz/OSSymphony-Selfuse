"""
Reward Script: Navigate to ArXiv cs.LG recent papers and append 6 new papers to daily_papers.ods
Task ID: osworld_multi_apps_web_papers_005
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: 6 new rows appended (rows 5-10 exist with data)   — 0.4 points
  Component 2: Each new row has all 4 columns filled with valid data — 0.4 points
  Component 3: Date_Added values in new rows use YYYY-MM-DD format — 0.2 points
  Total: 1.0
"""

import os
import re
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_papers_005'

# ODS XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
}

DATE_RE = re.compile(r'^\d{4}-\d{2}-\d{2}$')
ARXIV_ID_RE = re.compile(r'^\d{4}\.\d{4,5}$')


def parse_ods(file_path):
    """
    Parse ODS file and return list of rows as lists of string cell values.
    Each row is a list of cell text values.
    Returns None if parse fails.
    """
    try:
        with zipfile.ZipFile(file_path) as z:
            content_xml = z.read('content.xml').decode('utf-8')
    except Exception as e:
        print(f"ERROR: Cannot read ODS zip: {e}")
        return None

    try:
        root = ET.fromstring(content_xml)
    except Exception as e:
        print(f"ERROR: Cannot parse XML: {e}")
        return None

    # Navigate to the first table
    body = root.find('office:body', NS)
    if body is None:
        print("ERROR: No office:body found in content.xml")
        return None
    spreadsheet = body.find('office:spreadsheet', NS)
    if spreadsheet is None:
        print("ERROR: No office:spreadsheet found")
        return None
    table = spreadsheet.find('table:table', NS)
    if table is None:
        print("ERROR: No table:table found")
        return None

    rows = []
    for row_elem in table.findall('table:table-row', NS):
        row_data = []
        for cell_elem in row_elem.findall('table:table-cell', NS):
            # Get text content from text:p element(s)
            texts = cell_elem.findall('text:p', NS)
            cell_text = ' '.join(t.text or '' for t in texts).strip()
            row_data.append(cell_text)
        # Strip trailing empty cells
        while row_data and row_data[-1] == '':
            row_data.pop()
        rows.append(row_data)

    # Strip trailing empty rows
    while rows and all(v == '' for v in rows[-1]):
        rows.pop()

    return rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Initial state: 4 rows (1 header + 3 data rows).
    Golden state: 10 rows (1 header + 3 existing + 6 new papers appended).
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    rows = parse_ods(file_path)
    if rows is None:
        print("CRITICAL: Failed to parse ODS file")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Total rows parsed (including header): {len(rows)}")
    for i, row in enumerate(rows):
        print(f"  Row {i+1}: {row}")

    # Precondition: header row must exist with expected columns
    if len(rows) < 1:
        print("CRITICAL: File has no rows at all")
        print("REWARD: 0.0")
        return 0.0

    header = rows[0]
    expected_headers = ['arXiv_ID', 'Title', 'First_Author', 'Date_Added']
    if not all(h in header for h in expected_headers):
        print(f"CRITICAL: Header row missing expected columns. Found: {header}")
        print("REWARD: 0.0")
        return 0.0

    # Map column positions from header
    try:
        col_arxiv   = header.index('arXiv_ID')
        col_title   = header.index('Title')
        col_author  = header.index('First_Author')
        col_date    = header.index('Date_Added')
    except ValueError as e:
        print(f"CRITICAL: Cannot find column index: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Data rows are everything after header
    data_rows = rows[1:]
    print(f"INFO: Data rows found: {len(data_rows)} (expected >= 9 for task completion)")

    # --- Component 1: 6 new rows appended (rows 5-10, i.e., indices 4-9) ---
    # Initial has 3 data rows (indices 0-2). Task requires 6 more (indices 3-8).
    new_rows = data_rows[3:]  # rows beyond the original 3
    num_new = len(new_rows)
    print(f"\n--- Component 1: New rows appended (need 6, found {num_new}) ---")

    try:
        if num_new >= 6:
            print(f"PASS: Component 1 — {num_new} new rows appended (need >= 6) (0.4 pts)")
            total_score += 0.4
        elif num_new > 0:
            partial = round(0.4 * (num_new / 6), 2)
            print(f"PARTIAL: Component 1 — only {num_new}/6 new rows added, partial credit {partial} pts")
            if partial > 0:
                total_score += partial
        else:
            print(f"FAIL: Component 1 — no new rows found beyond existing 3 data rows")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # --- Component 2: Each new row has all 4 columns filled with non-empty values ---
    print(f"\n--- Component 2: All new rows have 4 columns filled ---")
    try:
        rows_to_check = new_rows[:6]  # check up to 6 new rows
        if len(rows_to_check) == 0:
            print("FAIL: Component 2 — no new rows to validate")
        else:
            complete_rows = 0
            for idx, row in enumerate(rows_to_check):
                # Pad if row has fewer than 4 columns
                while len(row) <= max(col_arxiv, col_title, col_author, col_date):
                    row.append('')

                arxiv_val  = row[col_arxiv].strip()
                title_val  = row[col_title].strip()
                author_val = row[col_author].strip()
                date_val   = row[col_date].strip()

                all_filled = (
                    len(arxiv_val) > 0 and
                    len(title_val) > 0 and
                    len(author_val) > 0 and
                    len(date_val) > 0
                )

                if all_filled:
                    complete_rows += 1
                    print(f"  PASS row {idx+5}: arXiv_ID={arxiv_val!r}, Title={title_val[:40]!r}, "
                          f"Author={author_val!r}, Date={date_val!r}")
                else:
                    missing = []
                    if not arxiv_val:   missing.append('arXiv_ID')
                    if not title_val:   missing.append('Title')
                    if not author_val:  missing.append('First_Author')
                    if not date_val:    missing.append('Date_Added')
                    print(f"  FAIL row {idx+5}: missing columns {missing}")

            if complete_rows == 6:
                print(f"PASS: Component 2 — all 6 new rows have all 4 columns filled (0.4 pts)")
                total_score += 0.4
            elif complete_rows > 0:
                partial = round(0.4 * (complete_rows / 6), 2)
                print(f"PARTIAL: Component 2 — {complete_rows}/6 rows fully complete, partial credit {partial} pts")
                if partial > 0:
                    total_score += partial
            else:
                print(f"FAIL: Component 2 — no new rows had all columns filled")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # --- Component 3: Date_Added values in new rows are in YYYY-MM-DD format ---
    print(f"\n--- Component 3: Date_Added format is YYYY-MM-DD ---")
    try:
        rows_to_check = new_rows[:6]
        if len(rows_to_check) == 0:
            print("FAIL: Component 3 — no new rows to validate")
        else:
            valid_dates = 0
            for idx, row in enumerate(rows_to_check):
                while len(row) <= col_date:
                    row.append('')
                date_val = row[col_date].strip()
                if DATE_RE.match(date_val):
                    valid_dates += 1
                    print(f"  PASS row {idx+5}: Date_Added={date_val!r} matches YYYY-MM-DD")
                else:
                    print(f"  FAIL row {idx+5}: Date_Added={date_val!r} does NOT match YYYY-MM-DD")

            if valid_dates == 6:
                print(f"PASS: Component 3 — all 6 new rows have valid YYYY-MM-DD dates (0.2 pts)")
                total_score += 0.2
            elif valid_dates > 0:
                partial = round(0.2 * (valid_dates / 6), 2)
                print(f"PARTIAL: Component 3 — {valid_dates}/6 rows have valid dates, partial credit {partial} pts")
                if partial > 0:
                    total_score += partial
            else:
                print(f"FAIL: Component 3 — no new rows had valid YYYY-MM-DD Date_Added")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 4)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: run against canonical ODS file on the VM Desktop
file_path = f'{WORKDIR}/Desktop/daily_papers.ods'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
