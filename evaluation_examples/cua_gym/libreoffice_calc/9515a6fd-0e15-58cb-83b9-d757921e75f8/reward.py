"""
Reward Script: Extract email data into spreadsheet and compute average
Task ID: osworld_multi_apps_email_data_007
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: 5 data rows present (Sender, Date, Progress columns) — 0.35 pts
  Component 2: Data values match expected email extraction (correct senders/dates/progress) — 0.35 pts
  Component 3: Rows sorted by Date ascending — 0.15 pts
  Component 4: D2 contains AVERAGE formula (or computed value ~56.2) — 0.15 pts
  Total: 1.0
"""

import os
import sys

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_email_data_007'
FILE_PATH = f'{WORKDIR}/project_tracker.ods'

# Ground truth from 5 emails in Project Alpha folder (sorted by date)
EXPECTED_ROWS = [
    ('carol.lee@techcorp.com',      '2025-03-03', 22),
    ('alice.morgan@techcorp.com',   '2025-03-10', 35),
    ('bob.stevenson@techcorp.com',  '2025-03-17', 58),
    ('david.park@techcorp.com',     '2025-03-24', 75),
    ('alice.morgan@techcorp.com',   '2025-03-31', 91),
]
EXPECTED_AVERAGE = 56.2  # (22+35+58+75+91)/5


def get_ods_rows(file_path):
    """
    Read all data rows from the first sheet of an ODS file using the odf library.
    Returns list of row dicts with keys: sender, date, progress
    Also returns raw rows for sorting check.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(file_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        raise ValueError("No sheets found in ODS file")

    sheet = sheets[0]
    rows = sheet.getElementsByType(TableRow)

    result = []
    d2_formula = None
    d2_value = None

    for i, row in enumerate(rows):
        cells = row.getElementsByType(TableCell)
        row_data = []
        for j, cell in enumerate(cells):
            ptext = cell.getElementsByType(P)
            if ptext:
                row_data.append(str(ptext[0]).strip())
            else:
                row_data.append(None)

            # Capture D2 formula and value (row 1 = index 1, col 3 = index 3)
            if i == 1 and j == 3:
                formula = cell.getAttribute('formula')
                val = cell.getAttribute('value')
                if formula:
                    d2_formula = formula
                if val:
                    d2_value = val

        if i == 0:
            # Skip header row
            continue
        result.append(row_data)

    return result, d2_formula, d2_value


def normalize_sender(s):
    """Extract email address from sender string, lowercase."""
    if s is None:
        return ''
    s = s.strip().lower()
    # Handle "Name <email>" format
    if '<' in s and '>' in s:
        start = s.index('<') + 1
        end = s.index('>')
        return s[start:end].strip()
    return s


def normalize_date(d):
    """Normalize date to YYYY-MM-DD format."""
    if d is None:
        return ''
    d = str(d).strip()
    # Already in YYYY-MM-DD
    if len(d) == 10 and d[4] == '-' and d[7] == '-':
        return d
    return d


def normalize_progress(p):
    """Normalize progress value, strip % if present, return int."""
    if p is None:
        return None
    p = str(p).strip()
    p = p.replace('%', '').strip()
    try:
        return int(float(p))
    except (ValueError, TypeError):
        return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file — precondition gate
    try:
        data_rows, d2_formula, d2_value = get_ods_rows(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ----------------------------------------------------------------
    # Component 1: 5 data rows present with Sender, Date, Progress columns (0.35 pts)
    # This fails on initial (only header row) and passes on golden (5 data rows)
    # ----------------------------------------------------------------
    try:
        non_empty_rows = []
        for row in data_rows:
            # A row is valid if it has at least 3 non-empty cells (Sender, Date, Progress)
            if (len(row) >= 3 and
                    row[0] and str(row[0]).strip() and
                    row[1] and str(row[1]).strip() and
                    row[2] and str(row[2]).strip()):
                non_empty_rows.append(row)

        if len(non_empty_rows) == 5:
            print(f"PASS: Component 1 — 5 data rows present (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 — expected 5 data rows, found {len(non_empty_rows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # ----------------------------------------------------------------
    # Component 2: Data values match expected email extraction (0.35 pts)
    # Checks senders, dates, and progress values match the 5 emails
    # ----------------------------------------------------------------
    try:
        if len(non_empty_rows) < 5:
            print("FAIL: Component 2 — not enough rows to check data accuracy")
        else:
            # Build a set of actual (sender, date, progress) tuples for comparison
            actual_set = set()
            for row in non_empty_rows:
                sender = normalize_sender(row[0])
                date = normalize_date(row[1])
                progress = normalize_progress(row[2])
                if sender and date and progress is not None:
                    actual_set.add((sender, date, progress))

            # Build expected set
            expected_set = set()
            for (sender, date, progress) in EXPECTED_ROWS:
                expected_set.add((sender, date, progress))

            matches = actual_set & expected_set
            mismatches = expected_set - actual_set
            extras = actual_set - expected_set

            if len(matches) == 5:
                print(f"PASS: Component 2 — all 5 rows match expected data (0.35 pts)")
                total_score += 0.35
            else:
                print(f"FAIL: Component 2 — {len(matches)}/5 rows match.")
                print(f"  Expected but missing: {mismatches}")
                print(f"  Unexpected extras: {extras}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # ----------------------------------------------------------------
    # Component 3: Rows sorted by Date ascending (0.15 pts)
    # Sorted order: 2025-03-03, 2025-03-10, 2025-03-17, 2025-03-24, 2025-03-31
    # ----------------------------------------------------------------
    try:
        if len(non_empty_rows) < 5:
            print("FAIL: Component 3 — not enough rows to check sort order")
        else:
            dates_in_order = [normalize_date(row[1]) for row in non_empty_rows]
            is_sorted = all(dates_in_order[i] <= dates_in_order[i+1]
                            for i in range(len(dates_in_order)-1))
            if is_sorted:
                print(f"PASS: Component 3 — rows sorted by date ascending: {dates_in_order} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 — rows NOT sorted by date. Order: {dates_in_order}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # ----------------------------------------------------------------
    # Component 4: D2 contains AVERAGE formula or computed value ~56.2 (0.15 pts)
    # Formula: =AVERAGE(C2:C6) or equivalent, result should be 56.2
    # ----------------------------------------------------------------
    try:
        d4_pass_reason = None

        if d2_formula:
            # Check formula contains AVERAGE and C2:C6 (or equivalent range)
            formula_upper = d2_formula.upper()
            if 'AVERAGE' in formula_upper and 'C2' in formula_upper and 'C6' in formula_upper:
                d4_pass_reason = f"formula match: {d2_formula}"

        if d4_pass_reason is None and d2_value:
            try:
                actual_avg = float(d2_value)
                if abs(actual_avg - EXPECTED_AVERAGE) < 0.5:
                    d4_pass_reason = f"computed value match: {actual_avg}"
                else:
                    print(f"FAIL: D2 computed value = {actual_avg}, expected ~{EXPECTED_AVERAGE}")
            except ValueError:
                print(f"FAIL: D2 value not numeric: {d2_value}")

        if d4_pass_reason is not None:
            print(f"PASS: Component 4 — D2 AVERAGE check passed ({d4_pass_reason}) (0.15 pts)")
            total_score += 0.15
        else:
            if not d2_formula and not d2_value:
                print(f"FAIL: Component 4 — D2 is empty (no formula or value found)")
            else:
                print(f"FAIL: Component 4 — D2 does not match AVERAGE(C2:C6)=56.2. formula={d2_formula}, value={d2_value}")
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
