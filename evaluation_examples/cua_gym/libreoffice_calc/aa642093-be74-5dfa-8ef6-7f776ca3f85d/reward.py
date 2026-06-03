"""
Reward Script: Install VSCode CSV Rainbow extension and write CSV filtering script
Task ID: osworld_multi_apps_vscode_ext_script_014
Domain: vs-code / os (multi-app)
Scoring:
  Component 1: mechatroner.rainbow-csv extension installed (0.3 pts)
  Component 2: process_csv.py exists with correct CSV filtering logic (0.4 pts)
  Component 3: high_revenue.csv exists with correct filtered rows (0.3 pts)
  Total: 1.0
"""

import os
import json
import csv

WORKDIR = '/home/user/Desktop'
EXTENSIONS_JSON = '/home/user/.vscode/extensions/extensions.json'
TASK_ID = 'osworld_multi_apps_vscode_ext_script_014'


def _is_rainbow_csv_installed(extensions_data):
    """Return True if mechatroner.rainbow-csv appears in the extensions list."""
    if not isinstance(extensions_data, list):
        return False
    for ext in extensions_data:
        if not isinstance(ext, dict):
            continue
        identifier = ext.get('identifier', {})
        ext_id = identifier.get('id', '') if isinstance(identifier, dict) else str(identifier)
        if 'mechatroner.rainbow-csv' in ext_id.lower():
            return True
    return False


def _get_revenue_value(row):
    """Extract the revenue value from a CSV row dict (case-insensitive key lookup)."""
    for key in row.keys():
        if key.lower() == 'revenue':
            return float(row[key])
    raise KeyError('revenue column not found')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: mechatroner.rainbow-csv extension is installed (0.3 points)
    # In the initial env, extensions.json is [] (empty list).
    # In the golden env, it contains an entry with identifier.id == 'mechatroner.rainbow-csv'.
    try:
        if not os.path.isfile(EXTENSIONS_JSON):
            print("FAIL: Component 1 — extensions.json not found at expected path")
        else:
            with open(EXTENSIONS_JSON, 'r') as f:
                extensions_data = json.load(f)
            if _is_rainbow_csv_installed(extensions_data):
                print("PASS: Component 1 — mechatroner.rainbow-csv extension is installed (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 1 — mechatroner.rainbow-csv not found in extensions registry (found {len(extensions_data)} extensions)")
    except Exception as e:
        print(f"ERROR: Component 1 — Could not check extensions: {e}")

    # Component 2: process_csv.py exists with correct CSV filtering logic (0.4 points)
    # The script must: use csv module, open sales_data.csv, filter revenue > 10000,
    # write filtered rows to high_revenue.csv.
    process_csv_path = os.path.join(WORKDIR, 'process_csv.py')
    try:
        if not os.path.isfile(process_csv_path):
            print(f"FAIL: Component 2 — process_csv.py not found at {process_csv_path}")
        else:
            with open(process_csv_path, 'r') as f:
                script_content = f.read()

            checks_passed = sum([
                1 if ('import csv' in script_content or 'csv.' in script_content) else 0,
                1 if 'sales_data.csv' in script_content else 0,
                1 if 'high_revenue.csv' in script_content else 0,
                1 if '10000' in script_content else 0,
                1 if 'revenue' in script_content.lower() else 0,
            ])
            total_checks = 5

            if checks_passed == total_checks:
                print(f"PASS: Component 2 — process_csv.py has all required filtering logic ({checks_passed}/{total_checks} checks pass) (0.4 pts)")
                total_score += 0.4
            elif checks_passed >= 3:
                print(f"PARTIAL: Component 2 — process_csv.py has {checks_passed}/{total_checks} required elements (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 2 — process_csv.py missing key filtering logic ({checks_passed}/{total_checks} checks pass)")
    except Exception as e:
        print(f"ERROR: Component 2 — Could not check process_csv.py: {e}")

    # Component 3: high_revenue.csv exists with correct filtered rows (0.3 points)
    # Must contain header row + only rows where revenue > 10000.
    # Expected: 9 rows from sales_data.csv with revenue > 10000.
    high_revenue_path = os.path.join(WORKDIR, 'high_revenue.csv')
    expected_high_revenue_count = 9  # rows with revenue > 10000 in the original sales_data.csv
    try:
        if not os.path.isfile(high_revenue_path):
            print(f"FAIL: Component 3 — high_revenue.csv not found at {high_revenue_path}")
        else:
            with open(high_revenue_path, 'r', newline='') as f:
                reader = csv.DictReader(f)
                rows = list(reader)
                fieldnames = reader.fieldnames

            has_revenue_col = (
                fieldnames is not None and
                any(col.lower() == 'revenue' for col in fieldnames)
            )

            if not has_revenue_col:
                print(f"FAIL: Component 3 — high_revenue.csv missing 'revenue' column (headers: {fieldnames})")
            elif len(rows) == 0:
                print("FAIL: Component 3 — high_revenue.csv is empty (no data rows)")
            else:
                # Check all rows have revenue > 10000
                invalid_rows = [
                    (row.get('product', 'unknown'), _get_revenue_value(row))
                    for row in rows
                    if _get_revenue_value(row) <= 10000
                ]

                if len(invalid_rows) == 0 and len(rows) == expected_high_revenue_count:
                    print(f"PASS: Component 3 — high_revenue.csv has {len(rows)} rows, all with revenue > 10000 (0.3 pts)")
                    total_score += 0.3
                elif len(invalid_rows) == 0 and len(rows) > 0:
                    print(f"PARTIAL: Component 3 — high_revenue.csv rows all have revenue > 10000, but count is {len(rows)} (expected {expected_high_revenue_count}) (0.15 pts)")
                    total_score += 0.15
                else:
                    print(f"FAIL: Component 3 — high_revenue.csv contains {len(invalid_rows)} row(s) with revenue <= 10000: {invalid_rows}")
    except Exception as e:
        print(f"ERROR: Component 3 — Could not verify high_revenue.csv: {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


verify_task()
