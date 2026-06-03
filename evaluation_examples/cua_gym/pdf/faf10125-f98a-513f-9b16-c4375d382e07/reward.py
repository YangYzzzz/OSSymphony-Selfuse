"""
Reward Script: Add blue border and corner markers to PDF
Task ID: pdf_pw_035
Domain: pdf
Scoring:
  Component 1: Output file exists with 10 pages (0.15)
  Component 2: Blue border rectangle on all pages (0.35)
  Component 3: Corner markers (L-shaped lines) on all pages (0.35)
  Component 4: Original certificate text preserved (0.15)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_pw_035'

# Expected border rectangle coordinates (36pt inset from Letter page edges)
BORDER_RECT = fitz.Rect(36.0, 36.0, 576.0, 756.0)
BLUE_COLOR = (0.0, 0.0, 1.0)
BORDER_WIDTH = 2.0
CORNER_LENGTH = 15.0
TOLERANCE = 2.0  # tolerance for coordinate comparison
COLOR_TOLERANCE = 0.1

# Corner marker expected endpoints (4 corners x 2 lines each = 8 lines)
# Each corner has a horizontal and vertical line segment of ~15pt
EXPECTED_CORNERS = [
    # Top-left corner
    {"start": (36.0, 36.0), "end": (51.0, 36.0)},   # horizontal
    {"start": (36.0, 36.0), "end": (36.0, 51.0)},   # vertical
    # Top-right corner
    {"start": (576.0, 36.0), "end": (561.0, 36.0)},  # horizontal
    {"start": (576.0, 36.0), "end": (576.0, 51.0)},  # vertical
    # Bottom-left corner
    {"start": (36.0, 756.0), "end": (51.0, 756.0)},  # horizontal
    {"start": (36.0, 756.0), "end": (36.0, 741.0)},  # vertical
    # Bottom-right corner
    {"start": (576.0, 756.0), "end": (561.0, 756.0)}, # horizontal
    {"start": (576.0, 756.0), "end": (576.0, 741.0)}, # vertical
]

def point_close(p1, p2, tol=TOLERANCE):
    """Check if two points are close enough."""
    return abs(p1[0] - p2[0]) <= tol and abs(p1[1] - p2[1]) <= tol

def color_close(c1, c2, tol=COLOR_TOLERANCE):
    """Check if two colors are close enough."""
    if c1 is None or c2 is None:
        return False
    return all(abs(a - b) <= tol for a, b in zip(c1, c2))

def has_blue_border_rect(page):
    """Check if the page has a blue border rectangle at the expected position."""
    drawings = page.get_drawings()
    for d in drawings:
        if not color_close(d.get('color'), BLUE_COLOR):
            continue
        if abs(d.get('width', 0) - BORDER_WIDTH) > 0.5:
            continue
        items = d.get('items', [])
        for item in items:
            if item[0] == 're':  # rectangle item
                rect = item[1]
                if (abs(rect.x0 - BORDER_RECT.x0) <= TOLERANCE and
                    abs(rect.y0 - BORDER_RECT.y0) <= TOLERANCE and
                    abs(rect.x1 - BORDER_RECT.x1) <= TOLERANCE and
                    abs(rect.y1 - BORDER_RECT.y1) <= TOLERANCE):
                    return True
    return False

def count_corner_markers(page):
    """Count how many of the 8 expected corner marker lines are present."""
    drawings = page.get_drawings()
    found = 0
    for expected in EXPECTED_CORNERS:
        marker_found = False
        for d in drawings:
            if not color_close(d.get('color'), BLUE_COLOR):
                continue
            if abs(d.get('width', 0) - BORDER_WIDTH) > 0.5:
                continue
            items = d.get('items', [])
            for item in items:
                if item[0] == 'l':  # line item
                    start = (item[1].x, item[1].y)
                    end = (item[2].x, item[2].y)
                    if (point_close(start, expected["start"]) and point_close(end, expected["end"])):
                        marker_found = True
                        break
                    # Check reversed direction too
                    if (point_close(start, expected["end"]) and point_close(end, expected["start"])):
                        marker_found = True
                        break
            if marker_found:
                break
        if marker_found:
            found += 1
    return found


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has exactly 10 pages (0.15 points)
    try:
        page_count = doc.page_count
        if page_count == 10:
            print(f"PASS: Component 1 - File has {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 - Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 - {e}")

    # Component 2: Blue border rectangle on ALL pages (0.35 points)
    # Each page contributes equally: 0.35 / 10 = 0.035 per page
    try:
        pages_with_border = 0
        for i in range(doc.page_count):
            page = doc[i]
            if has_blue_border_rect(page):
                pages_with_border += 1
            else:
                print(f"  FAIL: Page {i} missing blue border rectangle")
        
        border_score = 0.35 * (pages_with_border / max(doc.page_count, 1))
        if pages_with_border == doc.page_count and doc.page_count == 10:
            print(f"PASS: Component 2 - Blue border on all {pages_with_border}/{doc.page_count} pages (0.35 pts)")
            total_score += 0.35
        elif pages_with_border > 0:
            print(f"PARTIAL: Component 2 - Blue border on {pages_with_border}/{doc.page_count} pages ({border_score:.3f} pts)")
            total_score += border_score
        else:
            print(f"FAIL: Component 2 - No pages have blue border rectangle")
    except Exception as e:
        print(f"ERROR: Component 2 - {e}")

    # Component 3: Corner markers on ALL pages (0.35 points)
    # Each page should have 8 corner markers (2 per corner x 4 corners)
    # Score: pages_fraction * markers_fraction * 0.35
    try:
        total_markers = 0
        expected_total = 8 * 10  # 8 markers per page, 10 pages
        for i in range(doc.page_count):
            page = doc[i]
            markers = count_corner_markers(page)
            total_markers += markers
            if markers < 8:
                print(f"  Page {i}: {markers}/8 corner markers found")

        marker_fraction = total_markers / max(expected_total, 1)
        marker_score = 0.35 * marker_fraction
        if total_markers == expected_total:
            print(f"PASS: Component 3 - All {total_markers}/{expected_total} corner markers present (0.35 pts)")
            total_score += 0.35
        elif total_markers > 0:
            print(f"PARTIAL: Component 3 - {total_markers}/{expected_total} corner markers ({marker_score:.3f} pts)")
            total_score += marker_score
        else:
            print(f"FAIL: Component 3 - No corner markers found")
    except Exception as e:
        print(f"ERROR: Component 3 - {e}")

    # Component 4: Original certificate text preserved (0.15 points)
    # Check that key certificate text is still present on pages
    try:
        expected_names = ["Sarah Chen", "Marcus Johnson", "Elena Rodriguez"]
        names_found = 0
        for i, name in enumerate(expected_names):
            page = doc[i]
            text = page.get_text()
            if name in text:
                names_found += 1
        
        # Also check the generic certificate text on any page
        has_cert_text = False
        first_page_text = doc[0].get_text()
        if "Certificate of Completion" in first_page_text:
            has_cert_text = True

        if names_found == len(expected_names) and has_cert_text:
            print(f"PASS: Component 4 - Original certificate content preserved (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 4 - Names found: {names_found}/{len(expected_names)}, cert text: {has_cert_text}")
    except Exception as e:
        print(f"ERROR: Component 4 - {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/certificate_batch_bordered.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
