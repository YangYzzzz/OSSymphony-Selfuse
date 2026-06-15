"""
FINAL REWARD SCRIPT - SUCCESS
Task: Make all section headings start with uppercase letters for each word.
Generated: 2025-10-14 10:12:22
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os
import re


def verify_headings_title_case(file_path: str) -> float:
    """Verify that every section heading in the DOCX starts with an
    uppercase letter for each word (Title-Case).

    Scoring:
        • 1.0  – every heading satisfies the rule
        • <1.0 – proportional to the fraction of headings that are correct
        • 0.0  – no headings, file missing, or unreadable
    """

    max_score = 1.0
    total_score = 0.0

    print(f"Verifying document: {file_path}")

    # ---------- Preliminary checks (no points awarded) ----------
    if not os.path.exists(file_path):
        print("✗ File not found – cannot verify task")
        return 0.0  # nothing to score
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to load DOCX: {e}")
        return 0.0  # unreadable file → task failed

    # ---------- Gather all paragraphs styled as headings ----------
    headings = []
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ""
        if style_name.startswith("Heading"):
            text = para.text.strip()
            if text:
                headings.append(text)
                print(f"  Found heading: '{text}'")

    # If the document has no headings, the task cannot be assessed
    if not headings:
        print("✗ No headings found – cannot evaluate task")
        return 0.0

    # ---------- Check each heading for Title-Case correctness ----------
    total_headings = len(headings)
    correct_headings = 0

    for heading in headings:
        words = re.split(r"\s+", heading)
        heading_ok = True

        for word in words:
            # Skip tokens that contain no alphabetic characters (e.g., numbers, punctuation)
            match = re.search(r"[A-Za-z]", word)
            if not match:
                continue
            first_alpha = match.group(0)
            if not first_alpha.isupper():
                heading_ok = False
                print(f"    ✗ Word '{word}' in heading '{heading}' is not capitalized correctly")
                break

        if heading_ok:
            correct_headings += 1
            print("    ✓ Heading OK")

    print(f"Correct headings: {correct_headings}/{total_headings}")

    # ---------- Progressive scoring ----------
    total_score = (correct_headings / total_headings) * max_score
    final_score = round(total_score, 2)  # round for neatness

    print(f"REWARD: {final_score}")
    return final_score


# ----------------- Execute verification -----------------
if __name__ == "__main__":
    DOC_PATH = "/home/user/make_all_section_headings_start_with_uppercase_letters_for_each_word.docx"
    reward = verify_headings_title_case(DOC_PATH)

