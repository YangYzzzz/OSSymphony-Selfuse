"""
Reward Script: Circle Invalid Data in LibreOffice Calc ODS
Task ID: calc_dop_validate_circle_027
Domain: libreoffice_calc

Task: The agent must use the 'Circle Invalid Data' feature on the Ratings sheet
to mark the 9 cells in column D that violate the 1-5 whole-number data validation.

ODS Format Note: LibreOffice stores 'Circle Invalid Data' state in ODS XML as
  <table:detective><table:highlighted-range table:marked-invalid="true"/></table:detective>
  inside the table-cell element. This is the persisted form of the circles.

Scoring Rubric:
  Component 1: Any circle markers present in column D (0.3 points)
    — Verifies agent applied Circle Invalid Data at all (vs. doing nothing)
  Component 2: Exactly 9 cells in column D are marked invalid (0.4 points)
    — Verifies the complete set of invalid cells is marked
  Component 3: All 9 marked cells have values outside the valid range 1-5 (0.3 points)
    — Verifies no valid cells were incorrectly circled, and data values unchanged
"""

import os
import zipfile
import re
import xml.etree.ElementTree as ET

WORKDIR = '/home/user'  # VM path — all reward scripts run on the VM
TASK_ID = 'calc_dop_validate_circle_027'

# ODS namespace URIs
TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
OFFICE_NS = 'urn:oasis:names:tc:opendocument:xmlns:office:1.0'
TEXT_NS = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

# Expected invalid cell values (out of 1-5 range): 0, 0, 6, 6, 6, -1, -3, 11, 15
# These are the 9 values that should be circled
EXPECTED_INVALID_COUNT = 9
VALID_MIN = 1
VALID_MAX = 5


def parse_ods_marked_cells(file_path):
    """
    Parse ODS content.xml to find all cells with table:detective/table:highlighted-range
    table:marked-invalid='true' in column D of the Ratings sheet.

    Returns: list of (row_number, col_number, numeric_value) for each marked cell.
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('content.xml').decode('utf-8')

    root = ET.fromstring(content)
    body = root.find('.//{%s}spreadsheet' % OFFICE_NS)
    if body is None:
        raise ValueError("No spreadsheet body found in content.xml")

    tables = body.findall('{%s}table' % TABLE_NS)
    if not tables:
        raise ValueError("No table elements found in spreadsheet body")

    # Find the Ratings sheet
    ratings_table = None
    for t in tables:
        name = t.get('{%s}name' % TABLE_NS, '')
        if name == 'Ratings':
            ratings_table = t
            break

    if ratings_table is None:
        # Fall back to first sheet if 'Ratings' not found
        ratings_table = tables[0]

    # Walk through rows and cells, tracking row/col positions
    # ODS uses number-rows-repeated and number-columns-repeated for sparse storage
    marked_cells = []
    row_num = 0
    rows = ratings_table.findall('{%s}table-row' % TABLE_NS)

    for row in rows:
        row_repeat = int(row.get('{%s}number-rows-repeated' % TABLE_NS, '1'))
        row_num += 1

        cells = row.findall('{%s}table-cell' % TABLE_NS)
        col_num = 0
        for cell in cells:
            col_repeat = int(cell.get('{%s}number-columns-repeated' % TABLE_NS, '1'))
            col_num += 1

            # Check for detective element with marked-invalid
            detective = cell.find('{%s}detective' % TABLE_NS)
            if detective is not None:
                highlighted = detective.find('{%s}highlighted-range' % TABLE_NS)
                if highlighted is not None:
                    marked = highlighted.get('{%s}marked-invalid' % TABLE_NS)
                    if marked == 'true':
                        # Get numeric value from office:value attribute
                        val_str = cell.get('{%s}value' % OFFICE_NS)
                        try:
                            val = float(val_str) if val_str is not None else None
                        except (ValueError, TypeError):
                            val = None
                        marked_cells.append((row_num, col_num, val))

            col_num += col_repeat - 1

        row_num += row_repeat - 1

    return marked_cells


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be a valid ODS zip
    if not os.path.exists(file_path):
        print("CRITICAL: File not found: " + file_path)
        print("REWARD: 0.0")
        return 0.0

    try:
        with zipfile.ZipFile(file_path, 'r') as z:
            if 'content.xml' not in z.namelist():
                print("CRITICAL: Not a valid ODS file (no content.xml): " + file_path)
                print("REWARD: 0.0")
                return 0.0
    except Exception as e:
        print("CRITICAL: Cannot open file as zip/ODS: " + str(e))
        print("REWARD: 0.0")
        return 0.0

    # Parse marked cells
    try:
        marked_cells = parse_ods_marked_cells(file_path)
    except Exception as e:
        print("CRITICAL: Failed to parse ODS content.xml: " + str(e))
        print("REWARD: 0.0")
        return 0.0

    print("Marked cells found: " + str(len(marked_cells)))
    for (r, c, v) in marked_cells:
        col_letter = chr(64 + c) if 1 <= c <= 26 else str(c)
        print("  " + col_letter + str(r) + " = " + str(v))

    # Component 1: At least one circle marker present (0.3 points)
    # This FAILS on initial (0 markers) and PASSES on golden (9 markers)
    try:
        if len(marked_cells) > 0:
            print("PASS: Component 1 — Circle Invalid Data was applied (" + str(len(marked_cells)) + " cell(s) marked) (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 — No circle markers found (table:marked-invalid). Agent did not apply Circle Invalid Data.")
    except Exception as e:
        print("ERROR: Component 1 — " + str(e))

    # Component 2: Exactly 9 cells are marked (0.4 points)
    # This FAILS on initial (0 markers) and PASSES on golden (exactly 9 markers)
    try:
        if len(marked_cells) == EXPECTED_INVALID_COUNT:
            print("PASS: Component 2 — Exactly " + str(EXPECTED_INVALID_COUNT) + " cells are marked invalid (0.4 pts)")
            total_score += 0.4
        else:
            print("FAIL: Component 2 — Expected " + str(EXPECTED_INVALID_COUNT) + " marked cells, found " + str(len(marked_cells)))
    except Exception as e:
        print("ERROR: Component 2 — " + str(e))

    # Component 3: All marked cells have values outside 1-5, and all are in column D (0.3 points)
    # This verifies: (a) no valid cells were incorrectly circled, (b) data values were not changed
    # This FAILS on initial (no marked cells to check) and PASSES on golden (all 9 are valid violations)
    try:
        if len(marked_cells) > 0:
            all_in_col_d = all(col == 4 for (_, col, _) in marked_cells)
            all_invalid = all(
                v is not None and (v < VALID_MIN or v > VALID_MAX)
                for (_, _, v) in marked_cells
            )
            if all_in_col_d and all_invalid:
                print("PASS: Component 3 — All marked cells are in column D with values outside 1-5 range (0.3 pts)")
                total_score += 0.3
            else:
                if not all_in_col_d:
                    bad_cols = [(r, c, v) for (r, c, v) in marked_cells if c != 4]
                    print("FAIL: Component 3 — Some marked cells not in column D: " + str(bad_cols))
                if not all_invalid:
                    valid_vals = [(r, c, v) for (r, c, v) in marked_cells if v is not None and VALID_MIN <= v <= VALID_MAX]
                    print("FAIL: Component 3 — Some marked cells have valid values (should not be circled): " + str(valid_vals))
        else:
            print("FAIL: Component 3 — No marked cells to verify (prerequisite from Component 1 failed)")
    except Exception as e:
        print("ERROR: Component 3 — " + str(e))

    final_score = round(min(total_score, 1.0), 1)
    print("\nScore: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Default: test against golden file (path on VM)
file_path = WORKDIR + '/' + TASK_ID + '_initial.ods'
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
