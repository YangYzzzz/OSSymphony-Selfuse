"""
Reward Script: Bates Numbering for Audit Document Bundle
Task ID: pdf_fin_007
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with correct page count (85)
  Component 2 (0.20): First page contains correct Bates number FIN-AUD-00001
  Component 3 (0.20): Last page contains correct Bates number FIN-AUD-00085
  Component 4 (0.45): All 85 pages contain sequentially correct Bates numbers
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_007'
OUTPUT_FILE = os.path.join(WORKDIR, 'finance', 'audit_docs_bates.pdf')
EXPECTED_PAGES = 85
BATES_PREFIX = 'FIN-AUD-'
BATES_PATTERN = re.compile(r'FIN-AUD-(\d{5})')


def verify_task(file_path):
    """
    Verify Bates numbering task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the file
    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.15 points)
    # This checks that the output file exists AND preserves all 85 pages
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — File has {page_count} pages as expected (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: First page contains Bates number FIN-AUD-00001 (0.20 points)
    try:
        page0_text = doc[0].get_text()
        match = BATES_PATTERN.search(page0_text)
        if match and match.group(0) == 'FIN-AUD-00001':
            print(f"PASS: Component 2 — Page 1 has Bates number FIN-AUD-00001 (0.20 pts)")
            total_score += 0.20
        elif match:
            print(f"FAIL: Component 2 — Page 1 has Bates number {match.group(0)}, expected FIN-AUD-00001")
        else:
            print(f"FAIL: Component 2 — No Bates number found on page 1")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Last page contains Bates number FIN-AUD-00085 (0.20 points)
    try:
        last_text = doc[-1].get_text()
        match = BATES_PATTERN.search(last_text)
        expected_last = f'FIN-AUD-{EXPECTED_PAGES:05d}'
        if match and match.group(0) == expected_last:
            print(f"PASS: Component 3 — Last page has Bates number {expected_last} (0.20 pts)")
            total_score += 0.20
        elif match:
            print(f"FAIL: Component 3 — Last page has Bates number {match.group(0)}, expected {expected_last}")
        else:
            print(f"FAIL: Component 3 — No Bates number found on last page")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: All pages have sequentially correct Bates numbers (0.45 points)
    # Check every page for the correct sequential Bates number
    try:
        correct_count = 0
        errors = []
        for i in range(doc.page_count):
            page_text = doc[i].get_text()
            expected_bates = f'FIN-AUD-{(i + 1):05d}'
            if expected_bates in page_text:
                correct_count += 1
            else:
                # Only collect first few errors for diagnostics
                if len(errors) < 5:
                    match = BATES_PATTERN.search(page_text)
                    found = match.group(0) if match else 'NONE'
                    errors.append(f"Page {i+1}: expected {expected_bates}, found {found}")

        if correct_count == doc.page_count:
            print(f"PASS: Component 4 — All {correct_count}/{doc.page_count} pages have correct sequential Bates numbers (0.45 pts)")
            total_score += 0.45
        elif correct_count > 0:
            fraction = correct_count / doc.page_count
            partial = round(0.45 * fraction, 4)
            if partial > 0:
                print(f"PARTIAL: Component 4 — {correct_count}/{doc.page_count} pages correct, errors: {errors[:3]} ({partial:.4f} pts)")
                total_score += partial
        else:
            print(f"FAIL: Component 4 — No pages have correct Bates numbers")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
