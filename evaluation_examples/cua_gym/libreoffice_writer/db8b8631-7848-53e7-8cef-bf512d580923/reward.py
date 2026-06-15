"""
Reward Script: Insert cross-reference field to bookmark 'KeyFinding'
Task ID: writer_af_045
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): A REF field exists in the paragraph containing 'As described earlier'
  Component 2 (0.3): The REF field targets the 'KeyFinding' bookmark
  Component 3 (0.3): The field display text matches the bookmarked sentence
"""

import os
import re

WORKDIR = '/home/user'
TASK_ID = 'writer_af_045'

EXPECTED_BOOKMARK_TEXT = 'The primary result shows a 15% improvement in efficiency'


def persist_app_state(domain: str):
    """Save any unsaved GUI state before verification."""
    import time
    os.environ["DISPLAY"] = ":0"
    if domain in {"libreoffice_calc", "libreoffice_writer", "libreoffice_impress"}:
        try:
            import pyautogui
            pyautogui.hotkey("ctrl", "s")
            time.sleep(0.8)
            print(f"PERSIST: ctrl+s sent for {domain}")
        except Exception as e:
            print(f"PERSIST_WARN: save hook failed: {e}")


def verify_task(file_path):
    """
    Verify that a cross-reference field referencing bookmark 'KeyFinding' was inserted
    on the paragraph starting with 'As described earlier:'.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    wns = '{http://schemas.openxmlformats.org/wordprocessingml/2006/main}'

    # Locate the target paragraph containing 'As described earlier'
    target_para = None
    target_idx = None
    for i, para in enumerate(doc.paragraphs):
        if 'As described earlier' in para.text:
            target_para = para
            target_idx = i
            break

    if target_para is None:
        print("FAIL: Could not find paragraph containing 'As described earlier'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found target paragraph at index {target_idx}: '{target_para.text[:100]}...'")

    # Extract field information from the target paragraph XML
    para_elem = target_para._element
    fld_chars = para_elem.findall(f'.//{wns}fldChar')
    instr_texts = para_elem.findall(f'.//{wns}instrText')

    # Component 1: A REF field exists in this paragraph (0.4 points)
    # Check for fldChar begin/end pair and instrText containing REF
    try:
        has_fld_begin = False
        has_fld_end = False
        has_fld_separate = False
        for fc in fld_chars:
            ftype = fc.get(f'{wns}fldCharType')
            if ftype == 'begin':
                has_fld_begin = True
            elif ftype == 'separate':
                has_fld_separate = True
            elif ftype == 'end':
                has_fld_end = True

        has_ref_instr = False
        for it in instr_texts:
            if it.text and 'REF' in it.text.upper():
                has_ref_instr = True

        if has_fld_begin and has_fld_end and has_ref_instr:
            print(f"PASS: Component 1 -- REF field structure found (begin={has_fld_begin}, separate={has_fld_separate}, end={has_fld_end}, REF instr={has_ref_instr}) (0.4 pts)")
            total_score += 0.4
        else:
            print(f"FAIL: Component 1 -- Missing REF field structure (begin={has_fld_begin}, separate={has_fld_separate}, end={has_fld_end}, REF instr={has_ref_instr})")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: The REF field targets 'KeyFinding' bookmark (0.3 points)
    try:
        targets_keyfinding = False
        for it in instr_texts:
            if it.text and 'KEYFINDING' in it.text.upper():
                targets_keyfinding = True
                print(f"INFO: Found instrText: '{it.text.strip()}'")
                break

        if targets_keyfinding:
            print(f"PASS: Component 2 -- REF field targets 'KeyFinding' bookmark (0.3 pts)")
            total_score += 0.3
        else:
            instr_vals = [it.text for it in instr_texts]
            print(f"FAIL: Component 2 -- REF field does not target 'KeyFinding'. instrTexts found: {instr_vals}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The field display text matches the bookmarked sentence (0.3 points)
    # The display text is in a run between fldChar separate and fldChar end
    try:
        # Parse the runs in order to find text between 'separate' and 'end'
        runs = para_elem.findall(f'{wns}r')
        in_field_result = False
        field_display_text = []
        for r in runs:
            fld = r.find(f'{wns}fldChar')
            if fld is not None:
                ftype = fld.get(f'{wns}fldCharType')
                if ftype == 'separate':
                    in_field_result = True
                    continue
                elif ftype == 'end':
                    in_field_result = False
                    continue
            if in_field_result:
                t_elem = r.find(f'{wns}t')
                if t_elem is not None and t_elem.text:
                    field_display_text.append(t_elem.text)

        display_text = ''.join(field_display_text).strip()
        # Also check the full paragraph text as fallback -- the display text
        # should appear after 'As described earlier: '
        para_text = target_para.text

        if display_text and EXPECTED_BOOKMARK_TEXT.lower() in display_text.lower():
            print(f"PASS: Component 3 -- Field display text matches: '{display_text}' (0.3 pts)")
            total_score += 0.3
        elif EXPECTED_BOOKMARK_TEXT.lower() in para_text.lower():
            # The text is in the paragraph (possibly the field was rendered differently)
            # Give full credit if the REF field structure is present (checked in C1)
            if has_fld_begin and has_ref_instr:
                print(f"PASS: Component 3 -- Bookmark text found in paragraph with REF field: '{para_text[:120]}' (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Bookmark text in paragraph but no REF field structure")
        else:
            print(f"FAIL: Component 3 -- Expected '{EXPECTED_BOOKMARK_TEXT}', display text: '{display_text}', para text: '{para_text[:120]}'")
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
