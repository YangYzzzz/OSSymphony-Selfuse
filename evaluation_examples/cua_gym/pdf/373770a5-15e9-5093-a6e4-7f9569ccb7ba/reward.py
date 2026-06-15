"""
Reward Script: Add 'CONFIDENTIAL - Internal Use Only' header to every page of a PDF
Task ID: pdf_fm_084
Domain: pdf
Scoring:
  Component 1 (0.2): Output file exists at correct path with 10 pages
  Component 2 (0.3): Header text present on ALL 10 pages
  Component 3 (0.25): Header font is Helvetica, 8pt, red (255,0,0)
  Component 4 (0.25): Header is centered horizontally in top margin area
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_084'
OUTPUT_FILE = os.path.join(WORKDIR, 'Documents', 'strategy_doc_marked.pdf')
EXPECTED_TEXT = 'CONFIDENTIAL - Internal Use Only'
EXPECTED_PAGES = 10


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
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    page_count = len(doc)

    # Component 1: Output file has correct page count (0.2 points)
    # This checks that the output PDF preserves all 10 original pages.
    # The initial_env does NOT have strategy_doc_marked.pdf, so this fails on initial.
    try:
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Output PDF has {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Header text present on ALL pages (0.3 points)
    # Awards partial credit proportional to how many pages have the header.
    try:
        pages_with_header = 0
        for i in range(page_count):
            page = doc[i]
            text = page.get_text('text')
            if EXPECTED_TEXT in text:
                pages_with_header += 1

        if pages_with_header == page_count and page_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 -- Header found on all {pages_with_header}/{page_count} pages (0.3 pts)")
            total_score += 0.3
        elif pages_with_header > 0:
            partial = 0.3 * (pages_with_header / EXPECTED_PAGES)
            print(f"PARTIAL: Component 2 -- Header on {pages_with_header}/{page_count} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- Header text not found on any page")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Font is Helvetica, 8pt, red color (0.25 points)
    # Check font properties of the header text on all pages.
    try:
        pages_correct_style = 0
        for i in range(page_count):
            page = doc[i]
            data = page.get_text('dict')
            for block in data['blocks']:
                if block['type'] != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        if EXPECTED_TEXT in span['text']:
                            c = span['color']
                            r_val = (c >> 16) & 0xFF
                            g_val = (c >> 8) & 0xFF
                            b_val = c & 0xFF
                            font_ok = 'helvetica' in span['font'].lower() or 'helv' in span['font'].lower()
                            size_ok = abs(span['size'] - 8.0) < 0.5
                            # Red: R should be high (>200), G and B should be low (<50)
                            color_ok = r_val > 200 and g_val < 50 and b_val < 50
                            if font_ok and size_ok and color_ok:
                                pages_correct_style += 1
                            else:
                                print(f"  Page {i}: font={span['font']}, size={span['size']}, color=({r_val},{g_val},{b_val})")

        if pages_correct_style == EXPECTED_PAGES:
            print(f"PASS: Component 3 -- Correct style (Helvetica, 8pt, red) on all {pages_correct_style} pages (0.25 pts)")
            total_score += 0.25
        elif pages_correct_style > 0:
            partial = 0.25 * (pages_correct_style / EXPECTED_PAGES)
            print(f"PARTIAL: Component 3 -- Correct style on {pages_correct_style}/{EXPECTED_PAGES} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 -- No pages have correct header style")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Header is centered horizontally in top margin area (0.25 points)
    # The header should be in the top ~30pt of the page and horizontally centered.
    try:
        pages_correct_position = 0
        for i in range(page_count):
            page = doc[i]
            page_width = page.rect.width
            data = page.get_text('dict')
            for block in data['blocks']:
                if block['type'] != 0:
                    continue
                for line in block['lines']:
                    for span in line['spans']:
                        if EXPECTED_TEXT in span['text']:
                            bbox = span['bbox']  # (x0, y0, x1, y1)
                            # Check top margin: y0 should be < 40 (top area)
                            in_top = bbox[1] < 40
                            # Check centering: midpoint of text should be near page center
                            text_mid_x = (bbox[0] + bbox[2]) / 2.0
                            page_mid_x = page_width / 2.0
                            is_centered = abs(text_mid_x - page_mid_x) < 30  # tolerance of 30pt
                            if in_top and is_centered:
                                pages_correct_position += 1
                            else:
                                print(f"  Page {i}: bbox={bbox}, text_mid_x={text_mid_x:.1f}, page_mid_x={page_mid_x:.1f}, in_top={in_top}")

        if pages_correct_position == EXPECTED_PAGES:
            print(f"PASS: Component 4 -- Header centered in top margin on all {pages_correct_position} pages (0.25 pts)")
            total_score += 0.25
        elif pages_correct_position > 0:
            partial = 0.25 * (pages_correct_position / EXPECTED_PAGES)
            print(f"PARTIAL: Component 4 -- Correct position on {pages_correct_position}/{EXPECTED_PAGES} pages ({partial:.2f} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- Header not properly positioned on any page")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_FILE):
    print(f"File not found: {OUTPUT_FILE}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_FILE)
