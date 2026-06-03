"""
Reward Script: Junior Faculty Comparison Table in LibreOffice Calc
Task ID: osworld_multi_apps_web_scholar_011
Domain: libreoffice_calc
Scoring:
  Component 1: File existence at correct path               (0.15 pts)
  Component 2: Correct header row with all 9 required cols  (0.25 pts)
  Component 3: All 3 researchers present (by name)          (0.25 pts)
  Component 4: Computed fields non-empty (Papers_Per_Year,
               Avg_Citations_Per_Paper) for all 3 rows      (0.20 pts)
  Component 5: Supporting data fields non-empty             (0.15 pts)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_scholar_011'
FILE_PATH = '/home/user/Desktop/junior_faculty_comparison.ods'

# Required column headers (case-insensitive match)
REQUIRED_COLUMNS = [
    'Name',
    'Current_Institution',
    'PhD_Year',
    'Total_Papers',
    'Papers_Per_Year',
    'Total_Citations',
    'Avg_Citations_Per_Paper',
    'Top_Venue',
    'H_Index',
]

# Required researchers (partial match, case-insensitive)
REQUIRED_RESEARCHERS = [
    'sara hooker',
    'ellie pavlick',
    'jacob andreas',
]


def read_ods_rows(filepath):
    """
    Read all non-empty rows from an ODS file using odf package.
    Returns a list of lists of string values.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(filepath)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        return []

    ws = sheets[0]
    rows = ws.getElementsByType(TableRow)
    all_rows = []
    for row in rows:
        cells = row.getElementsByType(TableCell)
        row_vals = []
        for cell in cells:
            repeat = cell.getAttribute('numbercolumnsrepeated')
            text_nodes = cell.getElementsByType(P)
            val = (text_nodes[0].firstChild.data
                   if text_nodes and text_nodes[0].firstChild else '')
            repeat_count = int(repeat) if repeat else 1
            row_vals.extend([val] * repeat_count)
        # Trim trailing empty cells
        while row_vals and row_vals[-1] == '':
            row_vals.pop()
        if row_vals:
            all_rows.append(row_vals)
    return all_rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File existence (0.15 points)
    # The task asks for the file to be saved at /home/user/Desktop/junior_faculty_comparison.ods
    # This FAILS on initial_env (file does not exist) -> PASSES on golden_env
    try:
        file_found = os.path.exists(file_path)
        if file_found:
            print(f"PASS: Component 1 — File exists at {file_path} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — File not found at {file_path}")
            # File does not exist; no further checks possible
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Load the ODS file
    try:
        all_rows = read_ods_rows(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    if not all_rows:
        print("CRITICAL: ODS file appears to be empty or unreadable")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    header_row = [str(v).strip() for v in all_rows[0]]
    data_rows = all_rows[1:]

    print(f"INFO: Header row: {header_row}")
    print(f"INFO: Data rows count: {len(data_rows)}")

    # Component 2: Correct header row with all 9 required columns (0.25 points)
    # Checks that all required column names are present in the header row
    # This FAILS on initial_env (no file) -> PASSES on golden_env
    try:
        header_lower = [h.lower().replace(' ', '_') for h in header_row]
        missing_cols = [
            req_col for req_col in REQUIRED_COLUMNS
            if req_col.lower().replace(' ', '_') not in header_lower
        ]

        if not missing_cols:
            print(f"PASS: Component 2 — All 9 required columns present: {header_row} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 — Missing columns: {missing_cols}; found: {header_row}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 researchers present (0.25 points)
    # Check that a row exists for each of the 3 researchers by name match
    # This FAILS on initial_env (no file) -> PASSES on golden_env
    try:
        if not data_rows:
            print("FAIL: Component 3 — No data rows found")
        else:
            # Find name column index
            name_col_idx = 0
            for i, h in enumerate(header_row):
                if h.lower() == 'name':
                    name_col_idx = i
                    break

            found_researchers = []
            for row in data_rows:
                if len(row) > name_col_idx:
                    name_val = str(row[name_col_idx]).strip().lower()
                    for req in REQUIRED_RESEARCHERS:
                        if req not in found_researchers and (
                            req in name_val or name_val in req
                        ):
                            found_researchers.append(req)

            missing_researchers = [r for r in REQUIRED_RESEARCHERS if r not in found_researchers]
            if not missing_researchers:
                print(f"PASS: Component 3 — All 3 researchers found: {[r.title() for r in found_researchers]} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Missing researchers: {missing_researchers}")
                print(f"INFO: Found researchers: {found_researchers}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Computed fields present and non-empty (0.20 points)
    # Checks that Papers_Per_Year and Avg_Citations_Per_Paper are non-empty
    # numeric values for all 3 data rows. These are derived fields that must
    # be computed.
    # This FAILS on initial_env (no file) -> PASSES on golden_env
    try:
        if not data_rows:
            print("FAIL: Component 4 — No data rows found")
        else:
            # Find computed column indices
            ppy_idx = None
            acpp_idx = None
            for i, h in enumerate(header_row):
                h_lower = h.lower().replace(' ', '_')
                if h_lower == 'papers_per_year':
                    ppy_idx = i
                elif h_lower == 'avg_citations_per_paper':
                    acpp_idx = i

            rows_with_data = [r for r in data_rows if len(r) > 0]
            computed_failures = []

            if ppy_idx is None or acpp_idx is None:
                computed_failures.append(
                    f"Computed columns not found (ppy_idx={ppy_idx}, acpp_idx={acpp_idx})"
                )
            else:
                for idx, row in enumerate(rows_with_data):
                    # Check Papers_Per_Year
                    if ppy_idx >= len(row) or not str(row[ppy_idx]).strip():
                        computed_failures.append(
                            f"Papers_Per_Year empty in data row {idx+1}"
                        )
                    else:
                        try:
                            float(str(row[ppy_idx]).strip())
                        except ValueError:
                            computed_failures.append(
                                f"Papers_Per_Year non-numeric in row {idx+1}: '{row[ppy_idx]}'"
                            )

                    # Check Avg_Citations_Per_Paper
                    if acpp_idx >= len(row) or not str(row[acpp_idx]).strip():
                        computed_failures.append(
                            f"Avg_Citations_Per_Paper empty in data row {idx+1}"
                        )
                    else:
                        try:
                            float(str(row[acpp_idx]).strip())
                        except ValueError:
                            computed_failures.append(
                                f"Avg_Citations_Per_Paper non-numeric in row {idx+1}: '{row[acpp_idx]}'"
                            )

            if not computed_failures and rows_with_data:
                print("PASS: Component 4 — Computed fields (Papers_Per_Year, Avg_Citations_Per_Paper) present and numeric for all rows (0.20 pts)")
                total_score += 0.20
            else:
                for fail_msg in computed_failures:
                    print(f"FAIL: Component 4 — {fail_msg}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Supporting data fields non-empty (0.15 points)
    # Checks that Current_Institution, PhD_Year, Total_Papers, Total_Citations,
    # Top_Venue, and H_Index are all populated for each data row.
    # This FAILS on initial_env (no file) -> PASSES on golden_env
    try:
        if not data_rows:
            print("FAIL: Component 5 — No data rows found")
        else:
            supporting_cols = [
                'Current_Institution',
                'PhD_Year',
                'Total_Papers',
                'Total_Citations',
                'Top_Venue',
                'H_Index',
            ]

            # Map column names to indices
            col_indices = {}
            for i, h in enumerate(header_row):
                h_lower = h.lower().replace(' ', '_')
                for sc in supporting_cols:
                    if h_lower == sc.lower().replace(' ', '_'):
                        col_indices[sc] = i

            supporting_failures = []
            rows_with_data = [r for r in data_rows if len(r) > 0]

            for sc in supporting_cols:
                if sc not in col_indices:
                    supporting_failures.append(
                        f"Supporting column '{sc}' not found in header"
                    )

            if not supporting_failures:
                for idx, row in enumerate(rows_with_data):
                    for sc, cidx in col_indices.items():
                        if cidx >= len(row) or not str(row[cidx]).strip():
                            supporting_failures.append(
                                f"Column '{sc}' empty in data row {idx+1}"
                            )

            if not supporting_failures and rows_with_data:
                print("PASS: Component 5 — All supporting data fields populated for all rows (0.15 pts)")
                total_score += 0.15
            else:
                for fail_msg in supporting_failures:
                    print(f"FAIL: Component 5 — {fail_msg}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
