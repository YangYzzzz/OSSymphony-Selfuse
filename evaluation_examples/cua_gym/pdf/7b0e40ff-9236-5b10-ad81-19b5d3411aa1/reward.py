"""
Reward Script: Add yellow highlight annotation to first paragraph on page 1 of meeting_notes.pdf
Task ID: pdf_fm_010
Domain: pdf
Scoring:
  Component 1 (0.4): Highlight annotation exists on page 0
  Component 2 (0.3): Highlight color is yellow (1, 1, 0)
  Component 3 (0.3): Highlight annotation covers the first paragraph area
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_010'
FILE_PATH = os.path.join(WORKDIR, 'Documents', 'meeting_notes.pdf')


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

    # Precondition: PDF has at least 1 page
    if len(doc) < 1:
        print("FAIL: PDF has no pages")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    page = doc[0]

    # Collect all Highlight annotations on page 0
    highlight_annots = []
    try:
        for annot in page.annots():
            if annot.type[1] == "Highlight":
                highlight_annots.append(annot)
    except Exception as e:
        print(f"ERROR: Could not iterate annotations: {e}")
        doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Highlight annotation exists on page 0 (0.4 points)
    # This FAILS on initial (no annotations) and PASSES on golden (has highlight)
    try:
        if len(highlight_annots) >= 1:
            print(f"PASS: Component 1 — Found {len(highlight_annots)} Highlight annotation(s) on page 0 (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No Highlight annotations found on page 0")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Highlight color is yellow (1, 1, 0) (0.3 points)
    # Only check if we found at least one highlight
    try:
        yellow_found = False
        for annot in highlight_annots:
            stroke = annot.colors.get("stroke")
            if stroke and len(stroke) >= 3:
                # Check if color is yellow (1, 1, 0) with tolerance
                if (abs(stroke[0] - 1.0) < 0.05 and
                    abs(stroke[1] - 1.0) < 0.05 and
                    abs(stroke[2] - 0.0) < 0.05):
                    yellow_found = True
                    break
        if yellow_found:
            print(f"PASS: Component 2 — Highlight has yellow color (1, 1, 0) (0.3 pts)")
            total_score += 0.3
        else:
            if highlight_annots:
                colors = [annot.colors.get("stroke") for annot in highlight_annots]
                print(f"FAIL: Component 2 — Highlight color is not yellow. Found: {colors}")
            else:
                print(f"FAIL: Component 2 — No highlight annotations to check color")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Highlight covers the first paragraph area (0.3 points)
    # Expected area is roughly (68, 99, 525, 159) based on golden exploration
    # We verify the annotation rect overlaps substantially with this region
    try:
        area_match = False
        expected_y0 = 99.0   # approximate top of first paragraph
        expected_y1 = 159.0  # approximate bottom of first paragraph
        for annot in highlight_annots:
            rect = annot.rect
            # The highlight should be on page 0, roughly in the first paragraph region
            # Check that it covers a reasonable area in the expected Y range
            # Allow generous tolerance since exact coordinates may vary
            if (rect.y0 < expected_y0 + 30 and
                rect.y1 > expected_y1 - 30 and
                rect.x1 - rect.x0 > 100):  # annotation has meaningful width
                area_match = True
                print(f"PASS: Component 3 — Highlight rect {tuple(rect)} covers first paragraph area (0.3 pts)")
                total_score += 0.3
                break
        if not area_match:
            if highlight_annots:
                rects = [tuple(a.rect) for a in highlight_annots]
                print(f"FAIL: Component 3 — Highlight rect(s) {rects} do not cover first paragraph area (~y0=99, y1=159)")
            else:
                print(f"FAIL: Component 3 — No highlight annotations to check area")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    doc.close()

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entrypoint
if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
