"""
Reward Script: Create a cover page PDF with specific text, fonts, sizes, colors, and background
Task ID: pdf_ro_023
Domain: pdf
Scoring:
  Component 1 (0.15): File exists, single page, Letter size
  Component 2 (0.15): Light gray background (#F0F0F0)
  Component 3 (0.25): 'Annual Financial Report' at 36pt bold
  Component 4 (0.15): 'Fiscal Year 2025-2026' at 24pt
  Component 5 (0.15): 'Prepared by: Finance Department' at 14pt
  Component 6 (0.15): 'Classification: Internal Only' in red at 12pt
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_023'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'cover_page.pdf')

# Tolerances
SIZE_TOL = 1.5       # font size tolerance in points
PAGE_DIM_TOL = 5.0   # page dimension tolerance in points
COLOR_TOL = 30       # RGB 0-255 color tolerance


def get_text_spans(page):
    """Extract all text spans with font details from a page."""
    data = page.get_text("dict")
    spans = []
    for block in data["blocks"]:
        if block["type"] != 0:
            continue
        for line in block["lines"]:
            for span in line["spans"]:
                c = span["color"]
                rgb = (c >> 16 & 0xFF, c >> 8 & 0xFF, c & 0xFF)
                spans.append({
                    "text": span["text"],
                    "font": span["font"],
                    "size": span["size"],
                    "color_rgb": rgb,
                    "bold": bool(span["flags"] & 16),
                    "bbox": span["bbox"],
                })
    return spans


def find_span(spans, search_text):
    """Find a span containing the search text (case-insensitive match)."""
    for span in spans:
        if search_text.lower() in span["text"].lower():
            return span
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print("CRITICAL: File not found:", file_path)
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print("CRITICAL: Cannot open PDF:", e)
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Single page with Letter dimensions (0.15 points)
    # This checks that the PDF was created from scratch as specified.
    # Initial env has NO file at all, so this component fails on initial.
    try:
        page_count = doc.page_count
        if page_count == 1:
            page = doc[0]
            w, h = page.rect.width, page.rect.height
            if abs(w - 612) <= PAGE_DIM_TOL and abs(h - 792) <= PAGE_DIM_TOL:
                print("PASS: Component 1 -- Single page, Letter size ({:.0f}x{:.0f}) (0.15 pts)".format(w, h))
                total_score += 0.15
            else:
                print("FAIL: Component 1 -- Page size {:.0f}x{:.0f}, expected ~612x792".format(w, h))
        else:
            print("FAIL: Component 1 -- Page count is {}, expected 1".format(page_count))
    except Exception as e:
        print("ERROR: Component 1 --", e)

    # Component 2: Light gray background (0.15 points)
    # Checks for a filled rectangle covering the full page in ~#F0F0F0
    try:
        page = doc[0]
        drawings = page.get_drawings()
        bg_found = 0
        for d in drawings:
            fill = d.get("fill")
            rect = d.get("rect")
            if fill and rect:
                # Check if rectangle covers most of the page
                page_rect = page.rect
                covers_page = (
                    rect.width >= page_rect.width * 0.9 and
                    rect.height >= page_rect.height * 0.9
                )
                if covers_page:
                    # #F0F0F0 = (240, 240, 240) -> (0.941, 0.941, 0.941) in 0-1 floats
                    fill_rgb_255 = tuple(int(c * 255) for c in fill[:3])
                    expected_gray = 240  # #F0F0F0
                    if all(abs(c - expected_gray) <= COLOR_TOL for c in fill_rgb_255):
                        print("PASS: Component 2 -- Light gray background fill {} (0.15 pts)".format(fill_rgb_255))
                        total_score += 0.15
                        bg_found = 1  # marker: background verified via drawing check
                        break
        if bg_found == 0:
            print("FAIL: Component 2 -- No light gray full-page background rectangle found")
    except Exception as e:
        print("ERROR: Component 2 --", e)

    # Extract text spans for components 3-6
    try:
        page = doc[0]
        spans = get_text_spans(page)
    except Exception as e:
        print("ERROR: Could not extract text spans:", e)
        spans = []

    # Component 3: 'Annual Financial Report' at 36pt bold (0.25 points)
    try:
        span = find_span(spans, "Annual Financial Report")
        if span:
            size_ok = abs(span["size"] - 36.0) <= SIZE_TOL
            bold_ok = span["bold"]
            if size_ok and bold_ok:
                print("PASS: Component 3 -- 'Annual Financial Report' at {:.1f}pt bold (0.25 pts)".format(span["size"]))
                total_score += 0.25
            elif size_ok:
                # Partial: correct size but not bold
                print("PARTIAL: Component 3 -- Correct size but not bold (0.15 pts)")
                total_score += 0.15
            elif bold_ok:
                # Partial: bold but wrong size
                print("PARTIAL: Component 3 -- Bold but size={:.1f}pt, expected 36pt (0.10 pts)".format(span["size"]))
                total_score += 0.10
            else:
                print("FAIL: Component 3 -- size={:.1f}pt bold={} (expected 36pt bold)".format(span["size"], span["bold"]))
        else:
            print("FAIL: Component 3 -- 'Annual Financial Report' text not found")
    except Exception as e:
        print("ERROR: Component 3 --", e)

    # Component 4: 'Fiscal Year 2025-2026' at 24pt (0.15 points)
    try:
        span = find_span(spans, "Fiscal Year 2025-2026")
        if span:
            size_ok = abs(span["size"] - 24.0) <= SIZE_TOL
            if size_ok:
                print("PASS: Component 4 -- 'Fiscal Year 2025-2026' at {:.1f}pt (0.15 pts)".format(span["size"]))
                total_score += 0.15
            else:
                print("FAIL: Component 4 -- size={:.1f}pt, expected 24pt".format(span["size"]))
        else:
            print("FAIL: Component 4 -- 'Fiscal Year 2025-2026' text not found")
    except Exception as e:
        print("ERROR: Component 4 --", e)

    # Component 5: 'Prepared by: Finance Department' at 14pt (0.15 points)
    try:
        span = find_span(spans, "Prepared by: Finance Department")
        if span:
            size_ok = abs(span["size"] - 14.0) <= SIZE_TOL
            if size_ok:
                print("PASS: Component 5 -- 'Prepared by: Finance Department' at {:.1f}pt (0.15 pts)".format(span["size"]))
                total_score += 0.15
            else:
                print("FAIL: Component 5 -- size={:.1f}pt, expected 14pt".format(span["size"]))
        else:
            print("FAIL: Component 5 -- 'Prepared by: Finance Department' text not found")
    except Exception as e:
        print("ERROR: Component 5 --", e)

    # Component 6: 'Classification: Internal Only' in red at 12pt (0.15 points)
    try:
        span = find_span(spans, "Classification: Internal Only")
        if span:
            size_ok = abs(span["size"] - 12.0) <= SIZE_TOL
            # Red: (255, 0, 0) or close
            r, g, b = span["color_rgb"]
            is_red = r > 200 and g < 60 and b < 60
            if size_ok and is_red:
                print("PASS: Component 6 -- 'Classification: Internal Only' at {:.1f}pt, red {} (0.15 pts)".format(span["size"], span["color_rgb"]))
                total_score += 0.15
            elif size_ok:
                # Partial: correct size but not red
                print("PARTIAL: Component 6 -- Correct size but color={} not red (0.05 pts)".format(span["color_rgb"]))
                total_score += 0.05
            elif is_red:
                # Partial: red but wrong size
                print("PARTIAL: Component 6 -- Red but size={:.1f}pt (0.05 pts)".format(span["size"]))
                total_score += 0.05
            else:
                print("FAIL: Component 6 -- size={:.1f}pt, color={} (expected 12pt red)".format(span["size"], span["color_rgb"]))
        else:
            print("FAIL: Component 6 -- 'Classification: Internal Only' text not found")
    except Exception as e:
        print("ERROR: Component 6 --", e)

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print()
    print("Score: {}/1.0".format(total_score))
    print("REWARD: {}".format(final_score))
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print("File not found:", FILE_PATH)
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
