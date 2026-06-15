"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, paragraph 2 of my report begins with the exact words "Background:" and I foolishly used Shift+Enter after every phrase. Now I just want those manual line breaks (\n) in that single paragraph swapped out for regular spaces so it flows like a normal sentence. How can I do this quickly without touching the rest of the document?
Generated: 2025-09-10 13:18:38
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
from docx import Document
from docx.oxml.ns import qn

def verify_task(file_path):
    """Reward script for the LibreOffice Writer task.

    Objective:
      1. Locate the paragraph whose text begins with the exact words
         "Background:".
      2. Ensure that within this single paragraph all manual line breaks
         (Shift+Enter → <w:br/>) and raw newline characters ("\n"/"\r")
         have been replaced by regular spaces so the text flows like a
         normal sentence.
      3. No points are given for natural conditions (file existence,
         document loading, etc.).

    Scoring (progressive):
      • 0.5  – no raw newline characters remain in the paragraph text.
      • 0.5  – no manual line-break (<w:br/>) elements remain in the
                 underlying XML runs of that paragraph.
      A perfect score of 1.0 is awarded only when both conditions are met.
    """

    print(f"Verifying document: {file_path}")

    # -----------------------------------------------------------------
    # Prerequisite: File must exist and be loadable – yields NO POINTS.
    # -----------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ Document not found.")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Could not open document: {e}")
        return 0.0

    # -----------------------------------------------------------------
    # Locate the specific paragraph (still NO POINTS for locating it).
    # -----------------------------------------------------------------
    target_para = None
    for para in doc.paragraphs:
        if para.text.strip().startswith("Background:"):
            target_para = para
            break

    if target_para is None:
        print("✗ Paragraph beginning with 'Background:' not found.")
        return 0.0

    print("✓ Located paragraph starting with 'Background:'")

    # -----------------------------------------------------------------
    # Requirement verifications (points awarded only for SUCCESS).
    # -----------------------------------------------------------------
    total_score = 0.0

    # Requirement 1 – no raw newline characters in visible text
    visible_text = target_para.text
    if ("\n" in visible_text) or ("\r" in visible_text):
        print("✗ Raw newline characters still present in paragraph text")
    else:
        print("✓ No raw newline characters found in paragraph text (0.5 points)")
        total_score += 0.5

    # Requirement 2 – no manual line-break (<w:br/>) elements in XML
    br_found = False
    for run in target_para.runs:
        for child in run._element:
            if child.tag == qn('w:br'):
                br_found = True
                break
        if br_found:
            break

    if br_found:
        print("✗ Manual line break elements (<w:br/>) still present in paragraph")
    else:
        print("✓ No manual line break elements found in paragraph (0.5 points)")
        total_score += 0.5

    # -----------------------------------------------------------------
    # Final score capped at 1.0
    # -----------------------------------------------------------------
    final_score = min(total_score, 1.0)
    print(f"Total score: {final_score}")
    return final_score


# ------------------------------ Runner ------------------------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/in_libreoffice_writer_paragraph_2_of_my_report_begins_with_the_exact_words_background_and_i_foolishl.docx"
    reward = verify_task(FILE_PATH)
    print(f"REWARD: {reward}")
