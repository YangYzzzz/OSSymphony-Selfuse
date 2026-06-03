"""
FINAL REWARD SCRIPT - SUCCESS
Task: Paragraph 9 is yelling at me in all caps. What’s the quickest way in LibreOffice Writer to flip just that paragraph back to normal sentence case?
Generated: 2025-09-10 16:42:46
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import re
from docx import Document

def _normalize(text: str) -> str:
    """Helper to normalise text for comparison (case-insensitive, only words)."""
    text = text.lower()
    tokens = re.findall(r"\b\w+\b", text)
    return " ".join(tokens)

def verify_sentence_case_fix(file_path: str) -> float:
    """Verify that paragraph 9 has been converted from ALL CAPS to sentence case.

    Scoring (progressive):
        0.5  – paragraph 9 still contains the exact expected words (content preserved)
        0.5  – paragraph 9 is **not** all uppercase anymore (contains lowercase letters)
        1.0  – both conditions satisfied
    """

    max_score = 1.0
    score = 0.0

    # -------- 1. Prerequisite: file must exist and load --------
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        print("REWARD: 0.0")
        return 0.0  # cannot continue

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to open DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect *non-empty* paragraphs so that blank lines do not affect indexing
    paragraphs = [p for p in doc.paragraphs if p.text.strip()]
    total_paras = len(paragraphs)
    print(f"✓ Loaded document – {total_paras} non-empty paragraphs found (no points, prerequisite)")

    if total_paras < 9:
        print("✗ Document has fewer than 9 paragraphs – cannot verify task")
        print("REWARD: 0.0")
        return 0.0

    # We use 0-based index – paragraph 9 is index 8
    target_para_text = paragraphs[8].text.strip()
    print("Paragraph 9 text:", target_para_text)

    # -------- 2. Verify content preserved (0.5) --------
    expected_text = "This is paragraph nine in all caps and it is yelling."
    if _normalize(target_para_text) == _normalize(expected_text):
        print("✓ Paragraph 9 content matches expected text (0.5)")
        score += 0.5
    else:
        print("✗ Paragraph 9 content does NOT match expected text (0 points)")

    # -------- 3. Verify case has been corrected (0.5) --------
    # Requirement: it should NOT be all uppercase any more → must contain lowercase letters
    if re.search(r"[a-z]", target_para_text):
        print("✓ Paragraph 9 contains lowercase letters – not all caps (0.5)")
        score += 0.5
    else:
        print("✗ Paragraph 9 is still all uppercase (0 points)")

    final_score = min(score, max_score)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path to the document in the autograder environment
    FILE_PATH = "/home/user/paragraph_9_is_yelling_at_me_in_all_caps_whats_the_quickest_way_in_libreoffice_writer_to_flip_just_t.docx"
    verify_sentence_case_fix(FILE_PATH)
