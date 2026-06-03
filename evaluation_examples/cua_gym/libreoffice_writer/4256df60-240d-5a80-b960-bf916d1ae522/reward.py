"""
Reward Script: Add page numbers in footer with 'Page X of Y' format, centered
Task ID: writer_tm_053
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Footer contains PAGE field code
  Component 2 (0.3): Footer contains NUMPAGES field code
  Component 3 (0.2): Footer text matches 'Page X of Y' pattern
  Component 4 (0.2): Footer paragraph is center-aligned
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_053'


def persist_app_state(domain):
    """Save any unsaved LibreOffice edits before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
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
        from docx import Document
        doc = Document(file_path)
    except Exception as e:
        print("CRITICAL: Cannot load file {}: {}".format(file_path, e))
        print("REWARD: 0.0")
        return 0.0

    # Precondition: document must have at least one section
    if len(doc.sections) == 0:
        print("CRITICAL: Document has no sections")
        print("REWARD: 0.0")
        return 0.0

    section = doc.sections[0]
    footer = section.footer
    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}

    # We look at all footer paragraphs but typically the field is in the first one
    footer_paras = footer.paragraphs
    if not footer_paras:
        print("FAIL: No footer paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    # Find the paragraph that contains field codes (could be any paragraph in footer)
    target_para = None
    for para in footer_paras:
        instr_texts = para._element.findall('.//w:instrText', ns)
        if len(instr_texts) > 0:
            target_para = para
            break

    # Component 1: Footer contains PAGE field code (0.3 points)
    # This checks that a PAGE field is present - only true in golden, not initial
    try:
        has_page_field = False
        if target_para is not None:
            instr_texts = target_para._element.findall('.//w:instrText', ns)
            for it in instr_texts:
                if it.text and 'PAGE' in it.text.upper() and 'NUMPAGES' not in it.text.upper():
                    has_page_field = True
                    break
        if has_page_field:
            print("PASS: Component 1 - PAGE field code found in footer (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 1 - No PAGE field code found in footer")
    except Exception as e:
        print("ERROR: Component 1 - {}".format(e))

    # Component 2: Footer contains NUMPAGES field code (0.3 points)
    # This checks that a NUMPAGES field is present - only true in golden, not initial
    try:
        has_numpages_field = False
        if target_para is not None:
            instr_texts = target_para._element.findall('.//w:instrText', ns)
            for it in instr_texts:
                if it.text and 'NUMPAGES' in it.text.upper():
                    has_numpages_field = True
                    break
        if has_numpages_field:
            print("PASS: Component 2 - NUMPAGES field code found in footer (0.3 pts)")
            total_score += 0.3
        else:
            print("FAIL: Component 2 - No NUMPAGES field code found in footer")
    except Exception as e:
        print("ERROR: Component 2 - {}".format(e))

    # Component 3: Footer text matches 'Page X of Y' pattern (0.2 points)
    # The cached/rendered text should follow the pattern "Page <num> of <num>"
    try:
        footer_text = ''
        for para in footer_paras:
            footer_text += para.text
        # Match pattern: "Page" followed by number, "of", number
        pattern = r'[Pp]age\s+\d+\s+of\s+\d+'
        if re.search(pattern, footer_text):
            print("PASS: Component 3 - Footer text matches 'Page X of Y' pattern: '{}'  (0.2 pts)".format(footer_text.strip()))
            total_score += 0.2
        else:
            print("FAIL: Component 3 - Footer text '{}' does not match 'Page X of Y' pattern".format(footer_text.strip()))
    except Exception as e:
        print("ERROR: Component 3 - {}".format(e))

    # Component 4: Footer paragraph is center-aligned (0.2 points)
    # Initial has no alignment (None), golden has CENTER
    try:
        from docx.enum.text import WD_PARAGRAPH_ALIGNMENT
        # Check alignment on the paragraph that contains the fields, or first paragraph
        check_para = target_para if target_para is not None else footer_paras[0]
        alignment = check_para.paragraph_format.alignment
        if alignment == WD_PARAGRAPH_ALIGNMENT.CENTER:
            print("PASS: Component 4 - Footer paragraph is center-aligned (0.2 pts)")
            total_score += 0.2
        else:
            print("FAIL: Component 4 - Footer alignment is '{}', expected CENTER".format(alignment))
    except Exception as e:
        print("ERROR: Component 4 - {}".format(e))

    final_score = min(total_score, 1.0)
    print("")
    print("Score: {}/1.0".format(total_score))
    print("REWARD: {}".format(final_score))
    return final_score


# Entry point
persist_app_state("libreoffice_writer")

file_path = '{}/{}.docx'.format(WORKDIR, TASK_ID)
if not os.path.exists(file_path):
    print("File not found: " + file_path)
    print("REWARD: 0.0")
else:
    verify_task(file_path)
