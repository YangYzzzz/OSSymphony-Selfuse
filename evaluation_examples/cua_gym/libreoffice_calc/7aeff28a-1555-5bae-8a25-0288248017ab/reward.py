"""
Reward Script: Fill missing DOIs, open-access URLs, and venue names in thesis bibliography spreadsheet
Task ID: osworld_multi_apps_web_references_006
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: All 8 rows have DOI filled (0.4 points)
  - Component 2: All 8 rows have Venue filled (0.3 points)
  - Component 3: All 8 rows have Open_Access_URL filled (0.3 points)
Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

FILE_PATH = '/home/user/Desktop/thesis_refs.ods'

# ODF XML namespaces
NS = {
    'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':  'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
}

def parse_ods(file_path):
    """
    Parse an ODS file and return a list of rows (each row is a list of cell text values).
    """
    with zipfile.ZipFile(file_path) as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    spreadsheet = root.find('.//office:spreadsheet', NS)
    tables = spreadsheet.findall('table:table', NS)
    if not tables:
        return []

    # Use the first sheet
    table = tables[0]
    rows_data = []
    for row_elem in table.findall('table:table-row', NS):
        cells = row_elem.findall('table:table-cell', NS)
        row_vals = []
        for cell in cells:
            p_elems = cell.findall('text:p', NS)
            val = ' '.join(p.text or '' for p in p_elems if p.text).strip()
            row_vals.append(val)
        rows_data.append(row_vals)
    return rows_data


def get_cell(row, col_idx):
    """Return cell value at col_idx in row, or '' if out of bounds."""
    if col_idx < len(row):
        return row[col_idx].strip()
    return ''


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.

    The task required filling:
      - Column C (index 2): DOI
      - Column D (index 3): Venue
      - Column E (index 4): Open_Access_URL
    for all 8 paper entries (rows 2-9 in the spreadsheet, i.e. data rows after header).

    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file
    try:
        rows = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find header row and identify column indices
    # Header row should be: Title, Year, DOI, Venue, Open_Access_URL
    header_row = None
    header_idx = None
    for i, row in enumerate(rows):
        row_joined = [v.strip() for v in row]
        if 'Title' in row_joined and 'DOI' in row_joined:
            header_row = row_joined
            header_idx = i
            break

    if header_row is None:
        print("CRITICAL: Cannot find header row with 'Title' and 'DOI' columns.")
        print("REWARD: 0.0")
        return 0.0

    # Find column indices
    try:
        doi_col = header_row.index('DOI')
    except ValueError:
        doi_col = 2  # fallback

    try:
        venue_col = header_row.index('Venue')
    except ValueError:
        venue_col = 3  # fallback

    try:
        oa_col = header_row.index('Open_Access_URL')
    except ValueError:
        oa_col = 4  # fallback

    try:
        title_col = header_row.index('Title')
    except ValueError:
        title_col = 0  # fallback

    # Extract data rows: the 8 paper entries after the header
    data_rows = []
    for row in rows[header_idx + 1:]:
        # A data row must have a non-empty Title
        title_val = get_cell(row, title_col)
        if title_val:
            data_rows.append(row)

    print(f"INFO: Found {len(data_rows)} data rows (expected 8)")

    if len(data_rows) == 0:
        print("CRITICAL: No data rows found.")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: DOI column filled for all 8 rows (0.4 points)
    try:
        doi_filled_count = 0
        doi_missing = []
        for i, row in enumerate(data_rows):
            doi_val = get_cell(row, doi_col)
            if doi_val and doi_val.lower() != 'n/a':
                doi_filled_count += 1
            else:
                doi_missing.append(i + 1)

        if doi_filled_count == 8 and len(data_rows) >= 8:
            print(f"PASS: Component 1 — All 8 rows have DOI filled (0.4 pts)")
            total_score += 0.4
        elif doi_filled_count > 0:
            # Partial credit based on fraction
            partial = round(0.4 * (doi_filled_count / 8), 2)
            print(f"PARTIAL: Component 1 — {doi_filled_count}/8 rows have DOI filled ({partial} pts). Missing rows: {doi_missing}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No DOI values found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 (DOI check) — {e}")

    # Component 2: Venue column filled for all 8 rows (0.3 points)
    try:
        venue_filled_count = 0
        venue_missing = []
        for i, row in enumerate(data_rows):
            venue_val = get_cell(row, venue_col)
            if venue_val and venue_val.lower() != 'n/a':
                venue_filled_count += 1
            else:
                venue_missing.append(i + 1)

        if venue_filled_count == 8 and len(data_rows) >= 8:
            print(f"PASS: Component 2 — All 8 rows have Venue filled (0.3 pts)")
            total_score += 0.3
        elif venue_filled_count > 0:
            partial = round(0.3 * (venue_filled_count / 8), 2)
            print(f"PARTIAL: Component 2 — {venue_filled_count}/8 rows have Venue filled ({partial} pts). Missing rows: {venue_missing}")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No Venue values found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 (Venue check) — {e}")

    # Component 3: Open_Access_URL filled for all 8 rows (0.3 points)
    # Per task description, 'N/A' is acceptable if no open-access version found.
    # So we check if each row has either a URL or 'N/A' (not an empty value).
    try:
        oa_filled_count = 0
        oa_missing = []
        for i, row in enumerate(data_rows):
            oa_val = get_cell(row, oa_col)
            if oa_val:  # non-empty (including 'N/A')
                oa_filled_count += 1
            else:
                oa_missing.append(i + 1)

        if oa_filled_count == 8 and len(data_rows) >= 8:
            print(f"PASS: Component 3 — All 8 rows have Open_Access_URL filled (0.3 pts)")
            total_score += 0.3
        elif oa_filled_count > 0:
            partial = round(0.3 * (oa_filled_count / 8), 2)
            print(f"PARTIAL: Component 3 — {oa_filled_count}/8 rows have Open_Access_URL filled ({partial} pts). Missing rows: {oa_missing}")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No Open_Access_URL values found (0.0 pts)")
    except Exception as e:
        print(f"ERROR: Component 3 (Open_Access_URL check) — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
