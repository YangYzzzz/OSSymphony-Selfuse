"""
Reward Script: Add Yann LeCun row to researchers.ods
Task ID: osworld_multi_apps_web_scholar_001
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: File has 5 rows total (header + 4 data rows incl. Yann LeCun) — 0.3 pts
  Component 2: Last row Name='Yann LeCun', Affiliation='New York University / Meta AI' — 0.3 pts
  Component 3: H_Index=138, Total_Citations in [700000, 800000] range, Top_Paper_Citations=62000 — 0.2 pts
  Component 4: Top_Paper title contains expected key phrase — 0.2 pts
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_scholar_001'
FILE_PATH = f'{WORKDIR}/researchers.ods'


def get_rows_from_ods(filepath):
    """
    Parse an ODS file and return a list of rows, each row being a list of string values.
    Uses the odf library (odfpy) available on the VM.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(filepath)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        return None, "No sheets found in ODS file"

    sheet = sheets[0]
    rows = sheet.getElementsByType(TableRow)

    parsed_rows = []
    for row in rows:
        cells = row.getElementsByType(TableCell)
        row_data = []
        for cell in cells:
            ps = cell.getElementsByType(P)
            text = str(ps[0]) if ps else None
            row_data.append(text)
        parsed_rows.append(row_data)

    return parsed_rows, None


def verify_task(file_path):
    """
    Verify that Yann LeCun's row was correctly added to researchers.ods.
    Returns a float between 0.0 and 1.0 representing task completion.
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load ODS data
    try:
        rows, error = get_rows_from_ods(file_path)
        if error:
            print(f"CRITICAL: Failed to load ODS file: {error}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: headers must be present
    if not rows:
        print("CRITICAL: No rows found in file")
        print("REWARD: 0.0")
        return 0.0

    header_row = rows[0]
    expected_headers = ['Name', 'Affiliation', 'H_Index', 'Total_Citations', 'Top_Paper', 'Top_Paper_Citations']
    headers_present = all(h in header_row for h in expected_headers)
    if not headers_present:
        print(f"CRITICAL: Expected headers not found. Got: {header_row}")
        print("REWARD: 0.0")
        return 0.0

    # Determine column indices from headers
    try:
        col_name = header_row.index('Name')
        col_affil = header_row.index('Affiliation')
        col_h_index = header_row.index('H_Index')
        col_total_cit = header_row.index('Total_Citations')
        col_top_paper = header_row.index('Top_Paper')
        col_top_paper_cit = header_row.index('Top_Paper_Citations')
    except ValueError as e:
        print(f"CRITICAL: Cannot find column index: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Data rows (excluding header)
    data_rows = rows[1:]

    # Component 1: File has 4 data rows (3 existing + 1 new Yann LeCun row) (0.3 points)
    # Initial file has 3 data rows; golden must have 4
    try:
        row_count = len(data_rows)
        if row_count >= 4:
            print(f"PASS: Component 1 — Data row count is {row_count} (>= 4, Yann LeCun row added) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected at least 4 data rows, found {row_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find Yann LeCun row (search in all data rows, not just last)
    lecun_row = None
    for row in data_rows:
        if len(row) > col_name and row[col_name] and 'Yann LeCun' in str(row[col_name]):
            lecun_row = row
            break

    # Component 2: Yann LeCun row has correct Name and Affiliation (0.3 points)
    try:
        if lecun_row is None:
            print("FAIL: Component 2 — No row found with Name='Yann LeCun'")
        else:
            name_val = lecun_row[col_name] if len(lecun_row) > col_name else None
            affil_val = lecun_row[col_affil] if len(lecun_row) > col_affil else None

            name_ok = name_val is not None and str(name_val).strip() == 'Yann LeCun'
            # Affiliation should contain NYU/Meta AI reference (flexible matching)
            affil_ok = (affil_val is not None and
                       'New York University' in str(affil_val) and
                       'Meta' in str(affil_val))

            if name_ok and affil_ok:
                print(f"PASS: Component 2 — Name='{name_val}', Affiliation='{affil_val}' (0.3 pts)")
                total_score += 0.3
            else:
                if not name_ok:
                    print(f"FAIL: Component 2 — Name mismatch. Expected 'Yann LeCun', found: {repr(name_val)}")
                if not affil_ok:
                    print(f"FAIL: Component 2 — Affiliation mismatch. Expected contains 'New York University' and 'Meta', found: {repr(affil_val)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: H_Index=138, Total_Citations ~750000, Top_Paper_Citations=62000 (0.2 points)
    try:
        if lecun_row is None:
            print("FAIL: Component 3 — No Yann LeCun row to check numeric values")
        else:
            h_index_val = lecun_row[col_h_index] if len(lecun_row) > col_h_index else None
            total_cit_val = lecun_row[col_total_cit] if len(lecun_row) > col_total_cit else None
            top_cit_val = lecun_row[col_top_paper_cit] if len(lecun_row) > col_top_paper_cit else None

            h_index_ok = False
            total_cit_ok = False
            top_cit_ok = False

            try:
                h_index_ok = h_index_val is not None and int(float(str(h_index_val))) == 138
            except (ValueError, TypeError):
                pass

            try:
                # Task says ~750000, so accept range [700000, 800000]
                total_cit_num = int(float(str(total_cit_val))) if total_cit_val else 0
                total_cit_ok = 700000 <= total_cit_num <= 800000
            except (ValueError, TypeError):
                pass

            try:
                top_cit_ok = top_cit_val is not None and int(float(str(top_cit_val))) == 62000
            except (ValueError, TypeError):
                pass

            if h_index_ok and total_cit_ok and top_cit_ok:
                print(f"PASS: Component 3 — H_Index={h_index_val}, Total_Citations={total_cit_val}, Top_Paper_Citations={top_cit_val} (0.2 pts)")
                total_score += 0.2
            else:
                if not h_index_ok:
                    print(f"FAIL: Component 3 — H_Index mismatch. Expected 138, found: {repr(h_index_val)}")
                if not total_cit_ok:
                    print(f"FAIL: Component 3 — Total_Citations mismatch. Expected ~750000 [700000-800000], found: {repr(total_cit_val)}")
                if not top_cit_ok:
                    print(f"FAIL: Component 3 — Top_Paper_Citations mismatch. Expected 62000, found: {repr(top_cit_val)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Top_Paper title is correct (0.2 points)
    try:
        if lecun_row is None:
            print("FAIL: Component 4 — No Yann LeCun row to check top paper")
        else:
            top_paper_val = lecun_row[col_top_paper] if len(lecun_row) > col_top_paper else None
            # Expected: 'Gradient-based learning applied to document recognition'
            # Check for key terms (case-insensitive, flexible)
            if top_paper_val is not None:
                paper_lower = str(top_paper_val).lower()
                paper_ok = ('gradient' in paper_lower and
                           'learning' in paper_lower and
                           'document' in paper_lower)
            else:
                paper_ok = False

            if paper_ok:
                print(f"PASS: Component 4 — Top_Paper='{top_paper_val}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 4 — Top_Paper mismatch. Expected contains 'gradient', 'learning', 'document'. Found: {repr(top_paper_val)}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
verify_task(FILE_PATH)
