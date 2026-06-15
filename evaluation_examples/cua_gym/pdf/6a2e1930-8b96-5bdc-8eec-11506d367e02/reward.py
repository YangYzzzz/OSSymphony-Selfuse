"""
Reward Script: Add rectangle border annotation and text note on page 3 of blueprint.pdf
Task ID: pdf_ro_014
Domain: pdf
Scoring:
  Component 1 (0.35): Square annotation exists on page 3 with correct rect ~(100,200,400,350)
  Component 2 (0.25): Square annotation has red stroke, no fill
  Component 3 (0.15): Square annotation has ~2pt border width
  Component 4 (0.25): Text annotation on page 3 with 'Needs architect approval'
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_ro_014'

def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document should have 5 pages
    if doc.page_count != 5:
        print(f"FAIL: Expected 5 pages, found {doc.page_count}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[2]  # page 3 (0-indexed = 2)
    annots = list(page.annots())

    # Collect annotations by type
    square_annots = [a for a in annots if a.type[1] == "Square"]
    text_annots = [a for a in annots if a.type[1] == "Text"]

    # Component 1: Square annotation exists on page 3 with correct rect (0.35 points)
    # Expected rect approx (100, 200, 400, 350) - allow tolerance for border adjustments
    try:
        rect_match = None
        if len(square_annots) > 0:
            for sa in square_annots:
                r = tuple(sa.rect)
                # Allow tolerance of 5 points for each coordinate
                if (abs(r[0] - 100) <= 5 and
                    abs(r[1] - 200) <= 5 and
                    abs(r[2] - 400) <= 5 and
                    abs(r[3] - 350) <= 5):
                    rect_match = sa
                    break

        if rect_match is not None:
            print(f"PASS: Component 1 -- Square annotation found on page 3 with rect {tuple(rect_match.rect)} (0.35 pts)")
            total_score += 0.35
        else:
            if len(square_annots) > 0:
                print(f"FAIL: Component 1 -- Square annotation(s) found but rect mismatch. Found: {[tuple(a.rect) for a in square_annots]}")
            else:
                print(f"FAIL: Component 1 -- No Square annotation found on page 3")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Square annotation has red stroke (1,0,0) and no fill (0.25 points)
    try:
        if rect_match is not None:
            colors = rect_match.colors
            stroke = colors.get("stroke", [])
            fill = colors.get("fill", [])

            # Check red stroke: [1.0, 0.0, 0.0]
            stroke_ok = (len(stroke) == 3 and
                         abs(stroke[0] - 1.0) < 0.05 and
                         abs(stroke[1] - 0.0) < 0.05 and
                         abs(stroke[2] - 0.0) < 0.05)

            # Check no fill (empty list or None)
            fill_ok = (fill is None or len(fill) == 0)

            if stroke_ok and fill_ok:
                print(f"PASS: Component 2 -- Red stroke {list(stroke)}, no fill (0.25 pts)")
                total_score += 0.25
            elif stroke_ok:
                print(f"FAIL: Component 2 -- Red stroke correct but fill present: {list(fill)}")
            elif fill_ok:
                print(f"FAIL: Component 2 -- No fill correct but stroke wrong: {list(stroke)}")
            else:
                print(f"FAIL: Component 2 -- stroke={list(stroke)}, fill={list(fill)}")
        else:
            print(f"FAIL: Component 2 -- No matching Square annotation to check colors")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Square annotation has ~2pt border width (0.15 points)
    try:
        if rect_match is not None:
            border = rect_match.border
            border_width = border.get("width", 0) if border else 0

            if abs(border_width - 2.0) < 0.5:
                print(f"PASS: Component 3 -- Border width {border_width} ~= 2pt (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 3 -- Border width {border_width}, expected ~2.0")
        else:
            print(f"FAIL: Component 3 -- No matching Square annotation to check border")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Text annotation on page 3 with 'Needs architect approval' (0.25 points)
    try:
        text_match = None
        for ta in text_annots:
            content = ta.info.get("content", "")
            if "Needs architect approval" in content:
                text_match = ta
                break

        if text_match is not None:
            print(f"PASS: Component 4 -- Text annotation with 'Needs architect approval' found (0.25 pts)")
            total_score += 0.25
        else:
            contents = [ta.info.get("content", "") for ta in text_annots]
            if len(text_annots) > 0:
                print(f"FAIL: Component 4 -- Text annotations found but content mismatch: {contents}")
            else:
                print(f"FAIL: Component 4 -- No Text annotation found on page 3")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    # Verify no annotations on other pages (sanity, not scored)
    for i in [0, 1, 3, 4]:
        other_annots = list(doc[i].annots())
        if len(other_annots) > 0:
            print(f"INFO: Page {i+1} has {len(other_annots)} unexpected annotations")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/Documents/blueprint_annotated.pdf'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
