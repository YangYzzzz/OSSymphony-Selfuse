"""
Reward Script: Visit DBLP page for Yoshua Bengio and extract 5 most recent publications
Task ID: osworld_multi_apps_web_scholar_005
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: File 'bengio_recent.ods' exists on Desktop (prerequisite gate)
  Component 2: Header row contains exactly the required 4 columns (0.25 pts)
  Component 3: Exactly 5 data rows present (0.25 pts)
  Component 4: Year column contains valid recent years (integer, >= 2020) (0.25 pts)
  Component 5: DBLP_URL column contains valid DBLP links for each row (0.25 pts)
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_web_scholar_005'
FILE_PATH = os.path.join(WORKDIR, 'Desktop', 'bengio_recent.ods')

REQUIRED_COLUMNS = ['Title', 'Year', 'Venue', 'DBLP_URL']


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Prerequisite gate: file must exist to continue
    if not os.path.exists(file_path):
        print(f"FAIL: File not found at {file_path}")
        print("REWARD: 0.0")
        return 0.0

    # Load the ODS file using pandas with odf engine
    try:
        import pandas as pd
        df = pd.read_excel(file_path, engine='odf')
    except ImportError:
        print("CRITICAL: pandas or odfpy not available. Cannot read ODS file.")
        print("REWARD: 0.0")
        return 0.0
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Header row contains exactly the required 4 columns (0.25 pts)
    # This checks that the file has proper structure matching the task requirements
    try:
        actual_columns = [str(c).strip() for c in df.columns.tolist()]
        expected_columns = REQUIRED_COLUMNS
        if actual_columns == expected_columns:
            print(f"PASS: Component 1 — Correct header columns {actual_columns} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected columns {expected_columns}, found {actual_columns}")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check columns: {e}")

    # Component 2: Exactly 5 data rows present (0.25 pts)
    # Task explicitly requires 5 most recent publications
    try:
        row_count = len(df)
        if row_count == 5:
            print(f"PASS: Component 2 — Exactly 5 data rows present (0.25 pts)")
            total_score += 0.25
        elif row_count > 0:
            print(f"FAIL: Component 2 — Expected 5 data rows, found {row_count}")
        else:
            print(f"FAIL: Component 2 — No data rows found")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check row count: {e}")

    # Component 3: Year column contains valid recent years (integer, >= 2018) (0.25 pts)
    # Task requires filling Year from DBLP — years should be recent for Bengio's publications
    try:
        if 'Year' in df.columns:
            years = df['Year'].tolist()
            valid_years = 0
            for year in years:
                try:
                    y = int(year)
                    if 2018 <= y <= 2030:
                        valid_years += 1
                except (ValueError, TypeError):
                    pass
            if valid_years == len(years) and valid_years > 0:
                print(f"PASS: Component 3 — All {valid_years} Year values are valid recent years: {years} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 — Only {valid_years}/{len(years)} Year values are valid recent years: {years}")
        else:
            print("FAIL: Component 3 — 'Year' column not found")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not check Year column: {e}")

    # Component 4: DBLP_URL column contains valid DBLP links (0.25 pts)
    # Task requires the direct link to each publication record from DBLP
    try:
        if 'DBLP_URL' in df.columns:
            urls = df['DBLP_URL'].tolist()
            valid_urls = 0
            dblp_pattern = re.compile(r'https?://dblp\.org/', re.IGNORECASE)
            for url in urls:
                if url and isinstance(url, str) and dblp_pattern.match(url.strip()):
                    valid_urls += 1
            if valid_urls == len(urls) and valid_urls > 0:
                print(f"PASS: Component 4 — All {valid_urls} DBLP_URL values are valid DBLP links (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 — Only {valid_urls}/{len(urls)} DBLP_URL values are valid DBLP links: {urls}")
        else:
            print("FAIL: Component 4 — 'DBLP_URL' column not found")
    except Exception as e:
        print(f"ERROR: Component 4 — Could not check DBLP_URL column: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run the verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
