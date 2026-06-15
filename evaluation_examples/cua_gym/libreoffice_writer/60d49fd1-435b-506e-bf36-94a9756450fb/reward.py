"""
Reward Script: Insert page break before Appendix section and restart page numbering from 1
Task ID: wrpara_020
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Document has 2+ sections (section break inserted)
  Component 2 (0.35): Second section has page numbering restart at 1
  Component 3 (0.30): Appendix heading is in the second section (after break)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'wrpara_020'


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            import time
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print("PERSIST: ctrl+s sent for " + domain)
        except Exception as e:
            print("PERSIST_WARN: save hook failed: " + str(e))


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file " + file_path + ": " + str(e))
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Document has 2+ sections (section break inserted) (0.35 points)
    # In the initial file, there is only 1 section. The golden has 2.
    try:
        num_sections = len(doc.sections)
        if num_sections >= 2:
            print("PASS: Component 1 -- Document has " + str(num_sections) + " sections (section break exists) (0.35 pts)")
            total_score += 0.35
        else:
            print("FAIL: Component 1 -- Expected 2+ sections, found " + str(num_sections))
    except Exception as e:
        print("ERROR: Component 1 -- " + str(e))

    # Component 2: Second section has page numbering restart at 1 (0.35 points)
    # The task requires page numbering to restart from 1 on the appendix page.
    # This is achieved via w:pgNumType with w:start="1" on the second section.
    try:
        if len(doc.sections) >= 2:
            second_section = doc.sections[1]
            sectPr = second_section._sectPr
            pgNumType = sectPr.find(qn('w:pgNumType'))
            if pgNumType is not None:
                start_val = pgNumType.get(qn('w:start'))
                if start_val == '1':
                    print("PASS: Component 2 -- Second section has pgNumType start=1 (0.35 pts)")
                    total_score += 0.35
                else:
                    print("FAIL: Component 2 -- pgNumType start=" + str(start_val) + ", expected '1'")
            else:
                print("FAIL: Component 2 -- No pgNumType element in second section")
        else:
            print("FAIL: Component 2 -- Cannot check page numbering without 2+ sections")
    except Exception as e:
        print("ERROR: Component 2 -- " + str(e))

    # Component 3: Appendix heading is in the second section (after the break) (0.30 points)
    # We verify that the 'Appendix' Heading 1 paragraph appears AFTER the section break.
    # In the golden file, the section break is stored as a sectPr inside a paragraph's pPr.
    # The Appendix heading should come after that paragraph.
    try:
        # Find the paragraph index where the section break (in pPr) occurs
        section_break_para_idx = None
        appendix_para_idx = None
        for i, para in enumerate(doc.paragraphs):
            # Check for sectPr in paragraph properties (inline section break)
            pPr = para._element.find(qn('w:pPr'))
            if pPr is not None:
                sect_in_pPr = pPr.find(qn('w:sectPr'))
                if sect_in_pPr is not None:
                    section_break_para_idx = i

            # Find the Appendix heading
            if para.style and para.style.name == 'Heading 1' and 'Appendix' in para.text:
                appendix_para_idx = i

        if section_break_para_idx is not None and appendix_para_idx is not None:
            if appendix_para_idx > section_break_para_idx:
                print("PASS: Component 3 -- Appendix heading (para " + str(appendix_para_idx) +
                      ") is after section break (para " + str(section_break_para_idx) + ") (0.30 pts)")
                total_score += 0.30
            else:
                print("FAIL: Component 3 -- Appendix heading (para " + str(appendix_para_idx) +
                      ") is NOT after section break (para " + str(section_break_para_idx) + ")")
        elif section_break_para_idx is None:
            print("FAIL: Component 3 -- No section break found in paragraph properties")
        else:
            print("FAIL: Component 3 -- No 'Appendix' Heading 1 paragraph found")
    except Exception as e:
        print("ERROR: Component 3 -- " + str(e))

    final_score = round(min(total_score, 1.0), 2)
    print("")
    print("Score: " + str(total_score) + "/1.0")
    print("REWARD: " + str(final_score))
    return final_score


# Persist app state before verification
persist_app_state("libreoffice_writer")

# Test against canonical artifact path
file_path = WORKDIR + '/' + TASK_ID + '.docx'
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
