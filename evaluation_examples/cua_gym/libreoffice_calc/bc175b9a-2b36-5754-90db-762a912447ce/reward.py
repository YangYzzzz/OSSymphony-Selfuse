"""
Reward Script: Add 4 coffee shops to coffee_spots.ods
Task ID: osworld_multi_apps_web_location_002
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1 (0.4 pts): File has exactly 7 data rows (4 new entries appended to existing 3)
  Component 2 (0.4 pts): All 4 new coffee shop names are present
  Component 3 (0.2 pts): All 4 new entries have correct data in all 6 columns
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_002'
FILE_PATH = f'{WORKDIR}/Desktop/coffee_spots.ods'

# Expected new entries (appended after original 3 rows)
EXPECTED_NEW_ENTRIES = [
    {
        'Name': 'Blue Bottle Coffee',
        'City': 'San Francisco',
        'Country': 'USA',
        'Rating': '4.4',
        'Specialty': 'Single-origin pour-over',
        'Address': '66 Mint St, SF'
    },
    {
        'Name': 'Intelligentsia',
        'City': 'Los Angeles',
        'Country': 'USA',
        'Rating': '4.5',
        'Specialty': 'Espresso bar',
        'Address': '3922 Sunset Blvd, LA'
    },
    {
        'Name': 'Stumptown Coffee',
        'City': 'Portland',
        'Country': 'USA',
        'Rating': '4.3',
        'Specialty': 'Cold brew',
        'Address': '128 SW 3rd Ave, Portland'
    },
    {
        'Name': 'Heart Coffee',
        'City': 'Portland',
        'Country': 'USA',
        'Rating': '4.6',
        'Specialty': 'Ethiopian pour-over',
        'Address': '537 SW 12th Ave, Portland'
    }
]

EXPECTED_NEW_NAMES = {e['Name'] for e in EXPECTED_NEW_ENTRIES}

COLUMNS = ['Name', 'City', 'Country', 'Rating', 'Specialty', 'Address']


def parse_ods_rows(file_path):
    """
    Parse ODS file and return list of data rows.
    Each row is a list of string values for the 6 columns.
    Uses XML parsing of the ODS zip structure.
    Returns (rows, error_msg). rows is list of non-empty rows.
    """
    try:
        ns = {
            'table': 'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
            'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
            'text': 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
        }
        with zipfile.ZipFile(file_path, 'r') as z:
            content = z.read('content.xml').decode('utf-8')
        root = ET.fromstring(content)
        all_rows = root.findall('.//table:table-row', ns)
        parsed = []
        for row in all_rows:
            cells = row.findall('.//text:p', ns)
            cell_vals = [c.text if c.text else '' for c in cells]
            # Filter out rows with no content
            if any(v for v in cell_vals):
                parsed.append(cell_vals)
        return parsed, None
    except Exception as e:
        return None, str(e)


def verify_task(file_path):
    """
    Verify task completion: 4 new coffee shop entries appended to coffee_spots.ods.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Parse the ODS file
    rows, error = parse_ods_rows(file_path)
    if error or rows is None:
        print(f"CRITICAL: Cannot parse ODS file: {error}")
        print("REWARD: 0.0")
        return 0.0

    # Identify header and data rows
    if not rows:
        print("CRITICAL: No rows found in file")
        print("REWARD: 0.0")
        return 0.0

    # First row should be the header
    header = rows[0]
    data_rows = rows[1:]  # All rows after header

    print(f"INFO: Header row: {header}")
    print(f"INFO: Total data rows (after header): {len(data_rows)}")

    # Build a dict-like structure from data rows using header positions
    def row_to_dict(row):
        d = {}
        for i, col in enumerate(COLUMNS):
            d[col] = row[i].strip() if i < len(row) else ''
        return d

    data_dicts = [row_to_dict(r) for r in data_rows]

    # Component 1: File has exactly 7 data rows (3 original + 4 new) (0.4 points)
    # This FAILS on initial (3 rows) and PASSES on golden (7 rows)
    try:
        expected_data_rows = 7  # 3 original + 4 new
        actual_data_rows = len(data_rows)
        if actual_data_rows == expected_data_rows:
            print(f"PASS: Component 1 — Exactly {expected_data_rows} data rows found (3 original + 4 new) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — Expected {expected_data_rows} data rows, found {actual_data_rows}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 4 new coffee shop names are present (0.4 points)
    # This FAILS on initial (names not present) and PASSES on golden (names present)
    try:
        found_names = {d['Name'] for d in data_dicts}
        missing_names = EXPECTED_NEW_NAMES - found_names
        if not missing_names:
            print(f"PASS: Component 2 — All 4 new coffee shop names found: {EXPECTED_NEW_NAMES} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Missing coffee shop names: {missing_names}")
            print(f"      Found names: {found_names}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 4 new entries have correct data in all 6 columns (0.2 points)
    # This FAILS on initial and PASSES on golden
    try:
        all_correct = True
        for expected in EXPECTED_NEW_ENTRIES:
            name = expected['Name']
            # Find the row with this name
            matching = [d for d in data_dicts if d['Name'] == name]
            if not matching:
                print(f"FAIL: Component 3 — Row for '{name}' not found")
                all_correct = False
                continue
            actual = matching[0]
            for col in COLUMNS:
                expected_val = expected[col]
                actual_val = actual.get(col, '')
                if expected_val != actual_val:
                    print(f"FAIL: Component 3 — '{name}' column '{col}': expected '{expected_val}', found '{actual_val}'")
                    all_correct = False

        if all_correct:
            print(f"PASS: Component 3 — All 4 new entries have correct data in all 6 columns (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Some new entries have incorrect data (see above)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
