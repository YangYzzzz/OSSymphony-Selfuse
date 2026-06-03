"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, whenever I try to center my Heading 1 style, it drags the Heading 2 paragraphs over as well. I need every single paragraph with the exact style name “Heading 1” to be centered horizontally, but anything set to “Heading 2” must remain left-aligned—no exceptions. What’s the step-by-step way to lock those two alignments in place through the Styles panel?
Generated: 2025-09-10 13:05:57
Status: success
Model: azure-o3
Total Steps: 5
"""

from docx import Document
from docx.enum.text import WD_ALIGN_PARAGRAPH
import os


def verify_heading_alignments(file_path: str) -> float:
    """Reward script for the LibreOffice Writer task.

    Requirements to earn points (progressive scoring):
    1. Every paragraph with style name *Heading 1* must be centred horizontally (0.5 pt).
    2. Every paragraph with style name *Heading 2* must be left-aligned (either
       explicit LEFT or default alignment, 0.5 pt).

    The script prints diagnostic information for full transparency and returns a
    float score between 0.0 and 1.0 inclusive.
    """

    print(f"Verifying heading alignments in: {file_path}")
    total_score = 0.0  # progressive score accumulator

    # ---------- 1. Preliminary checks (no points) ----------
    if not os.path.exists(file_path):
        print("✗ Document file not found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as exc:
        print(f"✗ Failed to load DOCX file: {exc}")
        print("REWARD: 0.0")
        return 0.0

    # ---------- 2. Collect paragraphs by style (no points for mere presence) ----------
    h1_paragraphs = []
    h2_paragraphs = []
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ""
        if style_name == "Heading 1":
            h1_paragraphs.append(para)
        elif style_name == "Heading 2":
            h2_paragraphs.append(para)

    if not h1_paragraphs:
        print("✗ No paragraphs with style 'Heading 1' were found – requirement cannot be verified")
    if not h2_paragraphs:
        print("✗ No paragraphs with style 'Heading 2' were found – requirement cannot be verified")
    if not h1_paragraphs or not h2_paragraphs:
        print("REWARD: 0.0")
        return 0.0  # cannot assess without both styles present

    print(f"✓ Located {len(h1_paragraphs)} Heading 1 and {len(h2_paragraphs)} Heading 2 paragraphs (0 points – prerequisite)")

    # ---------- 3. Requirement A: Heading 1 paragraphs are centred (0.5 pts) ----------
    all_h1_centred = True
    for p in h1_paragraphs:
        if p.alignment != WD_ALIGN_PARAGRAPH.CENTER:
            all_h1_centred = False
            print(f"✗ Heading 1 NOT centred: '{p.text[:40]}' (alignment code={p.alignment})")
            break
    if all_h1_centred:
        print("✓ All Heading 1 paragraphs are horizontally centred (0.5 points)")
        total_score += 0.5

    # ---------- 4. Requirement B: Heading 2 paragraphs are left-aligned (0.5 pts) ----------
    # Default left alignment can be represented as None or LEFT.
    all_h2_left = True
    for p in h2_paragraphs:
        if p.alignment not in (None, WD_ALIGN_PARAGRAPH.LEFT):
            all_h2_left = False
            print(f"✗ Heading 2 NOT left-aligned: '{p.text[:40]}' (alignment code={p.alignment})")
            break
    if all_h2_left:
        print("✓ All Heading 2 paragraphs are left-aligned (0.5 points)")
        total_score += 0.5

    # ---------- 5. Final score ----------
    final_score = min(total_score, 1.0)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path to the document that should have been modified by the agent
    FILE_PATH = "/home/user/in_libreoffice_writer_whenever_i_try_to_center_my_heading_1_style_it_drags_the_heading_2_paragraphs_.docx"
    verify_heading_alignments(FILE_PATH)
