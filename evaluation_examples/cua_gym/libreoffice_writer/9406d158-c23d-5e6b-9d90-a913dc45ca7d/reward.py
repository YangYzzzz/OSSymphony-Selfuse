"""
Reward Script: Change numbered list indentation
Task ID: writer_lec_012
Domain: libreoffice_writer
Scoring:
  Component 1 (0.5): Number position aligned at ~1.5 cm from left margin
  Component 2 (0.3): Text starts at ~2.5 cm from left margin
  Component 3 (0.2): All 6 list items have consistent indentation
"""

import os
from docx import Document
from docx.shared import Pt, Emu, Cm

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_012'

# Target values from task
TARGET_NUMBER_POS_CM = 1.5   # number aligned at 1.5 cm
TARGET_TEXT_POS_CM = 2.5     # text starts at 2.5 cm
TOLERANCE_CM = 0.15          # tolerance for matching


def twips_to_cm(twips):
    """Convert twips to centimeters. 1 inch = 1440 twips, 1 inch = 2.54 cm."""
    return twips / 1440.0 * 2.54


def emu_to_cm(emu):
    """Convert EMU to centimeters. 1 inch = 914400 EMU, 1 inch = 2.54 cm."""
    return emu / 914400.0 * 2.54


def interpret_indent_cm(left_val, hanging_val):
    """
    Interpret indent values (left, hanging) and return (number_pos_cm, text_pos_cm).
    The XML w:ind attributes are supposed to be in twips, but some tools write EMU.
    We detect the unit by checking which interpretation gives reasonable values.
    """
    left = int(left_val)
    hanging = int(hanging_val)

    # Interpretation 1: twips (standard OOXML)
    text_cm_twips = twips_to_cm(left)
    num_cm_twips = twips_to_cm(left - hanging)

    # Interpretation 2: EMU (sometimes written by programmatic tools)
    text_cm_emu = emu_to_cm(left)
    num_cm_emu = emu_to_cm(left - hanging)

    # Pick the interpretation that gives reasonable page values (0-30 cm)
    if 0 <= text_cm_twips <= 30 and 0 <= num_cm_twips <= 30:
        return num_cm_twips, text_cm_twips
    elif 0 <= text_cm_emu <= 30 and 0 <= num_cm_emu <= 30:
        return num_cm_emu, text_cm_emu
    else:
        # Fall back to twips interpretation
        return num_cm_twips, text_cm_twips


def get_list_indent_from_numbering(doc, num_id, ilvl=0):
    """
    Get indent values from numbering.xml for a given numId and level.
    Returns (number_pos_cm, text_pos_cm) or None.
    Checks both lvlOverride on the num element and the abstractNum definition.
    """
    ns_uri = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns = {'w': ns_uri}

    try:
        numbering_part = doc.part.numbering_part
        numbering_xml = numbering_part._element
    except Exception:
        return None

    # Find the num element for this numId
    target_abstract_id = None
    override_indent = None

    for num in numbering_xml.findall('.//w:num', ns):
        nid = num.attrib.get(f'{{{ns_uri}}}numId')
        if nid == str(num_id):
            # Check for lvlOverride
            for ovr in num.findall('w:lvlOverride', ns):
                ovr_ilvl = ovr.attrib.get(f'{{{ns_uri}}}ilvl')
                if ovr_ilvl == str(ilvl):
                    lvl = ovr.find('w:lvl', ns)
                    if lvl is not None:
                        pPr = lvl.find('w:pPr', ns)
                        if pPr is not None:
                            ind = pPr.find('w:ind', ns)
                            if ind is not None:
                                left = ind.attrib.get(f'{{{ns_uri}}}left')
                                hanging = ind.attrib.get(f'{{{ns_uri}}}hanging', '0')
                                if left:
                                    override_indent = (left, hanging)
            # Get abstractNumId
            abs_ref = num.find('w:abstractNumId', ns)
            if abs_ref is not None:
                target_abstract_id = abs_ref.attrib.get(f'{{{ns_uri}}}val')
            break

    if override_indent:
        return interpret_indent_cm(override_indent[0], override_indent[1])

    if target_abstract_id is None:
        return None

    # Find the abstractNum
    for abstractNum in numbering_xml.findall('.//w:abstractNum', ns):
        abs_id = abstractNum.attrib.get(f'{{{ns_uri}}}abstractNumId')
        if abs_id == target_abstract_id:
            for lvl in abstractNum.findall('.//w:lvl', ns):
                lvl_ilvl = lvl.attrib.get(f'{{{ns_uri}}}ilvl')
                if lvl_ilvl == str(ilvl):
                    pPr = lvl.find('w:pPr', ns)
                    if pPr is not None:
                        ind = pPr.find('w:ind', ns)
                        if ind is not None:
                            left = ind.attrib.get(f'{{{ns_uri}}}left')
                            hanging = ind.attrib.get(f'{{{ns_uri}}}hanging', '0')
                            if left:
                                return interpret_indent_cm(left, hanging)
    return None


def get_para_direct_indent_cm(para):
    """
    Get paragraph-level direct indent override.
    Returns (number_pos_cm, text_pos_cm) or None.
    """
    ns_uri = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns = {'w': ns_uri}

    pPr = para._element.find('w:pPr', ns)
    if pPr is None:
        return None
    ind = pPr.find('w:ind', ns)
    if ind is None:
        return None

    left = ind.attrib.get(f'{{{ns_uri}}}left')
    hanging = ind.attrib.get(f'{{{ns_uri}}}hanging', '0')
    if left:
        return interpret_indent_cm(left, hanging)
    return None


def get_numid_from_para_or_style(para):
    """Get the numId for a paragraph (from direct pPr or style)."""
    ns_uri = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
    ns = {'w': ns_uri}

    # Check paragraph-level numPr
    pPr = para._element.find('w:pPr', ns)
    if pPr is not None:
        numPr = pPr.find('w:numPr', ns)
        if numPr is not None:
            numId_elem = numPr.find('w:numId', ns)
            if numId_elem is not None:
                val = numId_elem.attrib.get(f'{{{ns_uri}}}val')
                if val and val != '0':
                    return int(val)

    # Check style-level numPr
    if para.style:
        style_elem = para.style.element
        style_pPr = style_elem.find('w:pPr', ns)
        if style_pPr is not None:
            numPr = style_pPr.find('w:numPr', ns)
            if numPr is not None:
                numId_elem = numPr.find('w:numId', ns)
                if numId_elem is not None:
                    val = numId_elem.attrib.get(f'{{{ns_uri}}}val')
                    if val and val != '0':
                        return int(val)
    return None


def get_effective_indent(doc, para):
    """
    Get effective indent for a numbered list paragraph.
    Priority: paragraph direct > numbering definition > style.
    Returns (number_pos_cm, text_pos_cm) or None.
    """
    # 1. Check paragraph-level direct indent
    direct = get_para_direct_indent_cm(para)
    if direct is not None:
        return direct

    # 2. Check numbering definition
    num_id = get_numid_from_para_or_style(para)
    if num_id is not None:
        numbering_indent = get_list_indent_from_numbering(doc, num_id, ilvl=0)
        if numbering_indent is not None:
            return numbering_indent

    return None


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

    # Find all numbered list paragraphs
    list_paras = [p for p in doc.paragraphs
                  if p.style and p.style.name == 'List Number']

    if len(list_paras) == 0:
        print("FAIL: No 'List Number' paragraphs found")
        print("REWARD: 0.0")
        return 0.0

    print(f"INFO: Found {len(list_paras)} 'List Number' paragraphs")

    # Get effective indentation for each list paragraph
    indents = []
    for i, para in enumerate(list_paras):
        indent = get_effective_indent(doc, para)
        if indent is not None:
            indents.append(indent)
            print(f"INFO: Para {i}: number_pos={indent[0]:.3f} cm, text_pos={indent[1]:.3f} cm")
        else:
            print(f"WARN: Para {i}: could not determine indent")

    if len(indents) == 0:
        print("FAIL: Could not determine indentation for any list paragraph")
        print("REWARD: 0.0")
        return 0.0

    # Use first paragraph as representative (they should all match)
    num_pos, text_pos = indents[0]

    # Component 1: Number position at ~1.5 cm (0.5 points)
    try:
        num_diff = abs(num_pos - TARGET_NUMBER_POS_CM)
        if num_diff <= TOLERANCE_CM:
            print(f"PASS: Component 1 — Number position at {num_pos:.3f} cm "
                  f"(target: {TARGET_NUMBER_POS_CM} cm, diff: {num_diff:.3f} cm) (0.5 pts)")
            total_score += 0.5
        else:
            print(f"FAIL: Component 1 — Number position at {num_pos:.3f} cm "
                  f"(target: {TARGET_NUMBER_POS_CM} cm, diff: {num_diff:.3f} cm)")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: Text starts at ~2.5 cm (0.3 points)
    try:
        text_diff = abs(text_pos - TARGET_TEXT_POS_CM)
        if text_diff <= TOLERANCE_CM:
            print(f"PASS: Component 2 — Text position at {text_pos:.3f} cm "
                  f"(target: {TARGET_TEXT_POS_CM} cm, diff: {text_diff:.3f} cm) (0.3 pts)")
            total_score += 0.3
        else:
            print(f"FAIL: Component 2 — Text position at {text_pos:.3f} cm "
                  f"(target: {TARGET_TEXT_POS_CM} cm, diff: {text_diff:.3f} cm)")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: All 6 list items have consistent indentation (0.2 points)
    try:
        if len(indents) >= 6:
            all_consistent = True
            for i, (n, t) in enumerate(indents):
                if abs(n - num_pos) > 0.01 or abs(t - text_pos) > 0.01:
                    all_consistent = False
                    print(f"FAIL: Component 3 — Para {i} has different indent: "
                          f"num={n:.3f}, text={t:.3f}")
                    break
            if all_consistent:
                # Only award if the indentation also matches the target
                if (abs(num_pos - TARGET_NUMBER_POS_CM) <= TOLERANCE_CM and
                        abs(text_pos - TARGET_TEXT_POS_CM) <= TOLERANCE_CM):
                    print(f"PASS: Component 3 — All {len(indents)} items have consistent "
                          f"correct indentation (0.2 pts)")
                    total_score += 0.2
                else:
                    print(f"FAIL: Component 3 — Indentation is consistent but does not "
                          f"match target values")
            else:
                print("FAIL: Component 3 — Inconsistent indentation across list items")
        else:
            print(f"FAIL: Component 3 — Only {len(indents)} items found "
                  f"(expected 6 with valid indent)")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
