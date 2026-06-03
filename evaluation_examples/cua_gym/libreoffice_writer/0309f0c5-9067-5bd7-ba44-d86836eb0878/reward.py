"""
Reward Script: Export tracked changes from a Writer document to a change log CSV
Task ID: writer_rm_031
Domain: libreoffice_writer
Scoring:
  - Component 1: change_log.csv file exists (0.15)
  - Component 2: CSV has correct header columns (0.15)
  - Component 3: Contains exactly 15 tracked changes (0.20)
  - Component 4: Contains all 3 expected authors (0.20)
  - Component 5: Correct change types — 9 Insertions, 6 Deletions (0.15)
  - Component 6: Date entries present in expected range (0.15)
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'writer_rm_031'
CHANGE_LOG_PATH = os.path.join(WORKDIR, 'change_log.csv')

EXPECTED_AUTHORS = {'Sarah Chen', 'Marcus Rivera', 'Elena Kowalski'}
EXPECTED_TOTAL = 15
EXPECTED_INSERTIONS = 9
EXPECTED_DELETIONS = 6
REQUIRED_COLUMNS = {'Author', 'Date', 'Type', 'Description'}


def verify_task():
    """
    Verify that a change log CSV was exported with all 15 tracked changes,
    3 authors, correct types, and date information.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: change_log.csv file exists (0.15 points)
    # This is a task-introduced artifact — does NOT exist on initial_env
    if os.path.exists(CHANGE_LOG_PATH):
        print(f"PASS: Component 1 — change_log.csv exists (0.15 pts)")
        total_score += 0.15
    else:
        print(f"FAIL: Component 1 — change_log.csv not found at {CHANGE_LOG_PATH}")
        print("REWARD: 0.0")
        return 0.0

    # Read the CSV file
    try:
        with open(CHANGE_LOG_PATH, 'r', newline='') as f:
            reader = csv.DictReader(f)
            headers = set(reader.fieldnames) if reader.fieldnames else set()
            rows = list(reader)
    except Exception as e:
        print(f"ERROR: Cannot parse CSV: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: CSV has correct header columns (0.15 points)
    try:
        if REQUIRED_COLUMNS.issubset(headers):
            print(f"PASS: Component 2 — CSV headers contain all required columns: {headers} (0.15 pts)")
            total_score += 0.15
        else:
            missing = REQUIRED_COLUMNS - headers
            print(f"FAIL: Component 2 — Missing columns: {missing}. Found: {headers}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Contains exactly 15 tracked changes (0.20 points)
    try:
        num_rows = len(rows)
        if num_rows == EXPECTED_TOTAL:
            print(f"PASS: Component 3 — Exactly {EXPECTED_TOTAL} change entries found (0.20 pts)")
            total_score += 0.20
        elif num_rows >= 10:
            partial = 0.10  # Partial credit: at least 10 entries
            print(f"PARTIAL: Component 3 — Found {num_rows} entries (expected {EXPECTED_TOTAL}), ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Found {num_rows} entries, expected {EXPECTED_TOTAL}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Contains all 3 expected authors (0.20 points)
    try:
        found_authors = set()
        for row in rows:
            author = row.get('Author', '').strip()
            if author:
                found_authors.add(author)
        if EXPECTED_AUTHORS.issubset(found_authors):
            print(f"PASS: Component 4 — All 3 authors found: {found_authors} (0.20 pts)")
            total_score += 0.20
        else:
            missing_authors = EXPECTED_AUTHORS - found_authors
            matched = len(EXPECTED_AUTHORS & found_authors)
            if matched > 0:
                partial = round(0.20 * matched / 3, 2)
                print(f"PARTIAL: Component 4 — Found {found_authors}, missing {missing_authors} ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 4 — Found {found_authors}, missing {missing_authors}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Correct change types — 9 Insertions, 6 Deletions (0.15 points)
    try:
        type_counts = {}
        for row in rows:
            ctype = row.get('Type', '').strip()
            type_counts[ctype] = type_counts.get(ctype, 0) + 1

        insertions = type_counts.get('Insertion', 0)
        deletions = type_counts.get('Deletion', 0)

        if insertions == EXPECTED_INSERTIONS and deletions == EXPECTED_DELETIONS:
            print(f"PASS: Component 5 — {insertions} Insertions + {deletions} Deletions (0.15 pts)")
            total_score += 0.15
        elif insertions + deletions == EXPECTED_TOTAL:
            partial = 0.08  # Types present but counts slightly off
            print(f"PARTIAL: Component 5 — Found {insertions} Insertions + {deletions} Deletions (expected 9+6) ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 5 — Type counts: {type_counts} (expected 9 Insertion, 6 Deletion)")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    # Component 6: Date entries present in expected range (0.15 points)
    try:
        dates_valid = 0
        for row in rows:
            date_str = row.get('Date', '').strip()
            if date_str and '2026-03' in date_str or '2026-04' in date_str:
                dates_valid += 1

        if dates_valid == EXPECTED_TOTAL:
            print(f"PASS: Component 6 — All {EXPECTED_TOTAL} entries have valid dates in expected range (0.15 pts)")
            total_score += 0.15
        elif dates_valid >= 10:
            partial = 0.08
            print(f"PARTIAL: Component 6 — {dates_valid}/{EXPECTED_TOTAL} entries have valid dates ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 6 — Only {dates_valid}/{EXPECTED_TOTAL} entries have valid dates")
    except Exception as e:
        print(f"ERROR: Component 6 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
