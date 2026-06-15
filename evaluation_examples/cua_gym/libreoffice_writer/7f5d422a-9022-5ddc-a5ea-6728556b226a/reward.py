"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set the italicized words to 14 and keep the rest at their current size.
Generated: 2025-10-14 05:59:59
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
from docx.shared import Pt
import os, math

def verify_task(file_path):
    """Verify that every italicised run is set to 14 pt while all non-italic text keeps
    whatever size (≠14 pt) it originally had.
    Progressive scoring is applied:
      • 0.2 – document contains at least one italic run
      • 0.5 – every italic run is sized exactly 14 pt
      • 0.3 – there exists at least one non-italic run whose size is not 14 pt,
               proving other text kept its original size
    The result is capped at 1.0 and printed as required.
    """
    print(f"Verifying document: {file_path}")

    # Prerequisite: file must exist and be readable (no points awarded for this)
    if not os.path.exists(file_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error loading document: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Initialise trackers
    italic_run_count = 0
    italics_all_14 = True
    non_italic_has_non14 = False
    pt_tolerance = 0.1  # allow tiny floating-point deviations

    # Inspect every run in every paragraph
    for para in doc.paragraphs:
        for run in para.runs:
            size = run.font.size  # None → inherits from style; treat as undefined
            size_pt = size.pt if size is not None else None
            is_italic = run.italic is True  # explicit True only

            if is_italic:
                italic_run_count += 1
                # Size must be explicitly 14 pt
                if size_pt is None or abs(size_pt - 14) > pt_tolerance:
                    italics_all_14 = False
                    print(f"   ✗ Italic run wrong size: '{run.text[:30]}' -> {size_pt}pt")
            else:
                # Confirm at least one non-italic run keeps a size other than 14 pt
                if size_pt is not None and abs(size_pt - 14) > pt_tolerance:
                    non_italic_has_non14 = True

    # Progressive scoring
    score = 0.0

    # 1) Presence of italic text
    if italic_run_count > 0:
        print(f"✓ Found {italic_run_count} italic runs (0.2 points)")
        score += 0.2
    else:
        print("✗ No italic runs found (0 points)")

    # 2) Correct size for all italic runs
    if italic_run_count > 0 and italics_all_14:
        print("✓ All italic runs are exactly 14 pt (0.5 points)")
        score += 0.5
    else:
        print("✗ Some italic runs are not 14 pt (0 points)")

    # 3) Confirmation that non-italic text kept original sizes
    if non_italic_has_non14:
        print("✓ Non-italic text retains sizes other than 14 pt (0.3 points)")
        score += 0.3
    else:
        print("✗ Could not confirm non-italic text kept original sizes (0 points)")

    final_score = min(score, 1.0)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ---------------------------------------------------------------------
# Execute verification when run as a script
# ---------------------------------------------------------------------
if __name__ == "__main__":
    file_path = "/home/user/set_the_italicized_words_to_14_and_keep_the_rest_at_their_current_size.docx"
    verify_task(file_path)

