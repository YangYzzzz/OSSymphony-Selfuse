"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer, I’m trying to drop a cross-reference into paragraph 6 that pulls in the exact text stored under the bookmark named “ref-01”. I keep ending up with the wrong format. Could you walk me through the clicks to insert that reference so the actual bookmarked wording shows up?
Generated: 2025-09-10 20:17:15
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from lxml import etree


def verify_cross_reference(file_path: str, bookmark_name: str = "ref-01", target_paragraph_idx: int = 5) -> float:
    """Reward-script verification for the LibreOffice Writer task.

    The task: Insert a cross-reference into *paragraph&nbsp;6* that shows the *exact text* stored in the
    bookmark named ``ref-01``.

    Scoring (progressive):
        • 0.4 pts – A REF field that targets the bookmark exists
        • 0.2 pts – That field is located in paragraph 6 (index 5, zero-based)
        • 0.4 pts – The paragraph actually displays the exact bookmarked wording

    Returns a float between 0.0 and 1.0.
    """

    score = 0.0
    max_score = 1.0

    print(f"Checking file: {file_path}\nBookmark to verify: {bookmark_name}\n")

    # ---------- 1. Prerequisite: file + XML load (no points) ----------
    if not os.path.exists(file_path):
        print("✗ File not found")
        return 0.0

    try:
        with zipfile.ZipFile(file_path) as z:
            if "word/document.xml" not in z.namelist():
                print("✗ document.xml not present in DOCX")
                return 0.0
            document_xml = z.read("word/document.xml")
    except Exception as exc:
        print(f"✗ Cannot open DOCX: {exc}")
        return 0.0

    try:
        root = etree.fromstring(document_xml)
    except Exception as exc:
        print(f"✗ Failed to parse document.xml: {exc}")
        return 0.0

    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # ---------- 2. Extract text inside the bookmark ----------
    bookmark_text = None
    for b_start in root.xpath(f"//w:bookmarkStart[@w:name='{bookmark_name}']", namespaces=ns):
        b_id = b_start.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id")
        texts = []
        n = b_start.getnext()
        while n is not None and not (
            n.tag.endswith("bookmarkEnd") and n.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id") == b_id
        ):
            texts.extend(n.xpath(".//w:t/text()", namespaces=ns))
            n = n.getnext()
        bookmark_text = "".join(texts).strip()
        break  # first occurrence is enough

    if bookmark_text is None:
        print("✗ Bookmark not found in document")
        return 0.0

    print(f"✓ Bookmark text captured: '{bookmark_text}'\n")

    # ---------- 3. Locate REF fields that point to that bookmark ----------
    ref_nodes = []

    # Simple fields <w:fldSimple w:instr="REF ref-01"> …
    for fld in root.xpath("//w:fldSimple", namespaces=ns):
        instr = fld.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}instr") or ""
        if bookmark_name.lower() in instr.lower() and "ref" in instr.lower():
            ref_nodes.append(fld)

    # Complex fields with <w:instrText> parts
    for instr in root.xpath("//w:instrText", namespaces=ns):
        if instr.text and bookmark_name.lower() in instr.text.lower() and "ref" in instr.text.lower():
            ref_nodes.append(instr)

    if not ref_nodes:
        print("✗ No cross-reference (REF) field targeting the bookmark found")
    else:
        print(f"✓ Found {len(ref_nodes)} cross-reference field(s) targeting the bookmark")
        score += 0.4  # Field exists

    # ---------- 4. If a field exists, validate its placement & displayed text ----------
    if ref_nodes:
        field_node = ref_nodes[0]
        # ascend to the paragraph element
        p_node = field_node
        while p_node is not None and p_node.tag != "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}p":
            p_node = p_node.getparent()

        if p_node is not None:
            # Determine paragraph index (0-based) inside body
            paragraphs = root.xpath(".//w:body/w:p", namespaces=ns)
            para_idx = paragraphs.index(p_node) if p_node in paragraphs else -1
            print(f"Field resides in paragraph index: {para_idx}")

            if para_idx == target_paragraph_idx:
                print("✓ Field is correctly placed in paragraph 6")
                score += 0.2
            else:
                print("✗ Field is NOT in paragraph 6 (idx 5)")

            # Extract visible text of that paragraph
            para_text = "".join(p_node.xpath(".//w:t/text()", namespaces=ns)).strip()
            print(f"Paragraph visible text: '{para_text}'")

            if bookmark_text in para_text:
                print("✓ Paragraph displays the exact bookmarked wording")
                score += 0.4
            else:
                print("✗ Paragraph does not display the bookmarked wording")
        else:
            print("✗ Unable to find the paragraph containing the field")

    final_score = min(score, max_score)
    print(f"\nTotal verification score: {final_score}")
    return final_score


if __name__ == "__main__":
    DOC_PATH = "/home/user/in_libreoffice_writer_im_trying_to_drop_a_cross_reference_into_paragraph_6_that_pulls_in_the_exact_t.docx"
    reward = verify_cross_reference(DOC_PATH)
    print(f"REWARD: {reward}")

