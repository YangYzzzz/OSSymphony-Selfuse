"""
FINAL REWARD SCRIPT - SUCCESS
Task: Change the first and second paragraphs so they use 2.0 line spacing.
Generated: 2025-10-14 06:10:15
Status: success
Model: azure-o3
Total Steps: 2
"""

from docx import Document
from docx.enum.text import WD_LINE_SPACING
from docx.oxml.ns import qn
import os


def is_double_spacing(paragraph):
    """Return True if the given paragraph is set to double (2.0) line spacing."""
    pf = paragraph.paragraph_format

    # 1) Check rule-based setting (preferred)
    if pf.line_spacing_rule == WD_LINE_SPACING.DOUBLE:
        return True

    # 2) Check explicit numeric spacing value (≈2.0)
    if isinstance(pf.line_spacing, (int, float)) and abs(float(pf.line_spacing) - 2.0) < 0.01:
        return True

    # 3) Fallback – inspect raw XML for >=480 twips (double-space) when rule is "auto"
    try:
        spacing_elm = paragraph._p.pPr.spacing  # <w:spacing …/>
        if spacing_elm is not None:
            line_val = spacing_elm.get(qn("w:line"))
            if line_val and line_val.isdigit() and int(line_val) >= 480:
                return True
    except Exception:
        pass

    return False


def verify_double_spacing_first_two(file_path):
    """Verify that the first TWO non-empty paragraphs use double line spacing.
    Returns a progressive score between 0.0 and 1.0.
    """
    print(f"Verifying file: {file_path}")

    # Prerequisite – file must exist & load ✓ (no points awarded)
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load document: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Gather non-empty paragraphs (ignores blanks)
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    print(f"Total non-empty paragraphs found: {len(paragraphs)}")
    if len(paragraphs) < 2:
        print("✗ Document has fewer than 2 paragraphs with text")
        print("REWARD: 0.0")
        return 0.0

    # Progressive scoring – 0.5 pt per correctly formatted paragraph
    score = 0.0
    for idx in range(2):
        para_ok = is_double_spacing(paragraphs[idx])
        if para_ok:
            score += 0.5
            print(f"✓ Paragraph {idx + 1} uses double spacing (0.5 points)")
        else:
            print(f"✗ Paragraph {idx + 1} does NOT use double spacing")

    final_score = min(score, 1.0)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# -------------------------------
# Execute verification when run
# -------------------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/change_the_first_and_second_paragraphs_so_they_use_20_line_spacing.docx"
    verify_double_spacing_first_two(DOC_PATH)
