"""
Reward Script: Delete highlight on 'passed' and add red highlight on 'failed' on page 2
Task ID: pdf_basic_151
Domain: pdf
Scoring:
  Component 1 (0.4): No highlight annotation exists overlapping any 'passed' word on page 2
  Component 2 (0.6): A red highlight annotation exists overlapping 'failed' on page 2
Total: 1.0

Task: Open ~/Desktop/inspection_checklist.pdf in Evince, navigate to page 2,
delete the existing highlight annotation on the word 'passed', then add a new
red highlight to the word 'failed' on the same page. Save the document.
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_basic_151'
FILE_PATH = f'{WORKDIR}/Desktop/inspection_checklist.pdf'
PAGE_NUM = 1  # Page 2 is index 1 (0-indexed)


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the PDF file
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    if doc.page_count < 2:
        print(f"CRITICAL: Expected at least 2 pages, found {doc.page_count}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[PAGE_NUM]

    # Get all annotations on page 2
    all_annots = list(page.annots())
    highlight_annots = [a for a in all_annots if a.type[1] == 'Highlight']

    print(f"INFO: Page 2 has {len(all_annots)} total annotations, "
          f"{len(highlight_annots)} highlight annotations")

    # Find 'passed' and 'failed' text locations
    passed_rects = page.search_for('passed')
    failed_rects = page.search_for('failed')
    print(f"INFO: Found {len(passed_rects)} 'passed' occurrences, "
          f"{len(failed_rects)} 'failed' occurrences on page 2")

    # Component 1: No highlight annotation overlaps any 'passed' text (0.4 points)
    # The initial state had a yellow highlight on 'passed'. This component checks it was removed.
    try:
        highlight_on_passed = False
        for annot in highlight_annots:
            annot_rect = annot.rect
            for pr in passed_rects:
                if annot_rect.intersects(pr):
                    highlight_on_passed = True
                    stroke_color = annot.colors.get('stroke', [])
                    print(f"FAIL: Component 1 — highlight still exists overlapping 'passed' "
                          f"at {pr}, annotation rect={annot_rect}, color={stroke_color}")
                    break
            if highlight_on_passed:
                break

        if not highlight_on_passed:
            print("PASS: Component 1 — No highlight annotation overlaps any 'passed' text (0.4 pts)")
            total_score += 0.4
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: A red highlight annotation overlaps 'failed' text on page 2 (0.6 points)
    # Red color in PDF is (1.0, 0.0, 0.0). Allow slight tolerance.
    try:
        red_highlight_on_failed = False
        red_color_tolerance = 0.15

        for annot in highlight_annots:
            if annot.type[1] != 'Highlight':
                continue
            annot_rect = annot.rect
            stroke = annot.colors.get('stroke', [])

            # Check if this annotation overlaps any 'failed' instance
            overlaps_failed = False
            for fr in failed_rects:
                if annot_rect.intersects(fr):
                    overlaps_failed = True
                    break

            if not overlaps_failed:
                continue

            # Check if the color is red: (R~1.0, G~0.0, B~0.0)
            if len(stroke) >= 3:
                r, g, b = stroke[0], stroke[1], stroke[2]
                is_red = (r > (1.0 - red_color_tolerance) and
                          g < red_color_tolerance and
                          b < red_color_tolerance)
                if is_red:
                    red_highlight_on_failed = True
                    print(f"PASS: Component 2 — Red highlight found on 'failed' at rect={annot_rect}, "
                          f"color=({r:.2f}, {g:.2f}, {b:.2f}) (0.6 pts)")
                    break
                else:
                    print(f"FAIL: Component 2 — Highlight on 'failed' found but color is not red: "
                          f"({r:.2f}, {g:.2f}, {b:.2f}), expected ~(1.0, 0.0, 0.0)")
            else:
                print(f"FAIL: Component 2 — Highlight on 'failed' has no stroke color defined")

        if not red_highlight_on_failed:
            # Check if any annotation overlaps failed but with wrong color (already printed above)
            overlaps_any_failed = any(
                any(annot.rect.intersects(fr) for fr in failed_rects)
                for annot in highlight_annots
            )
            if not overlaps_any_failed:
                print("FAIL: Component 2 — No highlight annotation found overlapping 'failed' text")

        if red_highlight_on_failed:
            total_score += 0.6

    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
