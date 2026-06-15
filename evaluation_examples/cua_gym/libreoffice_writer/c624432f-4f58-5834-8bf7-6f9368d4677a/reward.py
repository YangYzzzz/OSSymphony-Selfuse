"""
FINAL REWARD SCRIPT - SUCCESS
Task: Please center the main title at the top of my Writer document.
Generated: 2025-10-14 11:18:41
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
from docx import Document
from docx.enum.text import WD_PARAGRAPH_ALIGNMENT


def _effective_alignment(paragraph):
    """Return the paragraph's effective alignment, considering direct formatting and style."""
    # Direct formatting takes precedence
    if paragraph.alignment is not None:
        return paragraph.alignment

    # Fallback to style-defined alignment (if any)
    try:
        style_align = paragraph.style.paragraph_format.alignment  # may raise if style is None
        return style_align
    except Exception:
        return None


def verify_centered_title(file_path):
    """
    Verification logic for the task:
    1. Locate the first *non-empty* paragraph in the document (this should be the title).
    2. Confirm that this paragraph is CENTER-aligned.
    3. Ensure that it is truly the first paragraph in the file (i.e., it sits at the top—no other
       paragraphs, even empty ones, precede it).

    Scoring (progressive):
        • 0.8 points – paragraph is centered.
        • 0.2 points – paragraph is the very first paragraph in the document.
    The script never awards points for natural conditions such as file existence or successful load.
    """
    print(f"Checking document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0

    # Load the DOCX file (no points for successful load)
    try:
        doc = Document(file_path)
    except Exception as exc:
        print(f"✗ Unable to load document: {exc}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = list(doc.paragraphs)

    # Find first non-empty paragraph (candidate title)
    title_para = None
    for para in paragraphs:
        if para.text and para.text.strip():
            title_para = para
            break

    if title_para is None:
        print("✗ No non-empty paragraphs found – cannot locate title")
        print("REWARD: 0.0")
        return 0.0

    print(f"First content paragraph text: '{title_para.text.strip()}'")

    total_score = 0.0

    # Requirement 1 – CENTER alignment
    if _effective_alignment(title_para) == WD_PARAGRAPH_ALIGNMENT.CENTER:
        print("✓ Title paragraph is CENTER-aligned (0.8)")
        total_score += 0.8
    else:
        print("✗ Title paragraph is NOT center-aligned (0.0)")

    # Requirement 2 – at top of the document (index 0)
    if paragraphs.index(title_para) == 0:
        print("✓ Title paragraph is the very first paragraph (0.2)")
        total_score += 0.2
    else:
        print("✗ Other paragraphs found above the title (0.0)")

    # Cap at 1.0 and round for neatness
    final_score = min(total_score, 1.0)
    final_score = round(final_score, 2)

    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Default path for the autograder environment; adjust if necessary
    DOC_PATH = "/home/user/please_center_the_main_title_at_the_top_of_my_writer_document.docx"
    verify_centered_title(DOC_PATH)

