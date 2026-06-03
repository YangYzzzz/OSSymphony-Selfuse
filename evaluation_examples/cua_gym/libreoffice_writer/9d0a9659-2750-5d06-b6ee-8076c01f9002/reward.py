"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please format the essay in 12 pt: intro single-spaced, body 1.5-spaced, conclusion 1.5-spaced.
Generated: 2025-10-14 06:37:24
Status: success
Model: azure-o3
Total Steps: 3
"""

"""
Reward Script for Essay Formatting Verification
Task: Ensure the essay is formatted in 12-point font, with the introduction single-spaced, and both body and conclusion 1.5-spaced.
The script awards:
  • 0.50 points for correct 12-pt font on every run in the document (partial credit proportional to correctness)
  • 0.50 points for correct line-spacing on the three logical sections
A perfect document therefore earns 1.0.
The script prints detailed diagnostics then prints the final reward as:
    REWARD: <score>
"""

import os
from docx import Document
from docx.enum.text import WD_LINE_SPACING
from typing import List

FILE_PATH = (
    "/home/user/please_format_the_essay_in_12_pt_intro_single_spaced_body_15_spaced_conclusion_15_spaced.docx"
)

# -----------------------------------------------------------------------------
# Helper functions
# -----------------------------------------------------------------------------

def _spacing_matches(paragraph, expected: str) -> bool:
    """Return True if *paragraph* has the *expected* spacing.

    expected must be either 'single' or '1.5'.
    The check tolerates documents that specify spacing via either the explicit
    line_spacing value or the line_spacing_rule enum.
    """
    pf = paragraph.paragraph_format
    rule = pf.line_spacing_rule  # may be None
    ls = pf.line_spacing         # may be None or float

    if expected == "single":
        # Accept SINGLE rule *or* explicit 1.0 value (or default/None)
        if rule == WD_LINE_SPACING.SINGLE:
            return True
        if ls is not None and abs(ls - 1.0) < 1e-3:
            return True
        if rule is None and ls is None:
            # Writer often encodes default single-spacing this way
            return True
        return False

    if expected == "1.5":
        if rule == WD_LINE_SPACING.ONE_POINT_FIVE:
            return True
        if ls is not None and abs(ls - 1.5) < 1e-3:
            return True
        return False

    # Unsupported expectation value
    return False


def _font_runs_12pt(paragraph) -> List[bool]:
    """Return list indicating per-run correctness for 12-pt font in *paragraph*."""
    results = []
    for run in paragraph.runs:
        size = run.font.size  # may be None (inherits)
        if size is None:
            results.append(False)
        else:
            results.append(abs(size.pt - 12.0) <= 0.1)
    return results

# -----------------------------------------------------------------------------
# Main verification routine
# -----------------------------------------------------------------------------

def verify_essay_format(file_path: str) -> float:
    print(f"Checking document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found – task not completed")
        return 0.0  # No points if the file is missing

    try:
        doc = Document(file_path)
    except Exception as exc:
        print(f"✗ Could not open DOCX – {exc}")
        return 0.0

    # Filter out completely empty paragraphs (common trailing empties)
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    if not paragraphs:
        print("✗ Document contains no text paragraphs – nothing to grade")
        return 0.0

    # Identify logical sections: first = intro, last = conclusion, middle = body
    intro_para = paragraphs[0]
    conclusion_para = paragraphs[-1]
    body_paras = paragraphs[1:-1]  # may be empty for very short essays

    # ------------------------------------------------------------------
    # 1. FONT SIZE VERIFICATION (up to 0.50 points)
    # ------------------------------------------------------------------
    total_runs = 0
    correct_runs = 0
    for para in paragraphs:
        run_results = _font_runs_12pt(para)
        total_runs += len(run_results)
        correct_runs += sum(run_results)

    font_score = 0.0
    if total_runs:
        font_ratio = correct_runs / total_runs  # proportion correct
        font_score = 0.50 * font_ratio
    print(f"Font check: {correct_runs}/{total_runs} runs are 12-pt -> {font_score:.2f} pts")

    # ------------------------------------------------------------------
    # 2. LINE SPACING VERIFICATION (up to 0.50 points)
    # ------------------------------------------------------------------
    intro_ok = _spacing_matches(intro_para, "single")
    conclusion_ok = _spacing_matches(conclusion_para, "1.5") if conclusion_para is not intro_para else True
    body_ok = True  # default to True if no body paragraphs exist
    if body_paras:
        body_ok = all(_spacing_matches(p, "1.5") for p in body_paras)

    spacing_components = [intro_ok, body_ok, conclusion_ok]
    spacing_points = (sum(spacing_components) / 3.0) * 0.50

    print("Spacing check:")
    print(f"  • Introduction single-spaced : {'✓' if intro_ok else '✗'}")
    print(f"  • Body 1.5-spaced           : {'✓' if body_ok else '✗'}  (paragraphs: {len(body_paras)})")
    print(f"  • Conclusion 1.5-spaced      : {'✓' if conclusion_ok else '✗'}")
    print(f"  -> Spacing points: {spacing_points:.2f} pts")

    # ------------------------------------------------------------------
    # FINAL SCORE
    # ------------------------------------------------------------------
    total_score = round(min(font_score + spacing_points, 1.0), 2)
    print(f"Total reward score: {total_score}")
    return total_score

# -----------------------------------------------------------------------------
# Script entry point – runs automatically when executed
# -----------------------------------------------------------------------------
if __name__ == "__main__":
    reward_value = verify_essay_format(FILE_PATH)
    print(f"REWARD: {reward_value}")

