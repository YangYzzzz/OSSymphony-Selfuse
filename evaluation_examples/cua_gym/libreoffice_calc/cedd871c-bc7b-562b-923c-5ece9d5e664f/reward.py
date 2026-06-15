"""
Reward Script: Open Chrome and navigate to DBLP profiles for 3 researchers
(Slav Petrov, Ryan McDonald, Keith Hall), extract data, and fill in venue_analysis.ods
with researcher info and a Venue Overlap section.

Task ID: osworld_multi_apps_scholar_to_calc_014
Domain: libreoffice_calc
Scoring:
  - Component 1: All 3 researcher rows (Name, Affiliation, Publications, 3 venues) filled  (0.5 pts)
  - Component 2: Venue Overlap section has at least one shared venue populated              (0.3 pts)
  - Component 3: At least one shared venue lists 2+ researchers                             (0.2 pts)
  Total: 1.0
"""

import os
import zipfile
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_014'
FILE_PATH = f'{WORKDIR}/venue_analysis.ods'

# ODS XML namespaces
NS_TABLE = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
NS_TEXT = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'
NS_OFFICE = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'


def parse_ods(file_path):
    """
    Parse an ODS file and return a dict of {sheet_name: [[row_values], ...]}
    Each row is a list of cell string values.
    Empty trailing cells in each row are included (up to max repeat < 50).
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    sheets = {}

    tables = root.findall(f'.//{{{NS_TABLE}}}table')
    for table in tables:
        tname = table.get(f'{{{NS_TABLE}}}name')
        rows_data = []
        rows = table.findall(f'{{{NS_TABLE}}}table-row')
        for row in rows:
            cells = row.findall(f'{{{NS_TABLE}}}table-cell')
            row_data = []
            for cell in cells:
                # Get all text paragraphs
                texts = cell.findall(f'.//{{{NS_TEXT}}}p')
                cell_val = ' '.join([t.text or '' for t in texts if t.text]).strip()

                # Handle column-repeat attribute
                repeat = cell.get(f'{{{NS_TABLE}}}number-columns-repeated')
                if repeat and int(repeat) < 50:
                    row_data.extend([cell_val] * int(repeat))
                else:
                    row_data.append(cell_val)

            rows_data.append(row_data)

        sheets[tname] = rows_data

    return sheets


def get_cell(rows, row_idx, col_idx):
    """Safely get cell value by 0-based row and column index."""
    try:
        row = rows[row_idx]
        if col_idx < len(row):
            return row[col_idx].strip()
        return ''
    except (IndexError, AttributeError):
        return ''


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODS file
    try:
        sheets = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Check the 'Researchers' sheet exists
    if 'Researchers' not in sheets:
        print(f"CRITICAL: 'Researchers' sheet not found. Sheets available: {list(sheets.keys())}")
        print("REWARD: 0.0")
        return 0.0

    rows = sheets['Researchers']

    # -------------------------------------------------------------------------
    # Component 1: All 3 researcher rows filled in (0.5 points)
    # The initial_env has rows 3-5 empty (0-indexed: rows[2]-rows[4]).
    # The golden_env has rows 3-5 filled with researcher data.
    # Each researcher must have: Name, Affiliation, Publications, Venue1, Venue2, Venue3
    # -------------------------------------------------------------------------
    try:
        # Expected 3 researchers (rows index 2, 3, 4 — 0-based, header is row 1)
        # Row 0: Title, Row 1: Headers, Rows 2-4: researcher data
        EXPECTED_NAMES = {'slav petrov', 'ryan mcdonald', 'keith hall'}
        found_researchers = []

        # Scan rows looking for 3 researchers with all required fields
        for r_idx in range(1, min(10, len(rows))):  # Search in first 10 rows
            name = get_cell(rows, r_idx, 0)
            affiliation = get_cell(rows, r_idx, 1)
            publications = get_cell(rows, r_idx, 2)
            venue1 = get_cell(rows, r_idx, 3)
            venue2 = get_cell(rows, r_idx, 4)
            venue3 = get_cell(rows, r_idx, 5)

            name_lower = name.lower()
            if name_lower in EXPECTED_NAMES:
                # Check all fields are populated
                if affiliation and publications and venue1 and venue2 and venue3:
                    # Verify publications is a number
                    try:
                        pub_count = int(str(publications).replace(',', ''))
                        if pub_count > 0:
                            found_researchers.append(name_lower)
                            print(f"PASS: Found researcher '{name}' | "
                                  f"Affiliation: '{affiliation}' | "
                                  f"Pubs: {publications} | "
                                  f"Venues: {venue1}, {venue2}, {venue3}")
                        else:
                            print(f"FAIL: Researcher '{name}' has invalid publication count: {publications}")
                    except ValueError:
                        print(f"FAIL: Researcher '{name}' publications not a number: {publications}")
                else:
                    missing = []
                    if not affiliation:
                        missing.append('Affiliation')
                    if not publications:
                        missing.append('Publications')
                    if not venue1:
                        missing.append('Venue1')
                    if not venue2:
                        missing.append('Venue2')
                    if not venue3:
                        missing.append('Venue3')
                    print(f"FAIL: Researcher '{name}' is missing: {missing}")

        # All 3 must be present and complete
        missing_researchers = EXPECTED_NAMES - set(found_researchers)
        if len(found_researchers) == 3:
            print(f"PASS: Component 1 — All 3 researchers filled in (0.5 pts)")
            total_score += 0.5
        elif len(found_researchers) > 0:
            partial = len(found_researchers) / 3 * 0.5
            print(f"PARTIAL: Component 1 — {len(found_researchers)}/3 researchers filled in ({partial:.2f} pts)")
            print(f"  Missing: {missing_researchers}")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No researchers found. Expected: {EXPECTED_NAMES}")
            print(f"  Missing researchers: {missing_researchers}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: Venue Overlap section populated with at least one shared venue (0.3 points)
    # The initial_env has the Venue Overlap section with "Venue" / "Researchers" headers
    # but no data rows. Golden has at least one venue entry with researchers.
    # -------------------------------------------------------------------------
    try:
        # Find the "Venue Overlap" section by scanning for the header row
        venue_overlap_header_row = -1
        venue_data_start = -1

        for r_idx in range(len(rows)):
            cell0 = get_cell(rows, r_idx, 0).lower()
            cell1 = get_cell(rows, r_idx, 1).lower()
            if cell0 == 'venue' and cell1 == 'researchers':
                venue_overlap_header_row = r_idx
                venue_data_start = r_idx + 1
                break

        if venue_overlap_header_row == -1:
            print(f"FAIL: Component 2 — 'Venue Overlap' header row (Venue | Researchers) not found in sheet")
        else:
            # Count populated rows after the header
            populated_venues = []
            for r_idx in range(venue_data_start, min(venue_data_start + 20, len(rows))):
                venue_name = get_cell(rows, r_idx, 0)
                researchers_in_venue = get_cell(rows, r_idx, 1)
                if venue_name and researchers_in_venue:
                    populated_venues.append((venue_name, researchers_in_venue))

            if len(populated_venues) >= 1:
                print(f"PASS: Component 2 — Venue Overlap section has {len(populated_venues)} venue(s) populated (0.3 pts)")
                for vname, vresearchers in populated_venues:
                    print(f"  Venue: '{vname}' — Researchers: '{vresearchers}'")
                total_score += 0.3
            else:
                print(f"FAIL: Component 2 — Venue Overlap section is empty (no venue rows populated)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: At least one shared venue in overlap section lists 2+ researchers (0.2 points)
    # Verifies that the venue overlap data correctly identifies shared venues (2+ researchers).
    # -------------------------------------------------------------------------
    try:
        found_shared_venue = False
        # Re-scan the venue overlap section to find venues with 2+ researchers
        venues_for_comp3 = []
        venue_header_found = False
        for r_idx in range(len(rows)):
            cell0 = get_cell(rows, r_idx, 0).lower()
            cell1 = get_cell(rows, r_idx, 1).lower()
            if cell0 == 'venue' and cell1 == 'researchers':
                venue_header_found = True
                data_start = r_idx + 1
                for r2 in range(data_start, min(data_start + 20, len(rows))):
                    vname = get_cell(rows, r2, 0)
                    vresearchers = get_cell(rows, r2, 1)
                    if vname and vresearchers:
                        venues_for_comp3.append((vname, vresearchers))
                break

        for vname, vresearchers in venues_for_comp3:
            # Check the researchers cell — it should contain 2+ names
            # Names are typically comma-separated
            researcher_names = [n.strip() for n in vresearchers.split(',') if n.strip()]
            if len(researcher_names) >= 2:
                print(f"PASS: Component 3 — Venue '{vname}' shared by {len(researcher_names)} researchers: {researcher_names} (0.2 pts)")
                found_shared_venue = True
                break

        if found_shared_venue:
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — No venue found with 2+ researchers in the Venue Overlap section")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
