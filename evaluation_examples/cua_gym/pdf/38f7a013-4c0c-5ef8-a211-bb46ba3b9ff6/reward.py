"""
Reward Script: Stamp each page of court_filing.pdf with filing date and case number
Task ID: pdf_pw_040
Domain: pdf
Scoring:
  Component 1 (0.3): Output file exists with correct page count (18 pages)
  Component 2 (0.3): Case number on all pages in top area
  Component 3 (0.3): Filing date on all pages in top area
  Component 4 (0.1): Font is Times-Roman, 10pt, black
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_040'
OUTPUT_FILE = os.path.join(WORKDIR, 'legal', 'court_filing_stamped.pdf')
ORIGINAL_FILE = os.path.join(WORKDIR, 'legal', 'court_filing.pdf')
EXPECTED_PAGES = 18
CASE_NUMBER = 'Case No. 2026-CV-04521'
FILING_DATE = 'Filed: April 1, 2026'


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: output file must exist
    if not os.path.exists(OUTPUT_FILE):
        print(f"CRITICAL: Output file not found: {OUTPUT_FILE}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(OUTPUT_FILE)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {OUTPUT_FILE}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Correct page count matching original (0.3 points)
    # The stamped file must have exactly 18 pages (same as original)
    try:
        page_count = doc.page_count
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Page count is {page_count} (expected {EXPECTED_PAGES}) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — Page count is {page_count}, expected {EXPECTED_PAGES}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Case number stamp on ALL pages in top area (0.3 points)
    # Each page must contain "Case No. 2026-CV-04521" in the top region (y < 50)
    try:
        pages_with_case = 0
        for i in range(doc.page_count):
            page = doc[i]
            # Search for case number text in the top area
            text_dict = page.get_text('dict')
            found_case = False
            for block in text_dict.get('blocks', []):
                if block.get('type') != 0:
                    continue
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        if span.get('origin', (0, 999))[1] < 50:
                            if CASE_NUMBER in span.get('text', ''):
                                found_case = True
            if found_case:
                pages_with_case += 1

        if pages_with_case == EXPECTED_PAGES:
            print(f"PASS: Component 2 — Case number found on all {pages_with_case}/{EXPECTED_PAGES} pages (0.3 pts)")
            total_score += 0.3
        elif pages_with_case > 0:
            partial = 0.3 * (pages_with_case / EXPECTED_PAGES)
            print(f"PARTIAL: Component 2 — Case number on {pages_with_case}/{EXPECTED_PAGES} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — Case number not found on any page in top area")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Filing date stamp on ALL pages in top area (0.3 points)
    # Each page must contain "Filed: April 1, 2026" in the top region (y < 50)
    try:
        pages_with_date = 0
        for i in range(doc.page_count):
            page = doc[i]
            text_dict = page.get_text('dict')
            found_date = False
            for block in text_dict.get('blocks', []):
                if block.get('type') != 0:
                    continue
                for line in block.get('lines', []):
                    for span in line.get('spans', []):
                        if span.get('origin', (0, 999))[1] < 50:
                            if FILING_DATE in span.get('text', ''):
                                found_date = True
            if found_date:
                pages_with_date += 1

        if pages_with_date == EXPECTED_PAGES:
            print(f"PASS: Component 3 — Filing date found on all {pages_with_date}/{EXPECTED_PAGES} pages (0.3 pts)")
            total_score += 0.3
        elif pages_with_date > 0:
            partial = 0.3 * (pages_with_date / EXPECTED_PAGES)
            print(f"PARTIAL: Component 3 — Filing date on {pages_with_date}/{EXPECTED_PAGES} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — Filing date not found on any page in top area")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Stamp text uses Times-Roman font, 10pt, black (0.1 points)
    # Check font properties of stamp text on first page
    try:
        page = doc[0]
        text_dict = page.get_text('dict')
        correct_font = False
        correct_size = False
        correct_color = False
        stamps_found = 0

        for block in text_dict.get('blocks', []):
            if block.get('type') != 0:
                continue
            for line in block.get('lines', []):
                for span in line.get('spans', []):
                    if span.get('origin', (0, 999))[1] < 50:
                        span_text = span.get('text', '')
                        if CASE_NUMBER in span_text or FILING_DATE in span_text:
                            stamps_found += 1
                            font_name = span.get('font', '')
                            font_size = span.get('size', 0)
                            color_val = span.get('color', -1)

                            if 'Times' in font_name or 'times' in font_name:
                                correct_font = True
                            if abs(font_size - 10.0) < 0.5:
                                correct_size = True
                            if color_val == 0:  # black = 0
                                correct_color = True

        if stamps_found >= 2 and correct_font and correct_size and correct_color:
            print(f"PASS: Component 4 — Font: Times-Roman, Size: 10pt, Color: black (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 4 — stamps_found={stamps_found}, font_ok={correct_font}, size_ok={correct_size}, color_ok={correct_color}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
