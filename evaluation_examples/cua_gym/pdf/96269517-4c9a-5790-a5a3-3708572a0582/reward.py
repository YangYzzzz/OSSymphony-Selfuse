"""
Reward Script: Add settlement stamp to demand package PDF
Task ID: pdf_legal_092
Domain: pdf
Scoring:
  Component 1 (0.25): Stamped file exists at correct output path with correct page count
  Component 2 (0.35): 'FOR SETTLEMENT PURPOSES ONLY' text present on ALL 18 pages
  Component 3 (0.25): 'Federal Rule of Evidence 408' text present on ALL 18 pages
  Component 4 (0.15): Stamp text is purple and uses correct font sizes (11pt / 9pt)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_legal_092'
STAMPED_PATH = os.path.join(WORKDIR, 'legal', 'demand', 'demand_package_stamped.pdf')
EXPECTED_PAGES = 18
STAMP_LINE_1 = 'FOR SETTLEMENT PURPOSES ONLY'
STAMP_LINE_2 = 'Federal Rule of Evidence 408'
# Purple color: #800080 = RGB(128, 0, 128) = int 8388736
PURPLE_COLOR = 8388736
EXPECTED_SIZE_1 = 11.0  # font size for line 1
EXPECTED_SIZE_2 = 9.0   # font size for line 2
SIZE_TOLERANCE = 0.5


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Stamped file exists at correct path with 18 pages (0.25 points)
    # This check FAILS on initial_env (file does not exist) and PASSES on golden_env
    try:
        if not os.path.exists(STAMPED_PATH):
            print(f"FAIL: Component 1 — Stamped file not found at {STAMPED_PATH}")
            # No file means nothing else can be checked
            print(f"\nScore: {total_score}/1.0")
            print(f"REWARD: {total_score}")
            return total_score

        doc = fitz.open(STAMPED_PATH)
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Stamped file exists with {page_count} pages (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 2: 'FOR SETTLEMENT PURPOSES ONLY' on all 18 pages (0.35 points)
    # Awards partial credit proportional to pages that have the stamp
    try:
        pages_with_stamp1 = 0
        for i in range(doc.page_count):
            text = doc[i].get_text('text')
            if STAMP_LINE_1 in text:
                pages_with_stamp1 += 1

        if pages_with_stamp1 == EXPECTED_PAGES:
            print(f"PASS: Component 2 — '{STAMP_LINE_1}' found on all {EXPECTED_PAGES} pages (0.35 pts)")
            total_score += 0.35
        elif pages_with_stamp1 > 0:
            partial = 0.35 * (pages_with_stamp1 / EXPECTED_PAGES)
            print(f"PARTIAL: Component 2 — '{STAMP_LINE_1}' found on {pages_with_stamp1}/{EXPECTED_PAGES} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — '{STAMP_LINE_1}' not found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: 'Federal Rule of Evidence 408' on all 18 pages (0.25 points)
    # Awards partial credit proportional to pages that have the stamp
    try:
        pages_with_stamp2 = 0
        for i in range(doc.page_count):
            text = doc[i].get_text('text')
            if STAMP_LINE_2 in text:
                pages_with_stamp2 += 1

        if pages_with_stamp2 == EXPECTED_PAGES:
            print(f"PASS: Component 3 — '{STAMP_LINE_2}' found on all {EXPECTED_PAGES} pages (0.25 pts)")
            total_score += 0.25
        elif pages_with_stamp2 > 0:
            partial = 0.25 * (pages_with_stamp2 / EXPECTED_PAGES)
            print(f"PARTIAL: Component 3 — '{STAMP_LINE_2}' found on {pages_with_stamp2}/{EXPECTED_PAGES} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — '{STAMP_LINE_2}' not found on any page")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text color is purple and font sizes are correct (0.15 points)
    # Check on page 0 as representative — stamp should be consistent across pages
    try:
        page = doc[0]
        d = page.get_text('dict')
        found_stamp1_purple = False
        found_stamp1_size = False
        found_stamp2_purple = False
        found_stamp2_size = False

        for block in d['blocks']:
            if block.get('type', 0) != 0:
                continue
            for line in block['lines']:
                for span in line['spans']:
                    t = span['text'].strip()
                    if STAMP_LINE_1 in t:
                        if span['color'] == PURPLE_COLOR:
                            found_stamp1_purple = True
                        if abs(span['size'] - EXPECTED_SIZE_1) <= SIZE_TOLERANCE:
                            found_stamp1_size = True
                    if STAMP_LINE_2 in t:
                        if span['color'] == PURPLE_COLOR:
                            found_stamp2_purple = True
                        if abs(span['size'] - EXPECTED_SIZE_2) <= SIZE_TOLERANCE:
                            found_stamp2_size = True

        all_purple = found_stamp1_purple and found_stamp2_purple
        all_sizes = found_stamp1_size and found_stamp2_size

        if all_purple and all_sizes:
            print(f"PASS: Component 4 — Both stamps are purple (#800080) with correct sizes (11pt, 9pt) (0.15 pts)")
            total_score += 0.15
        elif all_purple or all_sizes:
            partial = 0.075
            details = []
            if all_purple:
                details.append("color correct")
            else:
                details.append("color wrong")
            if all_sizes:
                details.append("sizes correct")
            else:
                details.append("sizes wrong")
            print(f"PARTIAL: Component 4 — {', '.join(details)} ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 — Stamps not purple or wrong font sizes")
            print(f"  Stamp1 purple: {found_stamp1_purple}, size OK: {found_stamp1_size}")
            print(f"  Stamp2 purple: {found_stamp2_purple}, size OK: {found_stamp2_size}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 4), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
