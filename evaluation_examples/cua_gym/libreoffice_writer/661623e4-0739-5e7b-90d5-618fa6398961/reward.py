"""
Reward Script: Insert document title as a field in the header from document properties
Task ID: writer_tm_054
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): Header contains a DOCPROPERTY "Title" field code
  Component 2 (0.4): Header displays the correct title text "Cloud Migration Proposal"
  Component 3 (0.2): The displayed field value matches the document's core Title property
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_054'

NSMAP = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Get the document title from core properties (precondition reference)
    try:
        doc_title = doc.core_properties.title
        print(f"INFO: Document Title property = {doc_title!r}")
    except Exception as e:
        print(f"WARN: Cannot read doc title property: {e}")
        doc_title = None

    # Get header from first section
    try:
        section = doc.sections[0]
        header = section.header
        header_paras = header.paragraphs
    except Exception as e:
        print(f"CRITICAL: Cannot access header: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Collect all instrText content from the header XML
    docproperty_title_count = 0  # count of DOCPROPERTY Title field codes found
    field_display_text = ""

    try:
        # Parse the header XML to find field codes
        for para in header_paras:
            para_xml = para._element
            # Find all instrText elements
            instr_texts = para_xml.findall('.//w:instrText', NSMAP)
            for instr in instr_texts:
                instr_content = (instr.text or '').strip()
                print(f"INFO: Found instrText: {instr_content!r}")
                # Check for DOCPROPERTY "Title" or DOCPROPERTY Title
                if 'DOCPROPERTY' in instr_content.upper() and 'TITLE' in instr_content.upper():
                    docproperty_title_count += 1

            # Extract display text from the field (text between separate and end fldChar)
            # Walk through runs to find text between separate and end
            runs = para_xml.findall('.//w:r', NSMAP)
            field_result_depth = 0  # 0=outside, >0=inside field result
            for run in runs:
                fld_chars = run.findall('w:fldChar', NSMAP)
                for fc in fld_chars:
                    fld_type = fc.get('{http://schemas.openxmlformats.org/wordprocessingml/2006/main}fldCharType')
                    if fld_type == 'separate':
                        field_result_depth += 1
                    elif fld_type == 'end':
                        field_result_depth = max(0, field_result_depth - 1)
                if field_result_depth > 0:
                    t_elems = run.findall('w:t', NSMAP)
                    for t in t_elems:
                        if t.text:
                            field_display_text += t.text
    except Exception as e:
        print(f"ERROR: XML parsing failed: {e}")

    # Also get full header text via python-docx API
    header_full_text = ""
    for para in header_paras:
        header_full_text += para.text
    print(f"INFO: Header full text = {header_full_text!r}")
    print(f"INFO: Field display text = {field_display_text!r}")
    has_docproperty_title_field = docproperty_title_count > 0  # derived from XML scan
    print(f"INFO: Has DOCPROPERTY Title field = {has_docproperty_title_field} (count={docproperty_title_count})")

    # Component 1: Header contains a DOCPROPERTY "Title" field code (0.4 points)
    # This is the core requirement — a document property field, not just static text
    try:
        if has_docproperty_title_field:
            print(f"PASS: Component 1 — DOCPROPERTY Title field found in header (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 — No DOCPROPERTY Title field code found in header")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Header displays the correct title text (0.4 points)
    # The header text should contain "Cloud Migration Proposal"
    try:
        expected_title = "Cloud Migration Proposal"
        if expected_title.lower() in header_full_text.lower():
            print(f"PASS: Component 2 — Header displays '{expected_title}' (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 2 — Header text is {header_full_text!r}, expected to contain '{expected_title}'")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The field display value matches the document Title property (0.2 points)
    # This verifies the field is actually pulling from document properties
    try:
        if doc_title and field_display_text:
            if doc_title.strip().lower() == field_display_text.strip().lower():
                print(f"PASS: Component 3 — Field display '{field_display_text}' matches doc Title property '{doc_title}' (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Field display '{field_display_text}' != doc Title '{doc_title}'")
        elif doc_title and header_full_text and has_docproperty_title_field:
            # Fallback: if field display extraction didn't work but we have DOCPROPERTY field
            if doc_title.strip().lower() in header_full_text.strip().lower():
                print(f"PASS: Component 3 — Header text matches doc Title property (0.2 pts)")
                total_score += 0.2
            else:
                print(f"FAIL: Component 3 — Header text doesn't match doc Title property")
        else:
            print(f"FAIL: Component 3 — Missing doc title ({doc_title!r}) or field display text ({field_display_text!r})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice changes
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
