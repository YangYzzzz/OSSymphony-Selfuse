"""
Reward Script: Add page numbers to the bottom center of every page
Task ID: writer_tech_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Footer contains a PAGE field code
  Component 2 (0.3): Footer paragraph is center-aligned
  Component 3 (0.2): All sections have PAGE field in footer (covers multi-section docs)
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_004'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def _footer_has_page_field(footer_elem, ns, qn_func):
    """Check if a footer element contains a PAGE field code (begin + instrText PAGE + end)."""
    fld_chars = footer_elem.findall('.//w:fldChar', ns)
    has_begin = any(
        fc.get(qn_func('w:fldCharType')) == 'begin' for fc in fld_chars
    )
    has_end = any(
        fc.get(qn_func('w:fldCharType')) == 'end' for fc in fld_chars
    )
    instr_texts = footer_elem.findall('.//w:instrText', ns)
    has_page_instr = any(
        it.text and 'PAGE' in it.text.upper() for it in instr_texts
    )
    return has_begin and has_end and has_page_instr


def _footer_page_para_is_centered(footer_elem, ns, qn_func):
    """Check if the footer paragraph containing the PAGE field is center-aligned."""
    for p_elem in footer_elem.findall('.//w:p', ns):
        # Check if this paragraph has the PAGE field
        para_instrs = p_elem.findall('.//w:instrText', ns)
        para_has_page = any(
            it.text and 'PAGE' in it.text.upper() for it in para_instrs
        )
        if para_has_page:
            pPr = p_elem.find('w:pPr', ns)
            if pPr is not None:
                jc = pPr.find('w:jc', ns)
                if jc is not None and jc.get(qn_func('w:val')) == 'center':
                    return True
    return False


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from docx.oxml.ns import qn
    except ImportError as e:
        print(f"CRITICAL: Cannot import python-docx: {e}")
        print("REWARD: 0.0")
        return 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    num_sections = len(doc.sections)
    print(f"INFO: Document has {num_sections} section(s)")

    # Component 1: Footer contains a PAGE field code (0.5 points)
    # The PAGE field is represented as: fldChar(begin) + instrText(" PAGE ") + fldChar(end)
    # This is the core task requirement -- adding page numbers to the footer.
    try:
        section = doc.sections[0]
        footer = section.footer
        if _footer_has_page_field(footer._element, ns, qn):
            print(f"PASS: Component 1 -- Footer contains PAGE field code (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 -- Footer missing PAGE field code")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Footer paragraph is center-aligned (0.3 points)
    # Task says "bottom center" so footer text must be centered.
    try:
        section = doc.sections[0]
        footer = section.footer
        if _footer_page_para_is_centered(footer._element, ns, qn):
            print(f"PASS: Component 2 -- Footer PAGE field paragraph is center-aligned (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 -- Footer PAGE field paragraph is not center-aligned")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All sections have PAGE field in footer (0.2 points)
    # If the document has multiple sections, page numbers should appear on all pages.
    try:
        sections_with_page = 0

        for i, section in enumerate(doc.sections):
            footer = section.footer

            # A section can inherit footer from previous via is_linked_to_previous
            if section.footer.is_linked_to_previous and i > 0:
                sections_with_page += 1
                continue

            # Check for PAGE field in this section's footer
            if _footer_has_page_field(footer._element, ns, qn):
                sections_with_page += 1
            else:
                print(f"  Section {i}: No PAGE field in footer")

        if sections_with_page == num_sections:
            print(f"PASS: Component 3 -- All {num_sections} section(s) have PAGE field in footer (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 -- Only {sections_with_page}/{num_sections} sections have PAGE field")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
