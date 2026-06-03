"""
Reward Script: Verify colored tab/bookmark indicators on PDF pages
Task ID: pdf_res_094
Domain: pdf
Scoring: 0.1 pts for output file + page count, 0.18 pts each for 5 colored tabs (total 1.0)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_094'
OUTPUT_PATH = os.path.join(WORKDIR, 'thesis', 'tabbed_thesis_marked.pdf')

# Expected colored tabs: (page_index, color_name, (R, G, B) in 0-1 range)
# Colors use tolerance since exact values may vary by implementation
EXPECTED_TABS = [
    (0,  "red",    (1.0, 0.0, 0.0)),
    (14, "blue",   (0.0, 0.0, 1.0)),
    (29, "green",  (0.0, 0.5, 0.0)),   # green can be 0.0-0.8 for G channel
    (49, "orange", (1.0, 0.5, 0.0)),
    (69, "purple", (0.5, 0.0, 0.5)),
]

# Right edge threshold: tab rect should be near the right side of the page
RIGHT_EDGE_MIN_X = 500  # typical A4/letter width is ~595-612 pts


def is_color_match(actual, expected, tolerance=0.25):
    """Check if actual RGB color matches expected within tolerance."""
    if actual is None:
        return False
    if len(actual) < 3 or len(expected) < 3:
        return False
    return all(abs(a - e) < tolerance for a, e in zip(actual[:3], expected[:3]))


def is_right_edge_rect(rect):
    """Check if a rectangle is positioned on the right edge of the page."""
    # rect.x0 should be >= RIGHT_EDGE_MIN_X (near right margin)
    # width should be small (tab indicator, not a full-width element)
    width = rect.x1 - rect.x0
    return rect.x0 >= RIGHT_EDGE_MIN_X and width < 50


def check_tab_on_page(doc, page_idx, expected_color_name, expected_color_rgb):
    """
    Check if a colored tab rectangle exists on the right edge of the given page.
    Returns True if found, False otherwise.
    """
    page = doc[page_idx]
    drawings = page.get_drawings()

    for d in drawings:
        fill = d.get("fill")
        color = d.get("color")
        rect = d.get("rect")

        if rect is None:
            continue

        # Check if this drawing is on the right edge
        if not is_right_edge_rect(rect):
            continue

        # Check if fill or stroke color matches expected
        if is_color_match(fill, expected_color_rgb) or is_color_match(color, expected_color_rgb):
            return True

    return False


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Component 1: Output file exists and has 75 pages (0.1 points)
    try:
        if not os.path.exists(OUTPUT_PATH):
            print(f"FAIL: Output file not found: {OUTPUT_PATH}")
            print("REWARD: 0.0")
            return 0.0

        doc = pymupdf.open(OUTPUT_PATH)
        page_count = doc.page_count

        if page_count == 75:
            print(f"PASS: Component 1 -- Output file exists with {page_count} pages (0.1 pts)")
            total_score += 0.1
        else:
            print(f"FAIL: Component 1 -- Expected 75 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- Cannot load file: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Components 2-6: Check each colored tab (0.18 points each)
    for i, (page_idx, color_name, expected_rgb) in enumerate(EXPECTED_TABS):
        comp_num = i + 2
        try:
            if check_tab_on_page(doc, page_idx, color_name, expected_rgb):
                print(f"PASS: Component {comp_num} -- {color_name} tab on page {page_idx + 1} right edge (0.18 pts)")
                total_score += 0.18
            else:
                print(f"FAIL: Component {comp_num} -- No {color_name} tab found on page {page_idx + 1} right edge")
        except Exception as e:
            print(f"ERROR: Component {comp_num} -- {e}")

    doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification
verify_task()
