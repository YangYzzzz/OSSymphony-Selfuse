"""
FINAL REWARD SCRIPT - SUCCESS
Task: I'm finishing up a short story in LibreOffice Writer and want that classic storybook feel. Specifically, I need the very first letter of paragraph one to be a drop cap—just 1 character, spanning exactly 2 lines. How do I set that up?
Generated: 2025-09-10 17:07:51
Status: success
Model: azure-o3
Total Steps: 8
"""

import os
import zipfile
from lxml import etree as ET


def verify_drop_cap(file_path: str) -> float:
    """Verify that the very first (non-heading) paragraph in the DOCX file
    has drop-cap formatting of exactly 1 character spanning 2 lines.

    Progressive scoring (max 1.0):
        • 0.50 – Drop-cap element present on the target paragraph
        • 0.25 – Drop-cap spans exactly 2 lines
        • 0.25 – Drop-cap length is exactly 1 character
    """
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    total_score = 0.0

    # --------------- Safety checks ---------------
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        print("REWARD: 0.0")
        return 0.0  # No progress possible

    try:
        with zipfile.ZipFile(file_path) as z:
            if "word/document.xml" not in z.namelist():
                print("✗ document.xml missing in DOCX – cannot verify drop cap")
                print("REWARD: 0.0")
                return 0.0
            root = ET.fromstring(z.read("word/document.xml"))
    except Exception as e:
        print(f"✗ Error opening or parsing DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # --------------- Locate the first real paragraph ---------------
    first_para = None
    for p in root.findall(".//w:body/w:p", ns):
        # Consolidate paragraph text
        text = "".join(p.itertext()).strip()
        if not text:
            continue  # skip empty paragraphs
        # Skip headings (paragraph style starts with "Heading")
        pstyle = p.find("./w:pPr/w:pStyle", ns)
        if pstyle is not None and pstyle.get(f"{{{ns['w']}}}val", "").lower().startswith("heading"):
            continue
        first_para = p
        break

    if first_para is None:
        print("✗ No suitable body paragraph found – nothing to verify")
        print("REWARD: 0.0")
        return 0.0

    # --------------- Check drop-cap properties ---------------
    drop_elem = first_para.find("./w:pPr/w:dropCap", ns)

    if drop_elem is not None and drop_elem.get(f"{{{ns['w']}}}val") == "drop":
        print("✓ Drop cap present on first paragraph (0.50 points)")
        total_score += 0.50

        # lines attribute
        lines = drop_elem.get(f"{{{ns['w']}}}lines")
        if lines is not None and lines.isdigit() and int(lines) == 2:
            print("✓ Drop cap spans exactly 2 lines (0.25 points)")
            total_score += 0.25
        else:
            print(f"✗ Drop cap lines incorrect – expected 2, found {lines}")

        # length attribute (characters spanned)
        length = drop_elem.get(f"{{{ns['w']}}}length")
        if length is not None and length.isdigit() and int(length) == 1:
            print("✓ Drop cap length is exactly 1 character (0.25 points)")
            total_score += 0.25
        else:
            print(f"✗ Drop cap length incorrect – expected 1, found {length}")
    else:
        print("✗ No drop-cap formatting detected on the first paragraph")

    final_score = min(total_score, 1.0)  # Just in case
    print("REWARD:", final_score)
    return final_score


# -------------------- Execute Verification --------------------
if __name__ == "__main__":
    DOCX_PATH = "/home/user/im_finishing_up_a_short_story_in_libreoffice_writer_and_want_that_classic_storybook_feel_specificall.docx"
    verify_drop_cap(DOCX_PATH)
