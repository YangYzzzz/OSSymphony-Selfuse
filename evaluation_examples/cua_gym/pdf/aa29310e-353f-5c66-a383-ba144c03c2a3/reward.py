"""
Reward Script: Add yellow highlight on page 3 and green highlight on page 5 of market_analysis.pdf
Task ID: pdf_basic_168
Domain: pdf
Scoring:
  - Component 1 (0.5 pts): Yellow highlight annotation on page 3 covering 'market share increased by 12%'
  - Component 2 (0.5 pts): Green highlight annotation on page 5 covering 'projected growth rate of 8.5%'
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

FILE_PATH = '/home/user/Desktop/market_analysis.pdf'

# Color tolerance for float-based color comparison (0-1 scale)
COLOR_TOLERANCE = 0.1


def colors_match(actual, expected, tol=COLOR_TOLERANCE):
    """Compare two RGB color tuples (floats 0-1) with tolerance."""
    if actual is None or expected is None:
        return False
    if len(actual) != len(expected):
        return False
    return all(abs(a - e) <= tol for a, e in zip(actual, expected))


def find_highlight_on_page(page, target_text, expected_color):
    """
    Search for a Highlight annotation on the given page that:
      1. Is of type 'Highlight'
      2. Overlaps with the bounding rect of target_text
      3. Has a stroke color matching expected_color (tolerance COLOR_TOLERANCE)

    Returns (found: bool, message: str)
    """
    text_instances = page.search_for(target_text)
    if not text_instances:
        return False, f"Target text '{target_text}' not found on page"

    # Collect all Highlight annotations on the page
    all_highlights = [a for a in page.annots() if a.type[1] == "Highlight"]
    if not all_highlights:
        return False, "No Highlight annotations present on page"

    # Check each highlight for overlap and correct color
    for annot in all_highlights:
        annot_rect = annot.rect
        stroke = annot.colors.get("stroke")

        overlaps_text = any(annot_rect.intersects(inst) for inst in text_instances)
        if not overlaps_text:
            continue

        if colors_match(stroke, expected_color):
            return True, (f"Highlight rect={annot_rect}, color={stroke} "
                          f"overlaps text at {text_instances[0]}")
        else:
            return False, (f"Highlight overlaps text but wrong color: "
                           f"expected {expected_color}, got {stroke}")

    return False, (f"No highlight overlapping '{target_text}' found "
                   f"(checked {len(all_highlights)} highlight(s))")


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load PDF — gate on file existence and readability
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if doc.page_count < 5:
        print(f"CRITICAL: Expected at least 5 pages, found {doc.page_count}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # -----------------------------------------------------------------------
    # Component 1: Yellow highlight on page 3 covering 'market share increased by 12%' (0.5 pts)
    # Task-introduced change: initial_env has no annotations on any page.
    # -----------------------------------------------------------------------
    try:
        page3 = doc[2]  # 0-indexed: page index 2 = page number 3
        yellow = (1.0, 1.0, 0.0)
        p3_found, p3_msg = find_highlight_on_page(
            page3, "market share increased by 12%", yellow
        )
        if p3_found:
            print(f"PASS: Component 1 — Yellow highlight on page 3: {p3_msg} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Yellow highlight on page 3 not confirmed: {p3_msg}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # -----------------------------------------------------------------------
    # Component 2: Green highlight on page 5 covering 'projected growth rate of 8.5%' (0.5 pts)
    # Task-introduced change: initial_env has no annotations on any page.
    # -----------------------------------------------------------------------
    try:
        page5 = doc[4]  # 0-indexed: page index 4 = page number 5
        green = (0.0, 1.0, 0.0)
        p5_found, p5_msg = find_highlight_on_page(
            page5, "projected growth rate of 8.5%", green
        )
        if p5_found:
            print(f"PASS: Component 2 — Green highlight on page 5: {p5_msg} (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 2 — Green highlight on page 5 not confirmed: {p5_msg}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: verify against the canonical task file path
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
