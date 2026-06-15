"""
Reward Script: Heading 2 outline numbering subordinate to Heading 1
Task ID: writer_tech_089
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Heading 2 style has numPr linked to a multilevel numbering definition
  Component 2 (0.35): The multilevel numbering level for Heading 2 uses '%1.%2' format (subordinate)
  Component 3 (0.30): Heading 1 style also participates in the same multilevel numbering scheme
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_tech_089'
NS = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}


def persist_app_state(domain):
    """Save any unsaved changes in LibreOffice Writer."""
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_style_numpr(doc, style_id):
    """Get numPr (ilvl, numId) from a paragraph style definition."""
    for style_el in doc.styles.element.findall('.//w:style', NS):
        sid = style_el.get(f'{{{NS["w"]}}}styleId')
        if sid == style_id:
            ppr = style_el.find('w:pPr', NS)
            if ppr is not None:
                numpr = ppr.find('w:numPr', NS)
                if numpr is not None:
                    ilvl_el = numpr.find('w:ilvl', NS)
                    numid_el = numpr.find('w:numId', NS)
                    ilvl = ilvl_el.get(f'{{{NS["w"]}}}val') if ilvl_el is not None else None
                    numid = numid_el.get(f'{{{NS["w"]}}}val') if numid_el is not None else None
                    return ilvl, numid
    return None, None


def get_abstract_num_id_for_num(numbering_part, num_id):
    """Given a numId, find the abstractNumId it references."""
    root = numbering_part._element
    for num_el in root.findall('.//w:num', NS):
        nid = num_el.get(f'{{{NS["w"]}}}numId')
        if nid == num_id:
            abs_el = num_el.find('w:abstractNumId', NS)
            if abs_el is not None:
                return abs_el.get(f'{{{NS["w"]}}}val')
    return None


def get_abstract_num(numbering_part, abstract_num_id):
    """Get an abstractNum element by its ID."""
    root = numbering_part._element
    for abs_num in root.findall('.//w:abstractNum', NS):
        aid = abs_num.get(f'{{{NS["w"]}}}abstractNumId')
        if aid == abstract_num_id:
            return abs_num
    return None


def get_lvl_info(abstract_num_el, ilvl_val):
    """Get level info (numFmt, lvlText, multiLevelType) for a given ilvl."""
    for lvl in abstract_num_el.findall('w:lvl', NS):
        if lvl.get(f'{{{NS["w"]}}}ilvl') == ilvl_val:
            num_fmt_el = lvl.find('w:numFmt', NS)
            lvl_text_el = lvl.find('w:lvlText', NS)
            num_fmt = num_fmt_el.get(f'{{{NS["w"]}}}val') if num_fmt_el is not None else None
            lvl_text = lvl_text_el.get(f'{{{NS["w"]}}}val') if lvl_text_el is not None else None
            return num_fmt, lvl_text
    return None, None


def verify_task(file_path):
    """
    Verify that Heading 2 uses outline numbering subordinate to Heading 1.
    Returns: float between 0.0 and 1.0
    """
    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: Heading 2 style has numPr linked to a multilevel numbering (0.35 points)
    try:
        h2_ilvl, h2_numid = get_style_numpr(doc, 'Heading2')
        if h2_numid is not None and h2_ilvl is not None:
            # Verify it's a multilevel numbering definition
            try:
                numbering_part = doc.part.numbering_part
                abs_num_id = get_abstract_num_id_for_num(numbering_part, h2_numid)
                abs_num_el = get_abstract_num(numbering_part, abs_num_id) if abs_num_id else None
                if abs_num_el is not None:
                    ml_type_el = abs_num_el.find('w:multiLevelType', NS)
                    ml_type = ml_type_el.get(f'{{{NS["w"]}}}val') if ml_type_el is not None else None
                    if ml_type == 'multilevel':
                        print(f"PASS: Component 1 — Heading 2 has numPr (ilvl={h2_ilvl}, numId={h2_numid}) referencing multilevel abstractNum {abs_num_id} (0.35 pts)")
                        total_score += 0.35
                    else:
                        print(f"FAIL: Component 1 — Heading 2 numPr references a '{ml_type}' numbering, not 'multilevel'")
                else:
                    print(f"FAIL: Component 1 — Could not find abstractNum for numId={h2_numid}")
            except Exception as e:
                print(f"FAIL: Component 1 — Heading 2 has numPr but numbering part error: {e}")
        else:
            print(f"FAIL: Component 1 — Heading 2 style has no numPr (ilvl={h2_ilvl}, numId={h2_numid})")
    except Exception as e:
        print(f"ERROR: Component 1 — {e}")

    # Component 2: The multilevel numbering level for Heading 2 uses '%1.%2' format (0.35 points)
    try:
        h2_ilvl, h2_numid = get_style_numpr(doc, 'Heading2')
        if h2_numid is not None and h2_ilvl is not None:
            numbering_part = doc.part.numbering_part
            abs_num_id = get_abstract_num_id_for_num(numbering_part, h2_numid)
            abs_num_el = get_abstract_num(numbering_part, abs_num_id) if abs_num_id else None
            if abs_num_el is not None:
                num_fmt, lvl_text = get_lvl_info(abs_num_el, h2_ilvl)
                # The lvlText should contain both %1 and %2 to show subordination
                if lvl_text and '%1' in lvl_text and '%2' in lvl_text:
                    print(f"PASS: Component 2 — Heading 2 level uses lvlText='{lvl_text}' (contains %1.%2 subordination) (0.35 pts)")
                    total_score += 0.35
                else:
                    print(f"FAIL: Component 2 — Heading 2 level lvlText='{lvl_text}', expected pattern with '%1' and '%2' for subordination")
            else:
                print(f"FAIL: Component 2 — Could not find abstractNum for numId={h2_numid}")
        else:
            print(f"FAIL: Component 2 — Heading 2 has no numPr, cannot check level format")
    except Exception as e:
        print(f"ERROR: Component 2 — {e}")

    # Component 3: Heading 1 participates in the same multilevel numbering scheme (0.30 points)
    try:
        h1_ilvl, h1_numid = get_style_numpr(doc, 'Heading1')
        h2_ilvl, h2_numid = get_style_numpr(doc, 'Heading2')
        if h1_numid is not None and h1_ilvl is not None:
            if h1_numid == h2_numid:
                # Verify Heading 1 is at level 0 in the same numbering
                numbering_part = doc.part.numbering_part
                abs_num_id_h1 = get_abstract_num_id_for_num(numbering_part, h1_numid)
                abs_num_el = get_abstract_num(numbering_part, abs_num_id_h1) if abs_num_id_h1 else None
                if abs_num_el is not None:
                    num_fmt, lvl_text = get_lvl_info(abs_num_el, '0')
                    if lvl_text and '%1' in lvl_text:
                        print(f"PASS: Component 3 — Heading 1 at ilvl={h1_ilvl} in same numId={h1_numid}, lvlText='{lvl_text}' (0.30 pts)")
                        total_score += 0.30
                    else:
                        print(f"FAIL: Component 3 — Heading 1 level 0 lvlText='{lvl_text}', expected '%1'")
                else:
                    print(f"FAIL: Component 3 — Could not find abstractNum for Heading 1 numId={h1_numid}")
            else:
                print(f"FAIL: Component 3 — Heading 1 numId={h1_numid} differs from Heading 2 numId={h2_numid}")
        else:
            print(f"FAIL: Component 3 — Heading 1 style has no numPr (ilvl={h1_ilvl}, numId={h1_numid})")
    except Exception as e:
        print(f"ERROR: Component 3 — {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persist unsaved state before verification
persist_app_state('libreoffice_writer')

# Test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
