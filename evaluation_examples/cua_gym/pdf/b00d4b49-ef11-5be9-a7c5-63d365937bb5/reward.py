"""
Reward Script: Redact phone numbers from customer_list.pdf
Task ID: pdf_gf1_008
Domain: pdf
Scoring:
  Component 1 (0.20): Redacted PDF exists with exactly 4 pages
  Component 2 (0.40): No phone numbers matching (XXX) XXX-XXXX in extracted text
  Component 3 (0.25): Black-filled rectangles present covering phone locations (>= 5 per page)
  Component 4 (0.15): Customer names and addresses remain readable in the output
"""

import os
import re

WORKDIR = '/home/user/Documents'
TASK_ID = 'pdf_gf1_008'
REDACTED_PATH = f'{WORKDIR}/customer_list_redacted.pdf'
ORIGINAL_PATH = f'{WORKDIR}/customer_list.pdf'

# Phone number pattern from task description
PHONE_PATTERN = re.compile(r'\(\d{3}\) \d{3}-\d{4}')

# Known customer names (first names from each region page)
EXPECTED_NAMES = [
    # Page 0 - West Region
    ['Sarah Chen', 'Portland'],
    # Page 1 - East Region
    ['Robert Kowalski', 'Boston'],
    # Page 2 - Central Region
    ['Michelle Tanaka', 'Chicago'],
    # Page 3 - South Region
    ['Daniel Gutierrez', 'Atlanta'],
]


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: redacted file must exist
    if not os.path.exists(REDACTED_PATH):
        print(f"CRITICAL: Redacted file not found: {REDACTED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        import pymupdf
    except ImportError:
        import fitz as pymupdf

    try:
        doc = pymupdf.open(REDACTED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open redacted PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Redacted PDF has exactly 4 pages (0.20 points)
    try:
        page_count = doc.page_count
        if page_count == 4:
            print(f"PASS: Component 1 - Redacted PDF has 4 pages (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 - Expected 4 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: No phone numbers in extracted text (0.40 points)
    # This is the core redaction check - most heavily weighted
    try:
        all_text = ""
        phones_found = []
        for i in range(doc.page_count):
            page_text = doc[i].get_text("text")
            all_text += page_text
            page_phones = PHONE_PATTERN.findall(page_text)
            if page_phones:
                phones_found.extend(page_phones)

        if len(phones_found) == 0:
            print(f"PASS: Component 2 - No phone numbers found in extracted text (0.40 pts)")
            total_score += 0.40
        else:
            print(f"FAIL: Component 2 - Found {len(phones_found)} phone numbers still in text: {phones_found[:5]}")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Black-filled rectangles covering phone locations (0.25 points)
    # The golden file has 5 black rects per page (one per phone number, 20 total)
    try:
        total_black_rects = 0
        pages_with_rects = 0
        for i in range(min(doc.page_count, 4)):
            drawings = doc[i].get_drawings()
            black_rects = 0
            for d in drawings:
                fill = d.get("fill")
                if fill and len(fill) >= 3 and all(abs(c) < 0.05 for c in fill[:3]):
                    black_rects += 1
            total_black_rects += black_rects
            if black_rects >= 3:
                pages_with_rects += 1

        if total_black_rects >= 18 and pages_with_rects == 4:
            # At least 18 black rects total across all 4 pages, each page has >= 3
            print(f"PASS: Component 3 - {total_black_rects} black rectangles across {pages_with_rects} pages (0.25 pts)")
            total_score += 0.25
        elif total_black_rects >= 10 and pages_with_rects >= 2:
            # Partial: at least some redaction happening
            partial = 0.15
            print(f"PARTIAL: Component 3 - {total_black_rects} black rectangles across {pages_with_rects} pages ({partial} pts)")
            total_score += partial
        elif total_black_rects >= 5:
            partial = 0.08
            print(f"PARTIAL: Component 3 - {total_black_rects} black rectangles found ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 - Only {total_black_rects} black rectangles found across {pages_with_rects} pages")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Names and addresses remain readable (0.15 points)
    # Check that key customer data is preserved after redaction
    try:
        all_text = ""
        for i in range(doc.page_count):
            all_text += doc[i].get_text("text")

        names_found = 0
        names_checked = 0
        for name_info in EXPECTED_NAMES:
            name = name_info[0]
            city = name_info[1]
            names_checked += 1
            if name in all_text and city in all_text:
                names_found += 1

        if names_found == names_checked:
            print(f"PASS: Component 4 - All {names_found}/{names_checked} customer names and cities still readable (0.15 pts)")
            total_score += 0.15
        elif names_found > 0:
            partial = round(0.15 * (names_found / names_checked), 2)
            print(f"PARTIAL: Component 4 - {names_found}/{names_checked} customer names readable ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 - No expected customer names found in redacted PDF")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(REDACTED_PATH):
    print(f"File not found: {REDACTED_PATH}")
    print("REWARD: 0.0")
else:
    verify_task()
