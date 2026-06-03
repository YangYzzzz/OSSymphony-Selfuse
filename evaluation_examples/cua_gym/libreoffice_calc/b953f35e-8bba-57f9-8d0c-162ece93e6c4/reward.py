"""
Reward Script: Add Geoffrey Hinton as a new row in researchers.ods
Task ID: osworld_multi_apps_scholar_to_calc_002
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: New row for Geoffrey Hinton exists in the sheet         — 0.4 pts
  Component 2: All 5 field values are correct (Name, Affiliation,      — 0.3 pts
               H-Index text, Top Paper, Year text)
  Component 3: H-Index cell is numeric (ODS value-type=float, val=185) — 0.15 pts
  Component 4: Year-of-Top-Paper cell is numeric (float, val=1986)     — 0.15 pts
  Total: 1.0
"""

import os

# ODS reading via odfpy (available on this VM as 'odf' package)
# We attempt to import; if unavailable the verify function exits early with 0.0
_odf_import_error = None
try:
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P
except ImportError as e:
    _odf_import_error = str(e)

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_scholar_to_calc_002'
FILE_PATH = os.path.join(WORKDIR, 'researchers.ods')

# Ground truth values from task_config context
EXPECTED_NAME = 'Geoffrey Hinton'
EXPECTED_AFFILIATION = 'University of Toronto / Google Brain (Emeritus)'
EXPECTED_H_INDEX = 185
EXPECTED_TOP_PAPER = 'Learning representations by back-propagating errors'
EXPECTED_YEAR = 1986


def get_cell_text(cell):
    """Extract text content from an ODS TableCell."""
    ps = cell.getElementsByType(P)
    if ps and ps[0].firstChild:
        return ps[0].firstChild.data
    return ''


def read_ods_rows(file_path):
    """
    Load an ODS file and return all rows as a list of dicts.
    Each row is a list of {'text': str, 'type': str|None, 'value': str|None}.
    Skips fully-empty rows.
    """
    doc = load(file_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        return []

    # Use first sheet
    sheet = sheets[0]
    rows_out = []
    for row in sheet.getElementsByType(TableRow):
        cells = row.getElementsByType(TableCell)
        row_data = []
        for cell in cells:
            repeat = cell.getAttribute('numbercolumnsrepeated')
            val_type = cell.getAttribute('valuetype')
            val = cell.getAttribute('value')
            text = get_cell_text(cell)

            times = int(repeat) if repeat else 1
            # Cap repeats to avoid blank cell explosion
            if times > 50:
                times = 1
            for _ in range(times):
                row_data.append({'text': text, 'type': val_type, 'value': val})

        # Keep row only if at least one cell has content
        if any(c['text'] for c in row_data):
            rows_out.append(row_data)

    return rows_out


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    if _odf_import_error is not None:
        print(f"CRITICAL: Cannot verify — odfpy not available: {_odf_import_error}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODS file
    try:
        rows = read_ods_rows(file_path)
        print(f"INFO: Loaded {len(rows)} non-empty rows (including header)")
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find the Geoffrey Hinton row (skip header row 0)
    hinton_row = None
    for row in rows[1:]:  # skip header
        if row and row[0]['text'].strip() == EXPECTED_NAME:
            hinton_row = row
            break

    # Component 1: New row for Geoffrey Hinton exists (0.4 pts)
    # This FAILS on initial_env (no Hinton row) and PASSES on golden_env (Hinton row present)
    try:
        if hinton_row is not None:
            print(f"PASS: Component 1 — Row for '{EXPECTED_NAME}' found (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No row with Name='{EXPECTED_NAME}' found in file")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 5 text field values are correct (0.3 pts)
    # Checks: Name, Affiliation, H-Index display text, Top Paper, Year display text
    # This FAILS on initial_env (row absent) and PASSES on golden_env (correct values)
    try:
        if hinton_row is None:
            print(f"FAIL: Component 2 — Cannot check fields, row not found")
        else:
            # Extract text values (safe indexing)
            name_text        = hinton_row[0]['text'].strip() if len(hinton_row) > 0 else ''
            affil_text       = hinton_row[1]['text'].strip() if len(hinton_row) > 1 else ''
            h_index_text     = hinton_row[2]['text'].strip() if len(hinton_row) > 2 else ''
            top_paper_text   = hinton_row[3]['text'].strip() if len(hinton_row) > 3 else ''
            year_text        = hinton_row[4]['text'].strip() if len(hinton_row) > 4 else ''

            name_ok        = (name_text == EXPECTED_NAME)
            affil_ok       = (affil_text == EXPECTED_AFFILIATION)
            h_index_val_ok = (h_index_text == str(EXPECTED_H_INDEX))
            top_paper_ok   = (top_paper_text == EXPECTED_TOP_PAPER)
            year_val_ok    = (year_text == str(EXPECTED_YEAR))

            all_ok = name_ok and affil_ok and h_index_val_ok and top_paper_ok and year_val_ok

            if all_ok:
                print(f"PASS: Component 2 — All 5 field values correct (0.3 pts)")
                total_score += 0.3
            else:
                if not name_ok:
                    print(f"FAIL: Component 2 — Name: expected '{EXPECTED_NAME}', got '{name_text}'")
                if not affil_ok:
                    print(f"FAIL: Component 2 — Affiliation: expected '{EXPECTED_AFFILIATION}', got '{affil_text}'")
                if not h_index_val_ok:
                    print(f"FAIL: Component 2 — H-Index text: expected '{EXPECTED_H_INDEX}', got '{h_index_text}'")
                if not top_paper_ok:
                    print(f"FAIL: Component 2 — Top Paper: expected '{EXPECTED_TOP_PAPER}', got '{top_paper_text}'")
                if not year_val_ok:
                    print(f"FAIL: Component 2 — Year text: expected '{EXPECTED_YEAR}', got '{year_text}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: H-Index is stored as numeric (ODS value-type='float') (0.15 pts)
    # The task explicitly requires H-Index to be formatted as a number, not text.
    # This FAILS on initial_env (row absent) and PASSES on golden_env (type=float).
    try:
        if hinton_row is None:
            print(f"FAIL: Component 3 — Cannot check H-Index type, row not found")
        else:
            h_index_type  = hinton_row[2]['type'] if len(hinton_row) > 2 else None
            h_index_value = hinton_row[2]['value'] if len(hinton_row) > 2 else None

            # ODS stores numeric values with valuetype='float' and a value attribute
            h_is_numeric = (h_index_type == 'float')
            h_value_ok   = False
            if h_index_value is not None:
                try:
                    h_value_ok = (float(h_index_value) == EXPECTED_H_INDEX)
                except (ValueError, TypeError):
                    pass

            if h_is_numeric and h_value_ok:
                print(f"PASS: Component 3 — H-Index is numeric float={h_index_value} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — H-Index type='{h_index_type}' value='{h_index_value}' "
                      f"(expected type='float', value='{EXPECTED_H_INDEX}')")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Year-of-Top-Paper is stored as numeric (ODS value-type='float') (0.15 pts)
    # The task explicitly requires Year to be a 4-digit year (numeric).
    # This FAILS on initial_env (row absent) and PASSES on golden_env (type=float).
    try:
        if hinton_row is None:
            print(f"FAIL: Component 4 — Cannot check Year type, row not found")
        else:
            year_type  = hinton_row[4]['type']  if len(hinton_row) > 4 else None
            year_value = hinton_row[4]['value'] if len(hinton_row) > 4 else None

            year_is_numeric = (year_type == 'float')
            year_value_ok   = False
            if year_value is not None:
                try:
                    year_value_ok = (float(year_value) == EXPECTED_YEAR)
                except (ValueError, TypeError):
                    pass

            if year_is_numeric and year_value_ok:
                print(f"PASS: Component 4 — Year-of-Top-Paper is numeric float={year_value} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 — Year type='{year_type}' value='{year_value}' "
                      f"(expected type='float', value='{EXPECTED_YEAR}')")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
