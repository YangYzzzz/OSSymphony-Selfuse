"""
Reward Script: Four-level outline numbering scheme for corporate policy document
Task ID: writer_lec_029
Domain: libreoffice_writer

Scoring Rubric:
  Component 1 (0.25): Heading styles linked to a multi-level numbering definition
  Component 2 (0.25): Level 1 (ilvl=0) uses decimal format with '%1.' pattern
  Component 3 (0.25): Levels 2-3 use decimal with sublevel display ('%1.%2', '%1.%2.%3')
  Component 4 (0.25): Level 4 (ilvl=3) uses lowerLetter with ')' suffix pattern '%4)'
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_029'
FILE_PATH = os.path.join(WORKDIR, f'{TASK_ID}.docx')

WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'


def persist_app_state():
    """Save any unsaved changes in LibreOffice Writer."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(1.0)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_attr(element, attr_local_name):
    """Get attribute value using the wordprocessingml namespace."""
    return element.attrib.get(f'{{{WNS}}}{attr_local_name}')


def find_heading_numbering_info(doc):
    """
    Find the numbering definition linked to heading styles.
    Returns (numId, abstractNum_element) or (None, None).

    Numbering can be assigned via:
    1. Style definitions (style -> pPr -> numPr -> numId/ilvl)
    2. Direct paragraph properties (para -> pPr -> numPr -> numId/ilvl)

    We check both and look for a multi-level numbering definition (>=4 levels)
    that is linked to heading styles.
    """
    ns = {'w': WNS}

    # Strategy 1: Check style definitions for Heading 1-4
    style_num_ids = {}
    for style_name in ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
        try:
            style = doc.styles[style_name]
            pPr = style.element.find('.//w:pPr', ns)
            if pPr is not None:
                numPr = pPr.find('w:numPr', ns)
                if numPr is not None:
                    numId_el = numPr.find('w:numId', ns)
                    if numId_el is not None:
                        nid = get_attr(numId_el, 'val')
                        if nid:
                            style_num_ids[style_name] = nid
        except Exception:
            pass

    # Strategy 2: Check direct paragraph numPr on heading paragraphs
    para_num_ids = {}
    for para in doc.paragraphs:
        style_name = para.style.name if para.style else ''
        if style_name in ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
            numPr = para._element.find('.//w:numPr', ns)
            if numPr is not None:
                numId_el = numPr.find('w:numId', ns)
                if numId_el is not None:
                    nid = get_attr(numId_el, 'val')
                    if nid and nid != '0':
                        para_num_ids[style_name] = nid

    # Combine: prefer style-level, fallback to paragraph-level
    all_num_ids = {}
    for sn in ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
        if sn in style_num_ids:
            all_num_ids[sn] = style_num_ids[sn]
        elif sn in para_num_ids:
            all_num_ids[sn] = para_num_ids[sn]

    return all_num_ids, style_num_ids, para_num_ids


def resolve_abstract_num(doc, num_id):
    """Given a numId, find the corresponding abstractNum element and return it."""
    ns = {'w': WNS}
    try:
        numbering_part = doc.part.numbering_part
        root = numbering_part._element

        # Find num element with this numId
        for num in root.findall('.//w:num', ns):
            nid = get_attr(num, 'numId')
            if nid == str(num_id):
                abs_ref = num.find('w:abstractNumId', ns)
                if abs_ref is not None:
                    abs_id = get_attr(abs_ref, 'val')
                    # Find the abstractNum with this abstractNumId
                    for abstract in root.findall('.//w:abstractNum', ns):
                        aid = get_attr(abstract, 'abstractNumId')
                        if aid == abs_id:
                            return abstract
    except Exception:
        pass
    return None


def get_level_info(abstract_num, ilvl_val):
    """Get numFmt and lvlText for a specific ilvl in an abstractNum."""
    ns = {'w': WNS}
    for lvl in abstract_num.findall('w:lvl', ns):
        ilvl = get_attr(lvl, 'ilvl')
        if ilvl == str(ilvl_val):
            fmt_el = lvl.find('w:numFmt', ns)
            txt_el = lvl.find('w:lvlText', ns)
            fmt = get_attr(fmt_el, 'val') if fmt_el is not None else None
            txt = get_attr(txt_el, 'val') if txt_el is not None else None
            return fmt, txt
    return None, None


def verify_task(file_path):
    """
    Verify task completion with progressive scoring.
    Returns: float between 0.0 and 1.0
    """
    from docx import Document

    total_score = 0.0

    try:
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    # First, find the numbering linked to headings
    all_num_ids, style_num_ids, para_num_ids = find_heading_numbering_info(doc)

    # Component 1: Heading styles 1-4 are linked to a common multi-level numbering (0.25 pts)
    # This FAILS on initial (no numPr on heading styles) and PASSES on golden
    try:
        linked_count = 0
        common_num_id = None
        num_id_set = set()

        for sn in ['Heading 1', 'Heading 2', 'Heading 3', 'Heading 4']:
            if sn in all_num_ids:
                linked_count += 1
                num_id_set.add(all_num_ids[sn])

        # All 4 heading styles must reference a numbering definition
        # and they should all share the same numId (common outline list)
        if linked_count == 4 and len(num_id_set) == 1:
            common_num_id = num_id_set.pop()
            # Verify it's a multi-level definition (has >= 4 levels)
            abstract = resolve_abstract_num(doc, common_num_id)
            if abstract is not None:
                ns = {'w': WNS}
                levels = abstract.findall('w:lvl', ns)
                if len(levels) >= 4:
                    print(f"PASS: Component 1 -- All 4 heading styles linked to numId={common_num_id} with {len(levels)} levels (0.25 pts)")
                    total_score += 0.25
                else:
                    print(f"FAIL: Component 1 -- numId={common_num_id} has only {len(levels)} levels, need >= 4")
            else:
                print(f"FAIL: Component 1 -- Could not resolve abstractNum for numId={common_num_id}")
        elif linked_count == 0:
            print(f"FAIL: Component 1 -- No heading styles are linked to any numbering definition")
        else:
            print(f"FAIL: Component 1 -- Only {linked_count}/4 headings linked, numIds={num_id_set}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # For components 2-4, we need the abstract numbering definition
    abstract = None
    if all_num_ids:
        # Use any numId found (they should all be the same)
        some_num_id = list(all_num_ids.values())[0]
        abstract = resolve_abstract_num(doc, some_num_id)

    if abstract is None:
        print("FAIL: Components 2-4 -- No numbering definition found for heading styles")
        final_score = min(total_score, 1.0)
        print(f"\nScore: {total_score}/1.0")
        print(f"REWARD: {final_score}")
        return final_score

    # Component 2: Level 1 (ilvl=0) uses decimal format with '%1.' pattern (0.25 pts)
    # Task: Level 1 '1.' => numFmt=decimal, lvlText='%1.'
    try:
        fmt, txt = get_level_info(abstract, 0)
        if fmt == 'decimal' and txt is not None and '%1' in txt and txt.endswith('.'):
            print(f"PASS: Component 2 -- Level 1: numFmt={fmt}, lvlText={repr(txt)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 2 -- Level 1: expected decimal/'%1.', got numFmt={fmt}, lvlText={repr(txt)}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Levels 2-3 use decimal with sublevel display (0.25 pts)
    # Task: Level 2 '1.1' => numFmt=decimal, lvlText='%1.%2'
    #        Level 3 '1.1.1' => numFmt=decimal, lvlText='%1.%2.%3'
    try:
        fmt2, txt2 = get_level_info(abstract, 1)
        fmt3, txt3 = get_level_info(abstract, 2)

        # Level 2: decimal, pattern should show parent level + current: '%1.%2'
        lvl2_ok = (fmt2 == 'decimal' and txt2 is not None and '%1' in txt2 and '%2' in txt2)

        # Level 3: decimal, pattern should show all parent levels: '%1.%2.%3'
        lvl3_ok = (fmt3 == 'decimal' and txt3 is not None and '%1' in txt3 and '%2' in txt3 and '%3' in txt3)

        if lvl2_ok and lvl3_ok:
            print(f"PASS: Component 3 -- Level 2: {fmt2}/{repr(txt2)}, Level 3: {fmt3}/{repr(txt3)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 3 -- Level 2: {fmt2}/{repr(txt2)} (ok={lvl2_ok}), Level 3: {fmt3}/{repr(txt3)} (ok={lvl3_ok})")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Level 4 (ilvl=3) uses lowerLetter with ')' suffix (0.25 pts)
    # Task: Level 4 'a)' => numFmt=lowerLetter, lvlText='%4)'
    try:
        fmt4, txt4 = get_level_info(abstract, 3)
        if fmt4 == 'lowerLetter' and txt4 is not None and '%4' in txt4 and ')' in txt4:
            print(f"PASS: Component 4 -- Level 4: numFmt={fmt4}, lvlText={repr(txt4)} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 4 -- Level 4: expected lowerLetter/'%4)', got numFmt={fmt4}, lvlText={repr(txt4)}")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
persist_app_state()

if not os.path.exists(FILE_PATH):
    print(f"File not found: {FILE_PATH}")
    print("REWARD: 0.0")
else:
    verify_task(FILE_PATH)
