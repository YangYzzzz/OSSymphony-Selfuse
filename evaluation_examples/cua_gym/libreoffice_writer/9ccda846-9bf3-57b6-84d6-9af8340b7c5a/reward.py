"""
Reward Script: Configure multi-level list bullet characters
Task ID: writer_list_049
Domain: libreoffice_writer
Scoring:
  Component 1: Level 1 bullet changed to U+25CB (hollow circle) — 0.5 pts
  Component 2: Level 2 bullet changed to U+25A0 (black square) — 0.5 pts
  (Level 0 bullet U+2022 is a precondition — same in both initial and golden, NOT scored)
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_list_049'

# Ground truth bullet characters from task spec
LEVEL0_BULLET = '\u2022'   # U+2022 BULLET (filled circle) — precondition
LEVEL1_BULLET = '\u25cb'   # U+25CB WHITE CIRCLE (hollow circle) — must change
LEVEL2_BULLET = '\u25a0'   # U+25A0 BLACK SQUARE — must change


def get_bullet_char_for_level(doc, num_id_str, ilvl_str):
    """
    Look up the bullet character for a given numId and ilvl from the numbering part.
    Checks both the abstractNum definition and any lvlOverride on the num element.
    Returns the character string, or None if not found.
    """
    numbering = doc.part.numbering_part
    if numbering is None:
        return None

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    root = numbering._element

    # Find the abstractNumId referenced by num_id_str
    abs_id = None
    for num_el in root.findall('.//w:num', ns):
        if num_el.get(qn('w:numId')) == num_id_str:
            abs_id_el = num_el.find('w:abstractNumId', ns)
            if abs_id_el is not None:
                abs_id = abs_id_el.get(qn('w:val'))

            # Also check for lvlOverride on this num element
            for ov in num_el.findall('w:lvlOverride', ns):
                if ov.get(qn('w:ilvl')) == ilvl_str:
                    ov_lvl = ov.find('w:lvl', ns)
                    if ov_lvl is not None:
                        lvl_text_ov = ov_lvl.find('w:lvlText', ns)
                        if lvl_text_ov is not None:
                            return lvl_text_ov.get(qn('w:val'))
            break

    if abs_id is None:
        return None

    # Fall through to abstractNum definition
    for abs_num in root.findall('.//w:abstractNum', ns):
        if abs_num.get(qn('w:abstractNumId')) == abs_id:
            for lvl_el in abs_num.findall('w:lvl', ns):
                if lvl_el.get(qn('w:ilvl')) == ilvl_str:
                    lvl_text = lvl_el.find('w:lvlText', ns)
                    if lvl_text is not None:
                        return lvl_text.get(qn('w:val'))

    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0

    Only scores task-introduced changes:
      - Level 1 bullet changed from U+2022 to U+25CB
      - Level 2 bullet changed from U+2022 to U+25A0
    Level 0 (U+2022) is a precondition and is NOT a scored component.
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print('CRITICAL: Cannot load file ' + str(file_path) + ': ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    # Precondition: verify the file has the expected list structure (numId=10, levels 0-2)
    try:
        ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
        para_num_ids = set()
        for para in doc.paragraphs:
            numPr = para._element.find('.//' + qn('w:numPr'))
            if numPr is not None:
                numId_el = numPr.find(qn('w:numId'))
                if numId_el is not None:
                    para_num_ids.add(numId_el.get(qn('w:val')))
        if '10' not in para_num_ids:
            print('PRECONDITION FAIL: numId=10 list not found in document. Cannot verify.')
            print('REWARD: 0.0')
            return 0.0
        print('PRECONDITION PASS: numId=10 list structure found')
    except Exception as e:
        print('ERROR checking precondition: ' + str(e))
        print('REWARD: 0.0')
        return 0.0

    # Component 1: Level 1 bullet is U+25CB (hollow circle) (0.5 points)
    # In initial_env this is U+2022 (same as all levels) — FAILS on initial
    # In golden_env this is U+25CB — PASSES on golden
    try:
        level1_char = get_bullet_char_for_level(doc, '10', '1')
        if level1_char is None:
            print('FAIL: Component 1 — could not retrieve level 1 bullet character')
        elif level1_char == LEVEL1_BULLET:
            print('PASS: Component 1 — Level 1 bullet is U+25CB (hollow circle) as required (0.5 pts)')
            total_score += 0.5
        else:
            codes = [hex(ord(c)) for c in level1_char]
            print('FAIL: Component 1 — Level 1 bullet expected U+25CB (hollow circle), found: '
                  + repr(level1_char) + ' ' + str(codes))
    except Exception as e:
        print('ERROR: Component 1 — ' + str(e))

    # Component 2: Level 2 bullet is U+25A0 (black square) (0.5 points)
    # In initial_env this is U+2022 — FAILS on initial
    # In golden_env this is U+25A0 — PASSES on golden
    try:
        level2_char = get_bullet_char_for_level(doc, '10', '2')
        if level2_char is None:
            print('FAIL: Component 2 — could not retrieve level 2 bullet character')
        elif level2_char == LEVEL2_BULLET:
            print('PASS: Component 2 — Level 2 bullet is U+25A0 (black square) as required (0.5 pts)')
            total_score += 0.5
        else:
            codes = [hex(ord(c)) for c in level2_char]
            print('FAIL: Component 2 — Level 2 bullet expected U+25A0 (black square), found: '
                  + repr(level2_char) + ' ' + str(codes))
    except Exception as e:
        print('ERROR: Component 2 — ' + str(e))

    final_score = min(total_score, 1.0)
    print('\nScore: ' + str(total_score) + '/1.0')
    print('REWARD: ' + str(final_score))
    return final_score


# Default: test against canonical artifact path
file_path = WORKDIR + '/topic_outline.docx'
if not os.path.exists(file_path):
    print('File not found: ' + file_path)
    print('REWARD: 0.0')
else:
    verify_task(file_path)
