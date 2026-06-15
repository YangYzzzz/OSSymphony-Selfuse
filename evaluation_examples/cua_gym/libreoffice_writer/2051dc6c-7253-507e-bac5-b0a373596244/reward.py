"""
Reward Script: Add a new record to mail merge data source (TeamMembers.csv)
Task ID: writer_mt_015
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): CSV has exactly 13 data records (was 12)
  Component 2 (0.3): 13th record has FirstName='James' and LastName='Wilson'
  Component 3 (0.2): 13th record has Email='jwilson@company.com'
  Component 4 (0.2): 13th record has Department='Engineering'
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'writer_mt_015'
CSV_PATH = os.path.join(WORKDIR, 'TeamMembers.csv')

def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: CSV file must exist
    if not os.path.exists(CSV_PATH):
        print(f"CRITICAL: CSV file not found at {CSV_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read CSV data
    try:
        with open(CSV_PATH, 'r', newline='') as f:
            reader = csv.DictReader(f)
            rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot parse CSV file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: CSV must have expected columns
    expected_cols = {'FirstName', 'LastName', 'Email', 'Department'}
    if not expected_cols.issubset(set(rows[0].keys())) if rows else True:
        print(f"CRITICAL: CSV missing expected columns. Found: {rows[0].keys() if rows else 'no rows'}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: CSV has {len(rows)} data records")

    # Component 1: CSV has exactly 13 data records (0.3 points)
    # Initial state has 12 records; task adds a 13th
    try:
        if len(rows) >= 13:
            print(f"PASS: Component 1 — CSV has {len(rows)} records (>= 13) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Expected >= 13 records, found {len(rows)}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Find the new record: look for James Wilson anywhere in the CSV
    # (it could be appended or inserted at any position)
    james_rows = [r for r in rows if r.get('FirstName', '').strip() == 'James' and r.get('LastName', '').strip() == 'Wilson']

    # Component 2: Record with FirstName='James' and LastName='Wilson' exists (0.3 points)
    try:
        if len(james_rows) >= 1:
            print(f"PASS: Component 2 — Found record with FirstName='James', LastName='Wilson' (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — No record found with FirstName='James' and LastName='Wilson'")
            # If the record doesn't exist at all, remaining checks will also fail
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Use the first matching James Wilson record for further checks
    new_record = james_rows[0] if james_rows else {}

    # Component 3: Email is 'jwilson@company.com' (0.2 points)
    try:
        actual_email = new_record.get('Email', '').strip()
        if actual_email == 'jwilson@company.com':
            print(f"PASS: Component 3 — Email is 'jwilson@company.com' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected Email='jwilson@company.com', found '{actual_email}'")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Department is 'Engineering' (0.2 points)
    try:
        actual_dept = new_record.get('Department', '').strip()
        if actual_dept == 'Engineering':
            print(f"PASS: Component 4 — Department is 'Engineering' (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 4 — Expected Department='Engineering', found '{actual_dept}'")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
