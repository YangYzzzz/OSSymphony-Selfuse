"""
Reward Script: Add circle annotation and text note on page 10 of system_design.pdf
Task ID: pdf_fm_040
Domain: pdf
Scoring:
  - Component 1 (0.3): Circle annotation exists on page 9 (0-indexed)
  - Component 2 (0.2): Circle annotation has blue border
  - Component 3 (0.2): Text annotation exists on page 9 (0-indexed)
  - Component 4 (0.3): Text annotation content matches expected text
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_040'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'engineering', 'system_design.pdf')
PAGE_NUM = 9  # page 10 in 1-indexed = page 9 in 0-indexed
EXPECTED_TEXT = 'Revise this component diagram per latest architecture review'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: file must exist and be loadable
    try:
        doc = pymupdf.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: must have at least 10 pages
    if len(doc) < 10:
        print(f"CRITICAL: PDF has only {len(doc)} pages, need at least 10")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[PAGE_NUM]

    # Collect annotations on the target page
    try:
        annots = list(page.annots()) if page.annots() else []
    except Exception as e:
        print(f"ERROR: Could not read annotations: {e}")
        annots = []

    # Separate annotations by type
    circle_annots = [a for a in annots if a.type[1] == 'Circle']
    text_annots = [a for a in annots if a.type[1] == 'Text']

    # Component 1: Circle annotation exists on page 10 (0.3 points)
    # This is a task-introduced change: initial has 0 annotations on this page
    try:
        if len(circle_annots) >= 1:
            print(f"PASS: Component 1 — Circle annotation found on page {PAGE_NUM + 1} ({len(circle_annots)} found) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — No Circle annotation on page {PAGE_NUM + 1}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Circle annotation has blue border (0.2 points)
    # Blue = stroke color (0.0, 0.0, 1.0)
    try:
        if len(circle_annots) >= 1:
            circle = circle_annots[0]
            stroke = circle.colors.get("stroke")
            if stroke is not None and len(stroke) == 3:
                # Check if stroke is blue (R~0, G~0, B~1)
                r, g, b = stroke[0], stroke[1], stroke[2]
                if r < 0.1 and g < 0.1 and b > 0.9:
                    print(f"PASS: Component 2 — Circle has blue border (stroke={stroke}) (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 2 — Circle border is not blue, stroke={stroke}")
            else:
                print(f"FAIL: Component 2 — Circle has no stroke color defined, stroke={stroke}")
        else:
            print(f"FAIL: Component 2 — No Circle annotation to check border color")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Text annotation exists on page 10 (0.2 points)
    # This is a task-introduced change: initial has 0 annotations on this page
    try:
        if len(text_annots) >= 1:
            print(f"PASS: Component 3 — Text annotation found on page {PAGE_NUM + 1} ({len(text_annots)} found) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — No Text annotation on page {PAGE_NUM + 1}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Text annotation content matches expected text (0.3 points)
    try:
        if len(text_annots) >= 1:
            # Check if any text annotation contains the expected content
            matching = [ta for ta in text_annots
                        if EXPECTED_TEXT.lower() in ta.info.get("content", "").lower()]
            if len(matching) >= 1:
                content = matching[0].info.get("content", "")
                print(f"PASS: Component 4 — Text annotation content matches: '{content}' (0.3 pts)")
                total_score += 0.3
            else:
                contents = [ta.info.get("content", "") for ta in text_annots]
                print(f"FAIL: Component 4 — No text annotation with expected content. Found: {contents}")
        else:
            print(f"FAIL: Component 4 — No Text annotation to check content")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
