"""
FINAL REWARD SCRIPT - SUCCESS
Task: LibreOffice keeps letting ‘Mr.’, ‘Ms.’ and ‘Dr.’ dangle at the end of a line in paragraph 3 of my report. What’s the quickest way to swap the regular space after each of those abbreviations for a hard (Ctrl+Shift+Space) one—just in that single paragraph?
Generated: 2025-09-10 14:23:30
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import re
from docx import Document

def verify_hard_spaces(file_path: str) -> float:
    """Reward script for verifying that, in paragraph 3 of the given DOCX file,
    the abbreviations “Mr.”, “Ms.” and “Dr.” are each followed by a non-breaking
    space (U+00A0) rather than a regular space.  Progressive scoring:
        • 0.3 points for every abbreviation correctly fixed (max 0.9)
        • Extra 0.1 bonus if ALL are correct (total 1.0)
    Returns a float between 0.0 and 1.0 and prints detailed diagnostics.
    """

    abbreviations = ["Mr.", "Ms.", "Dr."]
    max_score = 1.0
    score = 0.0

    # ---------- Load the document ----------
    if not os.path.exists(file_path):
        print(f"✗ File not found: {file_path}")
        print("REWARD: 0.0")
        return 0.0  # Cannot proceed without the file

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Failed to open DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    paragraphs = doc.paragraphs
    print(f"✓ Document loaded. Total paragraphs: {len(paragraphs)}")

    # ---------- Identify the target paragraph ----------
    if len(paragraphs) >= 3:
        target_para = paragraphs[2]  # Paragraph 3 (0-based index 2)
        print("Using paragraph 3 (index 2) as target paragraph.")
    else:
        # Fallback: first paragraph containing an abbreviation
        target_para = None
        for p in paragraphs:
            if any(abbr in p.text for abbr in abbreviations):
                target_para = p
                print("Fallback: paragraph containing abbreviations used as target paragraph.")
                break
        if target_para is None:
            print("✗ No paragraph with the specified abbreviations found.")
            print("REWARD: 0.0")
            return 0.0

    para_text = target_para.text
    print("Target paragraph text:")
    print(para_text)

    # ---------- Verification per abbreviation ----------
    all_correct = True  # Track whether every abbreviation passes
    for abbr in abbreviations:
        # Patterns for NBSP and regular space
        pattern_nbsp = re.escape(abbr) + "\u00A0"
        pattern_regular = re.escape(abbr) + " "

        has_nbsp = re.search(pattern_nbsp, para_text)
        has_reg = re.search(pattern_regular, para_text)

        if has_nbsp and not has_reg:
            score += 0.3
            print(f"✓ {abbr} followed by non-breaking space found and no regular space counterpart ( +0.3 )")
        else:
            all_correct = False
            if not has_nbsp:
                print(f"✗ {abbr} is NOT followed by a non-breaking space (0 points)")
            if has_reg:
                print(f"✗ {abbr} still followed by a regular space somewhere (0 points)")

    # ---------- Bonus for perfect replacement ----------
    if all_correct:
        score += 0.1
        print("✓ All abbreviations formatted correctly in paragraph ( +0.1 bonus )")
    else:
        print("Some abbreviations not correctly formatted – no bonus awarded.")

    # ---------- Finalise score ----------
    final_score = min(score, max_score)
    # Stabilise floating-point rounding; snap to 1.0 if very close
    if abs(final_score - 1.0) <= 1e-3:
        final_score = 1.0
    else:
        final_score = round(final_score, 3)

    print(f"Total score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score

# ---------------- Main Execution ----------------
if __name__ == "__main__":
    FILE_PATH = "/home/user/libreoffice_keeps_letting_mr_ms_and_dr_dangle_at_the_end_of_a_line_in_paragraph_3_of_my_report_whats.docx"
    verify_hard_spaces(FILE_PATH)

