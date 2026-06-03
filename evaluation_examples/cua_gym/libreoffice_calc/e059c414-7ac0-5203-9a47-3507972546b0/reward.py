"""
Reward Script: Extract first-author details from workshop PDFs into a sorted spreadsheet.
Task ID: osworld_multi_apps_pdf_author_extract_010
Domain: libreoffice_calc
Scoring:
  - Component 1: Correct headers (Name, Email, Affiliation, Country) — 0.25 pts
  - Component 2: 8 data rows present with non-empty Name, Affiliation, Country — 0.25 pts
  - Component 3: Data sorted by Country A-Z (primary sort) — 0.25 pts
  - Component 4: Within same Country, data sorted by Name A-Z (secondary sort) — 0.25 pts
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_pdf_author_extract_010'
TARGET_FILE = f'{WORKDIR}/workshop_authors.xlsx'

# Expected headers (case-sensitive as specified in task)
EXPECTED_HEADERS = ['Name', 'Email', 'Affiliation', 'Country']


def verify_task(file_path):
    """
    Verify that the agent correctly extracted first-author data from 8 workshop PDFs,
    created an xlsx with the correct headers, 8 data rows, and sorted by Country then Name.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load workbook (precondition gate)
    try:
        import openpyxl
        wb = openpyxl.load_workbook(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ws = wb.active

    # Read all rows (header + data)
    all_rows = list(ws.iter_rows(values_only=True))
    if len(all_rows) < 1:
        print("FAIL: Spreadsheet is empty")
        print("REWARD: 0.0")
        return 0.0

    header_row = list(all_rows[0]) if all_rows else []
    data_rows = [list(r) for r in all_rows[1:]] if len(all_rows) > 1 else []

    # Component 1: Correct headers — 'Name', 'Email', 'Affiliation', 'Country' (0.25 points)
    # Task explicitly asks for these 4 column headers. This FAILS on initial (no file).
    try:
        # Strip strings for comparison, allow case-insensitive matching with normalized whitespace
        header_normalized = [str(h).strip() if h is not None else '' for h in header_row]
        expected_normalized = EXPECTED_HEADERS[:]

        if header_normalized == expected_normalized:
            print(f"PASS: Component 1 — Headers exactly match: {header_normalized} (0.25 pts)")
            total_score += 0.25
        elif len(header_normalized) == 4 and [h.lower() for h in header_normalized] == [h.lower() for h in expected_normalized]:
            # Case-insensitive match — partial credit (headers present but wrong case)
            print(f"PASS (partial): Component 1 — Headers present (case mismatch): {header_normalized} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected headers {expected_normalized}, found {header_normalized}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: 8 data rows with non-empty Name, Affiliation, Country (0.25 points)
    # The task requires extraction of all 8 workshop paper first authors. FAILS on initial (no file).
    try:
        # Determine column indices based on (possibly normalized) header row
        header_lower = [str(h).strip().lower() if h is not None else '' for h in header_row]
        name_col = header_lower.index('name') if 'name' in header_lower else 0
        affil_col = header_lower.index('affiliation') if 'affiliation' in header_lower else 2
        country_col = header_lower.index('country') if 'country' in header_lower else 3

        if len(data_rows) == 8:
            # Check all rows have non-empty required fields
            valid_rows = 0
            for i, row in enumerate(data_rows):
                name = str(row[name_col]).strip() if row[name_col] is not None else ''
                affil = str(row[affil_col]).strip() if row[affil_col] is not None else ''
                country = str(row[country_col]).strip() if row[country_col] is not None else ''
                if name and affil and country:
                    valid_rows += 1
                else:
                    print(f"  Row {i+2}: missing data — name='{name}', affil='{affil}', country='{country}'")

            if valid_rows == 8:
                print(f"PASS: Component 2 — 8 data rows with all required fields present (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 — Expected 8 complete data rows, found {valid_rows} complete rows out of {len(data_rows)}")
        else:
            print(f"FAIL: Component 2 — Expected 8 data rows, found {len(data_rows)}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Data sorted by Country A-Z (primary sort key) (0.25 points)
    # Task explicitly requires sort by country then by name. FAILS on initial (no file).
    try:
        if len(data_rows) >= 1:
            header_lower = [str(h).strip().lower() if h is not None else '' for h in header_row]
            country_col = header_lower.index('country') if 'country' in header_lower else 3

            countries = []
            for row in data_rows:
                c = str(row[country_col]).strip() if row[country_col] is not None else ''
                countries.append(c)

            countries_sorted = sorted(countries)
            if countries == countries_sorted:
                print(f"PASS: Component 3 — Countries sorted A-Z: {countries} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Country sorting incorrect")
                print(f"  Found:    {countries}")
                print(f"  Expected: {countries_sorted}")
        else:
            print("FAIL: Component 3 — No data rows to check sorting")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Within same Country, data sorted by Name A-Z (secondary sort) (0.25 points)
    # Task requires sort by country then by name within same country. FAILS on initial (no file).
    try:
        if len(data_rows) >= 2:
            header_lower = [str(h).strip().lower() if h is not None else '' for h in header_row]
            name_col = header_lower.index('name') if 'name' in header_lower else 0
            country_col = header_lower.index('country') if 'country' in header_lower else 3

            # Group rows by country and check name sort within each group
            from itertools import groupby

            row_tuples = []
            for row in data_rows:
                name = str(row[name_col]).strip() if row[name_col] is not None else ''
                country = str(row[country_col]).strip() if row[country_col] is not None else ''
                row_tuples.append((country, name))

            # Check that within each run of the same country, names are sorted
            # Collect all country groups and check each
            unsorted_countries = []
            i = 0
            while i < len(row_tuples):
                current_country = row_tuples[i][0]
                group_names = []
                while i < len(row_tuples) and row_tuples[i][0] == current_country:
                    group_names.append(row_tuples[i][1])
                    i += 1
                if group_names != sorted(group_names):
                    unsorted_countries.append(current_country)
                    print(f"  Country '{current_country}': names not sorted: {group_names}, expected: {sorted(group_names)}")

            if len(unsorted_countries) == 0:
                print(f"PASS: Component 4 — Names sorted A-Z within each country (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Names not sorted correctly for countries: {unsorted_countries}")
        else:
            print("FAIL: Component 4 — Not enough data rows to check name sort within country")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(TARGET_FILE):
    print(f"File not found: {TARGET_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(TARGET_FILE)
