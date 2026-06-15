"""
Reward Script: Create a privilege log entry sheet as a new PDF
Task ID: pdf_legal_093
Domain: pdf
Scoring:
  Component 1: File exists and is a valid PDF                    — 0.15
  Component 2: Contains 'PRIVILEGE LOG' header text              — 0.15
  Component 3: Table exists with 8 columns                      — 0.25
  Component 4: Table has correct column headers                  — 0.25
  Component 5: Table has exactly 5 data rows (beyond header)     — 0.20
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_093'

# Pre-check: if the target file doesn't exist, short-circuit before importing pymupdf
_target_file = f'{WORKDIR}/legal/privilege_log.pdf'
if not os.path.exists(_target_file):
    print(f"File not found: {_target_file}")
    print("REWARD: 0.0")
    import sys
    sys.exit(0)

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

EXPECTED_HEADERS = [
    'Bates Range', 'Date', 'From', 'To', 'CC',
    'Subject', 'Privilege Asserted', 'Description'
]


def normalize(s):
    """Normalize whitespace in a string for comparison."""
    import re
    return re.sub(r'\s+', ' ', s).strip()


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: File exists and is a valid PDF (0.15 points)
    try:
        if not os.path.exists(file_path):
            print(f"FAIL: Component 1 — File not found at {file_path}")
            print("REWARD: 0.0")
            return 0.0
        doc = pymupdf.open(file_path)
        page_count = doc.page_count
        if page_count >= 1:
            print(f"PASS: Component 1 — Valid PDF with {page_count} page(s) (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — PDF has 0 pages")
            doc.close()
            print("REWARD: 0.0")
            return 0.0
    except Exception as e:
        print(f"ERROR: Component 1 — Cannot open PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Contains 'PRIVILEGE LOG' header text (0.15 points)
    try:
        full_text = ""
        for page in doc:
            full_text += page.get_text("text")
        if "PRIVILEGE LOG" in full_text.upper():
            print(f"PASS: Component 2 — 'PRIVILEGE LOG' header found (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 2 — 'PRIVILEGE LOG' header not found in text")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Table exists with 8 columns (0.25 points)
    table_rows = None
    try:
        # Search across all pages for a table with 8 columns
        for page_idx in range(doc.page_count):
            page = doc[page_idx]
            tables = list(page.find_tables())
            for table in tables:
                rows = table.extract()
                if rows and len(rows[0]) == 8:
                    table_rows = rows
                    break
            if table_rows is not None:
                break
        if table_rows is not None and len(table_rows[0]) == 8:
            print(f"PASS: Component 3 — Table found with 8 columns (0.25 pts)")
            total_score += 0.25
        else:
            # Report what we did find
            for page_idx in range(doc.page_count):
                page = doc[page_idx]
                tables = list(page.find_tables())
                for ti, table in enumerate(tables):
                    rows = table.extract()
                    col_count = len(rows[0]) if rows else 0
                    print(f"  Found table {ti} on page {page_idx}: {len(rows)} rows x {col_count} cols")
            print(f"FAIL: Component 3 — No table with 8 columns found")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Table has correct column headers (0.25 points)
    try:
        if table_rows is not None and len(table_rows) >= 1:
            header_row = [normalize(cell) for cell in table_rows[0]]
            expected_norm = [normalize(h) for h in EXPECTED_HEADERS]
            matches = sum(1 for h in expected_norm if h in header_row)
            if matches == 8:
                print(f"PASS: Component 4 — All 8 column headers match (0.25 pts)")
                total_score += 0.25
            elif matches >= 6:
                partial = round(0.25 * (matches / 8), 2)
                if partial > 0:
                    total_score += partial
                print(f"PARTIAL: Component 4 — {matches}/8 headers match ({partial} pts)")
                print(f"  Expected: {expected_norm}, Found: {header_row}")
            else:
                print(f"FAIL: Component 4 — Only {matches}/8 headers match")
                print(f"  Expected: {expected_norm}, Found: {header_row}")
        else:
            print(f"FAIL: Component 4 — No table rows available to check headers")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Table has exactly 5 data rows (beyond header) (0.20 points)
    try:
        if table_rows is not None:
            data_row_count = len(table_rows) - 1  # subtract header row
            if data_row_count == 5:
                print(f"PASS: Component 5 — Table has exactly 5 data rows (0.20 pts)")
                total_score += 0.20
            elif data_row_count >= 3:
                partial = round(0.20 * (min(data_row_count, 5) / 5), 2)
                print(f"PARTIAL: Component 5 — Table has {data_row_count} data rows, expected 5 ({partial} pts)")
                total_score += partial
            else:
                print(f"FAIL: Component 5 — Table has {data_row_count} data rows, expected 5")
        else:
            print(f"FAIL: Component 5 — No table available to check row count")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/legal/privilege_log.pdf'
verify_task(file_path)
