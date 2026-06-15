"""
Reward Script: Create a numbered list using lowercase Roman numerals for recipe instructions
Task ID: writer_lec_003
Domain: libreoffice_writer
Scoring:
  Component 1 (0.3): Six instruction paragraphs use a list style (not 'Normal')
  Component 2 (0.4): Six instruction paragraphs have numbering properties (numPr)
  Component 3 (0.3): The numbering format is lowerRoman
"""

import os

WORKDIR = '/home/user'
TASK_ID = 'writer_lec_003'

# Expected instruction step beginnings (to locate the 6 steps)
STEP_STARTS = [
    "Preheat the oven",
    "While the tomatoes",
    "Add the minced garlic",
    "Transfer the roasted tomatoes",
    "Remove the pot from heat",
    "Taste and adjust seasoning",
]

WML_NS = 'http://schemas.openxmlformats.org/wordprocessingml/2006/main'
NS = {'w': WML_NS}


def find_instruction_paragraphs(doc):
    """Find the 6 instruction step paragraphs by matching text beginnings."""
    found = []
    for para in doc.paragraphs:
        text = para.text.strip()
        for start in STEP_STARTS:
            if text.startswith(start):
                found.append(para)
                break
    return found


def get_numId_for_paragraph(para):
    """Extract numId value from paragraph's numbering properties, or None."""
    numPr_list = para._element.findall('.//w:numPr', NS)
    for numPr in numPr_list:
        numId_el = numPr.find('w:numId', NS)
        if numId_el is not None:
            return numId_el.get(f'{{{WML_NS}}}val')
    return None


def get_num_format(doc, numId_str):
    """Given a numId string, resolve through numbering part to find the numFmt for ilvl=0."""
    try:
        numbering_part = doc.part.numbering_part
        if numbering_part is None:
            return None
        numbering_xml = numbering_part._element

        # Find the <w:num> element with matching numId to get abstractNumId
        abstractNumId = None
        for num in numbering_xml.findall('.//w:num', NS):
            if num.get(f'{{{WML_NS}}}numId') == numId_str:
                # Check for level overrides first
                for ovr in num.findall('w:lvlOverride', NS):
                    if ovr.get(f'{{{WML_NS}}}ilvl') == '0':
                        lvl = ovr.find('w:lvl', NS)
                        if lvl is not None:
                            numFmt = lvl.find('w:numFmt', NS)
                            if numFmt is not None:
                                return numFmt.get(f'{{{WML_NS}}}val')
                absRef = num.find('w:abstractNumId', NS)
                if absRef is not None:
                    abstractNumId = absRef.get(f'{{{WML_NS}}}val')
                break

        if abstractNumId is None:
            return None

        # Find the abstractNum and get its ilvl=0 numFmt
        for absNum in numbering_xml.findall('.//w:abstractNum', NS):
            if absNum.get(f'{{{WML_NS}}}abstractNumId') == abstractNumId:
                for lvl in absNum.findall('.//w:lvl', NS):
                    if lvl.get(f'{{{WML_NS}}}ilvl') == '0':
                        numFmt = lvl.find('w:numFmt', NS)
                        if numFmt is not None:
                            return numFmt.get(f'{{{WML_NS}}}val')
        return None
    except Exception:
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

    # Locate the 6 instruction paragraphs
    steps = find_instruction_paragraphs(doc)
    if len(steps) != 6:
        print(f"CRITICAL: Expected 6 instruction steps, found {len(steps)}")
        print("REWARD: 0.0")
        return 0.0

    # Component 1: All 6 instruction paragraphs use a list-related style (0.3 points)
    # In initial_env these are 'Normal'; in golden they should be a list style
    try:
        list_style_count = 0
        for i, para in enumerate(steps):
            style_name = para.style.name if para.style else 'None'
            if 'list' in style_name.lower() or 'number' in style_name.lower():
                list_style_count += 1
                print(f"  Step {i+1}: style='{style_name}' -- list style detected")
            else:
                print(f"  Step {i+1}: style='{style_name}' -- NOT a list style")

        if list_style_count == 6:
            print(f"PASS: Component 1 -- All 6 steps have list styles (0.3 pts)")
            total_score += 0.3
        elif list_style_count > 0:
            partial = round(0.3 * (list_style_count / 6), 2)
            print(f"PARTIAL: Component 1 -- {list_style_count}/6 steps have list styles ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 1 -- No steps have list styles")
    except Exception as e:
        print(f"ERROR: Component 1 -- {e}")

    # Component 2: All 6 instruction paragraphs have numbering properties (numPr) (0.4 points)
    # In initial_env these have no numPr; in golden they should have numId referencing a numbering definition
    try:
        numbered_count = 0
        numIds_found = set()
        for i, para in enumerate(steps):
            numId = get_numId_for_paragraph(para)
            if numId is not None and numId != '0':
                numbered_count += 1
                numIds_found.add(numId)
                print(f"  Step {i+1}: numId={numId} -- numbered")
            else:
                print(f"  Step {i+1}: no numbering properties")

        if numbered_count == 6:
            print(f"PASS: Component 2 -- All 6 steps have numbering (numIds: {numIds_found}) (0.4 pts)")
            total_score += 0.4
        elif numbered_count > 0:
            partial = round(0.4 * (numbered_count / 6), 2)
            print(f"PARTIAL: Component 2 -- {numbered_count}/6 steps have numbering ({partial} pts)")
            total_score += partial
        else:
            print(f"FAIL: Component 2 -- No steps have numbering properties")
    except Exception as e:
        print(f"ERROR: Component 2 -- {e}")

    # Component 3: The numbering format is lowerRoman (0.3 points)
    # This checks the actual numFmt in the numbering definitions
    try:
        if numIds_found:
            formats_found = {}
            for numId in numIds_found:
                fmt = get_num_format(doc, numId)
                formats_found[numId] = fmt
                print(f"  numId={numId} -> numFmt={fmt}")

            if any(fmt == 'lowerRoman' for fmt in formats_found.values()):
                print(f"PASS: Component 3 -- Numbering format is lowerRoman (0.3 pts)")
                total_score += 0.3
            else:
                print(f"FAIL: Component 3 -- Numbering format is not lowerRoman (found: {formats_found})")
        else:
            print(f"FAIL: Component 3 -- No numbering found, cannot check format")
    except Exception as e:
        print(f"ERROR: Component 3 -- {e}")

    final_score = round(min(total_score, 1.0), 2)
    print(f"\nScore: {total_score}/1.0")
    print(f"REWARD: {final_score}")
    return final_score


# Entry point
def persist_app_state(domain):
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


persist_app_state("libreoffice_writer")

file_path = f'{WORKDIR}/{TASK_ID}.docx'
if not os.path.exists(file_path):
    print(f"File not found: {file_path}")
    print("REWARD: 0.0")
else:
    verify_task(file_path)
