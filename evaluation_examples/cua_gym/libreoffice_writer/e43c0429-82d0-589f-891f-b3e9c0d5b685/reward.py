"""
Reward Script: Apply 'List Bullet' style to document paragraphs with 0.635 cm indent
Task ID: writer_list_056
Domain: libreoffice_writer
Scoring:
  Component 1: All 5 paragraphs have 'List Bullet' style applied (0.6 pts)
  Component 2: Paragraphs with 'List Bullet' style have correct indent (0.635 cm / 360 twips)
               AND the numFmt is bullet type (0.4 pts)
               This is a compound check: FAILS if style not applied (handles initial_env)
  Total: 1.0
"""

import os
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_list_056'
FILE_PATH = f'{WORKDIR}/Desktop/daily_checklist.docx'

# Expected content for the 5 paragraphs (precondition gate)
EXPECTED_TEXTS = [
    'Check server health dashboard',
    'Review overnight error logs',
    'Verify backup completion status',
    'Monitor disk space utilization',
    'Confirm scheduled jobs executed successfully',
]

# 0.635 cm = 360 twips (1 inch = 1440 twips, 0.25 in * 1440 = 360)
EXPECTED_INDENT_TWIPS = 360


def get_indent_for_num_id(num_xml, num_id_val):
    """
    Given a numId value, trace: numId -> abstractNumId -> lvl[0] indent.
    Returns (left_twips, numFmt) or (None, None) if not found.
    """
    # Step 1: numId -> abstractNumId
    abstract_num_id = None
    for num_el in num_xml.findall(qn('w:num')):
        if num_el.get(qn('w:numId')) == num_id_val:
            abs_id_el = num_el.find(qn('w:abstractNumId'))
            if abs_id_el is not None:
                abstract_num_id = abs_id_el.get(qn('w:val'))
            break

    if abstract_num_id is None:
        return None, None

    # Step 2: abstractNumId -> lvl[0] pPr ind and numFmt
    for abs_num in num_xml.findall(qn('w:abstractNum')):
        if abs_num.get(qn('w:abstractNumId')) == abstract_num_id:
            for lvl in abs_num.findall(qn('w:lvl')):
                if lvl.get(qn('w:ilvl')) == '0':
                    # Get numFmt
                    num_fmt_el = lvl.find(qn('w:numFmt'))
                    num_fmt = num_fmt_el.get(qn('w:val')) if num_fmt_el is not None else None
                    # Get indent left
                    pPr = lvl.find(qn('w:pPr'))
                    if pPr is not None:
                        ind = pPr.find(qn('w:ind'))
                        if ind is not None:
                            left_val = ind.get(qn('w:left'))
                            if left_val is not None:
                                return int(left_val), num_fmt
            break

    return None, None


def get_list_bullet_num_id(doc):
    """
    Get the numId used by 'List Bullet' style from the style definition.
    Returns numId string or None.
    """
    for style in doc.styles:
        if style.name == 'List Bullet':
            pPr = style.element.find(qn('w:pPr'))
            if pPr is not None:
                numPr = pPr.find(qn('w:numPr'))
                if numPr is not None:
                    numId_el = numPr.find(qn('w:numId'))
                    if numId_el is not None:
                        return numId_el.get(qn('w:val'))
    return None


def get_para_effective_num_id(para):
    """
    Get the numId for a paragraph from its direct pPr/numPr or from its style.
    Returns numId string or None.
    """
    pPr = para._element.find(qn('w:pPr'))
    if pPr is not None:
        numPr = pPr.find(qn('w:numPr'))
        if numPr is not None:
            numId_el = numPr.find(qn('w:numId'))
            if numId_el is not None:
                return numId_el.get(qn('w:val'))
    return None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    # Precondition gate: load the document
    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Precondition gate: verify 5 paragraphs with expected content
    paras = [p for p in doc.paragraphs if p.text.strip()]
    if len(paras) != 5:
        print(f"PRECONDITION FAIL: Expected 5 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    texts_match = all(
        paras[i].text.strip() == EXPECTED_TEXTS[i]
        for i in range(5)
    )
    if not texts_match:
        print("PRECONDITION FAIL: Paragraph texts do not match expected content")
        for i, p in enumerate(paras):
            print(f"  Para {i}: {p.text!r}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 5 paragraphs have 'List Bullet' style applied (0.6 points)
    # FAILS on initial (Normal style) -> PASSES on golden (List Bullet style)
    try:
        list_bullet_styles = [p.style.name == 'List Bullet' for p in paras]
        list_bullet_count = sum(list_bullet_styles)
        if list_bullet_count == 5:
            print(f"PASS: Component 1 — All 5 paragraphs have 'List Bullet' style applied (0.6 pts)")
            total_score += 0.6
        elif list_bullet_count > 0:
            partial = round(0.6 * list_bullet_count / 5, 2)
            print(f"PARTIAL: Component 1 — {list_bullet_count}/5 paragraphs have 'List Bullet' style ({partial} pts)")
            total_score += partial
        else:
            style_names = [p.style.name for p in paras]
            print(f"FAIL: Component 1 — No paragraphs have 'List Bullet' style (found: {style_names})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")
        list_bullet_count = 0

    # Component 2: 'List Bullet' style paragraphs are numbered with bullet format
    #              AND the bullet indent is 0.635 cm (360 twips)
    #              This is a compound check anchored to the style change — only meaningful
    #              when paragraphs actually use List Bullet style.
    #              FAILS on initial (paragraphs use Normal, not List Bullet) ->
    #              PASSES on golden (paragraphs use List Bullet with correct indent)
    try:
        # This check only applies if paragraphs have 'List Bullet' style
        if list_bullet_count == 0:
            print(f"FAIL: Component 2 — No 'List Bullet' paragraphs to check indent on")
        else:
            # Get the numbering part
            numbering_part = doc.part.numbering_part
            if numbering_part is None:
                print(f"FAIL: Component 2 — No numbering part found in document")
            else:
                num_xml = numbering_part._element

                # Get the numId that 'List Bullet' style uses
                list_bullet_num_id = get_list_bullet_num_id(doc)
                if list_bullet_num_id is None:
                    print(f"FAIL: Component 2 — 'List Bullet' style has no numId reference")
                else:
                    indent_twips, num_fmt = get_indent_for_num_id(num_xml, list_bullet_num_id)
                    # Verify: numFmt must be 'bullet' AND indent must be ~360 twips
                    is_bullet_fmt = (num_fmt == 'bullet')
                    indent_ok = (indent_twips is not None and abs(indent_twips - EXPECTED_INDENT_TWIPS) <= 36)

                    if is_bullet_fmt and indent_ok and list_bullet_count == 5:
                        print(f"PASS: Component 2 — 'List Bullet' style has numFmt=bullet and indent={indent_twips} twips (~{indent_twips/1440*2.54:.3f} cm) (0.4 pts)")
                        total_score += 0.4
                    elif is_bullet_fmt and indent_ok and list_bullet_count > 0:
                        partial = round(0.4 * list_bullet_count / 5, 2)
                        print(f"PARTIAL: Component 2 — 'List Bullet' style has numFmt=bullet and indent={indent_twips} twips, but only {list_bullet_count}/5 paragraphs converted ({partial} pts)")
                        total_score += partial
                    elif not is_bullet_fmt:
                        print(f"FAIL: Component 2 — Expected numFmt=bullet, found {num_fmt!r}")
                    elif not indent_ok:
                        print(f"FAIL: Component 2 — Expected indent ~{EXPECTED_INDENT_TWIPS} twips (0.635 cm), found {indent_twips} twips")
                    else:
                        print(f"FAIL: Component 2 — No 'List Bullet' paragraphs to apply indent check")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
