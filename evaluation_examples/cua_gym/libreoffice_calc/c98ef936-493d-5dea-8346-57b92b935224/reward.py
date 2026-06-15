"""
Reward Script: Count pages in PDFs and write summary CSV
Task ID: pdf_gf3_004
Domain: pdf (libreoffice_calc listed but actual domain is pdf/os)
Scoring:
  - Component 1 (0.15): CSV exists with correct header row
  - Component 2 (0.15): CSV has exactly 25 data rows
  - Component 3 (0.20): All 25 PDF filenames present in CSV
  - Component 4 (0.30): All page_count values are correct
  - Component 5 (0.20): All file_size_kb values are correct (within 0.15 tolerance)
"""

import os
import csv

WORKDIR = '/home/user'
TASK_ID = 'pdf_gf3_004'
CSV_PATH = os.path.join(WORKDIR, 'pdf_inventory.csv')
ARCHIVE_DIR = os.path.join(WORKDIR, 'pdf_archive')


def get_actual_pdf_data():
    """Scan the pdf_archive directory and return ground truth data."""
    import pymupdf
    data = {}
    if not os.path.isdir(ARCHIVE_DIR):
        return data
    for fname in os.listdir(ARCHIVE_DIR):
        if not fname.lower().endswith('.pdf'):
            continue
        fpath = os.path.join(ARCHIVE_DIR, fname)
        try:
            doc = pymupdf.open(fpath)
            page_count = doc.page_count
            doc.close()
        except Exception:
            page_count = -1
        file_size_kb = round(os.path.getsize(fpath) / 1024, 1)
        data[fname] = {'page_count': page_count, 'file_size_kb': file_size_kb}
    return data


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

    # Read CSV
    try:
        with open(CSV_PATH, 'r', newline='') as f:
            content = f.read()
    except Exception as e:
        print(f"CRITICAL: Cannot read CSV: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse CSV
    try:
        lines = content.strip().split('\n')
        reader = csv.DictReader(lines)
        fieldnames = reader.fieldnames
        rows = list(reader)
    except Exception as e:
        print(f"CRITICAL: Cannot parse CSV: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get actual PDF data from archive
    actual_data = get_actual_pdf_data()
    if not actual_data:
        print("CRITICAL: Could not read pdf_archive directory")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: CSV has correct header row (0.15 points)
    try:
        expected_headers = ['filename', 'page_count', 'file_size_kb']
        if fieldnames is not None:
            normalized = [h.strip().lower() for h in fieldnames]
            if normalized == expected_headers:
                print(f"PASS: Component 1 -- Correct header row: {fieldnames} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- Expected headers {expected_headers}, found {fieldnames}")
        else:
            print("FAIL: Component 1 -- No header row found")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: CSV has exactly 25 data rows (0.15 points)
    try:
        num_rows = len(rows)
        if num_rows == 25:
            print(f"PASS: Component 2 -- CSV has 25 data rows (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 -- Expected 25 data rows, found {num_rows}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Build a lookup from CSV rows by filename
    csv_lookup = {}
    for row in rows:
        fname = row.get('filename', '').strip()
        if fname:
            csv_lookup[fname] = row

    # Component 3: All 25 PDF filenames present in CSV (0.20 points)
    try:
        actual_filenames = set(actual_data.keys())
        csv_filenames = set(csv_lookup.keys())
        missing = actual_filenames - csv_filenames
        extra = csv_filenames - actual_filenames
        if len(missing) == 0 and len(extra) == 0 and len(csv_filenames) == 25:
            print(f"PASS: Component 3 -- All 25 filenames present and correct (0.20 pts)")
            total_score += 0.20
        else:
            # Partial credit: proportion of correct filenames
            correct_count = len(actual_filenames & csv_filenames)
            partial = round(0.20 * correct_count / 25, 3)
            if partial > 0:
                total_score += partial
                print(f"PARTIAL: Component 3 -- {correct_count}/25 filenames correct ({partial} pts)")
            else:
                print(f"FAIL: Component 3 -- Missing: {missing}, Extra: {extra}")
            if missing:
                print(f"  Missing filenames: {missing}")
            if extra:
                print(f"  Extra filenames: {extra}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: All page_count values are correct (0.30 points)
    try:
        correct_pages = 0
        total_checked = 0
        for fname, actual in actual_data.items():
            if fname not in csv_lookup:
                continue
            total_checked += 1
            try:
                csv_page_count = int(csv_lookup[fname].get('page_count', -1))
            except (ValueError, TypeError):
                csv_page_count = -1
            if csv_page_count == actual['page_count']:
                correct_pages += 1
            else:
                print(f"  page_count mismatch: {fname}: expected {actual['page_count']}, got {csv_page_count}")

        if total_checked > 0:
            ratio = correct_pages / 25
            points = round(0.30 * ratio, 3)
            if correct_pages == 25:
                print(f"PASS: Component 4 -- All 25 page counts correct (0.30 pts)")
            else:
                print(f"PARTIAL: Component 4 -- {correct_pages}/25 page counts correct ({points} pts)")
            total_score += points
        else:
            print("FAIL: Component 4 -- No matching filenames to check page counts")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: All file_size_kb values are correct (0.20 points)
    try:
        correct_sizes = 0
        total_checked = 0
        for fname, actual in actual_data.items():
            if fname not in csv_lookup:
                continue
            total_checked += 1
            try:
                csv_size = float(csv_lookup[fname].get('file_size_kb', -1))
            except (ValueError, TypeError):
                csv_size = -1.0
            # Allow small tolerance for rounding differences
            if abs(csv_size - actual['file_size_kb']) < 0.15:
                correct_sizes += 1
            else:
                print(f"  file_size_kb mismatch: {fname}: expected {actual['file_size_kb']}, got {csv_size}")

        if total_checked > 0:
            ratio = correct_sizes / 25
            points = round(0.20 * ratio, 3)
            if correct_sizes == 25:
                print(f"PASS: Component 5 -- All 25 file sizes correct (0.20 pts)")
            else:
                print(f"PARTIAL: Component 5 -- {correct_sizes}/25 file sizes correct ({points} pts)")
            total_score += points
        else:
            print("FAIL: Component 5 -- No matching filenames to check file sizes")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
