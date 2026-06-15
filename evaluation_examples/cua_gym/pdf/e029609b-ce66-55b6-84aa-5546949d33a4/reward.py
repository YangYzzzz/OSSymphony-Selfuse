"""
Reward Script: Apply consistent headers to every page of a budget proposal PDF
Task ID: pdf_fin_030
Domain: pdf
Scoring:
  Component 1: Header text on all 22 pages (0.40)
  Component 2: Separator line below header on all pages (0.20)
  Component 3: Header font size ~8pt and gray color (0.20)
  Component 4: Page count preserved at 22 (0.20)
"""

import os
import sys

try:
    import fitz  # PyMuPDF
except ImportError:
    import pymupdf as fitz

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_030'
EXPECTED_HEADER = 'CONFIDENTIAL - FY2025 Budget Proposal - Zenith Corp'
EXPECTED_PAGE_COUNT = 22
OUTPUT_PATH = os.path.join(WORKDIR, 'finance', 'budget_proposal_2025_headed.pdf')


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    num_pages = len(doc)

    # Component 1: Header text present on all 22 pages (0.40 points)
    # Check that the expected header text appears in the top region of every page
    try:
        pages_with_header = 0
        for i in range(num_pages):
            page = doc[i]
            # Check text in top 50pt strip
            clip = fitz.Rect(0, 0, page.rect.width, 50)
            header_text = page.get_textbox(clip).strip()
            if EXPECTED_HEADER in header_text:
                pages_with_header += 1

        if pages_with_header == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 1 — Header text found on all {EXPECTED_PAGE_COUNT} pages (0.40 pts)")
            total_score += 0.40
        elif pages_with_header > 0:
            # Partial credit proportional to pages with headers
            partial = 0.40 * (pages_with_header / EXPECTED_PAGE_COUNT)
            print(f"PARTIAL: Component 1 — Header on {pages_with_header}/{EXPECTED_PAGE_COUNT} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No pages have the expected header text")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Separator line below header on all pages (0.20 points)
    # Check for a drawing/line in the header area (y < 50) on every page
    try:
        pages_with_line = 0
        for i in range(num_pages):
            page = doc[i]
            drawings = page.get_drawings()
            # Look for any line-type drawing in the header area (y < 50)
            header_lines = []
            for d in drawings:
                if d['rect'].y1 <= 50:
                    # Check if it contains a line item
                    for item in d.get('items', []):
                        if item[0] == 'l':  # line item
                            header_lines.append(d)
                            break
            if len(header_lines) > 0:
                pages_with_line += 1

        if pages_with_line == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 2 — Separator line found on all {EXPECTED_PAGE_COUNT} pages (0.20 pts)")
            total_score += 0.20
        elif pages_with_line > 0:
            partial = 0.20 * (pages_with_line / EXPECTED_PAGE_COUNT)
            print(f"PARTIAL: Component 2 — Line on {pages_with_line}/{EXPECTED_PAGE_COUNT} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No separator lines found in header area")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Header font is ~8pt and gray color (0.20 points)
    # Check font properties on a sample of pages (first, middle, last)
    try:
        sample_pages = [0, num_pages // 2, num_pages - 1]
        font_ok_count = 0
        color_ok_count = 0

        for pg_idx in sample_pages:
            page = doc[pg_idx]
            data = page.get_text('dict')
            for block in data['blocks']:
                bbox = block.get('bbox', (0, 0, 0, 0))
                if bbox[1] < 50 and 'lines' in block:
                    for line in block['lines']:
                        for span in line['spans']:
                            if EXPECTED_HEADER in span.get('text', ''):
                                # Check font size (allow 7-9pt range)
                                size = span.get('size', 0)
                                if 7.0 <= size <= 9.0:
                                    font_ok_count += 1
                                else:
                                    print(f"  Page {pg_idx}: font size {size}, expected ~8pt")

                                # Check color is gray (not black, not white)
                                # Color is stored as integer: 8421504 = 0x808080 = gray
                                color_val = span.get('color', 0)
                                # Gray colors: R=G=B, not 0 (black) and not 0xFFFFFF (white)
                                if isinstance(color_val, int):
                                    r = (color_val >> 16) & 0xFF
                                    g = (color_val >> 8) & 0xFF
                                    b = color_val & 0xFF
                                    # Consider gray if R~=G~=B and value between 64-200
                                    is_gray = (abs(r - g) < 20 and abs(g - b) < 20
                                               and 40 < r < 220)
                                    if is_gray:
                                        color_ok_count += 1
                                    else:
                                        print(f"  Page {pg_idx}: color RGB=({r},{g},{b}), expected gray")

        sample_count = len(sample_pages)
        style_score = 0.0
        if font_ok_count >= sample_count:
            style_score += 0.10
            print(f"PASS: Component 3a — Font size ~8pt on all sampled pages")
        elif font_ok_count > 0:
            style_score += 0.10 * (font_ok_count / sample_count)
            print(f"PARTIAL: Component 3a — Font size OK on {font_ok_count}/{sample_count} sampled pages")
        else:
            print(f"FAIL: Component 3a — Font size not ~8pt on sampled pages")

        if color_ok_count >= sample_count:
            style_score += 0.10
            print(f"PASS: Component 3b — Gray color on all sampled pages")
        elif color_ok_count > 0:
            style_score += 0.10 * (color_ok_count / sample_count)
            print(f"PARTIAL: Component 3b — Gray color on {color_ok_count}/{sample_count} sampled pages")
        else:
            print(f"FAIL: Component 3b — Color not gray on sampled pages")

        if style_score > 0:
            print(f"PASS: Component 3 — Style checks ({style_score:.2f} pts)")
            total_score += style_score
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Page count preserved at 22 (0.20 points)
    # Ensures original content was not lost or pages duplicated
    try:
        if num_pages == EXPECTED_PAGE_COUNT:
            print(f"PASS: Component 4 — Page count is {EXPECTED_PAGE_COUNT} as expected (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 4 — Page count is {num_pages}, expected {EXPECTED_PAGE_COUNT}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
