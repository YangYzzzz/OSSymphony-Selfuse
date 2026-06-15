"""
Reward Script: Add yellow highlight annotations on page 2 of study_material.pdf
Task ID: pdf_adv_139
Domain: pdf
Scoring:
  Component 1 (0.4): Exactly 3 highlight annotations exist on page 2
  Component 2 (0.3): All 3 highlights are yellow (stroke = (1.0, 1.0, 0.0))
  Component 3 (0.3): All 3 highlights cover the specified rectangular regions
"""

import os

try:
    import pymupdf
except ImportError:
    import fitz as pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_adv_139'
PDF_PATH = '/home/user/Documents/study_material.pdf'

# Expected annotation rectangles (from task instruction, with tolerance for PyMuPDF padding)
# Task specifies: (72,700,500,715), (72,680,500,695), (72,660,500,675)
EXPECTED_RECTS = [
    (72, 700, 500, 715),
    (72, 680, 500, 695),
    (72, 660, 500, 675),
]
RECT_TOLERANCE = 10.0  # points


def rects_close(r1, r2, tol=RECT_TOLERANCE):
    """Check if two rects are approximately equal within tolerance."""
    return all(abs(a - b) <= tol for a, b in zip(r1, r2))


def verify_task(pdf_path):
    """
    Verify task completion: 3 yellow highlight annotations on page 2
    at the specified rectangles.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: open the PDF
    try:
        doc = pymupdf.open(pdf_path)
    except Exception as e:
        print(f"CRITICAL: Cannot open PDF {pdf_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Page 2 is index 1 (0-based)
    try:
        page = doc[1]
    except Exception as e:
        print(f"CRITICAL: Cannot access page 2 (index 1): {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Collect all highlight annotations on page 2
    try:
        highlight_annots = [a for a in page.annots() if a.type[1] == "Highlight"]
    except Exception as e:
        print(f"ERROR: Cannot enumerate annotations on page 2: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Exactly 3 highlight annotations on page 2 (0.4 points)
    try:
        count = len(highlight_annots)
        if count == 3:
            print(f"PASS: Component 1 — exactly 3 highlight annotations on page 2 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — expected 3 highlight annotations on page 2, found {count}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: All 3 highlights are yellow (stroke = 1.0, 1.0, 0.0) (0.3 points)
    try:
        if count == 3:
            yellow = (1.0, 1.0, 0.0)
            all_yellow = True
            for i, a in enumerate(highlight_annots):
                stroke = a.colors.get("stroke")
                if stroke is None or not all(abs(s - y) < 0.05 for s, y in zip(stroke, yellow)):
                    print(f"FAIL: Component 2 — annotation {i+1} not yellow, stroke={stroke}")
                    all_yellow = False
                    break
            if all_yellow:
                print(f"PASS: Component 2 — all 3 highlight annotations are yellow (0.3 pts)")
                total_score += 0.3
        else:
            print(f"FAIL: Component 2 — skipped (wrong annotation count: {count})")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 3 highlights cover the expected rectangular regions (0.3 points)
    try:
        if count == 3:
            actual_rects = [tuple(a.rect) for a in highlight_annots]
            # Each expected rect must match one actual rect (unordered)
            matched_expected = set()
            matched_actual = set()
            for ei, er in enumerate(EXPECTED_RECTS):
                for ai, ar in enumerate(actual_rects):
                    if ai not in matched_actual and rects_close(ar, er):
                        matched_expected.add(ei)
                        matched_actual.add(ai)
                        break

            if len(matched_expected) == 3:
                print(f"PASS: Component 3 — all 3 highlights cover expected rect regions (0.3 pts)")
                total_score += 0.3
            else:
                unmatched = [EXPECTED_RECTS[i] for i in range(3) if i not in matched_expected]
                print(f"FAIL: Component 3 — {3 - len(matched_expected)} expected rects unmatched")
                for u in unmatched:
                    print(f"  Missing coverage for expected rect: {u}")
                print(f"  Actual rects found: {actual_rects}")
        else:
            print(f"FAIL: Component 3 — skipped (wrong annotation count: {count})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(PDF_PATH):
    print(f"File not found: {PDF_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(PDF_PATH)
