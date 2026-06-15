"""
Reward Script: Add a FreeText annotation with red border on page 7
Task ID: pdf_res_086
Domain: pdf
Scoring:
  Component 1 (0.20): Output file exists with correct page count (11 pages)
  Component 2 (0.30): FreeText annotation present on page 7
  Component 3 (0.25): Annotation text matches expected comment
  Component 4 (0.15): Annotation has red border (stroke color)
  Component 5 (0.10): Annotation positioned near (350, 500)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_res_086'
OUTPUT_PATH = os.path.join(WORKDIR, 'papers', 'feedback_copy_noted.pdf')
EXPECTED_TEXT = 'This section needs revision - see email from 03/15/2026'
PAGE_INDEX = 6  # page 7 is 0-indexed as 6
EXPECTED_PAGES = 11


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
        import fitz
        doc = fitz.open(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load PDF {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Output file has correct page count (0.20 points)
    # This checks the saved output file — initial_env does NOT have this file at all,
    # so this component scores 0 on initial_env (file not found early exit above).
    try:
        page_count = len(doc)
        if page_count == EXPECTED_PAGES:
            print(f"PASS: Component 1 — Page count is {page_count} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 1 — Expected {EXPECTED_PAGES} pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: FreeText annotation exists on page 7 (0.30 points)
    try:
        page = doc[PAGE_INDEX]
        annots = list(page.annots()) if page.annots() else []
        freetext_annots = [a for a in annots if a.type[1] == "FreeText"]
        if len(freetext_annots) >= 1:
            print(f"PASS: Component 2 — Found {len(freetext_annots)} FreeText annotation(s) on page 7 (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 2 — No FreeText annotations on page 7 (found {len(annots)} total annotations)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Annotation text matches expected comment (0.25 points)
    try:
        page = doc[PAGE_INDEX]
        annots = list(page.annots()) if page.annots() else []
        freetext_annots = [a for a in annots if a.type[1] == "FreeText"]
        text_matched = False
        for a in freetext_annots:
            content = a.info.get("content", "")
            if EXPECTED_TEXT in content:
                text_matched = True
                break
        if text_matched:
            print(f"PASS: Component 3 — Annotation text matches expected comment (0.25 pts)")
            total_score += 0.25
        else:
            found_texts = [a.info.get("content", "") for a in freetext_annots]
            print(f"FAIL: Component 3 — Expected text '{EXPECTED_TEXT}', found: {found_texts}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    # Component 4: Annotation has red border/stroke color (0.15 points)
    try:
        page = doc[PAGE_INDEX]
        annots = list(page.annots()) if page.annots() else []
        freetext_annots = [a for a in annots if a.type[1] == "FreeText"]
        red_border_found = False
        for a in freetext_annots:
            stroke = a.colors.get("stroke")
            if stroke is not None and len(stroke) >= 3:
                # Check if stroke is red: R close to 1.0, G and B close to 0.0
                if stroke[0] > 0.8 and stroke[1] < 0.2 and stroke[2] < 0.2:
                    red_border_found = True
                    break
        if red_border_found:
            print(f"PASS: Component 4 — Annotation has red border (0.15 pts)")
            total_score += 0.15
        else:
            colors_found = [a.colors for a in freetext_annots]
            print(f"FAIL: Component 4 — No red border found, colors: {colors_found}")
    except Exception as e:
        print(f"ERROR: Component 4 — {e}")

    # Component 5: Annotation positioned near (350, 500) within tolerance (0.10 points)
    try:
        page = doc[PAGE_INDEX]
        annots = list(page.annots()) if page.annots() else []
        freetext_annots = [a for a in annots if a.type[1] == "FreeText"]
        position_ok = False
        tolerance = 50  # allow 50pt tolerance for position
        for a in freetext_annots:
            rect = a.rect
            # Check if the annotation's top-left corner is near (350, 500)
            x0, y0 = rect.x0, rect.y0
            if abs(x0 - 350) < tolerance and abs(y0 - 500) < tolerance:
                position_ok = True
                break
        if position_ok:
            print(f"PASS: Component 5 — Annotation positioned near (350, 500) (0.10 pts)")
            total_score += 0.10
        else:
            rects_found = [tuple(a.rect) for a in freetext_annots]
            print(f"FAIL: Component 5 — Annotation not near (350, 500), rects: {rects_found}")
    except Exception as e:
        print(f"ERROR: Component 5 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point: test against canonical artifact path
if not os.path.exists(OUTPUT_PATH):
    print(f"File not found: {OUTPUT_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(OUTPUT_PATH)
