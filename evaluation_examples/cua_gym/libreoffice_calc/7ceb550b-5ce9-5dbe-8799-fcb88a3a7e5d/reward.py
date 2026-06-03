"""
Reward Script: Combine dates.xlsx and events.ods into schedule.csv sorted by date
Task ID: osworld_multi_apps_terminal_calc_006
Domain: libreoffice_calc (multi-app terminal task)
Scoring:
  Component 1 (0.4): schedule.csv exists on Desktop with correct headers (Date, Event)
  Component 2 (0.3): All 12 date-event pairs are present and correctly matched
  Component 3 (0.3): Rows are sorted by date in ascending order
"""

import os
import csv
from datetime import datetime

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_terminal_calc_006'

# Expected date-event pairs (ground truth from combining dates.xlsx and events.ods)
EXPECTED_PAIRS = {
    '2025-01-08': 'New Year Kickoff Meeting',
    '2025-02-18': 'Quarterly Budget Planning',
    '2025-03-03': 'Q1 Strategy Review',
    '2025-04-15': 'Spring Product Launch',
    '2025-05-30': 'Customer Appreciation Day',
    '2025-06-22': 'Midsummer Tech Conference',
    '2025-07-10': 'Annual Team Retreat',
    '2025-08-05': 'Engineering Summit',
    '2025-09-12': 'Fall Innovation Workshop',
    '2025-10-04': 'October Sales Seminar',
    '2025-11-27': 'Thanksgiving Charity Gala',
    '2025-12-19': 'Year-End Awards Ceremony',
}

EXPECTED_SORTED_DATES = sorted(EXPECTED_PAIRS.keys())


def verify_task():
    """
    Verify that schedule.csv was created correctly on the Desktop:
    - Correct headers (Date, Event)
    - All date-event pairs present and correctly matched
    - Rows sorted by date ascending
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0
    csv_path = os.path.join(WORKDIR, 'Desktop', 'schedule.csv')

    # Precondition gate: file must exist to score anything
    if not os.path.exists(csv_path):
        print(f"FAIL: schedule.csv not found at {csv_path}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Load CSV content
    try:
        with open(csv_path, 'r', newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot read schedule.csv: {e}")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    if len(rows) == 0:
        print("FAIL: schedule.csv is empty")
        print(f"\nScore: 0.0/1.0")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct headers (Date, Event) — 0.4 points
    # This FAILS on initial (no schedule.csv) -> PASSES on golden
    try:
        header = rows[0]
        # Normalize: strip whitespace and check column names
        if (len(header) >= 2 and
                header[0].strip() == 'Date' and
                header[1].strip() == 'Event'):
            print(f"PASS: Component 1 — headers correct: {header} (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected headers ['Date', 'Event'], found {header}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Parse data rows (skip header)
    data_rows = rows[1:]

    # Component 2: All 12 date-event pairs present and correctly matched — 0.3 points
    # This FAILS on initial (no schedule.csv) -> PASSES on golden
    try:
        actual_pairs = {}
        parse_errors = []
        for row in data_rows:
            if len(row) >= 2:
                date_str = row[0].strip()
                event_str = row[1].strip()
                # Normalize date format: accept 'YYYY-MM-DD'
                # Also handle date objects stored as datetime strings
                try:
                    # Try parsing as YYYY-MM-DD
                    dt = datetime.strptime(date_str, '%Y-%m-%d')
                    normalized_date = dt.strftime('%Y-%m-%d')
                except ValueError:
                    # Try other common formats
                    try:
                        dt = datetime.strptime(date_str, '%Y/%m/%d')
                        normalized_date = dt.strftime('%Y-%m-%d')
                    except ValueError:
                        parse_errors.append(f"Cannot parse date: {date_str!r}")
                        normalized_date = date_str
                actual_pairs[normalized_date] = event_str

        if parse_errors:
            print(f"WARN: Date parse errors: {parse_errors}")

        # Check all expected pairs are present and matched correctly
        correct_pairs = 0
        for date, expected_event in EXPECTED_PAIRS.items():
            actual_event = actual_pairs.get(date)
            if actual_event == expected_event:
                correct_pairs += 1
            else:
                print(f"  MISMATCH: {date} -> expected '{expected_event}', got '{actual_event}'")

        if correct_pairs == len(EXPECTED_PAIRS):
            print(f"PASS: Component 2 — all {correct_pairs}/12 date-event pairs correct (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — only {correct_pairs}/12 date-event pairs correct, expected 12")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Rows sorted by date ascending — 0.3 points
    # This FAILS on initial (no schedule.csv) -> PASSES on golden
    try:
        # Extract the date column from data rows
        date_values = []
        for row in data_rows:
            if len(row) >= 1:
                date_str = row[0].strip()
                try:
                    dt = datetime.strptime(date_str, '%Y-%m-%d')
                    date_values.append(dt)
                except ValueError:
                    try:
                        dt = datetime.strptime(date_str, '%Y/%m/%d')
                        date_values.append(dt)
                    except ValueError:
                        print(f"WARN: Skipping unparseable date: {date_str!r}")

        if len(date_values) > 0:
            is_sorted = all(date_values[i] <= date_values[i+1] for i in range(len(date_values)-1))
            if is_sorted:
                print(f"PASS: Component 3 — {len(date_values)} dates sorted in ascending order (0.3 pts)")
                total_score += 0.3
            else:
                # Find first out-of-order pair
                for i in range(len(date_values)-1):
                    if date_values[i] > date_values[i+1]:
                        print(f"FAIL: Component 3 — dates not sorted at position {i+1}: "
                              f"{date_values[i].strftime('%Y-%m-%d')} > {date_values[i+1].strftime('%Y-%m-%d')}")
                        break
        else:
            print("FAIL: Component 3 — no parseable dates found in data rows")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint: run verification
verify_task()
