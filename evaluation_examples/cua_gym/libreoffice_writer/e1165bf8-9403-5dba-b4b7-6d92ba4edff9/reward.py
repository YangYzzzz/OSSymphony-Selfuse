"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve got a 10-page Writer doc, and I need to be able to jump straight to the conclusions section later on. What’s the quickest way to stick a bookmark called "main-result" at the very start of paragraph 6?
Generated: 2025-09-10 17:27:50
Status: success
Model: azure-o3
Total Steps: 2
"""

import os
import zipfile
from lxml import etree

def verify_writer_bookmark(file_path: str) -> float:
    """Verify that the DOCX file contains a bookmark called 'main-result' at
    the very start of paragraph 6 (1-based index).

    Progressive scoring:
        0.0  – file missing / unreadable or bookmark absent
        +0.6 – bookmark with correct name exists in document
        +0.2 – bookmark is located inside paragraph 6 (1-based)
        +0.2 – bookmark appears before any text within that paragraph
    Returns a float between 0.0 and 1.0 inclusive.
    """
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    total_score = 0.0

    # ---------- prerequisite: file must exist ----------
    if not os.path.exists(file_path):
        print("✗ File not found:", file_path)
        print("REWARD: 0.0")
        return 0.0  # cannot continue

    # ---------- load document.xml from the DOCX package ----------
    try:
        with zipfile.ZipFile(file_path) as z:
            doc_xml = z.read("word/document.xml")
    except Exception as e:
        print(f"✗ Error reading DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    root = etree.fromstring(doc_xml)
    paragraphs = root.findall(".//w:p", ns)
    print(f"- Total paragraphs detected: {len(paragraphs)}")

    # ---------- requirement 1: bookmark exists ----------
    bm_xpath = ".//w:bookmarkStart[@w:name='main-result']"
    bm_elem = root.find(bm_xpath, ns)
    if bm_elem is None:
        print("✗ Bookmark 'main-result' not found")
        print(f"REWARD: {total_score}")
        return total_score  # 0.0 – nothing else to award

    print("✓ Bookmark 'main-result' found (0.6)")
    total_score += 0.6

    # ---------- locate the paragraph containing the bookmark ----------
    # ascend through parents until we reach the <w:p> element
    paragraph_elem = bm_elem.getparent()
    while paragraph_elem is not None and paragraph_elem.tag != "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p":
        paragraph_elem = paragraph_elem.getparent()

    if paragraph_elem is None:
        print("✗ Bookmark not inside a paragraph – cannot verify placement")
        print(f"REWARD: {total_score}")
        return total_score

    # Determine the paragraph index (0-based in list, but we need 6th = index 5)
    try:
        paragraph_index = paragraphs.index(paragraph_elem)
    except ValueError:
        paragraph_index = -1  # should not happen, but stay safe

    if paragraph_index == 5:
        print("✓ Bookmark is in paragraph 6 (0.2)")
        total_score += 0.2
    else:
        print(f"✗ Bookmark is in paragraph {paragraph_index + 1}, expected 6")

    # ---------- verify bookmark appears before any text in that paragraph ----------
    nodes_in_paragraph = list(paragraph_elem.iter())
    try:
        bm_node_index = nodes_in_paragraph.index(bm_elem)
    except ValueError:
        bm_node_index = None  # should not happen

    first_text_index = None
    for i, node in enumerate(nodes_in_paragraph):
        if node.tag == "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}t" and (node.text or "").strip():
            first_text_index = i
            break

    # Bookmark must appear strictly before first text (or there is no text)
    if bm_node_index is not None and (first_text_index is None or bm_node_index < first_text_index):
        print("✓ Bookmark precedes all text in paragraph (0.2)")
        total_score += 0.2
    else:
        print("✗ Bookmark does not appear at the very start of the paragraph")

    # ---------- finalise ----------
    total_score = round(min(total_score, 1.0), 2)
    print("Final score:", total_score)
    print("REWARD:", total_score)
    return total_score


if __name__ == "__main__":
    # Path to the document provided in the task context
    FILE_PATH = "/home/user/ive_got_a_10_page_writer_doc_and_i_need_to_be_able_to_jump_straight_to_the_conclusions_section_later.docx"
    verify_writer_bookmark(FILE_PATH)
