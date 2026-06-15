"""
Reward Script: Create a custom list style with three levels
Task ID: writer_bs_057
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): Paragraphs have numbering (numPr) applied
  Component 2 (0.30): Level formats correct (upperRoman, upperLetter, decimal)
  Component 3 (0.20): Indentation approximately correct per level
  Component 4 (0.20): Manual numbering prefixes removed from text
"""

import os
import re
from docx import Document
from docx.oxml.ns import qn

WORKDIR = '/home/user'
TASK_ID = 'writer_bs_057'


def persist_app_state(domain):
    """Save any unsaved GUI state before verification."""
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        import time
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print(f"PERSIST: ctrl+s sent for {domain}")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


def get_numbering_info(doc):
    """
    Parse the numbering XML to find the abstractNum definition used by numId
    referenced in the document paragraphs. Returns dict mapping ilvl -> {numFmt, lvlText, indent_left}.
    """
    try:
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return None, None
    except Exception:
        return None, None

    numbering_elem = numbering_part._element
    WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Find all numId -> abstractNumId mappings
    # Use the LAST definition for a given numId (later overrides earlier)
    num_to_abstract = {}
    for num_elem in numbering_elem.findall(f'{{{WNS}}}num'):
        num_id = num_elem.get(f'{{{WNS}}}numId')
        abstract_ref = num_elem.find(f'{{{WNS}}}abstractNumId')
        if abstract_ref is not None:
            num_to_abstract[num_id] = abstract_ref.get(f'{{{WNS}}}val')

    # Build abstractNum definitions
    abstract_defs = {}
    for abstract_elem in numbering_elem.findall(f'{{{WNS}}}abstractNum'):
        abstract_id = abstract_elem.get(f'{{{WNS}}}abstractNumId')
        multi_type = None
        mt_elem = abstract_elem.find(f'{{{WNS}}}multiLevelType')
        if mt_elem is not None:
            multi_type = mt_elem.get(f'{{{WNS}}}val')

        levels = {}
        for lvl in abstract_elem.findall(f'{{{WNS}}}lvl'):
            ilvl = lvl.get(f'{{{WNS}}}ilvl')
            num_fmt_elem = lvl.find(f'{{{WNS}}}numFmt')
            lvl_text_elem = lvl.find(f'{{{WNS}}}lvlText')
            pPr = lvl.find(f'{{{WNS}}}pPr')

            num_fmt = num_fmt_elem.get(f'{{{WNS}}}val') if num_fmt_elem is not None else None
            lvl_text = lvl_text_elem.get(f'{{{WNS}}}val') if lvl_text_elem is not None else None

            indent_left = None
            if pPr is not None:
                ind = pPr.find(f'{{{WNS}}}ind')
                if ind is not None:
                    indent_left = ind.get(f'{{{WNS}}}left')
                    if indent_left is not None:
                        indent_left = int(indent_left)

            levels[ilvl] = {
                'numFmt': num_fmt,
                'lvlText': lvl_text,
                'indent_left': indent_left,
            }

        abstract_defs[abstract_id] = {
            'multiLevelType': multi_type,
            'levels': levels,
        }

    return num_to_abstract, abstract_defs


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

    # Gather paragraph numbering info
    numbered_paras = []  # list of (para_index, ilvl, numId, text)
    for i, para in enumerate(doc.paragraphs):
        pPr = para._element.find(qn('w:pPr'))
        if pPr is not None:
            numPr = pPr.find(qn('w:numPr'))
            if numPr is not None:
                ilvl_elem = numPr.find(qn('w:ilvl'))
                numId_elem = numPr.find(qn('w:numId'))
                ilvl_val = ilvl_elem.get(qn('w:val')) if ilvl_elem is not None else None
                numId_val = numId_elem.get(qn('w:val')) if numId_elem is not None else None
                if numId_val and numId_val != '0':
                    numbered_paras.append((i, ilvl_val, numId_val, para.text))

    num_to_abstract, abstract_defs = get_numbering_info(doc)

    # Component 1: Paragraphs have numbering (numPr) applied (0.30 points)
    # In the initial file, no paragraphs have numPr. In golden, ~32 paragraphs do.
    # We expect at least 15 paragraphs to have numbering for full credit.
    try:
        count_numbered = len(numbered_paras)
        # Check we have numbered paragraphs at all three levels
        levels_found = set()
        for _, ilvl, _, _ in numbered_paras:
            if ilvl is not None:
                levels_found.add(ilvl)

        has_level0 = '0' in levels_found
        has_level1 = '1' in levels_found
        has_level2 = '2' in levels_found

        if count_numbered >= 15 and has_level0 and has_level1 and has_level2:
            print(f"PASS: Component 1 -- {count_numbered} paragraphs with numbering across 3 levels (0.30 pts)")
            total_score += 0.30
        elif count_numbered >= 5 and len(levels_found) >= 2:
            print(f"PARTIAL: Component 1 -- {count_numbered} numbered paras, levels={levels_found} (0.15 pts)")
            total_score += 0.15
        else:
            print(f"FAIL: Component 1 -- Only {count_numbered} numbered paragraphs, levels={levels_found}")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Level formats correct (0.30 points)
    # Level 0 = upperRoman, Level 1 = upperLetter, Level 2 = decimal
    try:
        if num_to_abstract is None or abstract_defs is None:
            print("FAIL: Component 2 -- No numbering definitions found")
        else:
            # Find the abstractNum used by the paragraphs
            # Get the numId used by the numbered paragraphs
            num_ids_used = set(nid for _, _, nid, _ in numbered_paras)

            format_score = 0.0
            best_match = 0

            for nid in num_ids_used:
                abstract_id = num_to_abstract.get(nid)
                if abstract_id is None:
                    continue
                adef = abstract_defs.get(abstract_id)
                if adef is None:
                    continue

                levels = adef.get('levels', {})
                match_count = 0

                # Check level 0: upperRoman
                if '0' in levels and levels['0']['numFmt'] == 'upperRoman':
                    match_count += 1

                # Check level 1: upperLetter
                if '1' in levels and levels['1']['numFmt'] == 'upperLetter':
                    match_count += 1

                # Check level 2: decimal
                if '2' in levels and levels['2']['numFmt'] == 'decimal':
                    match_count += 1

                if match_count > best_match:
                    best_match = match_count
                    # Also print what we found
                    fmt0 = levels.get('0', {}).get('numFmt', 'missing')
                    fmt1 = levels.get('1', {}).get('numFmt', 'missing')
                    fmt2 = levels.get('2', {}).get('numFmt', 'missing')

            if best_match == 3:
                print(f"PASS: Component 2 -- Level formats correct: L0={fmt0}, L1={fmt1}, L2={fmt2} (0.30 pts)")
                total_score += 0.30
            elif best_match == 2:
                print(f"PARTIAL: Component 2 -- 2/3 level formats correct (0.15 pts)")
                total_score += 0.15
            elif best_match == 1:
                print(f"PARTIAL: Component 2 -- 1/3 level formats correct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 2 -- No matching level formats found")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Indentation approximately correct per level (0.20 points)
    # Task says: Level 1 at ~0.635cm, Level 2 at 1.27cm, Level 3 at 2.54cm
    # In EMU: 0.635cm = ~360000, 1.27cm = ~720000, 2.54cm = ~1440000 (but golden uses different values)
    # Golden actual values: ilvl0=457200, ilvl1=914400, ilvl2=1371600
    # We check that indentation increases with level and is in a reasonable range
    try:
        if num_to_abstract is None or abstract_defs is None:
            print("FAIL: Component 3 -- No numbering definitions found")
        else:
            indent_score = 0
            for nid in num_ids_used:
                abstract_id = num_to_abstract.get(nid)
                if abstract_id is None:
                    continue
                adef = abstract_defs.get(abstract_id)
                if adef is None:
                    continue

                levels = adef.get('levels', {})
                indent0 = levels.get('0', {}).get('indent_left')
                indent1 = levels.get('1', {}).get('indent_left')
                indent2 = levels.get('2', {}).get('indent_left')

                print(f"  Indents: L0={indent0}, L1={indent1}, L2={indent2}")

                cur_score = 0
                # Check increasing indentation
                if indent0 is not None and indent1 is not None and indent2 is not None:
                    if indent0 < indent1 < indent2:
                        cur_score += 1  # Indentation increases
                    # Check L1 indent is around 1.27cm (720000 EMU) with generous tolerance
                    # 1.27cm = 720000 EMU, but golden shows 914400 (= 1 inch)
                    # Task instruction says "Level 2 uses uppercase letters with 1.27cm indent"
                    # Accept reasonable range 360000 to 1200000
                    if 360000 <= indent1 <= 1200000:
                        cur_score += 1
                    # Check L2 indent is around 2.54cm (1440000 EMU)
                    # Golden shows 1371600 (~1.5 inch). Accept range 720000 to 2000000
                    if 720000 <= indent2 <= 2000000:
                        cur_score += 1

                if cur_score > indent_score:
                    indent_score = cur_score

            if indent_score >= 3:
                print(f"PASS: Component 3 -- Indentation correct (0.20 pts)")
                total_score += 0.20
            elif indent_score >= 2:
                print(f"PARTIAL: Component 3 -- Indentation partially correct (0.10 pts)")
                total_score += 0.10
            else:
                print(f"FAIL: Component 3 -- Indentation incorrect or missing")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Manual numbering prefixes removed from text (0.20 points)
    # Initial file has text like "I. Revenue Growth...", "    A. Expand...", "        1. Identify..."
    # Golden file text should NOT start with these manual prefixes
    try:
        # Check numbered paragraphs at each level
        manual_prefix_pattern_l0 = re.compile(r'^\s*(I{1,3}V?|VI{0,3})\.\s')  # Roman numerals
        manual_prefix_pattern_l1 = re.compile(r'^\s*[A-C]\.\s')  # Uppercase letters
        manual_prefix_pattern_l2 = re.compile(r'^\s*\d+\.\s')  # Arabic numerals

        manual_found = 0
        checked = 0
        for _, ilvl, _, text in numbered_paras:
            if ilvl == '0':
                checked += 1
                if manual_prefix_pattern_l0.match(text):
                    manual_found += 1
            elif ilvl == '1':
                checked += 1
                if manual_prefix_pattern_l1.match(text):
                    manual_found += 1
            elif ilvl == '2':
                checked += 1
                if manual_prefix_pattern_l2.match(text):
                    manual_found += 1

        if checked == 0:
            # No numbered paras to check -- can't verify (depends on Component 1)
            print("FAIL: Component 4 -- No numbered paragraphs to check for manual prefixes")
        elif manual_found == 0:
            print(f"PASS: Component 4 -- No manual numbering prefixes in {checked} checked paragraphs (0.20 pts)")
            total_score += 0.20
        elif manual_found <= 3:
            print(f"PARTIAL: Component 4 -- {manual_found}/{checked} still have manual prefixes (0.10 pts)")
            total_score += 0.10
        else:
            print(f"FAIL: Component 4 -- {manual_found}/{checked} paragraphs still have manual numbering prefixes")
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

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
