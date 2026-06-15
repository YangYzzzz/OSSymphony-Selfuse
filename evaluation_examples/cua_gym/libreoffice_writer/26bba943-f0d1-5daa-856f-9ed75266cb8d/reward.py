"""
Reward Script: Insert FILLIN input field in Department line
Task ID: writer_tm_058
Domain: libreoffice_writer
Scoring:
  Component 1 (0.40): FILLIN field exists in the Department paragraph
  Component 2 (0.35): FILLIN prompt text matches 'Enter your department name'
  Component 3 (0.25): Field structure is complete (begin, separate, end)
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_tm_058'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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


def find_department_paragraph(doc):
    """Find the paragraph that starts with 'Department:'."""
    for i, para in enumerate(doc.paragraphs):
        if para.text.strip().startswith('Department:') or para.text.strip().startswith('Department :'):
            return i, para
    return None, None


def verify_task(file_path):
    """
    Verify that a FILLIN input field with prompt 'Enter your department name'
    has been inserted in the Department paragraph.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document
    from lxml import etree

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Locate the Department paragraph
    dept_idx, dept_para = find_department_paragraph(doc)
    if dept_para is None:
        print("FAIL: Could not find 'Department:' paragraph in the document")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found Department paragraph at index {dept_idx}: {dept_para.text!r}")

    # Parse the XML of the Department paragraph
    p_elem = dept_para._element
    ns = {'w': W_NS}

    # Collect all fldChar elements and instrText elements in this paragraph
    fld_chars = p_elem.findall('.//w:fldChar', ns)
    instr_texts = p_elem.findall('.//w:instrText', ns)

    # Also search full document body for FILLIN fields (in case it's in a different structure)
    body = doc.element.body
    all_instr = body.findall('.//w:instrText', ns)

    # Check for FILLIN field in the Department paragraph specifically
    has_fillin_in_dept = False
    fillin_prompt = None

    for instr in instr_texts:
        if instr.text and 'FILLIN' in instr.text.upper():
            has_fillin_in_dept = True
            fillin_prompt = instr.text.strip()
            break

    # If not found in paragraph, check if there's a FILLIN anywhere near (some implementations
    # may split across elements, but the standard approach is within the same paragraph)
    if not has_fillin_in_dept:
        # Check all instrText in the document for FILLIN
        for instr in all_instr:
            if instr.text and 'FILLIN' in instr.text.upper():
                # Check if this instrText is within or adjacent to a Department context
                parent_p = instr.getparent()
                while parent_p is not None and parent_p.tag != f'{{{W_NS}}}p':
                    parent_p = parent_p.getparent()
                if parent_p is not None and parent_p is p_elem:
                    has_fillin_in_dept = True
                    fillin_prompt = instr.text.strip()
                    break

    # Component 1: FILLIN field exists in Department paragraph (0.40 points)
    try:
        if has_fillin_in_dept:
            print(f"PASS: Component 1 — FILLIN field found in Department paragraph (0.40 pts)")
            total_score += 0.40
        elif len(fld_chars) > 0:
            # There are field chars but not FILLIN — might be a different field type
            # Check if any field code mentions input/fillin
            any_field = False
            for instr in instr_texts:
                if instr.text:
                    txt_upper = instr.text.upper()
                    if 'FILLIN' in txt_upper or 'ASK' in txt_upper or 'INPUT' in txt_upper:
                        any_field = True
                        fillin_prompt = instr.text.strip()
                        break
            if any_field:
                print(f"PASS: Component 1 — Input field found in Department paragraph (0.40 pts)")
                total_score += 0.40
                has_fillin_in_dept = True
            else:
                print(f"FAIL: Component 1 — Field chars found but no FILLIN/input field type")
        else:
            print(f"FAIL: Component 1 — No FILLIN field found in Department paragraph")
            print(f"  Found {len(fld_chars)} fldChar elements, {len(instr_texts)} instrText elements")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: FILLIN prompt text contains 'Enter your department name' (0.35 points)
    try:
        if fillin_prompt is not None:
            prompt_lower = fillin_prompt.lower()
            if 'enter your department name' in prompt_lower:
                print(f"PASS: Component 2 — Prompt text matches: {fillin_prompt!r} (0.35 pts)")
                total_score += 0.35
            elif 'department' in prompt_lower:
                # Partial credit: mentions department but not exact text
                print(f"PARTIAL: Component 2 — Prompt mentions department but not exact match: {fillin_prompt!r} (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 2 — Prompt text does not mention department: {fillin_prompt!r}")
        else:
            print(f"FAIL: Component 2 — No FILLIN prompt text found")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Field structure is complete (begin, separate, end) (0.25 points)
    try:
        if has_fillin_in_dept:
            fld_types = []
            for fc in fld_chars:
                ftype = fc.get(f'{{{W_NS}}}fldCharType')
                if ftype:
                    fld_types.append(ftype)

            has_begin = 'begin' in fld_types
            has_separate = 'separate' in fld_types
            has_end = 'end' in fld_types

            if has_begin and has_separate and has_end:
                print(f"PASS: Component 3 — Complete field structure (begin, separate, end) (0.25 pts)")
                total_score += 0.25
            elif has_begin and has_end:
                print(f"PARTIAL: Component 3 — Field has begin and end but missing separate (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 — Incomplete field structure: {fld_types}")
        else:
            print(f"FAIL: Component 3 — No field to check structure for")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

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
