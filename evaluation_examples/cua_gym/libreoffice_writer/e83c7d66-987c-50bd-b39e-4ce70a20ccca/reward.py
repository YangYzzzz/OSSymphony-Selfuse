"""
FINAL REWARD SCRIPT - SUCCESS
Task: The ragged right edge in paragraphs 2, 3, 4, and 5 is driving me nuts, but I don’t want the rest of my document to hyphenate. In LibreOffice Writer, how do I switch hyphenation ON for exactly those four paragraphs only and leave paragraph 1 and everything after paragraph 5 untouched?
Generated: 2025-09-10 18:38:41
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree

"""
Reward Script: Verify selective hyphenation in a DOCX produced with LibreOffice Writer.
Task requirement:
 - Hyphenation must be ENABLED (ON) only for paragraphs 2-5.
 - Paragraph 1 and all paragraphs after 5 must keep hyphenation OFF/DEFAULT.

Scoring (progressive):
  • 0.60 points – each of the target paragraphs (2-5) correctly set to ON (0.15 each)
  • 0.40 points – the remaining paragraphs NOT set to ON (distributed proportionally)
Returns 1.0 only when every rule is satisfied.
"""

FILE_PATH = "/home/user/the_ragged_right_edge_in_paragraphs_2_3_4_and_5_is_driving_me_nuts_but_i_dont_want_the_rest_of_my_do.docx"

# Namespace used in DOCX XML
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

def _hyphenation_state(paragraph):
    """Determine explicit hyphenation state for a <w:p> element.

    Returns:
        'on'       – hyphenation explicitly allowed (w:suppressAutoHyphens w:val="0")
        'off'      – hyphenation explicitly suppressed (element present & val≠0)
        'default'  – no explicit setting (inherit document/default settings)
    """
    suppr = paragraph.xpath("./w:pPr/w:suppressAutoHyphens", namespaces=NS)
    if not suppr:
        return "default"
    val = suppr[0].get(f"{{{NS['w']}}}val")
    if val is None:
        # Element present with no val attribute ⇒ true (suppressed)
        return "off"
    return "on" if val.lower() in ("0", "false") else "off"

def verify_hyphenation(file_path: str) -> float:
    print(f"Verifying hyphenation for document: {file_path}")

    if not os.path.exists(file_path):
        print("✗ File not found")
        print("REWARD: 0.0")
        return 0.0

    # Extract document.xml from DOCX package
    try:
        with zipfile.ZipFile(file_path) as z:
            document_xml = z.read("word/document.xml")
    except Exception as e:
        print(f"✗ Unable to open DOCX or read document.xml: {e}")
        print("REWARD: 0.0")
        return 0.0

    root = etree.fromstring(document_xml)
    paragraphs = root.xpath("//w:body/w:p", namespaces=NS)

    # Keep only non-empty text paragraphs (ignore empty/structural ones)
    text_paragraphs = []
    for p in paragraphs:
        txt = "".join(p.xpath(".//w:t/text()", namespaces=NS)).strip()
        if txt:
            text_paragraphs.append(p)

    if len(text_paragraphs) < 5:
        print(f"✗ Less than 5 textual paragraphs found ({len(text_paragraphs)}) – cannot verify.")
        print("REWARD: 0.0")
        return 0.0

    states = [_hyphenation_state(p) for p in text_paragraphs]
    for i, state in enumerate(states, start=1):
        print(f"Paragraph {i}: hyphenation = {state}")

    score = 0.0

    # --- Requirement 1: paragraphs 2-5 must be ON ---
    target_indices = range(1, 5)  # zero-based 1-4 correspond to paragraphs 2-5 (1-based)
    per_target = 0.60 / 4  # 0.15 each
    for idx in target_indices:
        if idx < len(states) and states[idx] == "on":
            score += per_target
        else:
            print(f"✗ Paragraph {idx + 1} is not set to hyphenation ON.")

    # --- Requirement 2: all other paragraphs must NOT be ON ---
    other_indices = [i for i in range(len(states)) if i not in target_indices]
    if other_indices:
        correct = sum(states[i] != "on" for i in other_indices)
        score += 0.40 * (correct / len(other_indices))
        if correct != len(other_indices):
            wrong = len(other_indices) - correct
            print(f"✗ {wrong} non-target paragraph(s) incorrectly have hyphenation ON.")
    else:
        # No extra paragraphs – trivially grant full 0.40
        score += 0.40

    final_score = round(min(score, 1.0), 4)
    print(f"Computed score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    verify_hyphenation(FILE_PATH)

