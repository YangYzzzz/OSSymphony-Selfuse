"""
Reward Script: Add headers to thesis PDF
Task ID: pdf_ro_022
Domain: pdf
Scoring:
  Component 1 (0.15): Output file exists with correct page count (85)
  Component 2 (0.30): Header text 'Johnson - Master Thesis 2026' present on pages 2-85
  Component 3 (0.25): Correct page numbers on pages 2-85
  Component 4 (0.20): Font is Times-Roman at 9pt for header text
  Component 5 (0.10): Page 1 (title page) has no header text in top region
                       AND at least one other page does have it (compound check)
"""

import os
import sys

# PyMuPDF - available on VM
try:
    import fitz
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_022'
OUTPUT_FILE = os.path.join(WORKDIR, 'Documents', 'thesis_headers.pdf')

HEADER_TEXT = 'Johnson - Master Thesis 2026'
EXPECTED_PAGES = 85
HEADER_FONT = 'Times-Roman'
HEADER_SIZE = 9.0
# Region: anything with y < 45 is "top of page" (header area)
HEADER_Y_MAX = 45.0


def get_top_spans(page):
    """Get all text spans in the header region (y < HEADER_Y_MAX) of a page."""
    data = page.get_text("dict")
    spans = []
    for block in data["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                bbox = span["bbox"]
                if bbox[1] < HEADER_Y_MAX:
                    spans.append(span)
    return spans


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the PDF
    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.15 points)
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Page count is {page_count} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Header text present on pages 2-85 (indices 1-84) (0.30 points)
    try:
        pages_with_header = 0
        expected_header_pages = EXPECTED_PAGES - 1  # 84 pages (skip page 1)
        sample_pages = list(range(1, min(EXPECTED_PAGES, len(doc))))

        for page_idx in sample_pages:
            page = doc[page_idx]
            top_spans = get_top_spans(page)
            header_found = any(HEADER_TEXT in span["text"] for span in top_spans)
            if header_found:
                pages_with_header += 1

        if pages_with_header == expected_header_pages:
            print(f"PASS: Component 2 -- Header text found on all {pages_with_header}/{expected_header_pages} pages (0.30 pts)")
            total_score += 0.30
        elif pages_with_header > 0:
            # Partial credit: proportional
            partial = 0.30 * (pages_with_header / expected_header_pages)
            print(f"PARTIAL: Component 2 -- Header found on {pages_with_header}/{expected_header_pages} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No header text found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Correct page numbers on pages 2-85 (0.25 points)
    try:
        correct_page_numbers = 0
        expected_count = EXPECTED_PAGES - 1  # 84 pages

        for page_idx in range(1, min(EXPECTED_PAGES, len(doc))):
            page = doc[page_idx]
            top_spans = get_top_spans(page)
            expected_num = str(page_idx + 1)  # page 2-85 (1-indexed display)

            # Look for page number span (should be near x=500)
            num_found = False
            for span in top_spans:
                text = span["text"].strip()
                if text == expected_num and span["bbox"][0] >= 450:
                    num_found = True
                    break
            if num_found:
                correct_page_numbers += 1

        if correct_page_numbers == expected_count:
            print(f"PASS: Component 3 -- All {correct_page_numbers}/{expected_count} page numbers correct (0.25 pts)")
            total_score += 0.25
        elif correct_page_numbers > 0:
            partial = 0.25 * (correct_page_numbers / expected_count)
            print(f"PARTIAL: Component 3 -- {correct_page_numbers}/{expected_count} page numbers correct ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No correct page numbers found")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Font is Times-Roman at 9pt (0.20 points)
    try:
        correct_font_pages = 0
        expected_count = EXPECTED_PAGES - 1

        for page_idx in range(1, min(EXPECTED_PAGES, len(doc))):
            page = doc[page_idx]
            top_spans = get_top_spans(page)
            font_ok = False
            for span in top_spans:
                if HEADER_TEXT in span["text"]:
                    if (HEADER_FONT.lower() in span["font"].lower() and
                            abs(span["size"] - HEADER_SIZE) < 0.5):
                        font_ok = True
                        break
            if font_ok:
                correct_font_pages += 1

        if correct_font_pages == expected_count:
            print(f"PASS: Component 4 -- Font {HEADER_FONT} {HEADER_SIZE}pt on all {correct_font_pages} pages (0.20 pts)")
            total_score += 0.20
        elif correct_font_pages > 0:
            partial = 0.20 * (correct_font_pages / expected_count)
            print(f"PARTIAL: Component 4 -- Correct font on {correct_font_pages}/{expected_count} pages ({partial:.3f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Font mismatch on header text")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Component 5: Title page (page 1, index 0) has NO header AND page 2 DOES have header (0.10 points)
    # Compound check: both conditions must be true
    try:
        page0 = doc[0]
        top_spans_p0 = get_top_spans(page0)
        title_has_header = any(HEADER_TEXT in span["text"] for span in top_spans_p0)

        page1 = doc[1]
        top_spans_p1 = get_top_spans(page1)
        page2_has_header = any(HEADER_TEXT in span["text"] for span in top_spans_p1)

        if not title_has_header and page2_has_header:
            print(f"PASS: Component 5 -- Title page has no header, page 2 does (0.10 pts)")
            total_score += 0.10
        elif title_has_header:
            print(f"FAIL: Component 5 -- Title page incorrectly has header text")
        else:
            print(f"FAIL: Component 5 -- Page 2 missing header (cannot confirm skip logic)")
    except Exception as e:
        print(f"ERROR: Component 5 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
