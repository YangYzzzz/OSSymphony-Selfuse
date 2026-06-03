"""
Reward Script: Create CV Professors Database from Stanford Vision Lab and CMU Robotics Institute
Task ID: osworld_multi_apps_web_faculty_009
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: Correct column headers (Name, University, Specialty, Lab_Website) — 0.2 pts
  Component 2: Both universities (Stanford and CMU) are covered — 0.3 pts
  Component 3: Sufficient data rows (at least 5 faculty entries) — 0.2 pts
  Component 4: Data sorted by University then Name — 0.3 pts
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_faculty_009'
FILE_PATH = f'{WORKDIR}/Desktop/cv_professors.ods'

REQUIRED_COLUMNS = ['Name', 'University', 'Specialty', 'Lab_Website']


def load_ods_data(file_path):
    """
    Load ODS file and return (headers, data_rows) where data_rows is a list of dicts.
    Uses odfpy library.
    """
    from odf.opendocument import load
    from odf.table import Table, TableRow, TableCell
    from odf.text import P

    doc = load(file_path)
    all_rows = []

    for sheet in doc.spreadsheet.getElementsByType(Table):
        rows = sheet.getElementsByType(TableRow)
        for row in rows:
            cells = row.getElementsByType(TableCell)
            row_vals = []
            for cell in cells:
                ps = cell.getElementsByType(P)
                val = ' '.join([p.firstChild.data if p.firstChild else '' for p in ps])
                repeat = cell.getAttribute('numbercolumnsrepeated')
                if repeat and int(repeat) > 1:
                    row_vals.extend([val] * int(repeat))
                else:
                    row_vals.append(val)
            # Strip trailing empty columns
            while row_vals and row_vals[-1] == '':
                row_vals.pop()
            if row_vals:
                all_rows.append(row_vals)
        # Only process the first sheet
        break

    if not all_rows:
        return None, []

    headers = all_rows[0]
    data_rows = all_rows[1:]
    return headers, data_rows


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: File must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODS file
    try:
        headers, data_rows = load_ods_data(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if headers is None:
        print("CRITICAL: No data found in ODS file")
        print("REWARD: 0.0")
        return 0.0

    print(f"File loaded. Headers: {headers}")
    print(f"Data rows: {len(data_rows)}")

    # Component 1: Correct column headers (0.2 points)
    # Headers must be exactly: Name, University, Specialty, Lab_Website
    try:
        # Normalize headers for comparison (strip whitespace, case-insensitive check)
        headers_stripped = [h.strip() for h in headers]
        expected_cols = REQUIRED_COLUMNS
        # Check all required columns are present (case-insensitive)
        headers_lower = [h.lower() for h in headers_stripped]
        expected_lower = [c.lower() for c in expected_cols]
        missing_cols = [c for c in expected_lower if c not in headers_lower]
        if not missing_cols:
            print(f"PASS: Component 1 — All required columns present: {headers_stripped} (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Missing columns: {missing_cols}. Found: {headers_stripped}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Build column index mapping
    col_idx = {}
    try:
        for i, h in enumerate(headers):
            col_idx[h.strip().lower()] = i
    except Exception as e:
        print(f"ERROR: Building column index — {e}")

    # Component 2: Both universities (Stanford and CMU) are covered (0.3 points)
    # The task requires data from both Stanford Vision Lab and CMU Robotics Institute
    try:
        if 'university' not in col_idx:
            print("FAIL: Component 2 — 'University' column not found")
        else:
            uni_idx = col_idx['university']
            universities = set()
            for row in data_rows:
                if len(row) > uni_idx and row[uni_idx].strip():
                    universities.add(row[uni_idx].strip())

            has_stanford = any('stanford' in u.lower() for u in universities)
            has_cmu = any('cmu' in u.lower() or 'carnegie' in u.lower() for u in universities)

            if has_stanford and has_cmu:
                print(f"PASS: Component 2 — Both Stanford and CMU are present. Universities: {universities} (0.3 pts)")
                total_score += 0.3
            elif has_stanford:
                print(f"FAIL: Component 2 — Only Stanford present, CMU missing. Universities: {universities}")
            elif has_cmu:
                print(f"FAIL: Component 2 — Only CMU present, Stanford missing. Universities: {universities}")
            else:
                print(f"FAIL: Component 2 — Neither Stanford nor CMU found. Universities: {universities}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Sufficient data rows (at least 5 faculty entries) (0.2 points)
    # Both sources combined should yield multiple faculty
    try:
        non_empty_rows = [row for row in data_rows if any(v.strip() for v in row)]
        if len(non_empty_rows) >= 5:
            print(f"PASS: Component 3 — Sufficient data: {len(non_empty_rows)} faculty rows (need >= 5) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Insufficient data: {len(non_empty_rows)} faculty rows (need >= 5)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data sorted by University then Name (0.3 points)
    # The task explicitly says "File sorted by University then Name"
    try:
        if 'university' not in col_idx or 'name' not in col_idx:
            print("FAIL: Component 4 — Cannot check sort: required columns missing")
        else:
            uni_idx = col_idx['university']
            name_idx = col_idx['name']
            non_empty_rows = [row for row in data_rows if any(v.strip() for v in row)]

            if len(non_empty_rows) < 2:
                print("FAIL: Component 4 — Not enough rows to verify sort order")
            else:
                # Extract (university, name) pairs
                sort_keys = []
                for row in non_empty_rows:
                    uni = row[uni_idx].strip() if len(row) > uni_idx else ''
                    name = row[name_idx].strip() if len(row) > name_idx else ''
                    sort_keys.append((uni, name))

                # Check if the current order matches sorted order
                sorted_keys = sorted(sort_keys, key=lambda x: (x[0].lower(), x[1].lower()))
                current_normalized = [(u.lower(), n.lower()) for u, n in sort_keys]
                expected_normalized = [(u.lower(), n.lower()) for u, n in sorted_keys]

                if current_normalized == expected_normalized:
                    print(f"PASS: Component 4 — Data correctly sorted by University then Name (0.3 pts)")
                    total_score += 0.3
                else:
                    # Find first mismatch
                    for i, (cur, exp) in enumerate(zip(current_normalized, expected_normalized)):
                        if cur != exp:
                            print(f"FAIL: Component 4 — Sort order incorrect at row {i+1}: found ({sort_keys[i][0]}, {sort_keys[i][1]}), expected ({sorted_keys[i][0]}, {sorted_keys[i][1]})")
                            break
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
