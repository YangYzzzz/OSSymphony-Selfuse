"""
Reward Script: Verify page numbering check report
Task ID: pdf_cr_070
Domain: pdf
Scoring:
  Component 1 (0.15): numbering_check.txt exists and is non-empty
  Component 2 (0.15): Report mentions correct total page count (8)
  Component 3 (0.45): Per-page entries present for all 8 pages with correct numbers and HEADER/FOOTER location
  Component 4 (0.25): Sequential check result reported as PASS
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'pdf_cr_070'

OUTPUT_FILE = os.path.join(WORKDIR, 'Desktop', 'numbering_check.txt')
PDF_FILE = os.path.join(WORKDIR, 'Desktop', 'numbered.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: PDF must exist (not scored - it's present in initial_env too)
    if not os.path.exists(PDF_FILE):
        print(f"CRITICAL: PDF not found at {PDF_FILE}")
        print("REWARD: 0.0")
        return 0.0

    # Determine actual page count from PDF for reference
    try:
        import fitz
        doc = fitz.open(PDF_FILE)
        actual_page_count = doc.page_count
        doc.close()
    except Exception as e:
        print(f"WARNING: Could not read PDF page count: {e}")
        actual_page_count = 8  # fallback

    # Component 1: numbering_check.txt exists and is non-empty (0.15 points)
    # This file does NOT exist in initial_env, so it measures task-introduced change.
    try:
        if os.path.exists(OUTPUT_FILE):
            content = open(OUTPUT_FILE, 'r').read()
            if len(content.strip()) > 0:
                print(f"PASS: Component 1 -- numbering_check.txt exists and has {len(content)} chars (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 1 -- numbering_check.txt exists but is empty")
        else:
            print(f"FAIL: Component 1 -- numbering_check.txt not found at {OUTPUT_FILE}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # If file doesn't exist or is empty, no further checks possible
    if total_score < 0.15:
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    content = open(OUTPUT_FILE, 'r').read()

    # Component 2: Report mentions correct total page count (0.15 points)
    try:
        # Look for mention of the actual page count (e.g., "Total pages: 8" or "8 pages")
        page_count_pattern = re.search(r'(?:total\s+pages|pages?\s*[:\s]\s*)(\d+)', content, re.IGNORECASE)
        count_mentioned = re.search(r'\b' + str(actual_page_count) + r'\b', content)
        if page_count_pattern and int(page_count_pattern.group(1)) == actual_page_count:
            print(f"PASS: Component 2 -- Total page count {actual_page_count} correctly reported (0.15 pts)")
            total_score += 0.15
        elif count_mentioned:
            # Less strict: page count number appears somewhere in context of pages
            page_context = re.search(r'(?:total|pages?).*\b' + str(actual_page_count) + r'\b', content, re.IGNORECASE)
            if page_context:
                print(f"PASS: Component 2 -- Page count {actual_page_count} mentioned in context (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 -- Page count {actual_page_count} not found in report context")
        else:
            print(f"FAIL: Component 2 -- Expected total page count {actual_page_count} not found in report")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Per-page entries for all pages with correct numbering and location (0.45 points)
    # The golden report has lines like: "Page X (physical): Found number Y in FOOTER"
    # We check that each physical page is reported with correct sequential number and location
    try:
        pages_found = 0
        correct_entries = 0

        for page_num in range(1, actual_page_count + 1):
            # Look for a per-page report entry mentioning this page number
            # Flexible pattern: "Page X" with associated number and header/footer
            page_pattern = re.search(
                r'Page\s+' + str(page_num) + r'.*?(?:number|#|:)\s*' + str(page_num) + r'\b.*?(?:HEADER|FOOTER|header|footer)',
                content,
                re.IGNORECASE
            )
            if page_pattern:
                correct_entries += 1
            else:
                # Slightly less strict: just "Page X" with HEADER or FOOTER mentioned
                alt_pattern = re.search(
                    r'Page\s+' + str(page_num) + r'.*?(?:HEADER|FOOTER|header|footer)',
                    content,
                    re.IGNORECASE
                )
                if alt_pattern:
                    correct_entries += 1

        fraction = correct_entries / actual_page_count if actual_page_count > 0 else 0
        points = round(0.45 * fraction, 4)
        if correct_entries == actual_page_count:
            print(f"PASS: Component 3 -- All {actual_page_count} pages reported with numbering and location ({points} pts)")
            total_score += points
        elif correct_entries > 0:
            print(f"PARTIAL: Component 3 -- {correct_entries}/{actual_page_count} pages correctly reported ({points} pts)")
            total_score += points
        else:
            print(f"FAIL: Component 3 -- No pages correctly reported")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Sequential check result reported as PASS (0.25 points)
    try:
        seq_pass = re.search(r'Sequential\s+check\s*:\s*PASS', content, re.IGNORECASE)
        if seq_pass:
            print(f"PASS: Component 4 -- Sequential check: PASS found in report (0.25 pts)")
            total_score += 0.25
        else:
            # Check if there's any sequential/sequence mention with pass
            alt_seq = re.search(r'(?:sequential|sequence).*?(?:PASS|pass|correct|valid)', content, re.IGNORECASE)
            if alt_seq:
                print(f"PASS: Component 4 -- Sequential validation pass found (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 4 -- Sequential check PASS not found in report")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    # Check if it might be elsewhere
    alt_path = os.path.join(WORKDIR, 'numbering_check.txt')
    if os.path.exists(alt_path):
        OUTPUT_FILE = alt_path
        print(f"NOTE: Found numbering_check.txt at alternate location: {alt_path}")

verify_task()
