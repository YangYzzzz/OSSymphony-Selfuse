"""
Reward Script: Visit URLs and update spreadsheet with status and page titles
Task ID: osworld_multi_apps_multi_simple_009
Domain: libreoffice_calc (ODS format)
Scoring:
  Component 1: Status column (C2:C6) filled with 'OK' or 'FAILED' for all 5 rows (0.5 pts)
  Component 2: Title column (D2:D6) filled with non-empty page titles for all 5 rows (0.5 pts)
  Total: 1.0
"""

import os
import math

# Use pandas with odf engine for .ods file support
import pandas as pd

WORKDIR = '/home/user'
TASK_ID = 'osworld_multi_apps_multi_simple_009'
FILE_PATH = f'{WORKDIR}/links/websites.ods'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    The task requires:
    1. Opening Chrome and visiting each of 5 URLs in column B (rows 2-6)
    2. Updating column C (Status) with 'OK' if site loads, 'FAILED' if not
    3. Recording the page title in column D (Title)
    4. Saving the spreadsheet

    Initial state: Status (C2:C6) and Title (D2:D6) are all empty/NaN.
    Golden state: Status column has 'OK'/'FAILED' values, Title column has page titles.
    """
    total_score = 0.0

    # Load the file — precondition gate
    try:
        df = pd.read_excel(file_path, engine='odf', header=0)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Verify basic structure: must have Status and Title columns
    if 'Status' not in df.columns or 'Title' not in df.columns:
        print(f"CRITICAL: File missing required columns. Found: {list(df.columns)}")
        print("REWARD: 0.0")
        return 0.0

    # Must have exactly 5 data rows
    if len(df) != 5:
        print(f"CRITICAL: Expected 5 data rows, found {len(df)}")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: File loaded. Columns: {list(df.columns)}, Rows: {len(df)}")

    # Component 1: Status column (C2:C6) filled with 'OK' or 'FAILED' for all 5 URLs (0.5 points)
    # This FAILS on initial_env (all NaN) and PASSES on golden_env (all 'OK')
    try:
        valid_statuses = {'OK', 'FAILED'}
        status_values = df['Status'].tolist()
        filled_count = 0
        for i, val in enumerate(status_values):
            # Check for NaN/None
            is_nan = False
            try:
                is_nan = math.isnan(float(val)) if val is not None else True
            except (TypeError, ValueError):
                is_nan = (val is None or str(val).strip() == '')

            if not is_nan:
                val_str = str(val).strip().upper()
                if val_str in {'OK', 'FAILED'}:
                    filled_count += 1
                    print(f"PASS: Row {i+2} Status = {val!r} (valid)")
                else:
                    print(f"FAIL: Row {i+2} Status = {val!r} (not 'OK' or 'FAILED')")
            else:
                print(f"FAIL: Row {i+2} Status is empty/NaN")

        if filled_count == 5:
            print(f"PASS: Component 1 — All 5 Status values filled with OK/FAILED (0.5 pts)")
            total_score += 0.5
        elif filled_count > 0:
            partial = round(filled_count / 5 * 0.5, 2)
            print(f"PARTIAL: Component 1 — {filled_count}/5 Status values filled ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No Status values filled (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Title column (D2:D6) filled with non-empty page titles for all 5 URLs (0.5 points)
    # This FAILS on initial_env (all NaN) and PASSES on golden_env (all have actual titles)
    try:
        title_values = df['Title'].tolist()
        titles_filled = 0
        for i, val in enumerate(title_values):
            # Check for NaN/None/empty
            is_empty = False
            try:
                is_empty = math.isnan(float(val)) if val is not None else True
            except (TypeError, ValueError):
                is_empty = (val is None or str(val).strip() == '')

            if not is_empty and str(val).strip() != '':
                titles_filled += 1
                print(f"PASS: Row {i+2} Title = {str(val)[:50]!r} (non-empty)")
            else:
                print(f"FAIL: Row {i+2} Title is empty/NaN")

        if titles_filled == 5:
            print(f"PASS: Component 2 — All 5 Title values filled (0.5 pts)")
            total_score += 0.5
        elif titles_filled > 0:
            partial = round(titles_filled / 5 * 0.5, 2)
            print(f"PARTIAL: Component 2 — {titles_filled}/5 Title values filled ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No Title values filled (0 pts)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
