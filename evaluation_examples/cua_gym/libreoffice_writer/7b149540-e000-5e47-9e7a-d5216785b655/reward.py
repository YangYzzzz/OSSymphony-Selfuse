"""
FINAL REWARD SCRIPT - SUCCESS
Task: I’ve wrapped up my report but just remembered the appendix is missing. In LibreOffice Writer, how do I jump to the very end, insert a manual page break, and then add the heading “Appendix A” formatted with the built-in Heading 1 style so it starts on its own page?
Generated: 2025-09-10 19:13:44
Status: success
Model: azure-o3
Total Steps: 5
"""

import os
import zipfile
from docx import Document
from lxml import etree


def verify_appendix_task(file_path: str) -> float:
    """Verify LibreOffice Writer task:
    1. Document ends with a manual page break.
    2. Heading "Appendix A" exists and is styled with built-in Heading 1.
    3. The page break occurs immediately before that heading so it starts on its own page.

    Returns a progressive score between 0.0 and 1.0.
    """

    print(f"Verifying appendix task for: {file_path}\n")

    # Preconditions (NO POINTS AWARDED FOR THESE!)
    if not os.path.exists(file_path):
        print("✗ File does not exist.")
        return 0.0
    try:
        document = Document(file_path)
    except Exception as exc:
        print(f"✗ Could not load DOCX: {exc}")
        return 0.0

    paragraphs = document.paragraphs

    # ------------------------------------------------------------------
    # Requirement 1: Heading "Appendix A" using built-in Heading 1 style
    # ------------------------------------------------------------------
    heading_index = None
    for idx, para in enumerate(paragraphs):
        if para.text.strip().lower() == "appendix a" and para.style.name.lower() == "heading 1":
            heading_index = idx  # capture the LAST matching instance (should be at the end)

    score = 0.0  # progressive score accumulator
    MAX_SCORE = 1.0

    if heading_index is not None:
        print(f"✓ Found 'Appendix A' with style 'Heading 1' at paragraph index {heading_index} (0.5 points).")
        score += 0.5
    else:
        print("✗ 'Appendix A' with style 'Heading 1' not found.")

    # -------------------------------------------------------------
    # Requirement 2: Manual page break directly before the heading
    # -------------------------------------------------------------
    page_break_ok = False
    if heading_index is not None:
        try:
            # Parse raw XML to inspect <w:br w:type="page"/> elements
            with zipfile.ZipFile(file_path) as z:
                xml_bytes = z.read("word/document.xml")
            root = etree.fromstring(xml_bytes)
            ns = {"w": "http://schemas.openxmlformats.org/wordprocessingml/2006/main"}
            body = root.find("w:body", ns)
            p_elems = [elem for elem in body if elem.tag.endswith('}p')]  # order of paragraphs in XML

            # Map python-docx paragraphs to XML <w:p> elements by matching their text content
            target_xml_index = None
            py_cursor = 0
            for xml_idx, p in enumerate(p_elems):
                xml_text = "".join(t.text for t in p.xpath('.//w:t', namespaces=ns)).strip()
                while py_cursor < len(paragraphs):
                    py_text = paragraphs[py_cursor].text.strip()
                    if py_text == xml_text:
                        if py_cursor == heading_index:
                            target_xml_index = xml_idx
                        py_cursor += 1
                        break
                    py_cursor += 1

            def para_has_page_break(p_elem):
                return bool(p_elem.xpath('.//w:br[@w:type="page"]', namespaces=ns))

            if target_xml_index is not None:
                # Page break may be inside heading paragraph OR previous paragraph
                if para_has_page_break(p_elems[target_xml_index]):
                    page_break_ok = True
                    print("✓ Manual page break found in heading paragraph (0.5 points).")
                elif target_xml_index > 0 and para_has_page_break(p_elems[target_xml_index - 1]):
                    page_break_ok = True
                    print("✓ Manual page break found in paragraph immediately before heading (0.5 points).")
                else:
                    print("✗ No manual page break immediately before heading.")
            else:
                print("✗ Unable to align heading paragraph in XML for page-break analysis.")
        except Exception as exc:
            print(f"✗ XML analysis error: {exc}")

    if page_break_ok:
        score += 0.5

    # -------------------------
    # Final score & reporting
    # -------------------------
    final_score = min(score, MAX_SCORE)
    print(f"\nTotal score: {final_score}/{MAX_SCORE}")
    print(f"REWARD: {final_score}")
    return final_score


if __name__ == "__main__":
    # Path to the document to verify (provided by the task environment)
    DOC_PATH = "/home/user/ive_wrapped_up_my_report_but_just_remembered_the_appendix_is_missing_in_libreoffice_writer_how_do_i_.docx"
    verify_appendix_task(DOC_PATH)

