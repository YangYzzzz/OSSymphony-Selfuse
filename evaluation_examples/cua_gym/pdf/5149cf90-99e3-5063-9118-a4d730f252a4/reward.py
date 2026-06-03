"""
Reward Script: Change yellow highlight annotation to green on page 7 of quality_report.pdf
Task ID: pdf_basic_120
Domain: pdf
Scoring:
  Component 1: Page 7 has exactly one Highlight annotation (0.4 pts)
  Component 2: That highlight annotation color is green [0.0, 1.0, 0.0] (0.6 pts)
  Total: 1.0
"""

import os
import pymupdf  # PyMuPDF

WORKDIR = '/home/user/Desktop'
TASK_ID = 'pdf_basic_120'
FILE_PATH = f'{WORKDIR}/quality_report.pdf'

# Target: green color as (R, G, B) floats 0-1
GREEN_COLOR = [0.0, 1.0, 0.0]
YELLOW_COLOR = [1.0, 1.0, 0.0]
COLOR_TOLERANCE = 0.05  # tolerance for float comparison

PAGE_NUM = 6  # Page 7 is index 6 (0-indexed)


def colors_match(actual, expected, tol=COLOR_TOLERANCE):
    """Compare two RGB color lists/tuples with tolerance."""
    if actual is None or expected is None:
        return False
    if len(actual) != len(expected):
        return False
    return all(abs(a - e) <= tol for a, e in zip(actual, expected))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Task: Change the color of the yellow highlight annotation on page 7 to green.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: file must exist and be openable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: PDF must have at least 10 pages (task context states 10 pages)
    if doc.page_count < 7:
        print(f"CRITICAL: PDF has only {doc.page_count} pages, expected at least 7")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Page 7 has at least one Highlight annotation (0.4 points)
    # This verifies the annotation was preserved and not deleted
    # NOTE: The initial_env also has a highlight here, so this alone would score on initial.
    # We intentionally use this as part of a compound check to gate Component 2.
    # However, to ensure initial scores 0.0, we make this component only
    # award points when the highlight is NOT yellow (i.e., the color was changed).
    # So Component 1 and 2 are merged: we require color != yellow for any points.
    try:
        page = doc[PAGE_NUM]
        highlight_annots = [a for a in page.annots() if a.type[1] == "Highlight"]

        if len(highlight_annots) == 0:
            print(f"FAIL: Component 1 — No Highlight annotations found on page 7")
        else:
            # Found at least one highlight annotation
            highlight = highlight_annots[0]
            stroke_color = highlight.colors.get("stroke")
            print(f"INFO: Found highlight on page 7 with stroke color: {stroke_color}")

            # Component 1: Highlight exists AND color is no longer yellow (0.4 points)
            # A yellow color means the task was NOT completed.
            # A non-yellow color means at least some change was made.
            if stroke_color and not colors_match(stroke_color, YELLOW_COLOR):
                print(f"PASS: Component 1 — Highlight annotation exists on page 7 and color changed from yellow ({0.4} pts)")
                total_score += 0.4
            else:
                if colors_match(stroke_color, YELLOW_COLOR):
                    print(f"FAIL: Component 1 — Highlight is still yellow {stroke_color}, should be green")
                else:
                    print(f"FAIL: Component 1 — Unexpected highlight color state: {stroke_color}")

            # Component 2: Highlight color is specifically green [0.0, 1.0, 0.0] (0.6 points)
            if stroke_color and colors_match(stroke_color, GREEN_COLOR):
                print(f"PASS: Component 2 — Highlight color is green {stroke_color} ({0.6} pts)")
                total_score += 0.6
            else:
                print(f"FAIL: Component 2 — Expected green {GREEN_COLOR}, found {stroke_color}")

    except Exception as e:
        print(f"ERROR: Could not check page 7 annotations: {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Run verification
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
