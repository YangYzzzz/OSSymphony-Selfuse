"""
Reward Script: Add colored double-line border frame to audit_certificate.pdf
Task ID: pdf_fin_089
Domain: pdf
Scoring:
  - Component 1 (0.15): Output file exists with correct page count (3 pages)
  - Component 2 (0.45): Outer dark blue border on all 3 pages (~2pt, ~20pt margin)
  - Component 3 (0.40): Inner gold border on all 3 pages (~1pt, ~25pt margin)
"""

import os
import fitz  # PyMuPDF

WORKDIR = '/home/user'
TASK_ID = 'pdf_fin_089'
OUTPUT_PATH = os.path.join(WORKDIR, 'finance', 'audit_certificate_framed.pdf')
EXPECTED_PAGES = 3

# Tolerance for color and dimension checks
COLOR_TOL = 0.15
RECT_TOL = 5.0  # points
WIDTH_TOL = 0.5  # points


def color_close(actual, expected, tol=COLOR_TOL):
    """Check if two RGB color tuples are close enough."""
    if actual is None or expected is None:
        return False
    if len(actual) != len(expected):
        return False
    return all(abs(a - e) < tol for a, e in zip(actual, expected))


def rect_close(actual_rect, expected_coords, tol=RECT_TOL):
    """Check if a rect is close to expected (x0, y0, x1, y1)."""
    if actual_rect is None:
        return False
    ax0, ay0, ax1, ay1 = actual_rect.x0, actual_rect.y0, actual_rect.x1, actual_rect.y1
    ex0, ey0, ex1, ey1 = expected_coords
    return (abs(ax0 - ex0) < tol and abs(ay0 - ey0) < tol and
            abs(ax1 - ex1) < tol and abs(ay1 - ey1) < tol)


def is_rectangle_drawing(drawing):
    """Check if a drawing is a rectangle (has 're' item type)."""
    items = drawing.get('items', [])
    for item in items:
        if item[0] == 're':
            return True
    return False


def find_border_rects(page):
    """Find rectangle drawings on a page, returning list of (color, width, rect) tuples."""
    drawings = page.get_drawings()
    rects = []
    for d in drawings:
        if is_rectangle_drawing(d):
            rects.append({
                'color': d.get('color'),
                'width': d.get('width'),
                'rect': d.get('rect'),
                'fill': d.get('fill'),
            })
    return rects


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist
    if not os.path.exists(file_path):
        print(f"CRITICAL: Output file not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.15 points)
    # This is task-introduced: the output file doesn't exist in initial_env
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 -- Output file exists with {page_count} pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Expected border properties
    # Outer border: dark blue, ~2pt width, ~20pt margin from edge
    # For Letter size (612x792): rect should be ~(20, 20, 592, 772)
    DARK_BLUE = (0.0, 0.0, 0.55)
    OUTER_WIDTH = 2.0
    # Inner border: gold, ~1pt width, ~25pt margin from edge
    # rect should be ~(25, 25, 587, 767)
    GOLD = (0.85, 0.65, 0.13)
    INNER_WIDTH = 1.0

    # Component 2: Outer dark blue border on all pages (0.45 points)
    # 0.15 pts per page
    try:
        outer_pass_count = 0
        for i in range(min(len(doc), EXPECTED_PAGES)):
            page = doc[i]
            pw, ph = page.rect.width, page.rect.height
            expected_outer_rect = (20.0, 20.0, pw - 20.0, ph - 20.0)
            rects = find_border_rects(page)

            found_outer = False
            for r in rects:
                if (color_close(r['color'], DARK_BLUE) and
                        abs(r['width'] - OUTER_WIDTH) < WIDTH_TOL and
                        rect_close(r['rect'], expected_outer_rect) and
                        r['fill'] is None):
                    found_outer = True
                    break

            if found_outer:
                outer_pass_count += 1
                print(f"  Page {i}: Outer dark blue border FOUND")
            else:
                print(f"  Page {i}: Outer dark blue border NOT FOUND (rects: {[(r['color'], r['width'], str(r['rect'])) for r in rects]})")

        outer_score = (outer_pass_count / EXPECTED_PAGES) * 0.45
        if outer_pass_count == EXPECTED_PAGES:
            print(f"PASS: Component 2 -- Outer dark blue border on all {EXPECTED_PAGES} pages (0.45 pts)")
        else:
            print(f"PARTIAL: Component 2 -- Outer dark blue border on {outer_pass_count}/{EXPECTED_PAGES} pages ({outer_score:.2f} pts)")
        total_score += outer_score
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Inner gold border on all pages (0.40 points)
    # ~0.133 pts per page
    try:
        inner_pass_count = 0
        for i in range(min(len(doc), EXPECTED_PAGES)):
            page = doc[i]
            pw, ph = page.rect.width, page.rect.height
            expected_inner_rect = (25.0, 25.0, pw - 25.0, ph - 25.0)
            rects = find_border_rects(page)

            found_inner = False
            for r in rects:
                if (color_close(r['color'], GOLD) and
                        abs(r['width'] - INNER_WIDTH) < WIDTH_TOL and
                        rect_close(r['rect'], expected_inner_rect) and
                        r['fill'] is None):
                    found_inner = True
                    break

            if found_inner:
                inner_pass_count += 1
                print(f"  Page {i}: Inner gold border FOUND")
            else:
                print(f"  Page {i}: Inner gold border NOT FOUND (rects: {[(r['color'], r['width'], str(r['rect'])) for r in rects]})")

        inner_score = (inner_pass_count / EXPECTED_PAGES) * 0.40
        if inner_pass_count == EXPECTED_PAGES:
            print(f"PASS: Component 3 -- Inner gold border on all {EXPECTED_PAGES} pages (0.40 pts)")
        else:
            print(f"PARTIAL: Component 3 -- Inner gold border on {inner_pass_count}/{EXPECTED_PAGES} pages ({inner_score:.2f} pts)")
        total_score += inner_score
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score:.2f}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
