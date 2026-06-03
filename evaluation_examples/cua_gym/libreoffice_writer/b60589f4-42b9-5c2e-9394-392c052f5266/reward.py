"""
Reward Script: Set the page orientation back to portrait from landscape.
Task ID: writer_page_066
Domain: libreoffice_writer
Scoring:
  Component 1: Section orientation is PORTRAIT (0.5 pts)
  Component 2: Page dimensions match A4 portrait proportions, width < height (0.3 pts)
  Component 3: All four page margins preserved at 2.54 cm (0.2 pts)
"""

import os
from docx import Document
from docx.enum.section import WD_ORIENT

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_page_066'
FILE_NAME = 'wide_report.docx'

# A4 dimensions in EMU (English Metric Units): 1 cm = 360000 EMU
# A4 portrait: width=21.0 cm (7560000 EMU), height=29.7 cm (10692000 EMU)
# A4 landscape: width=29.7 cm, height=21.0 cm
# Tolerance: ±10000 EMU (~0.028 cm)
A4_SHORT_SIDE_CM = 21.0009   # measured from actual files
A4_LONG_SIDE_CM  = 29.7004
MARGIN_EXPECTED_CM = 2.5400
TOLERANCE_CM = 0.05


def cm_close(actual_cm, expected_cm, tol=TOLERANCE_CM):
    return abs(actual_cm - expected_cm) <= tol


def verify_task(file_path):
    """
    Verify that the document page orientation was changed from landscape to portrait.
    Returns a float between 0.0 and 1.0.
    """
    total_score = 0.0

    # Guard: load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least one section
    if len(doc.sections) == 0:
        print("CRITICAL: Document has no sections.")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]

    # Component 1: Section orientation must be PORTRAIT (0.5 points)
    # Initial state is LANDSCAPE; task requires changing to PORTRAIT.
    # This FAILS on initial_env (LANDSCAPE) and PASSES on golden_env (PORTRAIT).
    try:
        orientation = section.orientation
        if orientation == WD_ORIENT.PORTRAIT:
            print(f"PASS: Component 1 — orientation is PORTRAIT (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — expected PORTRAIT, found {orientation}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Page dimensions reflect A4 portrait (width < height) (0.3 points)
    # In initial_env: page_width=29.7 cm, page_height=21.0 cm (landscape).
    # In golden_env:  page_width=21.0 cm, page_height=29.7 cm (portrait).
    # Both width and height must be swapped to the portrait values.
    try:
        width_cm  = section.page_width.cm
        height_cm = section.page_height.cm
        width_ok  = cm_close(width_cm,  A4_SHORT_SIDE_CM)
        height_ok = cm_close(height_cm, A4_LONG_SIDE_CM)
        if width_ok and height_ok:
            print(
                f"PASS: Component 2 — page dimensions are A4 portrait "
                f"(width={width_cm:.4f}cm, height={height_cm:.4f}cm) (0.3 pts)"
            )
            total_score += 0.3
        else:
            print(
                f"FAIL: Component 2 — expected width≈{A4_SHORT_SIDE_CM}cm, "
                f"height≈{A4_LONG_SIDE_CM}cm; found width={width_cm:.4f}cm, "
                f"height={height_cm:.4f}cm"
            )
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All four margins are preserved at 2.54 cm (0.2 points)
    # The task spec states margins must stay unchanged at top=bottom=left=right=2.54 cm.
    # This check verifies no margin was accidentally altered during the orientation change.
    # Note: margins are the same in both initial and golden states per task spec,
    # so this is a sub-condition combined with the orientation change — it confirms
    # the task was done correctly WITHOUT corrupting the margins.
    # We include this only because the score for it is 0.0 if orientation is wrong
    # (Component 1 would have failed), keeping total initial score at 0.0.
    # Actually, to be safe we gate this on orientation being correct:
    try:
        if orientation == WD_ORIENT.PORTRAIT:
            top_cm    = section.top_margin.cm
            bottom_cm = section.bottom_margin.cm
            left_cm   = section.left_margin.cm
            right_cm  = section.right_margin.cm
            margins_ok = (
                cm_close(top_cm,    MARGIN_EXPECTED_CM) and
                cm_close(bottom_cm, MARGIN_EXPECTED_CM) and
                cm_close(left_cm,   MARGIN_EXPECTED_CM) and
                cm_close(right_cm,  MARGIN_EXPECTED_CM)
            )
            if margins_ok:
                print(
                    f"PASS: Component 3 — all margins preserved at 2.54 cm "
                    f"(top={top_cm:.4f}, bottom={bottom_cm:.4f}, "
                    f"left={left_cm:.4f}, right={right_cm:.4f}) (0.2 pts)"
                )
                total_score += 0.2
            else:
                print(
                    f"FAIL: Component 3 — margins not preserved: "
                    f"top={top_cm:.4f}, bottom={bottom_cm:.4f}, "
                    f"left={left_cm:.4f}, right={right_cm:.4f} "
                    f"(expected all={MARGIN_EXPECTED_CM})"
                )
        else:
            print("SKIP: Component 3 — skipped because orientation is not PORTRAIT")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


file_path = os.path.join(WORKDIR, FILE_NAME)
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
