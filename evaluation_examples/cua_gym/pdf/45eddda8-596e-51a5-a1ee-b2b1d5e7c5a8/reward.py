"""
Reward Script: Add colored sidebar annotation strips to PDF pages
Task ID: pdf_ro_031
Domain: pdf
Scoring:
  - Component 1 (0.2): Output file exists with 10 pages
  - Component 2 (0.4): Pages 1-5 have green (#00AA00) sidebar rect
  - Component 3 (0.4): Pages 6-10 have yellow (#FFD700) sidebar rect
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_031'
OUTPUT_FILE = os.path.join(WORKDIR, 'Documents', 'report_color_coded.pdf')

# Color tolerances: #00AA00 = (0, 170, 0) -> (0.0, 0.667, 0.0) in float
# #FFD700 = (255, 215, 0) -> (1.0, 0.843, 0.0) in float
GREEN_EXPECTED = (0.0, 0.667, 0.0)
YELLOW_EXPECTED = (1.0, 0.843, 0.0)
COLOR_TOLERANCE = 0.05

# Sidebar rect expected: (0, 0, 18, 792) — 0.25 inch = 18 points wide, full page height
SIDEBAR_WIDTH_EXPECTED = 18.0
RECT_TOLERANCE = 5.0  # points tolerance for rect dimensions


def color_matches(actual, expected, tol=COLOR_TOLERANCE):
    """Check if actual RGB color tuple matches expected within tolerance."""
    if actual is None or len(actual) < 3:
        return False
    for a, e in zip(actual[:3], expected):
        if abs(a - e) > tol:
            return False
    return True


def find_sidebar_drawing(drawings, page_height):
    """Find a filled rectangle along the left edge spanning full page height."""
    for d in drawings:
        fill = d.get('fill')
        rect = d.get('rect')
        if fill is None or rect is None:
            continue
        # Check it's along left edge: x0 near 0, x1 near 18, y0 near 0, y1 near page_height
        x0, y0, x1, y1 = rect.x0, rect.y0, rect.x1, rect.y1
        if (abs(x0) < RECT_TOLERANCE and
            abs(x1 - SIDEBAR_WIDTH_EXPECTED) < RECT_TOLERANCE and
            abs(y0) < RECT_TOLERANCE and
            abs(y1 - page_height) < RECT_TOLERANCE):
            return d
    return None


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists with 10 pages (0.2 points)
    try:
        if not os.path.exists(OUTPUT_FILE):
            print(f"FAIL: Component 1 — Output file not found: {OUTPUT_FILE}")
            print("REWARD: 0.0")
            return 0.0

        import fitz
        doc = fitz.open(OUTPUT_FILE)
        page_count = doc.page_count

        if page_count == 10:
            print(f"PASS: Component 1 — File exists with {page_count} pages (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 1 — Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 2: Pages 1-5 (index 0-4) have green sidebar (0.4 points)
    try:
        green_pass = 0
        for i in range(5):
            if i >= page_count:
                break
            page = doc[i]
            drawings = page.get_drawings()
            sidebar = find_sidebar_drawing(drawings, page.rect.height)
            if sidebar is not None and color_matches(sidebar.get('fill'), GREEN_EXPECTED):
                green_pass += 1
            else:
                actual_fill = sidebar.get('fill') if sidebar else None
                print(f"  FAIL: Page {i+1} — expected green sidebar, found fill={actual_fill}")

        if green_pass == 5:
            print(f"PASS: Component 2 — All 5 pages (1-5) have green sidebar (0.4 pts)")
            total_score += 0.4
        elif green_pass > 0:
            partial = round(0.4 * green_pass / 5, 2)
            print(f"PARTIAL: Component 2 — {green_pass}/5 pages have green sidebar ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No pages 1-5 have green sidebar")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Pages 6-10 (index 5-9) have yellow sidebar (0.4 points)
    try:
        yellow_pass = 0
        for i in range(5, 10):
            if i >= page_count:
                break
            page = doc[i]
            drawings = page.get_drawings()
            sidebar = find_sidebar_drawing(drawings, page.rect.height)
            if sidebar is not None and color_matches(sidebar.get('fill'), YELLOW_EXPECTED):
                yellow_pass += 1
            else:
                actual_fill = sidebar.get('fill') if sidebar else None
                print(f"  FAIL: Page {i+1} — expected yellow sidebar, found fill={actual_fill}")

        if yellow_pass == 5:
            print(f"PASS: Component 3 — All 5 pages (6-10) have yellow sidebar (0.4 pts)")
            total_score += 0.4
        elif yellow_pass > 0:
            partial = round(0.4 * yellow_pass / 5, 2)
            print(f"PARTIAL: Component 3 — {yellow_pass}/5 pages have yellow sidebar ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 3 — No pages 6-10 have yellow sidebar")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
