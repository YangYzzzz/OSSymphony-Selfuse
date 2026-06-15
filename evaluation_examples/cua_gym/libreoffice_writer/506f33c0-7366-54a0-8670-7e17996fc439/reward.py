"""
Reward Script: Format project phases as uppercase letter numbered list
Task ID: writer_lec_004
Domain: libreoffice_writer
Scoring:
  Component 1 (0.4): All four phase paragraphs have numbering applied
  Component 2 (0.6): Numbering format is upperLetter (A., B., C., D.) AND text preserved in order
"""

import os
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_004'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

EXPECTED_PHASES = ['Planning', 'Development', 'Testing', 'Deployment']


def get_num_format(doc, num_id):
    """Resolve numId -> abstractNumId -> numFmt for ilvl 0."""
    try:
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return None
        numbering_elem = numbering_part._element

        # Find <w:num w:numId="num_id"> to get abstractNumId
        abstract_num_id = None
        for num_el in numbering_elem.findall(f'{{{WNS}}}num'):
            if num_el.get(f'{{{WNS}}}numId') == str(num_id):
                abs_ref = num_el.find(f'{{{WNS}}}abstractNumId')
                if abs_ref is not None:
                    abstract_num_id = abs_ref.get(f'{{{WNS}}}val')
                break

        if abstract_num_id is None:
            return None

        # Find <w:abstractNum w:abstractNumId="abstract_num_id"> -> lvl ilvl=0 -> numFmt
        for abs_num in numbering_elem.findall(f'{{{WNS}}}abstractNum'):
            if abs_num.get(f'{{{WNS}}}abstractNumId') == str(abstract_num_id):
                for lvl in abs_num.findall(f'{{{WNS}}}lvl'):
                    if lvl.get(f'{{{WNS}}}ilvl') == '0':
                        fmt_el = lvl.find(f'{{{WNS}}}numFmt')
                        if fmt_el is not None:
                            return fmt_el.get(f'{{{WNS}}}val')
        return None
    except Exception as e:
        print(f"  DEBUG: Error resolving numFmt: {e}")
        return None


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

    # Precondition gate: all four phase paragraphs must exist (text preserved)
    phase_paras = []
    for para in doc.paragraphs:
        text = para.text.strip()
        if text in EXPECTED_PHASES:
            phase_paras.append(para)

    if len(phase_paras) < 4:
        print(f"FAIL: Precondition — Found only {len(phase_paras)} of 4 expected phase paragraphs")
        print("REWARD: 0.0")
        return 0.0

    # Check order is preserved (precondition gate, not scored)
    actual_texts = [p.text.strip() for p in phase_paras]
    if actual_texts != EXPECTED_PHASES:
        print(f"FAIL: Precondition — Phase order incorrect. Found: {actual_texts}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All four phase paragraphs have numbering applied (0.4 points)
    # This FAILS on initial (plain paragraphs) -> PASSES on golden (numbered)
    try:
        numbered_count = 0
        num_ids = []
        for para in phase_paras:
            numPr = para._element.find(f'.//{{{WNS}}}numPr')
            if numPr is not None:
                numId_el = numPr.find(f'{{{WNS}}}numId')
                if numId_el is not None:
                    nid = numId_el.get(f'{{{WNS}}}val')
                    if nid and nid != '0':
                        numbered_count += 1
                        num_ids.append(nid)

        if numbered_count == 4:
            print(f"PASS: Component 1 — All 4 phase paragraphs have numbering (numIds: {num_ids}) (0.4 pts)")
            total_score += 0.4
        elif numbered_count > 0:
            partial = round(0.4 * numbered_count / 4, 2)
            print(f"PARTIAL: Component 1 — {numbered_count}/4 paragraphs have numbering ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 — No paragraphs have numbering applied")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Numbering format is upperLetter (0.6 points)
    # This FAILS on initial (no numbering) -> PASSES on golden (upperLetter)
    try:
        upper_letter_count = 0
        for para in phase_paras:
            numPr = para._element.find(f'.//{{{WNS}}}numPr')
            if numPr is not None:
                numId_el = numPr.find(f'{{{WNS}}}numId')
                if numId_el is not None:
                    nid = numId_el.get(f'{{{WNS}}}val')
                    if nid and nid != '0':
                        fmt = get_num_format(doc, nid)
                        if fmt == 'upperLetter':
                            upper_letter_count += 1
                        else:
                            print(f"  DEBUG: Para '{para.text.strip()}' has numFmt '{fmt}', expected 'upperLetter'")

        if upper_letter_count == 4:
            print(f"PASS: Component 2 — All 4 paragraphs use upperLetter numbering (0.6 pts)")
            total_score += 0.6
        elif upper_letter_count > 0:
            partial = round(0.6 * upper_letter_count / 4, 2)
            print(f"PARTIAL: Component 2 — {upper_letter_count}/4 paragraphs use upperLetter ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 — No paragraphs use upperLetter numbering")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
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
