"""
Reward Script: Build co-authorship analysis for Stanford NLP Group
Task ID: osworld_multi_apps_web_scholar_014
Domain: libreoffice_calc (ODS format)
Scoring:
  - Component 1: File exists as ODS with 3 correctly named sheets (0.2 pts)
  - Component 2: Sheet 1 (FacultyList) has faculty names with valid DBLP URLs (0.3 pts)
  - Component 3: Sheet 2 (CoauthorshipMatrix) has matrix structure with numeric cell values (0.3 pts)
  - Component 4: Sheet 3 (TopPairs) has sorted collaboration pairs in descending order (0.2 pts)
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_scholar_014'
FILE_PATH = '/home/user/Desktop/stanford_nlp_coauthorship.ods'


def get_cell_value(cell):
    """Extract text value from an ODS cell element."""
    try:
        from odf.text import P
        paras = cell.getElementsByType(P)
        if paras:
            return str(paras[0]).strip()
        return ''
    except Exception:
        return ''


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: File must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        from odf.opendocument import load
        doc = load(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        from odf.table import Table, TableRow, TableCell
        from odf.text import P
        sheets = doc.spreadsheet.getElementsByType(Table)
    except Exception as e:
        print(f"CRITICAL: Cannot access spreadsheet content: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: File has 3 sheets with correct names (0.2 points)
    # This verifies the file structure matches task requirements
    try:
        sheet_names = [s.getAttribute('name') for s in sheets]
        num_sheets = len(sheets)
        print(f"INFO: Found {num_sheets} sheets: {sheet_names}")

        expected_sheets = ['FacultyList', 'CoauthorshipMatrix', 'TopPairs']
        # Check if we have at least 3 sheets
        if num_sheets >= 3:
            # Check if names roughly match (case-insensitive, partial match allowed)
            sheets_ok = True
            for i, expected in enumerate(expected_sheets):
                if i < len(sheet_names):
                    actual = sheet_names[i]
                    # Accept exact match or close match
                    if expected.lower() not in actual.lower() and actual.lower() not in expected.lower():
                        # Check if it's a reasonable substitute
                        alt_names = {
                            'FacultyList': ['faculty', 'people', 'members', 'list'],
                            'CoauthorshipMatrix': ['matrix', 'coauthor', 'co-author', 'collaboration'],
                            'TopPairs': ['pairs', 'top', 'collaboration', 'sorted', 'ranking']
                        }
                        alts = alt_names.get(expected, [])
                        if not any(alt in actual.lower() for alt in alts):
                            sheets_ok = False
                            print(f"FAIL: Sheet {i+1} name mismatch - expected '{expected}' (or similar), found '{actual}'")

            if sheets_ok:
                print(f"PASS: Component 1 — 3 sheets with correct structure (names: {sheet_names}) (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — sheet names do not match expected structure")
        else:
            print(f"FAIL: Component 1 — expected 3 sheets, found {num_sheets}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Sheet 1 (FacultyList) has faculty names with valid DBLP URLs (0.3 points)
    # Must have at least 5 faculty rows with DBLP URL entries
    try:
        if len(sheets) >= 1:
            sheet1 = sheets[0]
            rows = sheet1.getElementsByType(TableRow)

            faculty_count = 0
            dblp_url_count = 0
            has_header = False

            for row_idx, row in enumerate(rows):
                cells = row.getElementsByType(TableCell)
                row_data = [get_cell_value(c) for c in cells]

                # Skip empty rows
                if not any(row_data):
                    continue

                # Check for header row
                if row_idx == 0 or (not has_header and any('faculty' in v.lower() or 'name' in v.lower() for v in row_data if v)):
                    has_header = True
                    print(f"INFO: Sheet 1 header row: {[v for v in row_data if v]}")
                    continue

                # Count faculty rows with data
                if len([v for v in row_data if v]) >= 1:
                    faculty_count += 1

                    # Check if this row has a DBLP URL
                    if any('dblp.org' in v.lower() for v in row_data if v):
                        dblp_url_count += 1

            print(f"INFO: Sheet 1 — {faculty_count} faculty rows, {dblp_url_count} with DBLP URLs")

            if faculty_count >= 5 and dblp_url_count >= 5:
                print(f"PASS: Component 2 — FacultyList has {faculty_count} faculty with {dblp_url_count} DBLP URLs (0.3 pts)")
                total_score += 0.3
            elif faculty_count >= 3 and dblp_url_count >= 3:
                # Partial credit for partial data
                print(f"PARTIAL: Component 2 — FacultyList has {faculty_count} faculty with {dblp_url_count} DBLP URLs (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — expected 5+ faculty with DBLP URLs, found {faculty_count} faculty, {dblp_url_count} with DBLP URLs")
        else:
            print("FAIL: Component 2 — Sheet 1 (FacultyList) not accessible")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sheet 2 (CoauthorshipMatrix) has matrix structure with numeric values (0.3 points)
    # Must have faculty names as both row and column headers, with numeric values in cells
    try:
        if len(sheets) >= 2:
            sheet2 = sheets[1]
            rows2 = sheet2.getElementsByType(TableRow)

            header_names = []
            numeric_values_count = 0
            row_headers_count = 0
            total_data_cells = 0

            matrix_data = []
            for row in rows2:
                cells = row.getElementsByType(TableCell)
                row_data = [get_cell_value(c) for c in cells]
                if any(v for v in row_data if v):
                    matrix_data.append([v for v in row_data])

            if matrix_data:
                # First row should be header
                header_row = matrix_data[0] if matrix_data else []
                # Remove empty trailing cells
                header_names = [v for v in header_row if v]
                print(f"INFO: Sheet 2 header names count: {len(header_names)}")

                # Count rows with row-headers (faculty names) and numeric data
                for row_data in matrix_data[1:]:
                    non_empty = [v for v in row_data if v]
                    if non_empty:
                        row_headers_count += 1
                        # Count numeric values (not empty, not the row header itself)
                        for val in row_data[1:]:
                            if val:
                                try:
                                    float(val)
                                    numeric_values_count += 1
                                    total_data_cells += 1
                                except ValueError:
                                    total_data_cells += 1

                print(f"INFO: Sheet 2 — {len(header_names)} column headers, {row_headers_count} data rows, {numeric_values_count} numeric values")

                # Check if matrix has reasonable structure
                # Need at least 3x3 matrix (3 faculty headers, 3 data rows)
                has_header_row = len(header_names) >= 4  # first col label + at least 3 faculty
                has_data_rows = row_headers_count >= 3
                has_numeric = numeric_values_count >= 3

                if has_header_row and has_data_rows and has_numeric:
                    print(f"PASS: Component 3 — CoauthorshipMatrix has {len(header_names)-1} faculty columns, {row_headers_count} rows, {numeric_values_count} numeric values (0.3 pts)")
                    total_score += 0.3
                elif has_data_rows and has_numeric:
                    print(f"PARTIAL: Component 3 — Matrix has data but missing column headers (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — Matrix structure incomplete: headers={len(header_names)}, rows={row_headers_count}, numeric={numeric_values_count}")
            else:
                print("FAIL: Component 3 — Sheet 2 (CoauthorshipMatrix) is empty")
        else:
            print("FAIL: Component 3 — Sheet 2 (CoauthorshipMatrix) not accessible")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Sheet 3 (TopPairs) has sorted collaboration pairs in descending order (0.2 points)
    # Must have at least 5 pairs sorted by shared paper count descending
    try:
        if len(sheets) >= 3:
            sheet3 = sheets[2]
            rows3 = sheet3.getElementsByType(TableRow)

            pairs_data = []
            for row in rows3:
                cells = row.getElementsByType(TableCell)
                row_data = [get_cell_value(c) for c in cells]
                if any(v for v in row_data if v):
                    pairs_data.append(row_data)

            # Skip header row
            data_rows = []
            for row in pairs_data[1:]:
                non_empty = [v for v in row if v]
                if non_empty:
                    data_rows.append(row)

            print(f"INFO: Sheet 3 — {len(data_rows)} data rows (pairs)")

            # Check if sorted descending by shared paper count
            # Typically column 4 (index 3) has the count
            is_sorted = True
            prev_count = None
            pair_count_valid = 0

            for row in data_rows:
                # Find numeric value in this row (should be shared paper count)
                numeric_vals = []
                for val in row:
                    if val:
                        try:
                            numeric_vals.append(float(val))
                        except ValueError:
                            pass

                # The last/highest numeric value might be the count (or a specific column)
                # Typically: Rank, Author A, Author B, SharedCount
                count_val = None
                for i, val in enumerate(row):
                    if val:
                        try:
                            fval = float(val)
                            # Avoid rank column (usually index 0)
                            if i > 0:
                                count_val = fval
                        except ValueError:
                            pass

                if count_val is not None:
                    pair_count_valid += 1
                    if prev_count is not None and count_val > prev_count:
                        is_sorted = False
                        print(f"FAIL: Sort order violation: {prev_count} -> {count_val}")
                        break
                    prev_count = count_val

            print(f"INFO: Sheet 3 — {pair_count_valid} pairs with valid counts, sorted={is_sorted}")

            if pair_count_valid >= 5 and is_sorted:
                print(f"PASS: Component 4 — TopPairs has {pair_count_valid} pairs sorted in descending order (0.2 pts)")
                total_score += 0.2
            elif pair_count_valid >= 3:
                # Partial credit for having pairs but not sorted
                if is_sorted:
                    print(f"PARTIAL: Component 4 — Only {pair_count_valid} pairs (expected 5+), sorted (0.1 pts)")
                else:
                    print(f"PARTIAL: Component 4 — {pair_count_valid} pairs but not sorted descending (0.1 pts)")
                total_score += 0.1
            else:
                print(f"FAIL: Component 4 — expected 5+ sorted pairs, found {pair_count_valid}")
        else:
            print("FAIL: Component 4 — Sheet 3 (TopPairs) not accessible")
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
