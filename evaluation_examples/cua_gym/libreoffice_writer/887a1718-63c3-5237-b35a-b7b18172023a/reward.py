"""
FINAL REWARD SCRIPT - SUCCESS
Task: Ensure the first two paragraphs are double spaced instead of single.
Generated: 2025-10-14 07:07:52
Status: success
Model: azure-o3
Total Steps: 2
"""

from pathlib import Path
from docx import Document
from docx.enum.text import WD_LINE_SPACING

"""
Reward Script: Verify that ONLY the first two paragraphs in the given DOCX file
are double-spaced and that the remaining paragraphs keep their original (non-double)
spacing.

Scoring (progressive):
  • 0.30 points for each of the first two paragraphs that is correctly set to
    double spacing  → max 0.60
  • 0.40 points distributed proportionally across the remaining paragraphs that
    are *not* double-spaced (they should stay single/other).  If there are no
    extra paragraphs the full 0.40 is granted automatically because the task
    only concerns the first two paragraphs.

The script prints detailed diagnostics for every paragraph and finally prints
"REWARD: X.X" where X.X ∈ [0.0, 1.0]. It never awards points for mere file
existence or successful loading (natural conditions).
"""

def verify_double_spacing(file_path: str) -> float:
    """Return a score ∈ [0,1] based on correct line-spacing requirements."""

    print(f"Verifying file: {file_path}")
    path = Path(file_path)
    if not path.exists():
        print("✗ File does not exist")
        return 0.0  # no points for missing file

    try:
        doc = Document(file_path)
    except Exception as exc:
        print(f"✗ Failed to load document: {exc}")
        return 0.0  # cannot inspect → 0 pts

    paragraphs = doc.paragraphs
    para_count = len(paragraphs)
    print(f"Paragraph count: {para_count}")

    if para_count < 2:
        print("✗ Document has fewer than two paragraphs – task unmet")
        return 0.0

    total_score = 0.0  # progressive score accumulator

    # 1) Check first two paragraphs must be double-spaced
    correct_first_two = 0
    for idx in range(2):
        p = paragraphs[idx]
        pf = p.paragraph_format
        rule = pf.line_spacing_rule
        spacing = pf.line_spacing

        # Determine if paragraph is double spaced
        is_double = False
        if rule == WD_LINE_SPACING.DOUBLE:
            is_double = True
        elif spacing and abs(float(spacing) - 2.0) < 0.01:
            is_double = True  # sometimes Word stores explicit value 2.0

        print(f"Paragraph {idx}: rule={rule} spacing={spacing} → double={is_double}")
        if is_double:
            correct_first_two += 1

    total_score += 0.3 * correct_first_two  # up to 0.60

    # 2) Remaining paragraphs must NOT be double-spaced
    remaining_total = max(para_count - 2, 0)
    if remaining_total == 0:
        total_score += 0.4  # nothing else to check, full remainder awarded
    else:
        remaining_correct = 0
        for idx in range(2, para_count):
            p = paragraphs[idx]
            pf = p.paragraph_format
            rule = pf.line_spacing_rule
            spacing = pf.line_spacing
            is_double = (rule == WD_LINE_SPACING.DOUBLE) or (
                spacing and abs(float(spacing) - 2.0) < 0.01)

            print(f"Paragraph {idx}: rule={rule} spacing={spacing} → double={is_double}")
            if not is_double:
                remaining_correct += 1

        # proportionally distribute 0.40 among correctly non-double paragraphs
        total_score += 0.4 * (remaining_correct / remaining_total)

    # Cap to 1.0 and round for neatness
    final_score = min(round(total_score, 3), 1.0)
    print(f"Total score: {final_score}")
    return final_score


if __name__ == "__main__":
    DOC_PATH = "/home/user/ensure_the_first_two_paragraphs_are_double_spaced_instead_of_single.docx"
    reward = verify_double_spacing(DOC_PATH)
    print(f"REWARD: {reward}")

