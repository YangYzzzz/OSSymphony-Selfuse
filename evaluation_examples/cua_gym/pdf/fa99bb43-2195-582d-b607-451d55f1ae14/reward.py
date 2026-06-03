"""
Reward Script: Add pink highlights to specific text in grant_proposal.pdf
Task ID: pdf_basic_049
Domain: pdf
Scoring:
  - Component 1: Highlight annotation over 'total budget: $125,000' on page 8 (0.5 pts)
  - Component 2: Highlight annotation over 'project timeline: 18 months' on page 9 (0.5 pts)
  Each component checks that the annotation is:
    (a) of type Highlight
    (b) overlaps the target text location
    (c) has a pink color (stroke approximately (1.0, 0.75, 0.8))
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user/Desktop'
TASK_ID = 'pdf_basic_049'
FILE_NAME = 'grant_proposal.pdf'


def is_pink_color(color_tuple, tolerance=0.08):
    """
    Check whether a color is pink.
    Pink in PDF annotations (as seen in golden): approximately (1.0, 0.75, 0.8)
    We allow a tolerance to handle minor floating-point or encoding differences.
    """
    if color_tuple is None or len(color_tuple) < 3:
        return False
    r, g, b = color_tuple[0], color_tuple[1], color_tuple[2]
    # Pink: R near 1.0, G near 0.75, B near 0.8
    return (abs(r - 1.0) <= tolerance and
            abs(g - 0.75) <= tolerance and
            abs(b - 0.8) <= tolerance)


def check_highlight_on_text(page, target_text, check_color=True):
    """
    Check if a Highlight annotation exists on a page that overlaps with the
    location of target_text. Optionally verify the annotation is pink.
    Returns (found_highlight: bool, found_pink: bool, detail: str)
    """
    # Find all instances of the target text on this page
    text_instances = page.search_for(target_text)
    if not text_instances:
        return False, False, f"Target text '{target_text}' not found on page"

    for annot in page.annots():
        if annot.type[1] != "Highlight":
            continue
        annot_rect = annot.rect
        # Check if annotation overlaps any instance of the target text
        for inst in text_instances:
            if annot_rect.intersects(inst):
                # Annotation found overlapping the text
                stroke = annot.colors.get("stroke")
                if check_color:
                    if stroke and is_pink_color(stroke):
                        return True, True, f"Found pink Highlight over '{target_text}', color={stroke}"
                    else:
                        return True, False, f"Found Highlight over '{target_text}' but color={stroke} is not pink"
                else:
                    return True, True, f"Found Highlight over '{target_text}'"
    return False, False, f"No Highlight annotation found over '{target_text}'"


def verify_task(file_path):
    """
    Verify that pink highlights have been added to:
      - 'total budget: $125,000' on page 8 (index 7)
      - 'project timeline: 18 months' on page 9 (index 8)
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: load the PDF
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: verify expected page count
    if doc.page_count != 15:
        print(f"WARN: Expected 15 pages, found {doc.page_count}. Continuing...")

    # Component 1: Pink highlight over 'total budget: $125,000' on page 8 (index 7) (0.5 points)
    try:
        page8 = doc[7]  # page 8 is 0-indexed as 7
        found, is_pink, detail = check_highlight_on_text(page8, "total budget: $125,000")
        if found and is_pink:
            print(f"PASS: Component 1 — Pink highlight over 'total budget: $125,000' on page 8 (0.5 pts)")
            print(f"  Detail: {detail}")
            total_score += 0.5
        elif found and not is_pink:
            print(f"FAIL: Component 1 — Highlight found over 'total budget: $125,000' on page 8, but not pink")
            print(f"  Detail: {detail}")
        else:
            print(f"FAIL: Component 1 — No pink highlight over 'total budget: $125,000' on page 8")
            print(f"  Detail: {detail}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Pink highlight over 'project timeline: 18 months' on page 9 (index 8) (0.5 points)
    try:
        page9 = doc[8]  # page 9 is 0-indexed as 8
        found, is_pink, detail = check_highlight_on_text(page9, "project timeline: 18 months")
        if found and is_pink:
            print(f"PASS: Component 2 — Pink highlight over 'project timeline: 18 months' on page 9 (0.5 pts)")
            print(f"  Detail: {detail}")
            total_score += 0.5
        elif found and not is_pink:
            print(f"FAIL: Component 2 — Highlight found over 'project timeline: 18 months' on page 9, but not pink")
            print(f"  Detail: {detail}")
        else:
            print(f"FAIL: Component 2 — No pink highlight over 'project timeline: 18 months' on page 9")
            print(f"  Detail: {detail}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against the canonical artifact path on the VM
file_path = f'{WORKDIR}/{FILE_NAME}'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
