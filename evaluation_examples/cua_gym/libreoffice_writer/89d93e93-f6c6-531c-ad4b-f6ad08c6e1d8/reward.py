"""
FINAL REWARD SCRIPT - SUCCESS
Task: The opening two paragraphs of my Writer document look a bit too cramped. What’s the quickest way to switch just those paragraphs to exactly 1.5-line spacing while leaving the rest of the text unchanged?
Generated: 2025-09-10 13:03:05
Status: success
Model: azure-o3
Total Steps: 9
"""

import os
from docx import Document
from docx.enum.text import WD_LINE_SPACING

# ---------------------------------------------------------------------------
# Reward Script for LibreOffice Writer Task
# ---------------------------------------------------------------------------
# Task Recap:
#   "The opening two paragraphs of my Writer document look a bit too cramped. 
#    What’s the quickest way to switch just those paragraphs to exactly 1.5-line
#    spacing while leaving the rest of the text unchanged?"
#
# Verification Logic:
#   1) Identify the FIRST TWO non-empty, non-heading paragraphs in the document
#      (they are the document’s opening body paragraphs).
#   2) Confirm BOTH are set to exactly 1.5-line spacing.
#   3) Confirm ALL REMAINING body paragraphs DO NOT have 1.5-line spacing
#      (to ensure only the first two were modified).
#   4) Progressive scoring:
#        • 0.6 points when the first two body paragraphs are correctly set.
#        • 0.4 points when the rest remain unchanged (not 1.5).
#      Final score is capped at 1.0.
#
# Anti-bias: No points for file existence, loading, or natural/default states.
# ---------------------------------------------------------------------------

def verify_line_spacing_task(file_path: str) -> float:
    """Return a progressive score [0.0-1.0] based on task completion."""

    max_score = 1.0
    score = 0.0

    # ---- 1. Load document (prerequisite – NO POINTS) ----------------------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to load DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # ---- 2. Collect body paragraphs (exclude empty & headings) ------------
    body_paras = [p for p in doc.paragraphs if p.text.strip()
                  and not (p.style and p.style.name.startswith("Heading"))]

    print(f"Total body paragraphs detected: {len(body_paras)}")
    if len(body_paras) < 2:
        print("✗ Document has fewer than two body paragraphs – cannot verify.")
        print("REWARD: 0.0")
        return 0.0

    # ---- 3. Verify FIRST TWO body paragraphs are 1.5-line spaced ----------
    first_two_ok = True
    for idx, para in enumerate(body_paras[:2], start=1):
        fmt = para.paragraph_format
        ls_rule = fmt.line_spacing_rule
        ls_val = fmt.line_spacing

        has_one_point_five = (
            ls_rule == WD_LINE_SPACING.ONE_POINT_FIVE or
            (ls_val is not None and abs(ls_val - 1.5) < 0.01)
        )

        if has_one_point_five:
            print(f"✓ Body paragraph {idx} correctly set to 1.5-line spacing")
        else:
            print(f"✗ Body paragraph {idx} is NOT set to 1.5-line spacing")
            first_two_ok = False

    if first_two_ok:
        score += 0.6  # award for correct spacing of first two paragraphs

    # ---- 4. Verify REMAINING body paragraphs are NOT 1.5 spaced -----------
    remaining_ok = True
    for idx, para in enumerate(body_paras[2:], start=3):
        fmt = para.paragraph_format
        ls_rule = fmt.line_spacing_rule
        ls_val = fmt.line_spacing

        is_one_point_five = (
            ls_rule == WD_LINE_SPACING.ONE_POINT_FIVE or
            (ls_val is not None and abs(ls_val - 1.5) < 0.01)
        )

        if is_one_point_five:
            print(f"✗ Body paragraph {idx} incorrectly has 1.5-line spacing")
            remaining_ok = False

    if remaining_ok:
        score += 0.4  # award for leaving remaining paragraphs unchanged

    # ---- 5. Final score ---------------------------------------------------
    final_score = min(score, max_score)
    print(f"Total Score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ---------------------------------------------------------------------------
# Execute verification when script is run directly
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/the_opening_two_paragraphs_of_my_writer_document_look_a_bit_too_cramped_whats_the_quickest_way_to_sw.docx"
    verify_line_spacing_task(FILE_PATH)

