"""
Reward Script: Research ACL/EMNLP/NAACL/EACL best paper awards 2020-2021 and populate spreadsheet
Task ID: osworld_multi_apps_acl_awards_calc_015
Domain: libreoffice_calc
Scoring:
  Component 1: Sheet1 has 8+ award paper rows with Year, Conference, Title, Authors, Topic Area (0.30 pts)
  Component 2: All 4 required conferences (ACL, EMNLP, NAACL, EACL) are represented in Sheet1 (0.20 pts)
  Component 3: Topics sheet has 5+ unique topic areas with COUNTIF formulas in column B (0.30 pts)
  Component 4: Topics sheet rows sorted by count (COUNTIF result) descending (0.20 pts)
"""

import os
import zipfile
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_015'
FILE_PATH = f'{WORKDIR}/awards_by_topic.ods'


def parse_ods(file_path):
    """
    Parse ODS file using ezodf.
    Returns (doc, error_message). doc is None on failure.
    """
    try:
        import ezodf
        doc = ezodf.opendoc(file_path)
        return doc, None
    except Exception as e:
        return None, str(e)


def get_sheet_data(sheet):
    """
    Extract all non-empty rows from a sheet as list of lists.
    Skips rows where all cells are None.
    """
    rows = []
    for r in range(sheet.nrows()):
        row = []
        for c in range(sheet.ncols()):
            cell = sheet[r, c]
            row.append(cell.value)
        if any(v is not None for v in row):
            rows.append(row)
    return rows


def is_countif_formula(cell_value):
    """Check if cell value is a COUNTIF formula string."""
    if not isinstance(cell_value, str):
        return False
    return 'COUNTIF' in cell_value.upper()


def evaluate_countif_on_topics(topics_rows, sheet1_rows):
    """
    Evaluate COUNTIF counts for topic rows.
    topics_rows[0] = header row, topics_rows[1:] = topic data
    sheet1_rows[0] = header row, sheet1_rows[1:] = data rows

    Returns list of (topic_name, actual_count) pairs for data rows.
    """
    # Extract topic areas from Sheet1 data rows
    topic_areas = []
    for row in sheet1_rows[1:]:  # skip header
        if len(row) >= 5 and row[4] is not None:
            topic_areas.append(str(row[4]).strip())

    results = []
    for row in topics_rows[1:]:  # skip header
        if len(row) >= 1 and row[0] is not None:
            topic_name = str(row[0]).strip()
            # Count occurrences of this topic in Sheet1
            count = sum(1 for t in topic_areas if t == topic_name)
            results.append((topic_name, count))
    return results


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODS document
    doc, err = parse_ods(file_path)
    if doc is None:
        print(f"CRITICAL: Cannot load file {file_path}: {err}")
        print("REWARD: 0.0")
        return 0.0

    # Check that both sheets exist
    sheet_names = [s.name for s in doc.sheets]
    if 'Sheet1' not in sheet_names:
        print(f"CRITICAL: Sheet1 not found. Sheets: {sheet_names}")
        print("REWARD: 0.0")
        return 0.0
    if 'Topics' not in sheet_names:
        print(f"CRITICAL: Topics sheet not found. Sheets: {sheet_names}")
        print("REWARD: 0.0")
        return 0.0

    sheet1 = doc.sheets['Sheet1']
    topics_sheet = doc.sheets['Topics']

    sheet1_rows = get_sheet_data(sheet1)
    topics_rows = get_sheet_data(topics_sheet)

    # -------------------------------------------------------------------------
    # Component 1: Sheet1 has 8+ award paper rows (0.30 pts)
    # Data rows = all rows except the header row (row 0)
    # -------------------------------------------------------------------------
    try:
        # sheet1_rows[0] should be the header
        data_rows = []
        for row in sheet1_rows[1:]:  # skip header row
            # A valid data row needs at least Year, Conference, and Title (cols 0,1,2)
            if len(row) >= 3 and row[0] is not None and row[1] is not None and row[2] is not None:
                data_rows.append(row)

        if len(data_rows) >= 8:
            print(f"PASS: Component 1 — Sheet1 has {len(data_rows)} data rows (>= 8 required) (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 1 — Sheet1 has {len(data_rows)} data rows, need >= 8")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -------------------------------------------------------------------------
    # Component 2: All 4 required conferences present in Sheet1 (0.20 pts)
    # Required: ACL, EMNLP, NAACL, EACL
    # -------------------------------------------------------------------------
    try:
        conferences_in_data = set()
        for row in sheet1_rows[1:]:  # skip header
            if len(row) >= 2 and row[1] is not None:
                conf = str(row[1]).strip().upper()
                conferences_in_data.add(conf)

        required_conferences = {'ACL', 'EMNLP', 'NAACL', 'EACL'}
        missing = required_conferences - conferences_in_data

        if not missing:
            print(f"PASS: Component 2 — All 4 required conferences present: {sorted(conferences_in_data & required_conferences)} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 2 — Missing conferences: {missing}. Found: {conferences_in_data}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # -------------------------------------------------------------------------
    # Component 3: Topics sheet has 5+ unique topic areas with COUNTIF formulas (0.30 pts)
    # -------------------------------------------------------------------------
    try:
        topic_entries = []
        topic_with_countif = []

        for row in topics_rows[1:]:  # skip header
            if len(row) >= 1 and row[0] is not None and str(row[0]).strip():
                topic_name = str(row[0]).strip()
                topic_entries.append(topic_name)
                # Check if column B has a COUNTIF formula
                if len(row) >= 2 and is_countif_formula(row[1]):
                    topic_with_countif.append(topic_name)

        unique_topics = list(set(topic_entries))
        num_with_countif = len(topic_with_countif)

        if len(unique_topics) >= 5 and num_with_countif >= 5:
            print(f"PASS: Component 3 — Topics sheet has {len(unique_topics)} unique topics, {num_with_countif} with COUNTIF formulas (0.30 pts)")
            total_score += 0.30
        elif len(unique_topics) >= 5:
            print(f"FAIL: Component 3 — Topics sheet has {len(unique_topics)} unique topics but only {num_with_countif}/{len(unique_topics)} have COUNTIF formulas")
        else:
            print(f"FAIL: Component 3 — Topics sheet has {len(unique_topics)} unique topics (need >= 5). Topics: {unique_topics}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # -------------------------------------------------------------------------
    # Component 4: Topics sheet is sorted by count descending (0.20 pts)
    # We evaluate the COUNTIF formulas manually by counting in Sheet1
    # -------------------------------------------------------------------------
    try:
        topic_counts = evaluate_countif_on_topics(topics_rows, sheet1_rows)

        if len(topic_counts) < 2:
            print(f"FAIL: Component 4 — Not enough topics to verify sort order (found {len(topic_counts)})")
        else:
            counts_only = [c for _, c in topic_counts]
            # Check descending sort: each count must be >= next count
            is_sorted_desc = all(counts_only[i] >= counts_only[i+1] for i in range(len(counts_only)-1))

            if is_sorted_desc:
                print(f"PASS: Component 4 — Topics sheet is sorted by count descending: {[(t, c) for t, c in topic_counts]} (0.20 pts)")
                total_score += 0.20
            else:
                print(f"FAIL: Component 4 — Topics sheet is NOT sorted by count descending. Counts: {[(t, c) for t, c in topic_counts]}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
