"""
FINAL REWARD SCRIPT - SUCCESS
Task: All the headings in my 25-page report are in Title Case, but the client wants them in sentence case (e.g., "Quarterly results" instead of "Quarterly Results"). There are about 40 headings spread across Heading 1 through Heading 3. Is there a quick way in LibreOffice Writer to convert every one of those headings to sentence case without editing each line manually?
Generated: 2025-09-10 19:29:15
Status: success
Model: azure-o3
Total Steps: 1
"""

from docx import Document
import os
import re


def is_sentence_case(text: str) -> bool:
    """Return True if the given heading text follows sentence-case rules.

    Basic rule used here:
      • First word may start with uppercase (proper start of a sentence)
      • Second alphabetical word must begin with lowercase (unless it is an
        acronym / digit).  This reliably distinguishes Title Case from
        sentence case for most headings.
    """
    text = text.strip()
    if not text:
        return True  # Empty headings are ignored / treated as compliant

    # Tokenise heading into alphanum words
    tokens = re.findall(r"[A-Za-z0-9]+", text)
    if len(tokens) < 2:
        # Single-word headings cannot reveal the difference – accept them
        return True

    second = tokens[1]
    for ch in second:
        if ch.isalpha():
            return ch.islower()  # sentence case => second word starts lower
    # If 2nd token has no alphabetic char (e.g. "Q1") treat as compliant
    return True


def verify_headings_sentence_case(file_path: str) -> float:
    """Verify that all Heading 1–3 paragraphs are in sentence case.

    Scoring (progressive):
        0.2  – File contains at least one recognised heading
        up to 0.8 – Proportion of headings in correct sentence case
    """
    print(f"Verifying headings sentence case in: {file_path}")

    total_score = 0.0
    max_score = 1.0

    # --- Load document -----------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Error loading document: {e}")
        return 0.0

    # --- Collect headings ---------------------------------------------------
    headings = []
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ""
        if style_name.startswith("Heading"):
            text = para.text.strip()
            if text:
                headings.append(text)

    if not headings:
        print("✗ No Heading 1-3 styles found in document")
        return 0.0

    print(f"✓ Found {len(headings)} heading paragraphs")
    total_score += 0.2  # award points only once headings are confirmed

    # --- Analyse sentence-case compliance ----------------------------------
    compliant = 0
    for h in headings:
        if is_sentence_case(h):
            compliant += 1
        else:
            print(f"  ✗ Not sentence case: '{h}'")

    print(f"Sentence-case headings: {compliant}/{len(headings)}")

    ratio = compliant / len(headings)  # 0.0-1.0 proportion
    total_score += 0.8 * ratio  # scale remaining points by ratio

    final_score = min(total_score, max_score)
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    DOC_PATH = "/home/user/all_the_headings_in_my_25_page_report_are_in_title_case_but_the_client_wants_them_in_sentence_case_e.docx"
    verify_headings_sentence_case(DOC_PATH)

