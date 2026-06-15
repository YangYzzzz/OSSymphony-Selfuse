"""
Reward Script: Configure outline numbering to legal-style format for Heading levels 1-3
Task ID: writer_fp_048
Domain: libreoffice_writer
Scoring:
  Component 1 (0.25): Heading1 style has numPr linked to a multilevel numbering definition
  Component 2 (0.25): Heading2 style has numPr linked to same numbering at ilvl=1
  Component 3 (0.25): Heading3 style has numPr linked to same numbering at ilvl=2
  Component 4 (0.25): The abstractNum definition uses decimal format with legal-style lvlText
"""

import os
import time

WORKDIR = '/home/user'
TASK_ID = 'writer_fp_048'


def persist_app_state(domain: str):
    """Save any unsaved GUI edits before verification."""
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
        from docx import Document
        from lxml import etree
        doc = Document(file_path)
    except Exception as e:
        print(f"CRITICAL: Cannot load file {file_path}: {e}")
        print("REWARD: 0.0")
        return 0.0

    ns = {'w': 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'}
    W = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'

    # Helper: extract numPr from a heading style definition
    def get_style_numPr(style_id):
        """Return (ilvl, numId) tuple or (None, None) if no numPr."""
        styles_el = doc.styles.element
        for style in styles_el.findall('w:style', ns):
            sid = style.get(f'{{{W}}}styleId')
            if sid == style_id:
                pPr = style.find('w:pPr', ns)
                if pPr is not None:
                    numPr = pPr.find('w:numPr', ns)
                    if numPr is not None:
                        ilvl_el = numPr.find('w:ilvl', ns)
                        numId_el = numPr.find('w:numId', ns)
                        ilvl = ilvl_el.get(f'{{{W}}}val') if ilvl_el is not None else None
                        numId = numId_el.get(f'{{{W}}}val') if numId_el is not None else None
                        return ilvl, numId
        return None, None

    # Helper: resolve numId -> abstractNumId
    def get_abstractNumId(numId_val):
        """Given a numId string, return the abstractNumId string."""
        try:
            numbering = doc.part.numbering_part.element
        except Exception:
            return None
        for num_el in numbering.findall('w:num', ns):
            nid = num_el.get(f'{{{W}}}numId')
            if nid == numId_val:
                abs_ref = num_el.find('w:abstractNumId', ns)
                if abs_ref is not None:
                    return abs_ref.get(f'{{{W}}}val')
        return None

    # Helper: get abstractNum element by abstractNumId
    def get_abstractNum(abs_num_id):
        """Return the abstractNum element for a given abstractNumId."""
        try:
            numbering = doc.part.numbering_part.element
        except Exception:
            return None
        for abs_num in numbering.findall('w:abstractNum', ns):
            aid = abs_num.get(f'{{{W}}}abstractNumId')
            if aid == abs_num_id:
                return abs_num
        return None

    # =========================================================
    # Component 1: Heading1 style has numPr with ilvl=0 (0.25 points)
    # =========================================================
    try:
        h1_ilvl, h1_numId = get_style_numPr('Heading1')
        if h1_ilvl is not None and h1_numId is not None and h1_ilvl == '0':
            print(f"PASS: Component 1 -- Heading1 has numPr with ilvl={h1_ilvl}, numId={h1_numId} (0.25 pts)")
            total_score += 0.25
        else:
            print(f"FAIL: Component 1 -- Heading1 numPr: ilvl={h1_ilvl}, numId={h1_numId} (expected ilvl=0 with a numId)")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # =========================================================
    # Component 2: Heading2 style has numPr with ilvl=1 linked to SAME numId (0.25 points)
    # =========================================================
    try:
        h2_ilvl, h2_numId = get_style_numPr('Heading2')
        if h2_ilvl is not None and h2_numId is not None and h2_ilvl == '1':
            # Must share same numbering definition as Heading1
            if h1_numId is not None and h2_numId == h1_numId:
                print(f"PASS: Component 2 -- Heading2 has numPr with ilvl={h2_ilvl}, numId={h2_numId} (same as H1) (0.25 pts)")
                total_score += 0.25
            elif h1_numId is None:
                # H1 failed but H2 is still correct on its own
                print(f"PASS: Component 2 -- Heading2 has numPr with ilvl={h2_ilvl}, numId={h2_numId} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 2 -- Heading2 numId={h2_numId} differs from Heading1 numId={h1_numId}")
        else:
            print(f"FAIL: Component 2 -- Heading2 numPr: ilvl={h2_ilvl}, numId={h2_numId} (expected ilvl=1 with a numId)")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # =========================================================
    # Component 3: Heading3 style has numPr with ilvl=2 linked to SAME numId (0.25 points)
    # =========================================================
    try:
        h3_ilvl, h3_numId = get_style_numPr('Heading3')
        if h3_ilvl is not None and h3_numId is not None and h3_ilvl == '2':
            ref_numId = h1_numId or h2_numId
            if ref_numId is not None and h3_numId == ref_numId:
                print(f"PASS: Component 3 -- Heading3 has numPr with ilvl={h3_ilvl}, numId={h3_numId} (same as H1/H2) (0.25 pts)")
                total_score += 0.25
            elif ref_numId is None:
                print(f"PASS: Component 3 -- Heading3 has numPr with ilvl={h3_ilvl}, numId={h3_numId} (0.25 pts)")
                total_score += 0.25
            else:
                print(f"FAIL: Component 3 -- Heading3 numId={h3_numId} differs from Heading1/2 numId={ref_numId}")
        else:
            print(f"FAIL: Component 3 -- Heading3 numPr: ilvl={h3_ilvl}, numId={h3_numId} (expected ilvl=2 with a numId)")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # =========================================================
    # Component 4: The abstractNum has legal-style numbering format (0.25 points)
    #   - All 3 levels must use decimal numFmt
    #   - lvlText for level 0: contains %1 and ends with .
    #   - lvlText for level 1: contains %1 and %2 (parent chain) and ends with .
    #   - lvlText for level 2: contains %1, %2, and %3 (full parent chain) and ends with .
    #   - multiLevelType must be 'multilevel'
    # =========================================================
    try:
        # Use whichever numId we found
        ref_numId = h1_numId or h2_numId or h3_numId
        if ref_numId is None:
            print("FAIL: Component 4 -- No numId found from any heading style, cannot check numbering format")
        else:
            abs_num_id = get_abstractNumId(ref_numId)
            if abs_num_id is None:
                print(f"FAIL: Component 4 -- Cannot resolve numId={ref_numId} to abstractNumId")
            else:
                abs_num = get_abstractNum(abs_num_id)
                if abs_num is None:
                    print(f"FAIL: Component 4 -- abstractNum {abs_num_id} not found")
                else:
                    # Check multiLevelType
                    ml_type = abs_num.find('w:multiLevelType', ns)
                    ml_val = ml_type.get(f'{{{W}}}val') if ml_type is not None else None

                    # Check each level
                    lvls = {}
                    for lvl in abs_num.findall('w:lvl', ns):
                        ilvl = lvl.get(f'{{{W}}}ilvl')
                        numFmt_el = lvl.find('w:numFmt', ns)
                        numFmt = numFmt_el.get(f'{{{W}}}val') if numFmt_el is not None else None
                        lvlText_el = lvl.find('w:lvlText', ns)
                        lvlText = lvlText_el.get(f'{{{W}}}val') if lvlText_el is not None else None
                        lvls[ilvl] = {'numFmt': numFmt, 'lvlText': lvlText}

                    checks_passed = 0
                    total_checks = 4

                    # Check 4a: multiLevelType is multilevel
                    if ml_val == 'multilevel':
                        checks_passed += 1
                    else:
                        print(f"  DETAIL: multiLevelType={ml_val}, expected 'multilevel'")

                    # Check 4b: Level 0 - decimal, lvlText has %1 and ends with .
                    lvl0 = lvls.get('0', {})
                    if lvl0.get('numFmt') == 'decimal' and lvl0.get('lvlText') and '%1' in lvl0['lvlText'] and lvl0['lvlText'].endswith('.'):
                        checks_passed += 1
                    else:
                        print(f"  DETAIL: Level 0 numFmt={lvl0.get('numFmt')}, lvlText={lvl0.get('lvlText')}")

                    # Check 4c: Level 1 - decimal, lvlText has %1 and %2, ends with .
                    lvl1 = lvls.get('1', {})
                    if lvl1.get('numFmt') == 'decimal' and lvl1.get('lvlText') and '%1' in lvl1['lvlText'] and '%2' in lvl1['lvlText'] and lvl1['lvlText'].endswith('.'):
                        checks_passed += 1
                    else:
                        print(f"  DETAIL: Level 1 numFmt={lvl1.get('numFmt')}, lvlText={lvl1.get('lvlText')}")

                    # Check 4d: Level 2 - decimal, lvlText has %1, %2, %3, ends with .
                    lvl2 = lvls.get('2', {})
                    if lvl2.get('numFmt') == 'decimal' and lvl2.get('lvlText') and '%1' in lvl2['lvlText'] and '%2' in lvl2['lvlText'] and '%3' in lvl2['lvlText'] and lvl2['lvlText'].endswith('.'):
                        checks_passed += 1
                    else:
                        print(f"  DETAIL: Level 2 numFmt={lvl2.get('numFmt')}, lvlText={lvl2.get('lvlText')}")

                    if checks_passed == total_checks:
                        print(f"PASS: Component 4 -- Legal-style numbering format verified (multilevel, decimal, %1./%1.%2./%1.%2.%3.) (0.25 pts)")
                        total_score += 0.25
                    else:
                        print(f"FAIL: Component 4 -- {checks_passed}/{total_checks} sub-checks passed for numbering format")
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
