"""
Reward Script: Cross-reference in indemnification clause
Task ID: writer_legal_022
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Placeholder '[see definitions]' removed from Section 8
  Component 2 (0.35): Cross-reference field (REF) referencing 'definitions_section' bookmark exists
  Component 3 (0.30): Cross-reference displays 'Section 1.5' text
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_legal_022'
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def persist_app_state(domain):
    """Save any unsaved LibreOffice changes."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def find_section8_paragraph(doc):
    """Find the first paragraph in Section 8 containing the indemnification text."""
    in_section8 = False
    for i, para in enumerate(doc.paragraphs):
        if 'Section 8' in para.text and ('Indemnification' in para.text or para.style.name.startswith('Heading')):
            in_section8 = True
            continue
        if in_section8 and para.style.name.startswith('Heading') and 'Section 8' not in para.text:
            break  # moved past Section 8
        if in_section8 and 'indemnify' in para.text.lower() and 'losses' in para.text.lower():
            return i, para
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    idx, target_para = find_section8_paragraph(doc)
    if target_para is None:
        print("CRITICAL: Could not find indemnification paragraph in Section 8")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found target paragraph at index {idx}")
    para_text = target_para.text

    # Component 1: Placeholder '[see definitions]' is removed (0.35 points)
    # In initial_env, text contains '[see definitions]'. In golden, it should be gone.
    try:
        if '[see definitions]' not in para_text:
            print(f"PASS: Component 1 -- Placeholder '[see definitions]' not found in text (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 1 -- Placeholder '[see definitions]' still present in text")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Cross-reference field (REF) referencing 'definitions_section' bookmark (0.35 points)
    # Check the paragraph XML for w:fldChar and w:instrText containing REF definitions_section
    try:
        para_xml = target_para._element
        fld_chars = para_xml.findall(f'.//{{{W_NS}}}fldChar')
        instr_texts = para_xml.findall(f'.//{{{W_NS}}}instrText')

        has_field = len(fld_chars) >= 2  # need at least begin and end
        has_ref_bookmark = False
        for instr in instr_texts:
            if instr.text and 'REF' in instr.text and 'definitions_section' in instr.text:
                has_ref_bookmark = True
                break

        if has_field and has_ref_bookmark:
            print(f"PASS: Component 2 -- Cross-reference field REF definitions_section found (0.35 pts)")
            total_score += 0.35
        else:
            print(f"FAIL: Component 2 -- No cross-reference field found (fldChars={len(fld_chars)}, ref_bookmark={has_ref_bookmark})")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Cross-reference displays 'Section 1.5' (0.30 points)
    # The cached/display text between fldChar separate and end should be 'Section 1.5'
    try:
        # Look for the display text of the field: text between 'separate' and 'end' fldChar
        runs = list(para_xml.findall(f'.//{{{W_NS}}}r'))
        in_field_result = False
        display_text = ''
        for run_elem in runs:
            fld = run_elem.find(f'{{{W_NS}}}fldChar')
            if fld is not None:
                fld_type = fld.get(f'{{{W_NS}}}fldCharType')
                if fld_type == 'separate':
                    in_field_result = True
                    continue
                elif fld_type == 'end':
                    in_field_result = False
                    continue
            if in_field_result:
                t_elem = run_elem.find(f'{{{W_NS}}}t')
                if t_elem is not None and t_elem.text:
                    display_text += t_elem.text

        # Also check the full paragraph text for 'Section 1.5'
        has_section_15_in_text = 'Section 1.5' in para_text
        has_section_15_in_field = 'Section 1.5' in display_text

        if has_section_15_in_field:
            print(f"PASS: Component 3 -- Field display text is '{display_text}' containing 'Section 1.5' (0.30 pts)")
            total_score += 0.30
        elif has_section_15_in_text:
            # Text says 'Section 1.5' but not necessarily in a field display
            # Give partial credit - the text is correct even if field structure isn't perfect
            print(f"PASS: Component 3 -- Paragraph text contains 'Section 1.5' (0.30 pts)")
            total_score += 0.30
        else:
            print(f"FAIL: Component 3 -- Expected 'Section 1.5' in field display, found: '{display_text}', para text snippet: '{para_text[150:200]}'")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
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
