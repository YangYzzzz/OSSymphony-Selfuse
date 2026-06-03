"""
FINAL REWARD SCRIPT - SUCCESS
Task: While editing my draft in LibreOffice Writer, I want to stick a footnote immediately after the word “methodology” in paragraph 2. The footnote itself should just say “Define scope.” What’s the quickest way to insert that without throwing off the rest of the layout?
Generated: 2025-09-10 18:07:13
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import re
import zipfile
from lxml import etree

"""
Reward Script for LibreOffice Writer Footnote Task
-------------------------------------------------
Task to verify:
1. A footnote reference must appear in *paragraph 2* immediately after the word
   "methodology".
2. The corresponding footnote text must be exactly "Define scope." (case-insensitive,
   trailing period optional).

Scoring (progressive):
• 0.5 – Footnote reference correctly placed in paragraph 2.
• 0.5 – Footnote text matches "Define scope.".
Returns 1.0 only when both conditions are satisfied.
"""

# File to check (path is supplied by the autograder environment)
FILE_PATH = (
    "/home/user/while_editing_my_draft_in_libreoffice_writer_i_want_to_stick_"
    "a_footnote_immediately_after_the_word_m.docx"
)

# XML namespace for WordprocessingML
NS = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}


def _get_paragraphs(xml_root):
    """Return all <w:p> elements in document order."""
    return xml_root.xpath("//w:body/w:p", namespaces=NS)


def _verify_reference_position(p2):
    """Check footnote reference is in paragraph 2 right after 'methodology'."""
    cumulative_text = ""
    for elem in p2.iter():
        tag_local = etree.QName(elem).localname
        if tag_local == "t":  # text node
            cumulative_text += elem.text or ""
        elif tag_local == "footnoteReference":
            # When we hit the reference the preceding text should end with 'methodology'
            if re.search(r"methodology[\s\W]*$", cumulative_text, re.IGNORECASE):
                fid = elem.get(f"{{{NS['w']}}}id")
                print("✓ Footnote reference correctly follows 'methodology' in paragraph 2")
                return True, fid
            else:
                print("✗ Footnote reference in paragraph 2 is NOT immediately after 'methodology'")
                return False, elem.get(f"{{{NS['w']}}}id")
    print("✗ No footnote reference found in paragraph 2")
    return False, None


def _verify_footnote_text(docx_zip, footnote_id):
    """Check that the footnote text equals 'Define scope.' (case-insensitive)."""
    if footnote_id is None:
        print("✗ No footnote ID available to check text")
        return False
    try:
        foot_xml = docx_zip.read("word/footnotes.xml")
    except KeyError:
        print("✗ footnotes.xml missing in DOCX")
        return False

    root = etree.fromstring(foot_xml)
    node = root.xpath(f"//w:footnote[@w:id='{footnote_id}']", namespaces=NS)
    if not node:
        print(f"✗ Footnote with id {footnote_id} not found in footnotes.xml")
        return False

    # Concatenate all text within the footnote element
    text_parts = [el.text for el in node[0].iter() if etree.QName(el).localname == "t" and el.text]
    foot_text = " ".join(text_parts).strip()
    print(f"Footnote text found: '{foot_text}'")

    if re.fullmatch(r"Define scope\.?", foot_text, flags=re.IGNORECASE):
        print("✓ Footnote text matches 'Define scope.'")
        return True
    else:
        print("✗ Footnote text does NOT match 'Define scope.'")
        return False


def verify_task(file_path: str) -> float:
    """Main verification routine. Returns a score between 0.0 and 1.0."""
    if not os.path.exists(file_path):
        print("✗ Document file not found – cannot verify task")
        print("REWARD: 0.0")
        return 0.0  # Immediate failure if file is missing

    score = 0.0
    with zipfile.ZipFile(file_path) as docx_zip:
        # Load main document XML
        doc_xml = docx_zip.read("word/document.xml")
        doc_root = etree.fromstring(doc_xml)

        # 1) Verify footnote reference placement in paragraph 2
        paragraphs = _get_paragraphs(doc_root)
        if len(paragraphs) < 2:
            print("✗ Document has fewer than 2 paragraphs – cannot satisfy requirement")
            print("REWARD: 0.0")
            return 0.0

        ref_ok, foot_id = _verify_reference_position(paragraphs[1])
        if ref_ok:
            score += 0.5

        # 2) Verify footnote text content
        text_ok = _verify_footnote_text(docx_zip, foot_id)
        if text_ok:
            score += 0.5

    final_score = min(score, 1.0)
    print(f"Final score: {final_score}")
    print(f"REWARD: {final_score}")
    return final_score


# Execute verification when run as a script
if __name__ == "__main__":
    verify_task(FILE_PATH)

