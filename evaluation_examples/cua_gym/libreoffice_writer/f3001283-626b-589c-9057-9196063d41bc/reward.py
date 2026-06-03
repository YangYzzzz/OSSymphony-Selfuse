"""
FINAL REWARD SCRIPT - SUCCESS
Task: In LibreOffice Writer 7.5, my cover page keeps bleeding into the next section whenever I edit the document. How can I insert a solid manual page break right after page 1 so the main text always begins on page 2, no matter what I add later?
Generated: 2025-09-10 13:14:29
Status: success
Model: azure-o3
Total Steps: 3
"""

import os
import zipfile
from lxml import etree


def verify_manual_page_break(file_path: str) -> float:
    """Verify that the DOCX/ODT document contains a **solid** (manual *or* section)
    page break right after the cover-page content so that main text always starts
    on a new page.

    Scoring (progressive):
    • 0.7  – A manual (w:br w:type="page") *or* section (w:sectPr w:type="nextPage")
              break is detected in the document XML.
    • 0.3  – That first page-break appears early (≤ 10th paragraph), implying it
              separates the cover from the body rather than somewhere deep in
              the document.
    The score is capped at 1.0 and printed as   REWARD: <score>   as required.
    """
    score = 0.0
    max_score = 1.0

    # Namespace used in DOCX XML
    ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}

    # --------------------------- Safety checks ----------------------------
    if not os.path.exists(file_path):
        print("✗ Document not found:", file_path)
        return 0.0  # No points if the file itself is missing

    try:
        with zipfile.ZipFile(file_path) as docx_zip:
            # A DOCX is a ZIP: the main document part is word/document.xml
            if "word/document.xml" not in docx_zip.namelist():
                print("✗ document.xml part missing – cannot analyse content")
                return 0.0

            xml_bytes = docx_zip.read("word/document.xml")
            root = etree.fromstring(xml_bytes)

            # The <w:body> element contains the flow of paragraphs/tables/etc.
            body = root.find(".//w:body", ns)
            if body is None:
                print("✗ <w:body> element not found – malformed DOCX")
                return 0.0

            # Iterate through direct children of <w:body> in order to detect the
            # first page-breaking construct.
            para_index = -1  # counts paragraphs only (tables don't increment)
            first_break_para_idx = None
            first_break_type = None  # "manual" or "section"

            for elem in body:
                # Count paragraphs for positional context
                if elem.tag.endswith("}p"):
                    para_index += 1
                    # Manual/explicit page break inside a paragraph
                    has_manual_break = bool(
                        elem.xpath('.//w:br[@w:type="page"]', namespaces=ns)
                    )
                    if has_manual_break:
                        first_break_para_idx = para_index
                        first_break_type = "manual"
                        break

                # Section break element (changes page/section properties)
                if elem.tag.endswith('}sectPr'):
                    # A section with w:type nextPage forces a new page
                    type_el = elem.find('.//w:type', ns)
                    if type_el is not None and type_el.get(f'{{{ns["w"]}}}val') == 'nextPage':
                        # Section break takes effect *after* the previous paragraph
                        first_break_para_idx = para_index + 1
                        first_break_type = "section"
                        break

            # --------------------- Scoring logic ---------------------------
            if first_break_para_idx is None:
                print("✗ No manual or section page break found – cover may bleed")
                return 0.0  # No page-break ⇒ task failed

            # Page-break exists → award base points
            print(f"✓ Found {first_break_type} page break at paragraph index {first_break_para_idx}")
            score += 0.7

            # Bonus if the break is early (within first 10 paragraphs) – strongly
            # suggests it separates the cover (usually short) from the main body.
            if first_break_para_idx <= 10:
                print("✓ Page break occurs early (within first 10 paragraphs)")
                score += 0.3
            else:
                print("✗ Page break occurs late (> 10 paragraphs) – could still work but not ideal")

            final_score = min(score, max_score)
            return final_score
    except Exception as exc:
        print("✗ Error while verifying document:", exc)
        return 0.0  # Any parsing error ⇒ 0 (cannot confidently verify)


if __name__ == "__main__":
    # Path provided by the task context
    DOC_PATH = "/home/user/in_libreoffice_writer_75_my_cover_page_keeps_bleeding_into_the_next_section_whenever_i_edit_the_docu.docx"

    reward_value = verify_manual_page_break(DOC_PATH)
    print(f"REWARD: {reward_value}")

