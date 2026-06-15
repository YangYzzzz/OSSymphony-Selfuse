"""
Reward Script: Insert a cross-reference to bookmark 'golden_ratio_definition' showing page number
Task ID: writer_struct_024
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): A PAGEREF field code exists in paragraph 77, appended after 'from page '
  Component 2 (0.3): The PAGEREF field references bookmark 'golden_ratio_definition'
  Component 3 (0.2): The field's cached display value is '4' (correct page number)
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user/Desktop'
TASK_ID = 'writer_struct_024'
FILE_PATH = f'{WORKDIR}/math_textbook_ch5.docx'

W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find paragraph 77 (0-indexed) which should contain the target sentence
    try:
        paras = doc.paragraphs
        target_para = None
        target_idx = None
        for i, para in enumerate(paras):
            if 'Recall the definition from page' in para.text:
                target_para = para
                target_idx = i
                break
        if target_para is None:
            print("FAIL: Could not find paragraph containing 'Recall the definition from page'")
            print(f"REWARD: {total_score}")
            return total_score
        else:
            print(f"INFO: Found target paragraph at index {target_idx}")
    except Exception as e:
        print(f"ERROR: Could not locate target paragraph: {e}")
        print(f"REWARD: {total_score}")
        return total_score

    # Component 1: A PAGEREF field code exists in the target paragraph (0.5 points)
    # This FAILS on initial (no field) and PASSES on golden (field present)
    try:
        para_xml = etree.tostring(target_para._element, pretty_print=True).decode()
        has_fld_char = 'fldChar' in para_xml
        has_instr_text = 'instrText' in para_xml

        if has_fld_char and has_instr_text:
            print(f"PASS: Component 1 — PAGEREF field code found in target paragraph (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — No field code (fldChar/instrText) found in target paragraph; has_fldChar={has_fld_char}, has_instrText={has_instr_text}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The field code references bookmark 'golden_ratio_definition' via PAGEREF (0.3 points)
    # This FAILS on initial and PASSES on golden
    try:
        instr_texts = target_para._element.findall(f'.//{{{W_NS}}}instrText')
        found_pageref = False
        for instr in instr_texts:
            if instr.text and 'PAGEREF' in instr.text and 'golden_ratio_definition' in instr.text:
                found_pageref = True
                print(f"PASS: Component 2 — instrText contains PAGEREF golden_ratio_definition: '{instr.text.strip()}' (0.3 pts)")
                break

        if found_pageref:
            total_score += 0.3
        else:
            instr_values = [i.text for i in instr_texts if i.text]
            print(f"FAIL: Component 2 — PAGEREF golden_ratio_definition not found in instrText; found: {instr_values}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: The field's cached display value is '4' (correct page number) (0.2 points)
    # Between the fldChar 'separate' and 'end' elements, there should be a run with text '4'
    # This FAILS on initial (no field) and PASSES on golden (field with value 4)
    try:
        runs = target_para._element.findall(f'.//{{{W_NS}}}r')
        in_field_value = False
        field_value = None

        for run_el in runs:
            fld_chars = run_el.findall(f'{{{W_NS}}}fldChar')
            for fc in fld_chars:
                fld_type = fc.get(f'{{{W_NS}}}fldCharType')
                if fld_type == 'separate':
                    in_field_value = True
                elif fld_type == 'end':
                    in_field_value = False

            if in_field_value:
                t_els = run_el.findall(f'{{{W_NS}}}t')
                for t_el in t_els:
                    if t_el.text is not None:
                        field_value = t_el.text.strip()

        if field_value == '4':
            print(f"PASS: Component 3 — Field cached value is '4' (correct page number) (0.2 pts)")
            total_score += 0.2
        else:
            print(f"FAIL: Component 3 — Expected field cached value '4', found: {repr(field_value)}")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
