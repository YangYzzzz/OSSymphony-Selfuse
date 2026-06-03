"""
FINAL REWARD SCRIPT - SUCCESS
Task: Could you make the Heading 1 on the first page centered?
Generated: 2025-10-14 11:34:47
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH


def verify_heading1_centered(file_path: str) -> float:
    """Verify that the first Heading 1 paragraph in the document is centered.

    Scoring (progressive):
      • 0.0  – File missing / unreadable or no Heading 1 found.
      • 0.3  – Heading 1 exists (content identified).
      • +0.7 – That Heading 1 is effectively CENTER aligned.
      → 1.0  – Full success (Heading 1 present **and** centered).
    """

    max_score = 1.0
    score = 0.0

    print(f"Verifying document: {file_path}")

    # ---------- 1) Basic file presence check (no points) ----------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0  # cannot proceed

    # ---------- 2) Attempt to load DOCX (prerequisite, no points) ----------
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error opening DOCX: {e}")
        return 0.0

    # ---------- 3) Locate the first Heading 1 paragraph ----------
    heading_para = None
    for para in doc.paragraphs:
        style_name = para.style.name.lower()
        if style_name.startswith("heading 1"):
            heading_para = para
            break

    if heading_para is None:
        print("✗ No Heading 1 paragraph found in document")
        return 0.0  # nothing else to score

    print(f"✓ Found Heading 1: '{heading_para.text.strip()}'")
    score += 0.3  # Heading 1 exists

    # ---------- 4) Determine its effective alignment ----------
    # Paragraph-level alignment overrides style-level alignment if defined
    effective_alignment = (
        heading_para.alignment
        if heading_para.alignment is not None
        else heading_para.style.paragraph_format.alignment
    )

    if effective_alignment == WD_ALIGN_PARAGRAPH.CENTER:
        print("✓ Heading 1 is CENTER aligned")
        score += 0.7
    else:
        alignment_names = {
            WD_ALIGN_PARAGRAPH.LEFT: "LEFT",
            WD_ALIGN_PARAGRAPH.RIGHT: "RIGHT",
            WD_ALIGN_PARAGRAPH.JUSTIFY: "JUSTIFY",
            WD_ALIGN_PARAGRAPH.DISTRIBUTE: "DISTRIBUTE",
        }
        align_str = alignment_names.get(effective_alignment, str(effective_alignment))
        print(f"✗ Heading 1 is not centered (alignment = {align_str})")

    final_score = min(score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


# ----------------- EXECUTION ENTRY POINT -----------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/could_you_make_the_heading_1_on_the_first_page_centered.docx"
    verify_heading1_centered(DOC_PATH)

