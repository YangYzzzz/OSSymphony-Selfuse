"""
FINAL REWARD SCRIPT - SUCCESS
Task: The page numbers keep shifting as I edit. In paragraph 9 of my document, I want to insert a live reference that shows the current page number of the bookmark named "main-result." How can I set up that cross-reference in LibreOffice Writer so it updates automatically?
Generated: 2025-09-10 18:23:49
Status: success
Model: azure-o3
Total Steps: 4
"""

import os
import zipfile
from lxml import etree


def verify_libreoffice_writer_cross_reference(file_path: str) -> float:
    """Reward-script verifier for the LibreOffice Writer task.

    Task to verify:
      1. A bookmark named **main-result** exists and has a matching end tag.
      2. There is a *live* PAGEREF field that references that bookmark.
      3. That field is located in **paragraph 9** of the document (1-based).

    Scoring (progressive):
      • 0.40 – valid bookmark with matching end tag
      • 0.40 – PAGEREF field referencing that bookmark exists
      • 0.20 – that PAGEREF field is in paragraph 9
      -> Maximum 1.0
    """

    max_score = 1.0
    score = 0.0
    print(f"Verifying Writer task in file: {file_path}\n")

    # -------------------------------------------------------------
    # 0. Prerequisite check – file must exist (no points awarded)
    # -------------------------------------------------------------
    if not os.path.exists(file_path):
        print("✗ File does not exist")
        print("REWARD: 0.0")
        return 0.0

    # -------------------------------------------------------------
    # 1. Load DOCX and extract main XML
    # -------------------------------------------------------------
    try:
        with zipfile.ZipFile(file_path, "r") as zf:
            if "word/document.xml" not in zf.namelist():
                print("✗ Main document.xml not present – invalid DOCX")
                print("REWARD: 0.0")
                return 0.0
            document_xml = zf.read("word/document.xml")
    except Exception as e:
        print(f"✗ Error loading DOCX: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Parse XML
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
    root = etree.fromstring(document_xml)

    # -------------------------------------------------------------
    # 2. Check bookmark named 'main-result' with matching end tag
    # -------------------------------------------------------------
    bookmark_valid = False
    bookmark_starts = root.xpath("//w:bookmarkStart[@w:name='main-result']", namespaces=ns)
    for bm_start in bookmark_starts:
        bm_id = bm_start.get("{http://schemas.openxmlformats.org/wordprocessingml/2006/main}id")
        end_xpath = f"//w:bookmarkEnd[@w:id='{bm_id}']"
        if root.xpath(end_xpath, namespaces=ns):
            bookmark_valid = True
            print(f"✓ Found bookmark 'main-result' with matching end (id={bm_id})")
            break
    if bookmark_valid:
        score += 0.4
    else:
        print("✗ Bookmark 'main-result' not found or lacks matching end tag")

    # -------------------------------------------------------------
    # 3. Check PAGEREF field that references the bookmark
    # -------------------------------------------------------------
    pageref_found = False
    pageref_paragraph_idx = None  # 0-based index
    instr_nodes = root.xpath("//w:instrText", namespaces=ns)
    all_paragraphs = root.xpath("//w:p", namespaces=ns)
    w_p_tag = "{" + ns["w"] + "}p"

    for instr in instr_nodes:
        raw_text = instr.text or ""
        norm_text = " ".join(raw_text.strip().lower().split())  # normalize spaces/case
        if norm_text.startswith("pageref") and "main-result" in norm_text:
            pageref_found = True
            # Ascend to containing <w:p>
            anc = instr
            while anc is not None and anc.tag != w_p_tag:
                anc = anc.getparent()
            if anc is not None:
                try:
                    pageref_paragraph_idx = all_paragraphs.index(anc)
                except ValueError:
                    pass
            break

    if pageref_found:
        print("✓ Found PAGEREF field referencing 'main-result'")
        score += 0.4
    else:
        print("✗ No PAGEREF field referencing 'main-result' found")

    # -------------------------------------------------------------
    # 4. Check placement in paragraph 9 (1-based => index 8)
    # -------------------------------------------------------------
    if pageref_found and pageref_paragraph_idx is not None:
        print(f"Field located in paragraph {pageref_paragraph_idx + 1} (1-based index)")
        if pageref_paragraph_idx == 8:  # paragraph 9
            print("✓ Field correctly placed in paragraph 9")
            score += 0.2
        else:
            print("✗ Field not located in paragraph 9 – no extra credit")
    elif pageref_found:
        print("⚠ Unable to determine the paragraph index for the PAGEREF field")

    # -------------------------------------------------------------
    # 5. Final score & output
    # -------------------------------------------------------------
    final_score = min(score, max_score)
    print(f"Total score: {final_score}/{max_score}")
    print(f"REWARD: {final_score}")
    return final_score


# ----------------- MAIN EXECUTION (for the grader) -----------------
if __name__ == "__main__":
    # Path where the task file is expected to be
    task_file = "/home/user/the_page_numbers_keep_shifting_as_i_edit_in_paragraph_9_of_my_document_i_want_to_insert_a_live_refer.docx"
    verify_libreoffice_writer_cross_reference(task_file)

