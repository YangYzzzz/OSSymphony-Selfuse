"""
FINAL REWARD SCRIPT - SUCCESS
Task: Can you adjust the spacing so the intro is single, the body is double, and the conclusion is 1.75 lines, keeping font at 12?
Generated: 2025-10-14 06:33:36
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
from docx import Document

"""
Reward Script for Writer Task
Task: Verify that a DOCX document has
  • Intro paragraph with single line spacing
  • Body paragraph with double line spacing
  • Conclusion paragraph with 1.75 line spacing
  • All text kept at 12-pt font size
The script awards a progressive score and returns exactly 1.0 only when
all requirements are satisfied.
"""

FILE_PATH = "/home/user/can_you_adjust_the_spacing_so_the_intro_is_single_the_body_is_double_and_the_conclusion_is_175_lines.docx"

# Expected spacing ratios (relative to the intro which is single-spaced)
DOUBLE_RATIO = 2.0      # double = 2 × single
RATIO_1_75   = 1.75     # 1.75 × single

# Tolerances to allow minor rounding differences in DOCX internals
RATIO_TOLERANCE      = 0.08   # 8 % tolerance for line-spacing ratios
FONT_SIZE_TOLERANCE  = 0.5    # ±0.5 pt around 12 pt

# ---------------- Utility Functions ---------------- #

def _get_spacing_val(paragraph):
    """Return the <w:spacing w:line> value (integer) or None."""
    if (
        paragraph._p is not None and
        paragraph._p.pPr is not None and
        paragraph._p.pPr.spacing is not None
    ):
        return paragraph._p.pPr.spacing.line
    return None


def _ratio_matches(actual_ratio, expected_ratio):
    if actual_ratio is None:
        return False
    return abs(actual_ratio - expected_ratio) <= expected_ratio * RATIO_TOLERANCE


def _paragraph_font_ok(paragraph):
    """Check that every run with an explicit font size is ≈12 pt."""
    for run in paragraph.runs:
        size = run.font.size
        if size is None:
            continue  # size inherited – assume style already 12 pt
        if abs(size.pt - 12.0) > FONT_SIZE_TOLERANCE:
            return False
    return True

# ---------------- Main Verification ---------------- #

def verify_writer_spacing(file_path: str) -> float:
    score = 0.0

    # 1) Prerequisite: file must load successfully (no points)
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print("✗ Unable to open DOCX:", e)
        return 0.0

    # 2) Identify non-empty paragraphs (intro, body, conclusion)
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    print(f"Found {len(paragraphs)} non-empty paragraphs")
    if len(paragraphs) < 3:
        print("✗ Need at least 3 meaningful paragraphs (intro, body, conclusion)")
        return 0.0

    intro, body, conclusion = paragraphs[0], paragraphs[1], paragraphs[-1]

    intro_spacing      = _get_spacing_val(intro)
    body_spacing       = _get_spacing_val(body)
    conclusion_spacing = _get_spacing_val(conclusion)

    print("Intro spacing value:", intro_spacing)
    print("Body spacing value:", body_spacing)
    print("Conclusion spacing value:", conclusion_spacing)

    # 3) Validate intro spacing exists (baseline single)
    if intro_spacing is None:
        print("✗ Intro paragraph has no explicit line spacing defined")
        return 0.0  # cannot evaluate ratios without baseline
    else:
        print("✓ Intro spacing captured as single-space baseline")
        score += 0.2

    # 4) Validate body is double-spaced relative to intro
    if body_spacing is not None:
        body_ratio = body_spacing / intro_spacing
        print("Body / Intro spacing ratio:", body_ratio)
        if _ratio_matches(body_ratio, DOUBLE_RATIO):
            print("✓ Body paragraph is approximately double-spaced")
            score += 0.3
        else:
            print("✗ Body paragraph spacing is not double")
    else:
        print("✗ Body paragraph has no explicit line spacing defined")

    # 5) Validate conclusion is 1.75-spaced relative to intro
    if conclusion_spacing is not None:
        concl_ratio = conclusion_spacing / intro_spacing
        print("Conclusion / Intro spacing ratio:", concl_ratio)
        if _ratio_matches(concl_ratio, RATIO_1_75):
            print("✓ Conclusion paragraph is approximately 1.75-spaced")
            score += 0.3
        else:
            print("✗ Conclusion paragraph spacing is not 1.75")
    else:
        print("✗ Conclusion paragraph has no explicit line spacing defined")

    # 6) Validate 12-pt font throughout (explicit or inherited)
    all_font_ok = True
    for idx, para in enumerate(paragraphs):
        if not _paragraph_font_ok(para):
            print(f"✗ Font size mismatch detected in paragraph {idx}")
            all_font_ok = False
            break
    if all_font_ok:
        print("✓ All explicit font sizes are 12 pt (or inherited)")
        score += 0.2

    # 7) Final progressive score (capped at 1.0)
    final_score = round(min(score, 1.0), 2)
    print(f"Final score: {final_score}")
    return final_score

# ---------------- Execute Verification ---------------- #
if __name__ == "__main__":
    reward_value = verify_writer_spacing(FILE_PATH)
    print(f"REWARD: {reward_value}")

