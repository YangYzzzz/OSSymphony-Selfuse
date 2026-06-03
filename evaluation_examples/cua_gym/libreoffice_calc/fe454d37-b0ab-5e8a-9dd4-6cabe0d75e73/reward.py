"""
Reward Script: Browse arxiv cs.AI Jan 2024, collect papers about
reasoning/planning/agent, fill agent_papers.ods with data rows
and COUNTIF summary formulas in G2:G4.

Task ID: osworld_multi_apps_arxiv_llms_calc_008
Domain: libreoffice_calc
Scoring:
  Component 1 (0.4): At least 6 data rows with arXiv ID, title, authors, keyword
                      in columns A-D; keywords restricted to reasoning/planning/agent
  Component 2 (0.4): COUNTIF formulas present in G2:G4 referencing column D
  Component 3 (0.2): Keyword summary labels in F2:F4 are still
                      reasoning/planning/agent (structure preserved)
"""

import os
import zipfile
import xml.etree.ElementTree as ET
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_008'
FILE_PATH = f'{WORKDIR}/agent_papers.ods'

TABLE_NS = 'urn:oasis:names:tc:opendocument:xmlns:table:1.0'
TEXT_NS  = 'urn:oasis:names:tc:opendocument:xmlns:text:1.0'

VALID_KEYWORDS = {'reasoning', 'planning', 'agent'}


def parse_ods(path):
    """
    Parse ODS (zip of XML) and return a list of rows per sheet.
    Each row is a list of dicts: {'text': str, 'formula': str or None}.
    Handles number-columns-repeated expansion.
    """
    sheets = {}
    with zipfile.ZipFile(path, 'r') as z:
        with z.open('content.xml') as f:
            tree = ET.parse(f)
            root = tree.getroot()

    for table in root.iter(f'{{{TABLE_NS}}}table'):
        sheet_name = table.get(f'{{{TABLE_NS}}}name')
        rows = []
        for row_el in table.findall(f'{{{TABLE_NS}}}table-row'):
            row_data = []
            for cell in row_el.findall(f'{{{TABLE_NS}}}table-cell'):
                formula = cell.get(f'{{{TABLE_NS}}}formula')
                texts = cell.findall(f'.//{{{TEXT_NS}}}p')
                text = ' '.join(t.text or '' for t in texts if t.text)
                row_data.append({'text': text, 'formula': formula})
                repeat = cell.get(f'{{{TABLE_NS}}}number-columns-repeated')
                if repeat and int(repeat) > 1:
                    for _ in range(int(repeat) - 1):
                        row_data.append({'text': '', 'formula': None})
            rows.append(row_data)
        sheets[sheet_name] = rows
    return sheets


def get_cell(rows, row_idx, col_idx):
    """
    Get cell at 1-based row_idx, col_idx. Returns {'text': '', 'formula': None} if out of bounds.
    """
    r = row_idx - 1
    c = col_idx - 1
    if r < 0 or r >= len(rows):
        return {'text': '', 'formula': None}
    row = rows[r]
    if c < 0 or c >= len(row):
        return {'text': '', 'formula': None}
    return row[c]


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load ODS
    try:
        sheets = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the active sheet (Sheet1)
    sheet_name = 'Sheet1'
    if sheet_name not in sheets:
        # Fallback: use first sheet
        if sheets:
            sheet_name = list(sheets.keys())[0]
            print(f"WARN: 'Sheet1' not found, using '{sheet_name}'")
        else:
            print("CRITICAL: No sheets found in ODS file")
            print("REWARD: 0.0")
            return 0.0

    rows = sheets[sheet_name]

    # -----------------------------------------------------------------------
    # Component 1: Data rows populated (0.4 points)
    # At least 6 data rows (rows 2+) with non-empty arXiv ID (col A),
    # non-empty Title (col B), and a valid keyword in col D
    # (one of: reasoning, planning, agent).
    # -----------------------------------------------------------------------
    try:
        data_rows_valid = 0
        data_rows_bad_keyword = 0
        # Iterate data rows starting at row 2 (0-indexed row 1)
        for ri in range(1, len(rows)):  # skip header row 0
            arxiv_id = get_cell(rows, ri + 1, 1)['text'].strip()
            title    = get_cell(rows, ri + 1, 2)['text'].strip()
            keyword  = get_cell(rows, ri + 1, 4)['text'].strip().lower()

            if not arxiv_id and not title:
                continue  # empty row, skip

            if arxiv_id and title:
                if keyword in VALID_KEYWORDS:
                    data_rows_valid += 1
                else:
                    data_rows_bad_keyword += 1

        if data_rows_valid >= 6:
            print(f"PASS: Component 1 — {data_rows_valid} valid data rows with correct keywords (0.4 pts)")
            total_score += 0.4
        elif data_rows_valid >= 3:
            partial = 0.2
            print(f"PARTIAL: Component 1 — only {data_rows_valid} valid data rows (need >= 6), partial ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — only {data_rows_valid} valid data rows (need >= 6); "
                  f"bad_keyword_rows={data_rows_bad_keyword}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: COUNTIF formulas in G2:G4 (0.4 points)
    # Each of G2, G3, G4 must contain a COUNTIF formula referencing column D
    # and one of the F-column cells (F2, F3, F4).
    # The ODS formula attribute looks like: of:=COUNTIF([.D...]:[.D...];[.F?])
    # -----------------------------------------------------------------------
    try:
        countif_hits = 0
        for row_i, col_f in [(2, 'F2'), (3, 'F3'), (4, 'F4')]:
            cell = get_cell(rows, row_i, 7)  # column G = col 7
            formula = cell.get('formula') or ''
            # Must reference column D and some form of F2/F3/F4
            has_countif = 'COUNTIF' in formula.upper()
            has_col_d   = re.search(r'\.D', formula, re.IGNORECASE) is not None
            # Accept any reference to the relevant F row
            f_row_num = str(row_i)
            has_f_ref  = re.search(rf'\.F\$?{f_row_num}', formula, re.IGNORECASE) is not None

            if has_countif and has_col_d and has_f_ref:
                countif_hits += 1
                print(f"  PASS: G{row_i} has COUNTIF formula referencing D and {col_f}: {formula}")
            elif has_countif and has_col_d:
                # Partial: COUNTIF references D column but not exact F row cell
                countif_hits += 0.5
                print(f"  PARTIAL: G{row_i} has COUNTIF formula referencing D but uncertain F ref: {formula}")
            else:
                print(f"  FAIL: G{row_i} missing COUNTIF formula (found: '{formula}')")

        if countif_hits >= 3:
            print(f"PASS: Component 2 — all 3 COUNTIF formulas present in G2:G4 (0.4 pts)")
            total_score += 0.4
        elif countif_hits >= 2:
            partial = 0.25
            print(f"PARTIAL: Component 2 — {countif_hits}/3 COUNTIF formulas present ({partial} pts)")
            total_score += partial
        elif countif_hits >= 1:
            partial = 0.13
            print(f"PARTIAL: Component 2 — {countif_hits}/3 COUNTIF formulas present ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — no COUNTIF formulas found in G2:G4")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -----------------------------------------------------------------------
    # Component 3: Summary labels F2:F4 are reasoning/planning/agent (0.2 points)
    # These should be set in the initial file, but we verify they are still
    # present (not accidentally deleted). We only award points if the COUNTIF
    # formulas are also present (i.e., task was completed).
    # -----------------------------------------------------------------------
    try:
        expected_labels = {2: 'reasoning', 3: 'planning', 4: 'agent'}
        label_hits = 0
        for row_i, expected in expected_labels.items():
            cell = get_cell(rows, row_i, 6)  # column F = col 6
            actual = cell['text'].strip().lower()
            if actual == expected:
                label_hits += 1
            else:
                print(f"  FAIL: F{row_i} expected '{expected}', found '{actual}'")

        # Only award these points if COUNTIF formulas were also present
        # (otherwise these labels exist in initial_env too and would give 0.2 on initial)
        if label_hits == 3 and countif_hits >= 3:
            print(f"PASS: Component 3 — F2:F4 labels correct (reasoning/planning/agent) (0.2 pts)")
            total_score += 0.2
        elif label_hits == 3:
            print(f"SKIP: Component 3 — F2:F4 labels correct but COUNTIF formulas not complete; "
                  f"not awarding to avoid pre-condition scoring")
        else:
            print(f"FAIL: Component 3 — {label_hits}/3 labels correct in F2:F4")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in given env
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
