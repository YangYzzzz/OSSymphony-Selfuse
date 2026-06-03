"""
Reward Script: Insert cross-reference to Figure 1's caption number
Task ID: osworld_writer_bibliography_crossref_005
Domain: libreoffice_writer

Task: Replace 'The diagram below' with 'Figure X' (cross-referenced to Figure 1)
in the sentence 'The diagram below illustrates the process flow.'

Scoring Rubric:
  Component 1: 'The diagram below' is removed from the target paragraph       (0.3 pts)
  Component 2: Paragraph now reads 'Figure 1 illustrates the process flow.'   (0.3 pts)
  Component 3: A REF cross-reference field code is present in that paragraph  (0.4 pts)
  Total: 1.0
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'osworld_writer_bibliography_crossref_005'

# XML namespaces used in OOXML
W_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def find_target_paragraph(doc):
    """
    Find the paragraph that originally read 'The diagram below illustrates the process flow.'
    In the golden file, it should read 'Figure 1 illustrates the process flow.'
    We identify it by the phrase 'illustrates the process flow.' being present.
    """
    for i, para in enumerate(doc.paragraphs):
        if 'illustrates the process flow' in para.text:
            return i, para
    return None, None


def get_ref_field_instrtext(para_element):
    """
    Extract all w:instrText values within REF field codes in the paragraph element.
    A cross-reference is a w:fldChar begin/separate/end block with w:instrText containing 'REF'.
    """
    ns = {'w': W_NS}
    instr_texts = []
    for instr in para_element.findall('.//w:instrText', ns):
        text = instr.text or ''
        if 'REF' in text:
            instr_texts.append(text.strip())
    return instr_texts


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Load document — gate check
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Find target paragraph
    para_idx, target_para = find_target_paragraph(doc)
    if target_para is None:
        print("CRITICAL: Could not find a paragraph with 'illustrates the process flow.'")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Target paragraph index={para_idx}, text={target_para.text!r}")

    # Component 1: 'The diagram below' is NO LONGER in the paragraph (0.3 pts)
    # This text is present in initial_env but removed in golden_env.
    try:
        if 'The diagram below' not in target_para.text and 'diagram below' not in target_para.text.lower():
            print(f"PASS: Component 1 — 'The diagram below' has been removed (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 1 — 'The diagram below' still present in paragraph. Text: {target_para.text!r}")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Paragraph text starts with 'Figure 1 illustrates the process flow.' (0.3 pts)
    # In the golden file the sentence reads:
    # '...consistency. Figure 1 illustrates the process flow.'
    # We check that 'Figure 1 illustrates the process flow' is in the full paragraph text.
    try:
        para_text = target_para.text
        if 'Figure 1 illustrates the process flow' in para_text:
            print(f"PASS: Component 2 — 'Figure 1 illustrates the process flow.' found in paragraph (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Expected 'Figure 1 illustrates the process flow.' in paragraph. Found: {para_text!r}")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: A REF cross-reference field code is present in the paragraph (0.4 pts)
    # The golden_env paragraph should contain a w:instrText element with 'REF' pointing to Figure 1,
    # indicating a live cross-reference, not just hardcoded text.
    # The actual instrText from golden: 'REF _Ref_Figure1 \* MERGEFORMAT'
    try:
        ref_instrs = get_ref_field_instrtext(target_para._element)
        # Accept any REF field code in the target paragraph as evidence of a cross-reference
        ref_found = len(ref_instrs) > 0
        if ref_found:
            print(f"PASS: Component 3 — REF cross-reference field code found: {ref_instrs} (0.4 pts)")
            total_score += 0.4
        else:
            # Check if there's any field code at all (fldChar elements)
            ns = {'w': W_NS}
            fld_chars = target_para._element.findall('.//w:fldChar', ns)
            instr_texts = target_para._element.findall('.//w:instrText', ns)
            all_instrs = [it.text for it in instr_texts if it.text]
            if fld_chars and all_instrs:
                print(f"FAIL: Component 3 — Field code found but no REF instruction. Instructions: {all_instrs}")
            else:
                print(f"FAIL: Component 3 — No REF cross-reference field code found in the paragraph. "
                      f"The text 'Figure 1' appears to be hardcoded plain text, not a cross-reference.")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 1)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
