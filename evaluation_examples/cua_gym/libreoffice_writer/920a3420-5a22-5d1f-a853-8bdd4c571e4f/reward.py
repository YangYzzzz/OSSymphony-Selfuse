"""
FINAL REWARD SCRIPT - SUCCESS
Task: I bookmarked my Methods section as "sec-methods" earlier. Now, in the ninth paragraph of the introduction, I just want LibreOffice Writer to show whatever page that bookmark currently sits on—so the number updates if the section moves. How do I drop in that kind of cross-reference?
Generated: 2025-09-10 14:39:45
Status: success
Model: azure-o3
Total Steps: 6
"""

import os
import re
import zipfile
import lxml.etree as ET
from docx import Document


def verify_task(file_path: str) -> float:
    """Verify LibreOffice Writer task:
    1. Bookmark named 'sec-methods' exists.
    2. A PAGEREF field referencing that bookmark exists.
    3. That PAGEREF is placed in the ninth paragraph of the Introduction section.

    Returns a progressive score between 0.0 and 1.0.
    """

    print("Verifying cross-reference to Methods bookmark …")
    max_score = 1.0
    score = 0.0

    # ------------------------------------------------------------------
    # 0. Basic file checks (no points)
    # ------------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        return 0.0

    # ------------------------------------------------------------------
    # 1. Load DOCX (python-docx) and raw XML (for deep analysis)
    # ------------------------------------------------------------------
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"✗ Unable to load DOCX: {e}")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            xml_bytes = z.read("word/document.xml")
        root = ET.fromstring(xml_bytes)
        ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    except Exception as e:
        print(f"✗ Failed to parse document XML: {e}")
        return 0.0

    # ------------------------------------------------------------------
    # 2. Requirement: bookmark named 'sec-methods' exists (0.3)
    # ------------------------------------------------------------------
    bookmark_found = False
    for b in root.findall(".//w:bookmarkStart", ns):
        name = b.get(f"{{{ns['w']}}}name")
        if name and name.lower() == "sec-methods":
            bookmark_found = True
            print("✓ Bookmark 'sec-methods' found in document")
            break
    if bookmark_found:
        score += 0.3
    else:
        print("✗ Bookmark 'sec-methods' not found")

    # ------------------------------------------------------------------
    # 3. Requirement: PAGEREF field referencing the bookmark exists (0.5)
    # ------------------------------------------------------------------
    pageref_found = False
    pageref_para_index = None  # index among XML paragraphs

    for instr in root.findall(".//w:instrText", ns):
        text = "".join(instr.itertext())
        if re.search(r"PAGEREF\s+sec-methods", text, re.I):
            pageref_found = True

            # Find ancestor <w:p> to locate paragraph index
            p_elem = instr
            while p_elem is not None and p_elem.tag != f"{{{ns['w']}}}p":
                p_elem = p_elem.getparent()
            if p_elem is not None:
                all_paras = list(root.findall('.//w:p', ns))
                pageref_para_index = all_paras.index(p_elem)
            print("✓ Found PAGEREF field referencing 'sec-methods'")
            break

    if pageref_found:
        score += 0.5
    else:
        print("✗ No PAGEREF field referencing 'sec-methods' found")

    # ------------------------------------------------------------------
    # 4. Requirement: PAGEREF is in 9th paragraph of Introduction (0.2)
    # ------------------------------------------------------------------
    if pageref_found and pageref_para_index is not None:
        # Locate paragraph index of the Introduction heading
        intro_index = None
        all_xml_paras = list(root.findall('.//w:p', ns))
        for idx, p_elem in enumerate(all_xml_paras):
            para_text = ''.join(p_elem.itertext()).strip()
            if para_text.lower() == 'introduction':
                intro_index = idx
                break

        if intro_index is not None:
            offset = pageref_para_index - intro_index
            if offset == 9:
                print("✓ PAGEREF field is 9 paragraphs after the Introduction heading (ninth paragraph)")
                score += 0.2
            else:
                print(f"✗ PAGEREF paragraph offset is {offset}, expected 9")
        else:
            print("✗ Introduction heading not found; cannot verify paragraph position")
    else:
        print("Skipping position verification due to missing PAGEREF")

    final_score = min(score, max_score)
    print(f"Computed score: {final_score}")
    return final_score


if __name__ == "__main__":
    path = "/home/user/i_bookmarked_my_methods_section_as_sec_methods_earlier_now_in_the_ninth_paragraph_of_the_introductio.docx"
    reward = verify_task(path)
    print(f"REWARD: {reward}")
