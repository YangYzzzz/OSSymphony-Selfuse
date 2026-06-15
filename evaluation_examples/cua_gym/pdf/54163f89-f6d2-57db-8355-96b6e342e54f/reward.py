"""
Reward Script: Verify that approved_stamp.pdf was stamped onto page 1 only of final_proposal.pdf
Task ID: pdf_fm_087
Domain: pdf
Scoring:
  - Component 1 (0.15): Stamped file exists and is valid PDF with 10 pages
  - Component 2 (0.35): Page 0 contains "APPROVED" text from the stamp overlay
  - Component 3 (0.20): Page 0 has additional vector drawings from stamp overlay
  - Component 4 (0.30): Pages 1-9 are unchanged (text matches original)
"""

import os
import pymupdf

WORKDIR = '/home/user'
TASK_ID = 'pdf_fm_087'

STAMPED_PATH = os.path.join(WORKDIR, 'Documents', 'final_proposal_stamped.pdf')
ORIGINAL_PATH = os.path.join(WORKDIR, 'Documents', 'final_proposal.pdf')


def verify_task():
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition: stamped file must exist and be a valid PDF
    if not os.path.exists(STAMPED_PATH):
        print(f"CRITICAL: Stamped file not found: {STAMPED_PATH}")
        print("REWARD: 0.0")
        return 0.0

    try:
        stamped_doc = pymupdf.open(STAMPED_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open stamped PDF: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition: original file must exist for comparison
    if not os.path.exists(ORIGINAL_PATH):
        print(f"CRITICAL: Original file not found: {ORIGINAL_PATH}")
        stamped_doc.close()
        print("REWARD: 0.0")
        return 0.0

    try:
        orig_doc = pymupdf.open(ORIGINAL_PATH)
    except Exception as e:
        print(f"CRITICAL: Cannot open original PDF: {e}")
        stamped_doc.close()
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Stamped file has exactly 10 pages (0.15 points)
    # The task says the original has 10 pages and the stamped output should also have 10 pages.
    # This is a task-introduced change because the stamped FILE is new.
    try:
        page_count = stamped_doc.page_count
        if page_count == 10:
            print(f"PASS: Component 1 -- Stamped PDF has 10 pages (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Expected 10 pages, found {page_count}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Page 0 of stamped file contains "APPROVED" text (0.35 points)
    # The stamp PDF has "APPROVED" and "2026-03-28" text. After stamping, page 0
    # should contain this text overlaid. The original page 0 does NOT have "APPROVED".
    try:
        stamped_page0_text = stamped_doc[0].get_text()
        has_approved = "APPROVED" in stamped_page0_text

        # Also verify original page 0 does NOT have "APPROVED" (sanity check)
        orig_page0_text = orig_doc[0].get_text()
        orig_has_approved = "APPROVED" in orig_page0_text

        if has_approved and not orig_has_approved:
            print(f"PASS: Component 2 -- 'APPROVED' text found on stamped page 0, absent from original (0.35 pts)")
            total_score += 0.35
        elif has_approved and orig_has_approved:
            # Stamp text was already in original -- shouldn't happen but handle gracefully
            print(f"FAIL: Component 2 -- 'APPROVED' found in both original and stamped, cannot confirm stamp was applied")
        else:
            print(f"FAIL: Component 2 -- 'APPROVED' text not found on stamped page 0")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Page 0 has more drawings than original (stamp adds vector graphics) (0.20 points)
    # The stamp PDF has 2 drawings (green stamp graphic). After stamping onto page 0,
    # the stamped page 0 should have MORE drawings than the original page 0.
    try:
        orig_drawings_count = len(orig_doc[0].get_drawings())
        stamped_drawings_count = len(stamped_doc[0].get_drawings())

        if stamped_drawings_count > orig_drawings_count:
            print(f"PASS: Component 3 -- Stamped page 0 has {stamped_drawings_count} drawings vs original {orig_drawings_count} (0.20 pts)")
            total_score += 0.20
        else:
            print(f"FAIL: Component 3 -- Stamped page 0 drawings ({stamped_drawings_count}) not greater than original ({orig_drawings_count})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Pages 1-9 text is unchanged (0.30 points)
    # The task says "stamp onto page 1 ONLY", so pages 2-10 (index 1-9) must be identical.
    # Award partial credit: 0.03 per matching page (9 pages * ~0.0333 each = 0.30).
    try:
        pages_matching = 0
        total_later_pages = 9
        for i in range(1, 10):
            orig_text = orig_doc[i].get_text()
            stamped_text = stamped_doc[i].get_text()
            if orig_text == stamped_text:
                pages_matching += 1
            else:
                print(f"  INFO: Page {i} text differs (orig_len={len(orig_text)}, stamped_len={len(stamped_text)})")

        if pages_matching == total_later_pages:
            print(f"PASS: Component 4 -- All 9 remaining pages (1-9) have unchanged text (0.30 pts)")
            total_score += 0.30
        elif pages_matching > 0:
            partial = round(0.30 * pages_matching / total_later_pages, 2)
            print(f"PARTIAL: Component 4 -- {pages_matching}/{total_later_pages} pages unchanged ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 4 -- No pages match original text")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    orig_doc.close()
    stamped_doc.close()

    final_score = min(round(total_score, 2), 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
verify_task()
