"""
Reward Script: Convert JSON survey data to Writer table with conditional formatting
Task ID: osworld_multi_apps_json_reformat_writer_006
Domain: libreoffice_writer
Scoring:
  Component 1: Table exists with correct structure (5 cols, 11 rows)  — 0.4 pts
  Component 2: All 10 data rows contain correct survey data            — 0.3 pts
  Component 3: Rows with rating < 3 have light red background (#FFCCCC) — 0.3 pts
"""

import os

# Use odfpy to read .odt files
from odf.opendocument import load
from odf.table import Table, TableRow, TableCell
from odf.text import P
from odf.style import TableCellProperties

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_json_reformat_writer_006'

# Expected data: (respondent_id, age, gender, rating, comment)
EXPECTED_DATA = [
    ('R001', '34', 'Female',     '4', 'Very satisfied with the service overall.'),
    ('R002', '28', 'Male',       '2', 'Product quality was disappointing.'),
    ('R003', '45', 'Female',     '5', 'Excellent experience, highly recommend!'),
    ('R004', '22', 'Male',       '3', 'Average experience, nothing special.'),
    ('R005', '31', 'Non-binary', '1', 'Terrible customer support, will not return.'),
    ('R006', '55', 'Female',     '4', 'Generally happy with my purchase.'),
    ('R007', '39', 'Male',       '5', 'Outstanding quality and fast delivery.'),
    ('R008', '26', 'Female',     '2', 'Item arrived damaged, very unhappy.'),
    ('R009', '48', 'Male',       '3', 'Decent product but overpriced.'),
    ('R010', '33', 'Female',     '5', 'Fantastic! Will definitely buy again.'),
]

# Rows with rating < 3 (0-indexed among data rows, so row index in table starting from row 1)
LOW_RATING_RESPONDENTS = {'R002', 'R005', 'R008'}  # ratings 2, 1, 2


def get_cell_bg_color(doc, cell):
    """
    Get the background color of a table cell by looking up its style
    in the document's automatic styles.
    Returns a hex color string (e.g., '#FFCCCC') or None.
    """
    cell_style_name = cell.getAttribute('stylename') if hasattr(cell, 'getAttribute') else None
    if not cell_style_name:
        return None

    if not hasattr(doc, 'automaticstyles'):
        return None

    for style in doc.automaticstyles.childNodes:
        if not hasattr(style, 'getAttribute'):
            continue
        if style.getAttribute('name') != cell_style_name:
            continue
        # Found the style, look for background-color in TableCellProperties
        for child in style.childNodes:
            if not hasattr(child, 'getAttribute'):
                continue
            # TableCellProperties element stores background as 'backgroundcolor'
            # in the odfpy API the attribute accessor uses element-local name
            try:
                bg = child.getAttribute('backgroundcolor')
                if bg and bg != 'transparent':
                    return bg.lower()
            except Exception:
                pass
    return None


def get_row_text(row):
    """Extract cell texts from a TableRow as a list of strings."""
    cells = row.getElementsByType(TableCell)
    texts = []
    for cell in cells:
        ps = cell.getElementsByType(P)
        cell_text = ''
        for p in ps:
            for node in p.childNodes:
                if hasattr(node, 'data'):
                    cell_text += node.data
                elif hasattr(node, 'childNodes'):
                    for child in node.childNodes:
                        if hasattr(child, 'data'):
                            cell_text += child.data
        texts.append(cell_text.strip())
    return texts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODT document
    try:
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------------------
    # Component 1: Table exists with correct structure (5 columns, 11 rows)
    # This verifies that the JSON text was converted to a table.
    # FAILS on initial_env (no table) → PASSES on golden_env (table present)
    # -------------------------------------------------------------------------
    try:
        tables = doc.getElementsByType(Table)
        num_tables = len(tables)

        if num_tables == 0:
            print("FAIL: Component 1 — No table found in document (still JSON text?)")
        else:
            table = tables[0]
            rows = table.getElementsByType(TableRow)
            num_rows = len(rows)
            # Verify header row and 10 data rows = 11 total
            if num_rows < 11:
                print(f"FAIL: Component 1 — Expected 11 rows (header + 10 data), found {num_rows}")
            else:
                # Verify header row has the 5 expected column names
                header_texts = get_row_text(rows[0])
                expected_headers = ['respondent_id', 'age', 'gender', 'rating', 'comment']
                headers_ok = all(
                    any(h.lower() == eh.lower() for h in header_texts)
                    for eh in expected_headers
                )
                # Also check column count
                first_data_row_cells = rows[1].getElementsByType(TableCell)
                num_cols = len(first_data_row_cells)

                if not headers_ok:
                    print(f"FAIL: Component 1 — Header columns mismatch. Expected {expected_headers}, found {header_texts}")
                elif num_cols != 5:
                    print(f"FAIL: Component 1 — Expected 5 columns, found {num_cols}")
                elif headers_ok and num_cols == 5:
                    print(f"PASS: Component 1 — Table found with {num_rows} rows and {num_cols} columns (0.4 pts)")
                    total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: All 10 data rows contain the correct survey data
    # Verifies that data was faithfully extracted from the JSON.
    # FAILS on initial_env (no table) → PASSES on golden_env (data rows present)
    # -------------------------------------------------------------------------
    try:
        tables = doc.getElementsByType(Table)
        if len(tables) == 0:
            print("FAIL: Component 2 — No table to verify data rows")
        else:
            table = tables[0]
            rows = table.getElementsByType(TableRow)
            if len(rows) < 11:
                print(f"FAIL: Component 2 — Not enough rows to verify data (found {len(rows)})")
            else:
                matched = 0
                mismatches = []
                for i, expected in enumerate(EXPECTED_DATA):
                    data_row = rows[i + 1]  # skip header row
                    actual = get_row_text(data_row)
                    if len(actual) < 5:
                        mismatches.append(f"Row {i+1}: too few cells ({len(actual)})")
                        continue
                    # Compare respondent_id, age, gender, rating, comment
                    exp_vals = list(expected)
                    act_vals = [actual[j] for j in range(5)]
                    if exp_vals == act_vals:
                        matched += 1
                    else:
                        mismatches.append(f"Row {i+1}: expected {exp_vals}, got {act_vals}")

                if matched == 10:
                    print(f"PASS: Component 2 — All 10 data rows match expected survey data (0.3 pts)")
                    total_score += 0.3
                elif matched >= 8:
                    # Partial credit not applicable per rubric, but report the issue
                    print(f"FAIL: Component 2 — {matched}/10 rows matched. Mismatches: {mismatches[:3]}")
                else:
                    print(f"FAIL: Component 2 — Only {matched}/10 rows matched. Mismatches: {mismatches[:3]}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Rows with rating < 3 have light red background (#FFCCCC)
    # Verifies conditional formatting was applied correctly.
    # FAILS on initial_env (no table) → PASSES on golden_env (red background rows)
    # -------------------------------------------------------------------------
    try:
        tables = doc.getElementsByType(Table)
        if len(tables) == 0:
            print("FAIL: Component 3 — No table to verify background colors")
        else:
            table = tables[0]
            rows = table.getElementsByType(TableRow)
            if len(rows) < 11:
                print(f"FAIL: Component 3 — Not enough rows to verify formatting (found {len(rows)})")
            else:
                # Expected: rows with rating < 3 (R002, R005, R008) have #FFCCCC background
                # Collect which rows have red background
                red_bg_respondents = []
                non_red_bg_respondents = []

                for i in range(1, min(len(rows), 11)):  # rows 1-10 (data rows)
                    data_row = rows[i]
                    row_texts = get_row_text(data_row)
                    if len(row_texts) < 1:
                        continue
                    respondent_id = row_texts[0] if row_texts else ''
                    rating_str = row_texts[3] if len(row_texts) > 3 else ''

                    # Check background color of first cell in this row
                    cells = data_row.getElementsByType(TableCell)
                    if not cells:
                        continue
                    bg_color = get_cell_bg_color(doc, cells[0])

                    try:
                        rating_val = int(rating_str)
                    except (ValueError, TypeError):
                        rating_val = None

                    if bg_color and ('#ffcccc' in bg_color or 'ffcccc' in bg_color.replace('#', '')):
                        red_bg_respondents.append((respondent_id, rating_val, bg_color))
                    else:
                        if rating_val is not None and rating_val < 3:
                            non_red_bg_respondents.append((respondent_id, rating_val, bg_color))

                # Check: exactly 3 rows with rating < 3 have red background
                expected_red_ids = LOW_RATING_RESPONDENTS
                actual_red_ids = {r[0] for r in red_bg_respondents}
                missing_red = expected_red_ids - actual_red_ids
                extra_red = actual_red_ids - expected_red_ids

                if not missing_red and not extra_red:
                    total_score += 0.3
                    print(f"PASS: Component 3 — Light red (#FFCCCC) background correctly applied to "
                          f"{len(red_bg_respondents)} rows with rating < 3: "
                          f"{sorted(actual_red_ids)} (0.3 pts)")
                elif missing_red or extra_red:
                    if missing_red:
                        print(f"FAIL: Component 3 — Missing red background on rows: {missing_red}")
                    if extra_red:
                        print(f"FAIL: Component 3 — Unexpected red background on rows: {extra_red}")
                    if non_red_bg_respondents:
                        print(f"FAIL: Component 3 — Low-rating rows without red bg: {non_red_bg_respondents}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/survey_results.odt'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
