"""
Reward Script: Add 4 award entries to awards.ods and apply filter for EMNLP rows
Task ID: osworld_multi_apps_acl_awards_calc_002
Domain: libreoffice_calc
Scoring:
  Component 1: 4 data rows present in the spreadsheet (0.4 pts)
  Component 2: Both EMNLP entries contain correct data (0.3 pts)
  Component 3: AutoFilter active with Conference='EMNLP' filter, ACL rows hidden (0.3 pts)
Total: 1.0
"""

import os
import zipfile
from xml.etree import ElementTree as ET

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_acl_awards_calc_002'

# ODS XML namespaces
NS = {
    'office': 'urn:oasis:names:tc:opendocument:xmlns:office:1.0',
    'table':  'urn:oasis:names:tc:opendocument:xmlns:table:1.0',
    'text':   'urn:oasis:names:tc:opendocument:xmlns:text:1.0',
    'calcext': 'urn:org:documentfoundation:names:experimental:calc:xmlns:calcext:1.0',
}


def parse_ods(file_path):
    """
    Parse an ODS file and return the row data from the first sheet.
    Returns: (rows, raw_rows, has_filter, filter_condition, filtered_row_indices)
    - rows: list of lists of cell text values (all rows including header)
    - has_filter: whether a database-range/filter is defined
    - filter_condition: dict describing filter (field_number, operator, value)
    - filtered_row_indices: set of 0-based row indices that are hidden by filter
    """
    with zipfile.ZipFile(file_path, 'r') as z:
        content = z.read('content.xml')
    root = ET.fromstring(content)

    body = root.find('office:body/office:spreadsheet', NS)
    table = body.find('table:table', NS)

    # Extract all rows and track visibility
    rows = []
    filtered_row_indices = set()
    raw_table_rows = table.findall('table:table-row', NS)
    for idx, tr in enumerate(raw_table_rows):
        visibility = tr.get('{urn:oasis:names:tc:opendocument:xmlns:table:1.0}visibility', 'visible')
        cells = tr.findall('table:table-cell', NS)
        row_values = []
        for cell in cells:
            tp = cell.find('text:p', NS)
            row_values.append(tp.text if tp is not None and tp.text else '')
        rows.append(row_values)
        if visibility == 'filter':
            filtered_row_indices.add(idx)

    # Check for database-range (filter) definition
    db_ranges = body.find('table:database-ranges', NS)
    has_filter = False
    filter_condition = {}
    if db_ranges is not None:
        for db_range in db_ranges.findall('table:database-range', NS):
            display_buttons = db_range.get(
                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}display-filter-buttons', 'false'
            )
            if display_buttons == 'true':
                has_filter = True
                filt = db_range.find('table:filter', NS)
                if filt is not None:
                    cond = filt.find('table:filter-condition', NS)
                    if cond is not None:
                        filter_condition = {
                            'field_number': cond.get(
                                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}field-number', ''),
                            'operator': cond.get(
                                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}operator', ''),
                            'value': cond.get(
                                '{urn:oasis:names:tc:opendocument:xmlns:table:1.0}value', ''),
                        }

    return rows, filtered_row_indices, has_filter, filter_condition


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        rows, filtered_row_indices, has_filter, filter_condition = parse_ods(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot parse file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: header row must exist
    if not rows:
        print("FAIL: No rows found in spreadsheet")
        print("REWARD: 0.0")
        return 0.0

    header = rows[0]
    expected_headers = ['Year', 'Conference', 'Paper Title', 'Authors', 'Award Type']
    for i, h in enumerate(expected_headers):
        if i >= len(header) or header[i] != h:
            print(f"FAIL: Header mismatch at col {i}: expected '{h}', got '{header[i] if i < len(header) else None}'")
            print("REWARD: 0.0")
            return 0.0

    data_rows = rows[1:]  # exclude header

    # Component 1: Exactly 4 data rows present (0.4 pts)
    # This fails on initial_env (0 data rows) and passes on golden (4 data rows).
    try:
        n_rows = len(data_rows)
        if n_rows == 4:
            print(f"PASS: Component 1 — 4 data rows present (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 4 data rows, found {n_rows}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Both EMNLP entries are present with correct data (0.3 pts)
    # Expected EMNLP entries (from task context ground truth):
    EMNLP_ENTRIES = [
        {
            'year': '2021',
            'title': 'Masked Language Modeling and the Distributional Hypothesis',
            'authors': 'Koustuv Sinha, Robin Jia, Dieuwke Hupkes, Joelle Pineau, Adina Williams, Douwe Kiela',
            'award_type': 'Best Paper',
        },
        {
            'year': '2022',
            'title': 'Entity Tracking in Language Models',
            'authors': 'Najoung Kim, Sebastian Schuster',
            'award_type': 'Best Paper',
        },
    ]
    try:
        emnlp_rows = [r for r in data_rows if len(r) >= 2 and r[1] == 'EMNLP']
        matched = 0
        for expected in EMNLP_ENTRIES:
            found = False
            for row in emnlp_rows:
                # Year is stored as float in ODS (e.g. "2021"), match as string
                year_val = str(row[0]).split('.')[0] if row[0] else ''
                title_val = row[2] if len(row) > 2 else ''
                authors_val = row[3] if len(row) > 3 else ''
                award_val = row[4] if len(row) > 4 else ''
                if (year_val == expected['year']
                        and title_val.strip() == expected['title']
                        and authors_val.strip() == expected['authors']
                        and award_val.strip() == expected['award_type']):
                    found = True
                    break
            if found:
                matched += 1
            else:
                print(f"FAIL: Component 2 — EMNLP entry not found: year={expected['year']}, title='{expected['title']}'")

        if matched == 2:
            print(f"PASS: Component 2 — Both EMNLP entries verified with correct data (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Only {matched}/2 EMNLP entries matched")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: AutoFilter active for Conference=EMNLP, and ACL rows hidden by filter (0.3 pts)
    # This fails on initial_env (no filter) and passes on golden (filter defined + ACL rows hidden).
    try:
        # Check autofilter/database-range is active
        filter_ok = False
        acl_hidden_ok = False

        if has_filter:
            # Filter should be on column index 1 (Conference column, 0-based field-number="1")
            fc_field = filter_condition.get('field_number', '')
            fc_op = filter_condition.get('operator', '')
            fc_val = filter_condition.get('value', '')
            if fc_field == '1' and fc_op == '=' and fc_val == 'EMNLP':
                filter_ok = True
                print(f"PASS: Component 3a — AutoFilter active on Conference='EMNLP'")
            else:
                print(f"FAIL: Component 3a — Filter condition unexpected: field={fc_field}, op={fc_op}, val={fc_val}")
        else:
            print("FAIL: Component 3a — No AutoFilter/database-range found")

        # Check ACL rows are hidden (row indices 3 and 4 in full rows list, i.e. data rows 2 and 3, 0-based)
        # In the full rows list (including header): header=0, data rows=1..4
        # ACL rows are at 1-based positions 3 and 4 (0-based: 3 and 4 including header offset)
        acl_data_row_indices = []
        for i, row in enumerate(data_rows):
            if len(row) >= 2 and row[1] == 'ACL':
                # full rows index = i + 1 (header is index 0)
                full_idx = i + 1
                acl_data_row_indices.append(full_idx)

        if acl_data_row_indices:
            all_acl_hidden = all(idx in filtered_row_indices for idx in acl_data_row_indices)
            # Also verify no EMNLP rows are hidden
            emnlp_data_row_indices = []
            for i, row in enumerate(data_rows):
                if len(row) >= 2 and row[1] == 'EMNLP':
                    full_idx = i + 1
                    emnlp_data_row_indices.append(full_idx)
            all_emnlp_visible = all(idx not in filtered_row_indices for idx in emnlp_data_row_indices)

            if all_acl_hidden and all_emnlp_visible:
                acl_hidden_ok = True
                print(f"PASS: Component 3b — ACL rows hidden by filter, EMNLP rows visible")
            else:
                if not all_acl_hidden:
                    print(f"FAIL: Component 3b — Not all ACL rows are hidden: {acl_data_row_indices}, filtered={filtered_row_indices}")
                if not all_emnlp_visible:
                    print(f"FAIL: Component 3b — Some EMNLP rows are hidden: {emnlp_data_row_indices}, filtered={filtered_row_indices}")
        else:
            print("FAIL: Component 3b — No ACL rows found to check filter visibility")

        if filter_ok and acl_hidden_ok:
            print("PASS: Component 3 — Filter verified: Conference=EMNLP active, ACL rows hidden (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 3 — Filter not fully verified (filter_ok={filter_ok}, acl_hidden_ok={acl_hidden_ok})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path in VM
file_path = f'{WORKDIR}/awards.ods'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
