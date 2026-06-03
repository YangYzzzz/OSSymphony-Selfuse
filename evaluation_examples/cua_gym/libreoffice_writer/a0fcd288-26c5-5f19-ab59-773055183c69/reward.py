"""
FINAL REWARD SCRIPT - SUCCESS
Task: Set paragraph 1 and paragraph 2 in this document to double line spacing.
Generated: 2025-10-14 08:15:38
Status: success
Model: azure-o3
Total Steps: 2
"""

from docx import Document
import os

# ------------------------------------------------------------
# Reward Script: Verify double line-spacing on the 1st two
# paragraphs of a DOCX document.
# ------------------------------------------------------------
# Task to verify:
#   "Set paragraph 1 and paragraph 2 in this document to double
#    line spacing."
#
# Scoring logic (progressive):
#   • Paragraph-1 double-spaced  → 0.5 points
#   • Paragraph-2 double-spaced  → 0.5 points
#   => Perfect completion        → 1.0 points
# ------------------------------------------------------------

W_NAMESPACE = "http://schemas.openxmlformats.org/wordprocessingml/2006/main"


def _is_double_spacing(paragraph):
    """Return True if the paragraph has ~2.0 line spacing.
    Accepts both the high-level python-docx API value
    and raw XML <w:spacing w:line="480"/> (≈ double-space)."""
    fmt = paragraph.paragraph_format
    # High-level API check ---------------------------------------------------
    if fmt.line_spacing is not None:
        try:
            # python-docx may return Decimal or float
            if abs(float(fmt.line_spacing) - 2.0) < 0.01:
                return True
        except Exception:
            pass

    # Low-level XML fallback --------------------------------------------------
    ppr = paragraph._p.pPr
    if ppr is not None:
        spacing = ppr.find(f"{{{W_NAMESPACE}}}spacing")
        if spacing is not None:
            line_val = spacing.get(f"{{{W_NAMESPACE}}}line")
            # In Word, double-space ≈ 480 twips (240 * 2)
            if line_val is not None:
                try:
                    iv = int(line_val)
                    if 470 <= iv <= 490:  # tolerance window
                        return True
                except ValueError:
                    pass
    return False


def verify_task(file_path):
    """Main verification function returning a progressive score (0-1)."""
    print(f"Verifying document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0

    # Attempt to load DOCX ----------------------------------------------------
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to load document: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    if len(paragraphs) < 2:
        print("✗ Document contains fewer than two paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Scoring ---------------------------------------------------------------
    total_score = 0.0
    per_paragraph_score = 0.5  # each correctly formatted paragraph earns 0.5

    for idx in range(2):
        para = paragraphs[idx]
        is_double = _is_double_spacing(para)
        preview = para.text[:40].strip() + ("..." if len(para.text) > 40 else "")
        print(f"Paragraph {idx + 1}: '{preview}' -> double spacing: {is_double}")
        if is_double:
            total_score += per_paragraph_score
        else:
            print(f"✗ Paragraph {idx + 1} is NOT set to double line spacing")

    total_score = min(total_score, 1.0)  # safety cap
    print(f"Final score: {total_score}")
    print(f"REWARD: {total_score}")
    return total_score


# -------------------------------------------------------------------------
# Execute verification when run as a script
# -------------------------------------------------------------------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/set_paragraph_1_and_paragraph_2_in_this_document_to_double_line_spacing.docx"
    verify_task(DOC_PATH)

