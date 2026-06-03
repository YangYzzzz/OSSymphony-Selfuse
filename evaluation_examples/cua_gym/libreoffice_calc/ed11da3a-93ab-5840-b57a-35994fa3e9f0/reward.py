"""
Reward Script: Fill blank cells in cv_researchers.ods faculty tracker
Task ID: osworld_multi_apps_web_scholar_004
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: Fei-Fei Li H_Index = 95                                      0.2 pts
  Component 2: Jitendra Malik Specialization = 'Computer Vision, Robotics'  0.2 pts
  Component 3: Jitendra Malik Best_Known_For = 'Normalized Cuts'             0.2 pts
  Component 4: Kaiming He H_Index = 62                                       0.2 pts
  Component 5: Devi Parikh Specialization = 'Vision-Language'               0.2 pts
  Total: 1.0
"""

import os
import odf.opendocument
import odf.table
import odf.text
from odf.namespaces import TABLENS

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_scholar_004'
FILE_PATH = f'{WORKDIR}/cv_researchers.ods'


def get_sheet_data(filepath):
    """
    Load the ODS file and return a dict mapping (row_idx, col_idx) -> cell_text
    for the first sheet, using 0-based indexing.
    Accounts for table:number-columns-repeated attributes via TABLENS namespace.
    Returns (data_dict, error_string_or_None).
    """
    try:
        doc = odf.opendocument.load(filepath)
    except Exception as e:
        return None, str(e)

    sheets = doc.spreadsheet.getElementsByType(odf.table.Table)
    if not sheets:
        return None, "No sheets found in document"

    sheet = sheets[0]
    data = {}
    repeat_key = (TABLENS, 'number-columns-repeated')

    for row_idx, row in enumerate(sheet.getElementsByType(odf.table.TableRow)):
        col_idx = 0
        for cell in row.childNodes:
            if not hasattr(cell, 'qname'):
                continue
            if cell.qname[1] not in ('table-cell', 'covered-table-cell'):
                continue
            repeat = int(cell.attributes.get(repeat_key, '1'))
            texts = [str(p) for p in cell.getElementsByType(odf.text.P)]
            text = '|'.join(texts).strip()
            for _ in range(repeat):
                data[(row_idx, col_idx)] = text
                col_idx += 1

    return data, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Column mapping (0-indexed):
      0: Name
      1: Institution
      2: H_Index
      3: Specialization
      4: Best_Known_For

    Row mapping (0-indexed, row 0 is header):
      1: Fei-Fei Li
      2: Jitendra Malik
      3: Kaiming He
      4: Devi Parikh
    """
    total_score = 0.0

    # Load the ODS file
    try:
        data, err = get_sheet_data(file_path)
        if data is None:
            print(f"CRITICAL: Cannot parse ODS file {file_path}: {err}")
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify the file has the expected structure (header row)
    try:
        name_header = data.get((0, 0), '')
        h_index_header = data.get((0, 2), '')
        if name_header != 'Name' or h_index_header != 'H_Index':
            print(f"CRITICAL: Unexpected file structure. Headers found: {[data.get((0,i),'') for i in range(5)]}")
            print("REWARD: 0.0")
            return 0.0
        print(f"PASS: File structure verified — header row present")
    except Exception as e:
        print(f"ERROR: Could not verify file structure: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Fei-Fei Li H_Index = 95 (0.2 points)
    # Row 1, Column 2 — was blank in initial_env; must be '95' in golden_env.
    try:
        ffl_h_index = data.get((1, 2), '')
        expected = '95'
        if ffl_h_index.strip() == expected:
            print(f"PASS: Component 1 — Fei-Fei Li H_Index = '{ffl_h_index}' (expected '{expected}') (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Fei-Fei Li H_Index: expected '{expected}', found '{ffl_h_index}'")
    except Exception as e:
        print(f"ERROR: Component 1 (Fei-Fei Li H_Index) — {e}")

    # Component 2: Jitendra Malik Specialization = 'Computer Vision, Robotics' (0.2 points)
    # Row 2, Column 3 — was blank in initial_env.
    try:
        jm_spec = data.get((2, 3), '')
        expected = 'Computer Vision, Robotics'
        if jm_spec.strip() == expected:
            print(f"PASS: Component 2 — Jitendra Malik Specialization = '{jm_spec}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 2 — Jitendra Malik Specialization: expected '{expected}', found '{jm_spec}'")
    except Exception as e:
        print(f"ERROR: Component 2 (Jitendra Malik Specialization) — {e}")

    # Component 3: Jitendra Malik Best_Known_For = 'Normalized Cuts' (0.2 points)
    # Row 2, Column 4 — was blank in initial_env.
    try:
        jm_bkf = data.get((2, 4), '')
        expected = 'Normalized Cuts'
        if jm_bkf.strip() == expected:
            print(f"PASS: Component 3 — Jitendra Malik Best_Known_For = '{jm_bkf}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Jitendra Malik Best_Known_For: expected '{expected}', found '{jm_bkf}'")
    except Exception as e:
        print(f"ERROR: Component 3 (Jitendra Malik Best_Known_For) — {e}")

    # Component 4: Kaiming He H_Index = 62 (0.2 points)
    # Row 3, Column 2 — was blank in initial_env.
    try:
        kh_h_index = data.get((3, 2), '')
        expected = '62'
        if kh_h_index.strip() == expected:
            print(f"PASS: Component 4 — Kaiming He H_Index = '{kh_h_index}' (expected '{expected}') (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Kaiming He H_Index: expected '{expected}', found '{kh_h_index}'")
    except Exception as e:
        print(f"ERROR: Component 4 (Kaiming He H_Index) — {e}")

    # Component 5: Devi Parikh Specialization = 'Vision-Language' (0.2 points)
    # Row 4, Column 3 — was blank in initial_env.
    try:
        dp_spec = data.get((4, 3), '')
        expected = 'Vision-Language'
        if dp_spec.strip() == expected:
            print(f"PASS: Component 5 — Devi Parikh Specialization = '{dp_spec}' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 5 — Devi Parikh Specialization: expected '{expected}', found '{dp_spec}'")
    except Exception as e:
        print(f"ERROR: Component 5 (Devi Parikh Specialization) — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
