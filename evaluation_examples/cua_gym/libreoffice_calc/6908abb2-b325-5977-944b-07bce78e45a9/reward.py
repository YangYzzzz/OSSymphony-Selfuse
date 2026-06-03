"""
Reward Script: Find Michelin-starred restaurants in NYC and record in Calc spreadsheet
Task ID: osworld_multi_apps_web_location_007
Domain: libreoffice_calc (multi_apps_web)
Scoring:
  Component 1: Correct column headers (Name, Stars, Cuisine, Neighborhood, Address) — 0.2 pts
  Component 2: Has substantive Michelin data (>=20 rows, valid star ratings 1/2/3) — 0.3 pts
  Component 3: All three star levels present (1, 2, 3 stars) — 0.3 pts
  Component 4: Data sorted correctly (Stars descending, then Name ascending) — 0.2 pts
  Total: 1.0
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_location_007'
FILE_PATH = f'{WORKDIR}/Desktop/nyc_michelin.ods'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist to proceed
    if not os.path.exists(file_path):
        print(f"CRITICAL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODS document using ezodf
    try:
        import ezodf
        doc = ezodf.opendoc(file_path)
        sheet = doc.sheets[0]
        print(f"INFO: Loaded '{file_path}' — sheet='{sheet.name}', rows={sheet.nrows()}, cols={sheet.ncols()}")
    except Exception as e:
        print(f"CRITICAL: Cannot load ODS file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    nrows = sheet.nrows()
    ncols = sheet.ncols()

    # Component 1: Correct column headers (0.2 points)
    # Expected: Name, Stars, Cuisine, Neighborhood, Address (case-insensitive)
    try:
        if nrows < 1 or ncols < 5:
            print(f"FAIL: Component 1 — sheet too small: {nrows} rows, {ncols} cols (need >=1 row, >=5 cols)")
        else:
            header_row = [str(sheet[0, c].value).strip().lower() if sheet[0, c].value is not None else '' for c in range(ncols)]
            expected_headers = ['name', 'stars', 'cuisine', 'neighborhood', 'address']
            # Check if expected headers appear (in order, first 5 columns)
            headers_found = all(h in header_row[:5] for h in expected_headers)
            if headers_found:
                print(f"PASS: Component 1 — Headers found: {header_row[:5]} (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 1 — Expected headers {expected_headers}, found {header_row[:5]}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Has substantive Michelin data (>=20 rows with valid star ratings 1/2/3) — 0.3 points
    # This tests that the agent actually fetched real data from the Michelin Guide website
    try:
        if nrows < 2:
            print(f"FAIL: Component 2 — No data rows (only {nrows} rows total)")
        else:
            # Find the Stars column index
            header_row_vals = [str(sheet[0, c].value).strip().lower() if sheet[0, c].value is not None else '' for c in range(ncols)]
            stars_col = None
            for idx, h in enumerate(header_row_vals):
                if h == 'stars':
                    stars_col = idx
                    break

            if stars_col is None:
                print(f"FAIL: Component 2 — Cannot find 'Stars' column in headers: {header_row_vals}")
            else:
                valid_rows = 0
                for r in range(1, nrows):
                    cell_val = sheet[r, stars_col].value
                    if cell_val is not None:
                        try:
                            stars_val = float(cell_val)
                            if stars_val in (1.0, 2.0, 3.0):
                                valid_rows += 1
                        except (ValueError, TypeError):
                            pass

                if valid_rows >= 20:
                    print(f"PASS: Component 2 — Found {valid_rows} rows with valid star ratings (>=20 required) (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 2 — Only {valid_rows} rows with valid star ratings (need >=20)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All three star levels present (1, 2, 3 stars) — 0.3 points
    # Michelin-starred NYC restaurants include 1, 2, and 3-star establishments
    try:
        if nrows < 2:
            print(f"FAIL: Component 3 — No data rows")
        else:
            # Find the Stars column index
            header_row_vals = [str(sheet[0, c].value).strip().lower() if sheet[0, c].value is not None else '' for c in range(ncols)]
            stars_col = None
            for idx, h in enumerate(header_row_vals):
                if h == 'stars':
                    stars_col = idx
                    break

            if stars_col is None:
                print(f"FAIL: Component 3 — Cannot find 'Stars' column")
            else:
                stars_present = set()
                for r in range(1, nrows):
                    cell_val = sheet[r, stars_col].value
                    if cell_val is not None:
                        try:
                            stars_val = float(cell_val)
                            if stars_val in (1.0, 2.0, 3.0):
                                stars_present.add(int(stars_val))
                        except (ValueError, TypeError):
                            pass

                if stars_present == {1, 2, 3}:
                    print(f"PASS: Component 3 — All three star levels present: {sorted(stars_present)} (0.3 pts)")
                    total_score += 0.3
                else:
                    print(f"FAIL: Component 3 — Not all star levels present, found: {sorted(stars_present)} (need 1, 2, 3)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Data sorted correctly (Stars descending, then Name ascending) — 0.2 points
    # Verifies the correct ordering as specified in the task
    try:
        if nrows < 3:
            print(f"FAIL: Component 4 — Too few rows to verify sorting ({nrows} rows)")
        else:
            # Find the Stars and Name column indices
            header_row_vals = [str(sheet[0, c].value).strip().lower() if sheet[0, c].value is not None else '' for c in range(ncols)]
            stars_col = None
            name_col = None
            for idx, h in enumerate(header_row_vals):
                if h == 'stars':
                    stars_col = idx
                if h == 'name':
                    name_col = idx

            if stars_col is None or name_col is None:
                print(f"FAIL: Component 4 — Cannot find Stars ({stars_col}) or Name ({name_col}) column")
            else:
                sort_violations = 0
                prev_stars = None
                prev_name = None
                data_rows = 0
                for r in range(1, nrows):
                    stars_val_raw = sheet[r, stars_col].value
                    name_val_raw = sheet[r, name_col].value
                    if stars_val_raw is None or name_val_raw is None:
                        continue
                    try:
                        stars_val = float(stars_val_raw)
                        name_val = str(name_val_raw).strip()
                    except (ValueError, TypeError):
                        continue

                    if prev_stars is not None:
                        # Stars must be non-increasing (descending)
                        if stars_val > prev_stars:
                            sort_violations += 1
                        # Within same star group, names must be ascending
                        elif stars_val == prev_stars and name_val.lower() < prev_name.lower():
                            sort_violations += 1

                    prev_stars = stars_val
                    prev_name = name_val
                    data_rows += 1

                if sort_violations == 0 and data_rows >= 2:
                    print(f"PASS: Component 4 — Data correctly sorted: Stars descending, Name ascending within groups (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 4 — {sort_violations} sort violation(s) found in {data_rows} data rows")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification against the canonical artifact path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
