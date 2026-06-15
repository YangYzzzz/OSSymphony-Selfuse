"""
Reward Script: Add 6 Bangkok street food market rows to asia_markets.ods
Task ID: osworld_multi_apps_web_location_009
Domain: libreoffice_calc (ODS file)
Scoring:
  Component 1 (0.4): At least 6 new rows with City='Bangkok', Country='Thailand' appended
  Component 2 (0.3): Each Bangkok row has all required fields filled (Name, Area, Opening_Hours, Specialty_Food)
  Component 3 (0.3): All new Bangkok rows have non-empty Source_URL
Total: 1.0
"""

import os

WORKDIR = '/home/user/Desktop'
TASK_ID = 'osworld_multi_apps_web_location_009'
FILE_PATH = f'{WORKDIR}/asia_markets.ods'

# Expected columns in the spreadsheet
REQUIRED_COLUMNS = ['Name', 'City', 'Country', 'Area', 'Opening_Hours', 'Specialty_Food', 'Source_URL']

def load_ods_data(file_path):
    """
    Load ODS file data using odfpy.
    Returns list of dicts, one per data row (excluding header).
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(file_path)
    sheets = doc.spreadsheet.getElementsByType(Table)
    if not sheets:
        raise ValueError("No sheets found in ODS file")

    sheet = sheets[0]
    all_rows = sheet.getElementsByType(TableRow)

    result_rows = []
    headers = []

    for i, row in enumerate(all_rows):
        cells = row.getElementsByType(TableCell)
        row_data = []
        for cell in cells:
            repeat = cell.getAttribute("numbercolumnsrepeated")
            paragraphs = cell.getElementsByType(P)
            val = ""
            for p in paragraphs:
                if p.firstChild:
                    val = str(p.firstChild)
                    break
            count = int(repeat) if repeat else 1
            # Guard against massive repeat counts for empty cells at end of row
            if count > 50:
                count = 1
            row_data.extend([val] * count)

        # Trim trailing empty strings
        while row_data and row_data[-1].strip() == "":
            row_data.pop()

        if i == 0:
            # Header row
            headers = row_data
        else:
            if any(v.strip() for v in row_data):
                # Non-empty data row
                row_dict = {}
                for j, col in enumerate(headers):
                    row_dict[col] = row_data[j] if j < len(row_data) else ""
                result_rows.append(row_dict)

    return headers, result_rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Add 6 Bangkok street food market rows to asia_markets.ods.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load file
    try:
        headers, rows = load_ods_data(file_path)
        print(f"INFO: Loaded {len(rows)} data rows, columns: {headers}")
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify headers are present (precondition gate, not scored)
    for col in REQUIRED_COLUMNS:
        if col not in headers:
            print(f"CRITICAL: Required column '{col}' missing from spreadsheet. Headers: {headers}")
            print("REWARD: 0.0")
            return 0.0

    # Extract Bangkok rows (City='Bangkok', Country='Thailand')
    bangkok_rows = [r for r in rows if r.get('City', '').strip() == 'Bangkok'
                    and r.get('Country', '').strip() == 'Thailand']
    print(f"INFO: Found {len(bangkok_rows)} Bangkok/Thailand rows")

    # Component 1: At least 6 Bangkok rows exist (0.4 points)
    # This FAILS on initial (0 Bangkok rows) and PASSES on golden (6 Bangkok rows)
    try:
        if len(bangkok_rows) >= 6:
            print(f"PASS: Component 1 — found {len(bangkok_rows)} Bangkok/Thailand rows (need >= 6) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected >= 6 Bangkok rows, found {len(bangkok_rows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All Bangkok rows have required non-empty fields (Name, Area, Opening_Hours, Specialty_Food)
    # 0.3 points — awarded proportionally based on how many rows have all 4 fields filled
    try:
        required_fields = ['Name', 'Area', 'Opening_Hours', 'Specialty_Food']
        rows_to_check = bangkok_rows[:6]  # Check at most 6 rows

        if rows_to_check:
            complete_count = 0
            for r in rows_to_check:
                all_filled = all(r.get(f, '').strip() for f in required_fields)
                if all_filled:
                    complete_count += 1
                else:
                    missing = [f for f in required_fields if not r.get(f, '').strip()]
                    print(f"  INFO: Row '{r.get('Name', '?')}' missing fields: {missing}")

            fraction = complete_count / len(rows_to_check)
            if fraction >= 1.0:
                print(f"PASS: Component 2 — all {complete_count}/{len(rows_to_check)} Bangkok rows have required fields filled (0.3 pts)")
                total_score += 0.3
            elif fraction >= 0.5:
                partial = round(0.3 * fraction, 2)
                print(f"PARTIAL: Component 2 — {complete_count}/{len(rows_to_check)} Bangkok rows fully filled, partial credit {partial} pts")
                total_score += partial
            else:
                print(f"FAIL: Component 2 — only {complete_count}/{len(rows_to_check)} Bangkok rows have all required fields")
        else:
            print("FAIL: Component 2 — no Bangkok rows to check (prerequisite from Component 1)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All Bangkok rows have a non-empty Source_URL (0.3 points)
    # This ensures the research task was done properly (sources were recorded)
    try:
        rows_to_check = bangkok_rows[:6]  # Check at most 6 rows

        if rows_to_check:
            url_filled_count = sum(1 for r in rows_to_check if r.get('Source_URL', '').strip())
            fraction = url_filled_count / len(rows_to_check)

            if fraction >= 1.0:
                print(f"PASS: Component 3 — all {url_filled_count}/{len(rows_to_check)} Bangkok rows have Source_URL (0.3 pts)")
                total_score += 0.3
            elif fraction >= 0.5:
                partial = round(0.3 * fraction, 2)
                print(f"PARTIAL: Component 3 — {url_filled_count}/{len(rows_to_check)} Bangkok rows have Source_URL, partial credit {partial} pts")
                total_score += partial
            else:
                print(f"FAIL: Component 3 — only {url_filled_count}/{len(rows_to_check)} Bangkok rows have Source_URL")
        else:
            print("FAIL: Component 3 — no Bangkok rows to check (prerequisite from Component 1)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
