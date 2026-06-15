"""
Reward Script: Configure chapter numbering with Roman numerals for Heading 1
and Arabic sub-numbers for Heading 2 (e.g., I, I.1, I.2, II, II.1)
Task ID: writer_lec_010
Domain: libreoffice_writer
Scoring:
  Component 1 (0.35): Heading 1 paragraphs have upperRoman numbering at ilvl=0
  Component 2 (0.35): Heading 2 paragraphs have decimal numbering at ilvl=1
  Component 3 (0.15): All headings share the same numId (multilevel list)
  Component 4 (0.15): lvlText patterns correct ('%1' for level 0, '%1.%2' for level 1)
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_010'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}


def get_val(elem, tag):
    """Get w:val attribute from a child element."""
    child = elem.find(f'w:{tag}', NS)
    if child is not None:
        return child.get(f'{{{WNS}}}val')
    return None


def get_numbering_info(doc):
    """Extract numbering properties from heading paragraphs and the numbering definitions."""
    heading1_nums = []  # list of (numId, ilvl) for Heading 1
    heading2_nums = []  # list of (numId, ilvl) for Heading 2

    for p in doc.paragraphs:
        if not p.style or 'Heading' not in p.style.name:
            continue

        ppr = p._element.find('w:pPr', NS)
        if ppr is None:
            if p.style.name == 'Heading 1':
                heading1_nums.append((None, None))
            elif p.style.name == 'Heading 2':
                heading2_nums.append((None, None))
            continue

        numpr = ppr.find('w:numPr', NS)
        if numpr is None:
            if p.style.name == 'Heading 1':
                heading1_nums.append((None, None))
            elif p.style.name == 'Heading 2':
                heading2_nums.append((None, None))
            continue

        num_id = get_val(numpr, 'numId')
        ilvl = get_val(numpr, 'ilvl')
        if p.style.name == 'Heading 1':
            heading1_nums.append((num_id, ilvl))
        elif p.style.name == 'Heading 2':
            heading2_nums.append((num_id, ilvl))

    return heading1_nums, heading2_nums


def get_abstract_num_levels(doc, num_id):
    """Given a numId, resolve the abstractNum and return level definitions as dict of ilvl -> {numFmt, lvlText}."""
    try:
        numbering_part = doc.part.numbering_part
        numbering_elem = numbering_part._element
    except Exception:
        return {}

    # Find num element to get abstractNumId
    abstract_num_id = None
    for num in numbering_elem.findall('w:num', NS):
        nid = num.get(f'{{{WNS}}}numId')
        if nid == str(num_id):
            abstract_num_id = get_val(num, 'abstractNumId')
            break

    if abstract_num_id is None:
        return {}

    # Find abstractNum element
    for abstract in numbering_elem.findall('w:abstractNum', NS):
        aid = abstract.get(f'{{{WNS}}}abstractNumId')
        if aid == str(abstract_num_id):
            levels = {}
            for lvl in abstract.findall('w:lvl', NS):
                ilvl = lvl.get(f'{{{WNS}}}ilvl')
                num_fmt = get_val(lvl, 'numFmt')
                lvl_text = get_val(lvl, 'lvlText')
                levels[ilvl] = {'numFmt': num_fmt, 'lvlText': lvl_text}
            return levels

    return {}


def persist_app_state(domain):
    """Try to save any unsaved document via Ctrl+S."""
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

    heading1_nums, heading2_nums = get_numbering_info(doc)

    print(f"Found {len(heading1_nums)} Heading 1 paragraphs, {len(heading2_nums)} Heading 2 paragraphs")

    # Component 1: Heading 1 paragraphs have upperRoman numbering at ilvl=0 (0.35 points)
    try:
        if len(heading1_nums) == 0:
            print("FAIL: Component 1 -- No Heading 1 paragraphs found")
        else:
            # All Heading 1 must have numPr with ilvl=0
            all_have_num = all(nid is not None for nid, _ in heading1_nums)
            all_ilvl_0 = all(ilvl == '0' for _, ilvl in heading1_nums if ilvl is not None)

            if not all_have_num:
                print(f"FAIL: Component 1 -- Not all Heading 1 paragraphs have numbering. Found: {heading1_nums}")
            elif not all_ilvl_0:
                print(f"FAIL: Component 1 -- Not all Heading 1 at ilvl=0. Found: {heading1_nums}")
            else:
                # Check the numFmt of level 0 in the referenced abstractNum
                first_num_id = heading1_nums[0][0]
                levels = get_abstract_num_levels(doc, first_num_id)
                if '0' in levels and levels['0']['numFmt'] == 'upperRoman':
                    print(f"PASS: Component 1 -- Heading 1 uses upperRoman numbering at ilvl=0 (0.35 pts)")
                    total_score += 0.35
                else:
                    actual_fmt = levels.get('0', {}).get('numFmt', 'MISSING')
                    print(f"FAIL: Component 1 -- Expected numFmt=upperRoman for level 0, found: {actual_fmt}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Heading 2 paragraphs have decimal numbering at ilvl=1 (0.35 points)
    try:
        if len(heading2_nums) == 0:
            print("FAIL: Component 2 -- No Heading 2 paragraphs found")
        else:
            all_have_num = all(nid is not None for nid, _ in heading2_nums)
            all_ilvl_1 = all(ilvl == '1' for _, ilvl in heading2_nums if ilvl is not None)

            if not all_have_num:
                print(f"FAIL: Component 2 -- Not all Heading 2 paragraphs have numbering. Found: {heading2_nums}")
            elif not all_ilvl_1:
                print(f"FAIL: Component 2 -- Not all Heading 2 at ilvl=1. Found: {heading2_nums}")
            else:
                first_num_id = heading2_nums[0][0]
                levels = get_abstract_num_levels(doc, first_num_id)
                if '1' in levels and levels['1']['numFmt'] == 'decimal':
                    print(f"PASS: Component 2 -- Heading 2 uses decimal numbering at ilvl=1 (0.35 pts)")
                    total_score += 0.35
                else:
                    actual_fmt = levels.get('1', {}).get('numFmt', 'MISSING')
                    print(f"FAIL: Component 2 -- Expected numFmt=decimal for level 1, found: {actual_fmt}")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: All headings share the same numId (multilevel consistency) (0.15 points)
    try:
        all_nums = heading1_nums + heading2_nums
        valid_ids = [nid for nid, _ in all_nums if nid is not None]
        if len(valid_ids) == 0:
            print("FAIL: Component 3 -- No headings have numbering assigned")
        elif len(set(valid_ids)) == 1:
            print(f"PASS: Component 3 -- All headings share numId={valid_ids[0]} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 3 -- Headings use different numIds: {set(valid_ids)}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: lvlText patterns correct (0.15 points)
    # Level 0 should produce just the Roman numeral (lvlText like '%1' without trailing period for chapter-style)
    # Level 1 should show parent.child (lvlText like '%1.%2')
    try:
        valid_ids = [nid for nid, _ in (heading1_nums + heading2_nums) if nid is not None]
        if len(valid_ids) == 0:
            print("FAIL: Component 4 -- No numbering to check lvlText")
        else:
            first_num_id = valid_ids[0]
            levels = get_abstract_num_levels(doc, first_num_id)

            lvl0_text = levels.get('0', {}).get('lvlText', '')
            lvl1_text = levels.get('1', {}).get('lvlText', '')

            # Level 0: should contain %1 (Roman numeral placeholder) - no %2 reference
            # Level 1: should contain both %1 and %2 with a separator (dot)
            lvl0_ok = '%1' in lvl0_text and '%2' not in lvl0_text
            lvl1_ok = '%1' in lvl1_text and '%2' in lvl1_text and '.' in lvl1_text

            if lvl0_ok and lvl1_ok:
                print(f"PASS: Component 4 -- lvlText patterns correct: level0='{lvl0_text}', level1='{lvl1_text}' (0.15 pts)")
                total_score += 0.15
            else:
                print(f"FAIL: Component 4 -- lvlText patterns: level0='{lvl0_text}' (ok={lvl0_ok}), level1='{lvl1_text}' (ok={lvl1_ok})")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook for LibreOffice Writer
persist_app_state("libreoffice_writer")

# Default: test against canonical artifact path
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
