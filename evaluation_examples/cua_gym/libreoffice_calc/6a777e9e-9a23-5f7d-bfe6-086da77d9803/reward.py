"""
Reward Script: Collect alignment/RLHF/instruction-tuning papers from arXiv cs.LG Feb 2024
Task ID: osworld_multi_apps_arxiv_llms_calc_006
Domain: libreoffice_calc (ODS file)
Scoring:
  - Component 1: At least 8 data rows present (0.3 points)
  - Component 2: All Topic values are from the allowed set (0.3 points)
  - Component 3: Rows are sorted by Date ascending (0.4 points)
Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_arxiv_llms_calc_006'
FILE_PATH = f'{WORKDIR}/alignment_papers.ods'

ALLOWED_TOPICS = {'Instruction Tuning', 'RLHF', 'Alignment', 'Other'}


def get_cell_value(cell):
    """Extract text value from ODF table cell."""
    try:
        from odf.text import P
        ps = cell.getElementsByType(P)
        texts = []
        for p in ps:
            if p.firstChild is not None:
                texts.append(p.firstChild.data)
        return "".join(texts)
    except Exception:
        return ""


def load_ods_rows(file_path):
    """Load all rows from the first sheet of an ODS file.
    Returns list of lists of string values (excluding header row).
    Also returns the header row separately.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell

    doc = load(file_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        return None, []

    sheet = sheets[0]
    rows = sheet.getElementsByType(TableRow)
    all_rows = []
    for row in rows:
        cells = row.getElementsByType(TableCell)
        values = [get_cell_value(cell) for cell in cells]
        # Pad to 5 columns if needed
        while len(values) < 5:
            values.append("")
        all_rows.append(values[:5])

    header = all_rows[0] if all_rows else []
    data_rows = all_rows[1:] if len(all_rows) > 1 else []
    return header, data_rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the ODS file
    try:
        from odf.opendocument import load as odf_load
    except ImportError as e:
        print(f"CRITICAL: odfpy not available: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        header, data_rows = load_ods_rows(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if header is None:
        print("CRITICAL: No sheets found in file")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: File loaded. Header: {header}")
    print(f"INFO: Data rows count: {len(data_rows)}")

    # Precondition gate: headers must be present and correct
    expected_headers = ['arXiv ID', 'Title', 'Authors', 'Date', 'Topic']
    if header != expected_headers:
        print(f"WARN: Headers don't match expected {expected_headers}, got {header}")
        # Still proceed — agent may have rearranged columns

    # Component 1: At least 8 data rows exist (0.3 points)
    # This FAILS on initial (0 data rows) and PASSES on golden (10 data rows)
    try:
        row_count = len(data_rows)
        if row_count >= 8:
            print(f"PASS: Component 1 — At least 8 data rows found ({row_count} rows) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected at least 8 data rows, found {row_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    if len(data_rows) == 0:
        # No data to check further components
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Determine column indices based on headers
    try:
        date_col_idx = header.index('Date') if 'Date' in header else 3
        topic_col_idx = header.index('Topic') if 'Topic' in header else 4
    except Exception:
        date_col_idx = 3
        topic_col_idx = 4

    # Component 2: All Topic values are from the allowed set (0.3 points)
    # This FAILS on initial (no data rows = no topics to check, but no rows means fail for min count)
    # On golden, all 10 rows have valid topics
    try:
        invalid_topics = []
        missing_topics = []
        for i, row in enumerate(data_rows):
            topic = row[topic_col_idx].strip() if topic_col_idx < len(row) else ""
            if not topic:
                missing_topics.append(i + 2)  # +2 for 1-indexed + header
            elif topic not in ALLOWED_TOPICS:
                invalid_topics.append((i + 2, topic))

        if not invalid_topics and not missing_topics:
            print(f"PASS: Component 2 — All {len(data_rows)} rows have valid Topic values from allowed set (0.3 pts)")
            total_score += 0.3
        else:
            if invalid_topics:
                print(f"FAIL: Component 2 — Invalid topic values found: {invalid_topics}")
            if missing_topics:
                print(f"FAIL: Component 2 — Missing topic values in rows: {missing_topics}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rows are sorted by Date ascending (0.4 points)
    # This FAILS on initial (no data rows) and PASSES on golden (dates in ascending order)
    try:
        dates = []
        invalid_date_rows = []
        for i, row in enumerate(data_rows):
            date_str = row[date_col_idx].strip() if date_col_idx < len(row) else ""
            if not date_str:
                invalid_date_rows.append(i + 2)
                dates.append(None)
            else:
                # Parse date string "YYYY-MM-DD"
                try:
                    # Handle possible date format variations
                    parts = date_str.replace('/', '-').split('-')
                    if len(parts) == 3:
                        dates.append(date_str[:10])  # Take first 10 chars "YYYY-MM-DD"
                    else:
                        dates.append(date_str)
                except Exception:
                    dates.append(date_str)

        # Check ascending order (skip None values for comparison)
        valid_dates = [d for d in dates if d is not None]
        is_sorted = all(valid_dates[i] <= valid_dates[i+1] for i in range(len(valid_dates)-1))

        if invalid_date_rows:
            print(f"WARN: Component 3 — Missing/invalid dates in rows: {invalid_date_rows}")

        if is_sorted and len(valid_dates) >= 8:
            print(f"PASS: Component 3 — Rows are sorted by Date ascending ({len(valid_dates)} valid dates) (0.4 pts)")
            total_score += 0.4
        elif not is_sorted:
            # Find first out-of-order pair
            for i in range(len(valid_dates)-1):
                if valid_dates[i] > valid_dates[i+1]:
                    print(f"FAIL: Component 3 — Rows not sorted ascending; date[{i}]={valid_dates[i]} > date[{i+1}]={valid_dates[i+1]}")
                    break
        else:
            print(f"FAIL: Component 3 — Not enough valid dates ({len(valid_dates)}) to verify sort order")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
