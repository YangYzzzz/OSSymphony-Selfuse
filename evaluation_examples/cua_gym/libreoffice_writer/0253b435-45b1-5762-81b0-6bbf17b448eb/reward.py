"""
Reward Script: Multi-level numbered list with 1., 1.1, 1.1.1 format
Task ID: wrpara_035
Domain: libreoffice_writer
Scoring:
  Component 1 (0.30): All outline paragraphs have numbering applied
  Component 2 (0.30): Correct level (ilvl) assignments matching hierarchy
  Component 3 (0.20): Level 0 numbering format is "X." (decimal, lvlText '%1.')
  Component 4 (0.20): Level 1/2 numbering formats are multi-level ("%1.%2" and "%1.%2.%3")
"""

import os
from docx import Document
from lxml import etree

WORKDIR = '/home/user'
TASK_ID = 'wrpara_035'
WNS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WNS}

# Expected hierarchy: paragraph index -> expected ilvl
# P3-P28 are the outline items (indices 3 through 28)
EXPECTED_LEVELS = {
    3: 0,   # Project Planning and Initiation
    4: 1,   # Stakeholder Requirements Gathering
    5: 2,   # Conduct Executive Interviews
    6: 2,   # Distribute Department Surveys
    7: 1,   # Feasibility Study and Risk Assessment
    8: 1,   # Project Charter and Timeline Development
    9: 0,   # System Design and Architecture
    10: 1,  # Database Schema Design
    11: 2,  # Define Entity Relationships
    12: 2,  # Establish Data Migration Mappings
    13: 1,  # User Interface Wireframing
    14: 1,  # API Integration Planning
    15: 0,  # Development and Implementation
    16: 1,  # Core Module Development
    17: 2,  # Build Inventory Management Module
    18: 2,  # Build Financial Reporting Module
    19: 1,  # Third-Party Integration Development
    20: 2,  # Connect Payment Gateway Services
    21: 2,  # Integrate Cloud Storage Providers
    22: 1,  # Quality Assurance and Testing
    23: 0,  # Deployment and Post-Launch Support
    24: 1,  # Staging Environment Deployment
    25: 1,  # Production Rollout and Monitoring
    26: 2,  # Configure Performance Dashboards
    27: 2,  # Establish Incident Response Procedures
    28: 1,  # End-User Training and Documentation
}

OUTLINE_INDICES = sorted(EXPECTED_LEVELS.keys())


def get_numPr(para):
    """Return (numId, ilvl) tuple or (None, None) if no numbering."""
    pPr = para._element.pPr
    if pPr is None:
        return None, None
    numPr = pPr.find(f'{{{WNS}}}numPr')
    if numPr is None:
        return None, None
    numId_elem = numPr.find(f'{{{WNS}}}numId')
    ilvl_elem = numPr.find(f'{{{WNS}}}ilvl')
    numId = numId_elem.get(f'{{{WNS}}}val') if numId_elem is not None else None
    ilvl = ilvl_elem.get(f'{{{WNS}}}val') if ilvl_elem is not None else None
    return numId, int(ilvl) if ilvl is not None else None


def get_numbering_formats(doc, numId_str):
    """Given a numId, resolve the abstractNum and return {ilvl: (numFmt, lvlText)} for levels 0-2."""
    numbering_part = doc.part.numbering_part
    if numbering_part is None:
        return {}
    root = etree.fromstring(numbering_part._element.xml.encode('utf-8'))

    # Find the w:num element with the given numId
    abstractNumId = None
    num_elem = None
    for n in root.findall('.//w:num', NS):
        if n.get(f'{{{WNS}}}numId') == numId_str:
            num_elem = n
            ref = n.find('w:abstractNumId', NS)
            if ref is not None:
                abstractNumId = ref.get(f'{{{WNS}}}val')
            break

    if abstractNumId is None:
        return {}

    formats = {}
    # Get base formats from abstractNum
    for absNum in root.findall('.//w:abstractNum', NS):
        if absNum.get(f'{{{WNS}}}abstractNumId') == abstractNumId:
            for lvl in absNum.findall('w:lvl', NS):
                ilvl = int(lvl.get(f'{{{WNS}}}ilvl'))
                if ilvl > 2:
                    continue
                numFmt_elem = lvl.find('w:numFmt', NS)
                lvlText_elem = lvl.find('w:lvlText', NS)
                numFmt = numFmt_elem.get(f'{{{WNS}}}val') if numFmt_elem is not None else None
                lvlText = lvlText_elem.get(f'{{{WNS}}}val') if lvlText_elem is not None else None
                formats[ilvl] = (numFmt, lvlText)
            break

    # Check for overrides in the num element
    if num_elem is not None:
        for ovr in num_elem.findall('w:lvlOverride', NS):
            olvl = int(ovr.get(f'{{{WNS}}}ilvl'))
            if olvl > 2:
                continue
            lvl = ovr.find('w:lvl', NS)
            if lvl is not None:
                numFmt_elem = lvl.find('w:numFmt', NS)
                lvlText_elem = lvl.find('w:lvlText', NS)
                numFmt = numFmt_elem.get(f'{{{WNS}}}val') if numFmt_elem is not None else None
                lvlText = lvlText_elem.get(f'{{{WNS}}}val') if lvlText_elem is not None else None
                formats[olvl] = (numFmt, lvlText)

    return formats


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

    paras = doc.paragraphs
    if len(paras) < 29:
        print(f"FAIL: Expected at least 29 paragraphs, found {len(paras)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All outline paragraphs (P3-P28) have numbering applied (0.30 points)
    try:
        numbered_count = 0
        numIds_found = set()
        for idx in OUTLINE_INDICES:
            numId, ilvl = get_numPr(paras[idx])
            if numId is not None and numId != '0':
                numbered_count += 1
                numIds_found.add(numId)

        total_outline = len(OUTLINE_INDICES)
        ratio = numbered_count / total_outline
        if ratio >= 0.95:  # allow 1 missed paragraph
            comp1 = 0.30
        elif ratio >= 0.7:
            comp1 = 0.20
        elif ratio >= 0.4:
            comp1 = 0.10
        else:
            comp1 = 0.0

        if comp1 > 0:
            print(f"PASS: Component 1 -- {numbered_count}/{total_outline} outline paragraphs have numbering ({comp1} pts)")
            total_score += comp1
        else:
            print(f"FAIL: Component 1 -- Only {numbered_count}/{total_outline} outline paragraphs have numbering")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: Correct level (ilvl) assignments (0.30 points)
    try:
        correct_levels = 0
        for idx in OUTLINE_INDICES:
            numId, ilvl = get_numPr(paras[idx])
            expected = EXPECTED_LEVELS[idx]
            if ilvl == expected:
                correct_levels += 1
            else:
                # Also accept if the numbering is applied but only the relative depth matters
                pass

        level_ratio = correct_levels / total_outline
        if level_ratio >= 0.95:
            comp2 = 0.30
        elif level_ratio >= 0.7:
            comp2 = 0.20
        elif level_ratio >= 0.4:
            comp2 = 0.10
        else:
            comp2 = 0.0

        if comp2 > 0:
            print(f"PASS: Component 2 -- {correct_levels}/{total_outline} paragraphs have correct ilvl ({comp2} pts)")
            total_score += comp2
        else:
            print(f"FAIL: Component 2 -- Only {correct_levels}/{total_outline} paragraphs have correct ilvl")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: Level 0 numbering format is "X." (decimal, lvlText '%1.') (0.20 points)
    try:
        # Use any numId found on outline paragraphs
        formats = {}
        for nid in numIds_found:
            formats = get_numbering_formats(doc, nid)
            if formats:
                break

        if not formats:
            print("FAIL: Component 3 -- No numbering format definitions found")
        else:
            lvl0 = formats.get(0)
            if lvl0 is None:
                print("FAIL: Component 3 -- No level 0 format definition found")
            else:
                numFmt, lvlText = lvl0
                # Accept decimal format with "X." pattern (e.g., '%1.' or '%1)')
                is_decimal = numFmt == 'decimal'
                has_dot = lvlText is not None and lvlText.endswith('.')
                # The lvlText should reference only %1 for a "1." style
                is_single_level = lvlText is not None and '%1' in lvlText and '%2' not in lvlText

                if is_decimal and has_dot and is_single_level:
                    print(f"PASS: Component 3 -- Level 0 format: numFmt={numFmt}, lvlText={lvlText!r} (0.20 pts)")
                    total_score += 0.20
                elif is_decimal:
                    print(f"PARTIAL: Component 3 -- Level 0 is decimal but lvlText={lvlText!r} (0.10 pts)")
                    total_score += 0.10
                else:
                    print(f"FAIL: Component 3 -- Level 0: numFmt={numFmt}, lvlText={lvlText!r}")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    # Component 4: Levels 1 and 2 numbering formats are multi-level (0.20 points)
    try:
        if not formats:
            print("FAIL: Component 4 -- No numbering format definitions found")
        else:
            comp4 = 0.0

            # Level 1: should be like "%1.%2" (multi-level, no trailing dot typically)
            lvl1 = formats.get(1)
            if lvl1 is not None:
                numFmt1, lvlText1 = lvl1
                is_decimal1 = numFmt1 == 'decimal'
                is_multi1 = lvlText1 is not None and '%1' in lvlText1 and '%2' in lvlText1
                if is_decimal1 and is_multi1:
                    print(f"PASS: Component 4a -- Level 1 format: numFmt={numFmt1}, lvlText={lvlText1!r} (0.10 pts)")
                    comp4 += 0.10
                else:
                    print(f"FAIL: Component 4a -- Level 1: numFmt={numFmt1}, lvlText={lvlText1!r}")
            else:
                print("FAIL: Component 4a -- No level 1 format definition found")

            # Level 2: should be like "%1.%2.%3" (three-level)
            lvl2 = formats.get(2)
            if lvl2 is not None:
                numFmt2, lvlText2 = lvl2
                is_decimal2 = numFmt2 == 'decimal'
                is_multi2 = lvlText2 is not None and '%1' in lvlText2 and '%2' in lvlText2 and '%3' in lvlText2
                if is_decimal2 and is_multi2:
                    print(f"PASS: Component 4b -- Level 2 format: numFmt={numFmt2}, lvlText={lvlText2!r} (0.10 pts)")
                    comp4 += 0.10
                else:
                    print(f"FAIL: Component 4b -- Level 2: numFmt={numFmt2}, lvlText={lvlText2!r}")
            else:
                print("FAIL: Component 4b -- No level 2 format definition found")

            if comp4 > 0:
                total_score += comp4
    except Exception as e:
        print(f"ERROR: Component 4 -- {e}")

    final_score = min(total_score, 1.0)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Persistence hook: save any unsaved LibreOffice state
def persist_app_state():
    import time
    os.environ["DISPLAY"] = ":0"
    try:
        import pyautogui
        pyautogui.hotkey("ctrl", "s")
        time.sleep(0.8)
        print("PERSIST: ctrl+s sent for libreoffice_writer")
    except Exception as e:
        print(f"PERSIST_WARN: save hook failed: {e}")


# Entry point
file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    persist_app_state()
    verify_task(file_path)
